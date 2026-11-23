#!/usr/bin/env python3
"""Resumable, rate-limited public-page observation for evidence-backed skills.

Raw HTML and the work queue stay outside the public repository. Public output is
limited to URL provenance, structural measurements, short titles and coverage.
This tool does not infer visual design or interactions from unrendered HTML.
"""
from __future__ import annotations
import argparse,concurrent.futures,datetime,hashlib,html,json,re,socket,ipaddress,sqlite3,threading,time,urllib.request,urllib.parse,urllib.error
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

MAIN='www.awwwards.com';AGENT='AwwwardsPageSkillsResearch/1.0 (+https://github.com/hxyang24/awwwards-web-design-skills)'
SOCIAL={'facebook.com','instagram.com','twitter.com','x.com','youtube.com','tiktok.com','linkedin.com','pinterest.com','pinterest.es','vimeo.com','discord.com','discord.gg','behance.net','dribbble.com','github.com','medium.com'}
ASSET=re.compile(r'\.(?:png|jpe?g|gif|webp|svg|ico|avif|mp4|webm|mov|mp3|ogg|pdf|zip|woff2?|ttf|css|m?js|xml|json|txt)$',re.I)
USER_PATH=re.compile(r'^/(?:login|logout|register|sign[-_]?in|sign[-_]?up|checkout|cart|account|admin|wp-admin|wp-login|api)(?:/|$)',re.I)
SEEDS=['/','/websites/','/websites/sites_of_the_day/','/websites/sites_of_the_month/','/websites/sites_of_the_year/','/websites/nominees/','/honors/winners','/winner-list/','/annual-awards/','/jury/2026/','/collections/','/library/','/directory/','/directory/homepage/','/directory/international/','/directory/freelance/','/directory/agency-studio/','/academy/','/jobs/','/market/','/pro','/plans/user-plans','/submit/','/faqs/','/blog/','/about-us/','/contact-us/','/conferences/','/privacy-policy/','/terms/','/cookies-policy/']
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def content_state_hint(title,headings):
 texts=[' '.join(x.lower().replace('’',"'").replace('‘',"'").split()) for x in [title,*headings]]
 for text in texts:
  if re.search(r"^(?:404(?:\s*[-|:]|$)|(?:this |the )?page (?:not found|doesn'?t exist|does not exist)|not found(?:\s*[-|:]|$))",text):return 'possible_not_found'
  if re.search(r"^(?:(?:this |the )?page (?:couldn'?t|cannot|can'?t) load|application error|something went wrong)",text):return 'possible_render_error'
  if re.search(r"^(?:your |this )?browser (?:is )?not supported|^unsupported browser",text):return 'possible_compatibility_fallback'
 return 'unclassified'
def normalize(value,base):
 try:
  u=urllib.parse.urlsplit(urllib.parse.urljoin(base,html.unescape(value)))
  if u.scheme not in ('http','https') or not u.hostname or u.username or u.password or u.port not in (None,80,443):return None
  host=u.hostname.lower().rstrip('.');host=MAIN if host=='awwwards.com' else host
  if host in ('localhost','localhost.localdomain') or host.endswith(('.local','.internal')):return None
  try:
   if not ipaddress.ip_address(host).is_global:return None
  except ValueError:pass
  path=u.path or '/'
  if ASSET.search(path) or USER_PATH.match(path):return None
  query=urllib.parse.parse_qsl(u.query,keep_blank_values=True)
  query=[(k,v) for k,v in query if k in ('page','load_more','year','sort','category','type','order') and len(v)<100]
  if any(k=='page' and (not v.isdigit() or not 1<=int(v)<=100000) for k,v in query):return None
  query=[(k,v) for k,v in query if not (k=='page' and v=='1')]
  return urllib.parse.urlunsplit((u.scheme,host,path,urllib.parse.urlencode(sorted(query)) ,''))
 except (ValueError,TypeError):return None
def same_site(a,b):
 def host(u):return urllib.parse.urlsplit(u).hostname.removeprefix('www.')
 return host(a)==host(b)
def public_dns(host):
 try:return all(ipaddress.ip_address(x[4][0]).is_global for x in socket.getaddrinfo(host,None,type=socket.SOCK_STREAM))
 except OSError:return False
def family(url):
 p=urllib.parse.urlsplit(url).path;host=urllib.parse.urlsplit(url).hostname
 if host!=MAIN:
  p=re.sub(r'^/(?:en|en-us|en-gb|de|fr|es|it|pt|pt-br|nl-nl|ar|ja|zh|zh-cn)(?=/|$)','',p,flags=re.I) or '/'
  if p=='/':return 'external.home'
  if host.removeprefix('www.')=='ponpon-mania.com':
   if p.rstrip('/')=='/chapters':return 'external.story-index'
   if re.fullmatch(r'/chapter/\d+/?',p):return 'external.story-chapter'
  if host.removeprefix('www.')=='aifont.ai' and re.fullmatch(r'/fonts/[^/]+/?',p):return 'external.prompt-detail'
  if host.removeprefix('www.')=='artemiilebedev.com' and p=='/alter-ego':return 'external.media-portfolio'
  patterns=[('not-found',r'/404(?:/|$)'),('gallery',r'/(?:gallery|archive)(?=/|$)'),('artwork',r'/artwork(?=/|$)'),('experiment',r'/(?:lab|experiments?|playground)(?=/|$)'),('project',r'/(?:work|works|project|projects|case-stud(?:y|ies))(?=/|$)'),('about',r'/(?:about|about-us|studio|team|who-we-are)(?=/|$)'),('contact',r'/(?:contact|contact-us|get-in-touch)(?=/|$)'),('product',r'/(?:products?|shop|collections?|dispensa)(?=/|$)'),('article',r'/(?:journal|blog|news|stories|insights|writing)(?=/|$)'),('service',r'/(?:services?|solutions?|expertise|process)(?=/|$)'),('careers',r'/(?:careers?|jobs?)(?=/|$)'),('legal',r'/(?:privacy|privacy-policy|terms|terms-and-conditions|legal|cookies)(?=/|$)')]
  for name,pattern in patterns:
   if re.search(pattern,p,re.I):return 'external.'+name
  return 'external.other'
 if p=='/':return 'main.home'
 if p.startswith('/sites/'):return 'main.award-detail'
 if p.startswith('/websites/'):
  if p=='/websites/':return 'main.website-explorer'
  if any(x in p for x in ['sites_of_the_','nominees']):return 'main.award-list'
  return 'main.category-list'
 if '/collections/' in p:return 'main.collection-detail' if p!='/collections/' else 'main.collection-index'
 if p.startswith('/academy/course/'):return 'main.course-detail'
 if p.startswith('/academy/'):return 'main.course-index'
 if p.startswith('/directory/'):return 'main.creator-directory'
 if p.startswith('/jury/'):return 'main.jury'
 if p.startswith('/jobs/'):return 'main.job-index' if p in ('/jobs/','/jobs/search/') else 'main.job-detail'
 if p.startswith('/market/'):return 'main.market-index' if p=='/market/' else 'main.market-detail'
 if p.startswith('/honors/'):return 'main.honors-list'
 if p.startswith('/library/'):return 'main.inspiration-library'
 if p.startswith('/elements/'):return 'main.element-library'
 if p.startswith('/plans/') or p=='/pro':return 'main.membership'
 if p.startswith(('/submit/','/submission/')):return 'main.submission'
 if p.startswith('/faqs/'):return 'main.faq'
 if p.startswith('/conferences/'):return 'main.conference'
 if p.startswith('/blog/') and not p.endswith('.html'):return 'main.editorial-index'
 if p.endswith('.html'):return 'main.article'
 if p.startswith('/annual-awards/'):return 'main.annual-awards'
 if p.startswith('/winner-list/'):return 'main.winner-index'
 if p.startswith('/contact-us/'):return 'main.contact'
 if p.startswith('/about-us/'):return 'main.about'
 if p.startswith(('/privacy-policy/','/terms/','/cookies-policy/')):return 'main.legal'
 if len([x for x in p.split('/') if x])==1:return 'main.creator-profile'
 return 'main.other'
class Structure(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tags=Counter();self.inputs=Counter();self.roles=Counter();self.links=[];self.active=None;self.title='';self.in_title=False;self.ignore=0;self.headings=Counter();self.canonical=None;self.heading_tag=None;self.heading_text='';self.heading_texts=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags[tag]+=1
  if tag in ('script','style'):self.ignore+=1
  if tag=='title':self.in_title=True
  if tag in ['h1','h2','h3','h4','h5','h6']:self.headings[tag]+=1
  if tag in ('h1','h2'):self.heading_tag=tag;self.heading_text=''
  if a.get('role'):self.roles[a['role']]+=1
  if tag=='input':self.inputs[a.get('type','text').lower()]+=1
  if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href')
  if tag=='a' and 'href' in a:self.active={'href':a['href'],'class':a.get('class',''),'text':''}
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.ignore=max(0,self.ignore-1)
  if tag=='title':self.in_title=False
  if tag==self.heading_tag:
   if len(self.heading_texts)<30:self.heading_texts.append(self.heading_text[:300])
   self.heading_tag=None;self.heading_text=''
  if tag=='a' and self.active:self.links.append(self.active);self.active=None
 def handle_data(self,data):
  if self.in_title:self.title+=data
  if self.heading_tag and not self.ignore:self.heading_text+=data[:300]
  if self.active and not self.ignore:self.active['text']+=data[:100]
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None
class Robots:
 def __init__(self,text):
  groups=[];agents=[];rules=[];started=False
  for line in text.splitlines():
   line=line.split('#',1)[0].strip()
   if ':' not in line:continue
   k,v=(x.strip() for x in line.split(':',1));k=k.lower()
   if k=='user-agent':
    if started:groups.append((agents,rules));agents=[];rules=[];started=False
    agents.append(v.lower())
   elif k in ('allow','disallow') and agents:
    started=True
    if v:rules.append((k=='allow',v))
  groups.append((agents,rules));self.rules=[r for ag,rs in groups if '*' in ag for r in rs]
 def allowed(self,url):
  u=urllib.parse.urlsplit(url);target=urllib.parse.quote(urllib.parse.unquote(u.path),safe='/:%@!$&\'()*+,;=-._~')+('?' + u.query if u.query else '')
  matches=[]
  for allow,p in self.rules:
   end=p.endswith('$');p=p[:-1] if end else p;regex='^'+re.escape(p).replace(r'\*','.*')+('$' if end else '')
   if re.search(regex,target):matches.append((len(p.replace('*','')),allow))
  return max(matches,default=(0,True))[1]
class Collector:
 def __init__(self,state,out,raw,interval=1.2,max_bytes=4194304):
  self.state=Path(state).resolve();self.out=Path(out).resolve();self.raw=Path(raw).resolve();self.interval=interval;self.max_bytes=max_bytes
  for p in [self.state.parent,self.out,self.raw]:p.mkdir(parents=True,exist_ok=True)
  if self.state.is_relative_to(self.out) or self.raw.is_relative_to(self.out):raise ValueError('Private queue/cache must be outside public output')
  self.lock=threading.RLock();self.host_locks={};self.last={};self.robots={};self.opener=urllib.request.build_opener(NoRedirect);self.db=sqlite3.connect(self.state,check_same_thread=False)
  self.db.executescript('CREATE TABLE IF NOT EXISTS queue(url TEXT PRIMARY KEY,origin TEXT,scope TEXT,priority INTEGER,state TEXT DEFAULT "pending",record TEXT);CREATE TABLE IF NOT EXISTS roots(host TEXT PRIMARY KEY,official_url TEXT);CREATE TABLE IF NOT EXISTS host_backoff(host TEXT PRIMARY KEY,retry_after REAL);')
  observed=[json.loads(r) for (r,) in self.db.execute('SELECT record FROM queue WHERE record IS NOT NULL') if json.loads(r).get('inspection_level')=='http_dom']
  self.seen=Counter(r['family'] for r in observed)
  self.seen_on_host=Counter((urllib.parse.urlsplit(r['url']).hostname,r['family']) for r in observed)
 def add(self,url,origin,scope,priority):
  u=normalize(url,origin)
  if not u:return
  with self.lock:self.db.execute('INSERT OR IGNORE INTO queue(url,origin,scope,priority)VALUES(?,?,?,?)',(u,origin,scope,priority));self.db.commit()
 def pace(self,host):
  with self.lock:lock=self.host_locks.setdefault(host,threading.Lock())
  with lock:
   delay=self.interval-(time.monotonic()-self.last.get(host,0))
   if delay>0:time.sleep(delay)
   self.last[host]=time.monotonic()
 def request(self,url):
  host=urllib.parse.urlsplit(url).hostname
  if not public_dns(host):raise ValueError('Non-public or unresolved host')
  self.pace(host)
  try:
   with self.opener.open(urllib.request.Request(url,headers={'User-Agent':AGENT,'Accept':'text/html,application/xhtml+xml,text/plain;q=0.8'}),timeout=25) as f:
    b=f.read(self.max_bytes+1);return f.status,dict(f.headers),b[:self.max_bytes],len(b)>self.max_bytes
  except urllib.error.HTTPError as e:
   if e.code in (429,503):
    retry=e.headers.get('Retry-After','60')
    try:delay=max(5,min(3600,int(retry)))
    except ValueError:delay=60
    with self.lock:self.db.execute('INSERT INTO host_backoff(host,retry_after)VALUES(?,?) ON CONFLICT(host)DO UPDATE SET retry_after=MAX(retry_after,excluded.retry_after)',(host,time.time()+delay));self.db.commit()
   if e.code in (404,410):
    b=e.read(self.max_bytes+1);return e.code,dict(e.headers),b[:self.max_bytes],len(b)>self.max_bytes
   return e.code,dict(e.headers),b'',False
 def policy(self,url):
  host=urllib.parse.urlsplit(url).netloc
  with self.lock:
   if host in self.robots:return self.robots[host]
  robots_url=urllib.parse.urlunsplit((urllib.parse.urlsplit(url).scheme,host,'/robots.txt','',''))
  try:
   current=robots_url
   for hop in range(6):
    code,headers,body,truncated=self.request(current)
    if 300<=code<400 and headers.get('Location') and hop<5:
     target=urllib.parse.urljoin(current,headers['Location']);parts=urllib.parse.urlsplit(target)
     if parts.scheme not in ('http','https') or parts.username or parts.password:break
     current=target;continue
    break
   if code==200 and not truncated and not body.lstrip().startswith(b'<'):r=Robots(body.decode('utf-8','replace'));proof={'url':robots_url,'final_url':current,'status':code,'sha256':hashlib.sha256(body).hexdigest(),'policy':'rules'}
   elif code in (404,410):r=Robots('');proof={'url':robots_url,'status':code,'policy':'no_robots_file'}
   else:r=Robots('User-agent: *\nDisallow: /');proof={'url':robots_url,'status':code,'policy':'blocked_or_unavailable'}
  except Exception as e:r=Robots('User-agent: *\nDisallow: /');proof={'url':robots_url,'policy':'unavailable','error_type':type(e).__name__}
  with self.lock:self.robots[host]=(r,proof)
  return r,proof
 def initialize(self,legacy):
  for path in SEEDS:self.add('https://'+MAIN+path,'https://'+MAIN+'/','main',0)
  if legacy:
   for row in json.loads(Path(legacy).read_text(encoding='utf-8'))['rows']:self.add(row['official_url'],row['source_url'],'main',4)
 def claim(self):
  with self.lock:
   candidates=self.db.execute('SELECT url,origin,scope,priority FROM queue WHERE state="pending"').fetchall()
   cooling={h for (h,) in self.db.execute('SELECT host FROM host_backoff WHERE retry_after>?',(time.time(),))}
   def score(x):
    f=family(x[0]);host=urllib.parse.urlsplit(x[0]).hostname
    # A new awarded website must not inherit the global count of every other
    # site's homepage/project pages. Inspect distinct inner-page families per
    # host before repeatedly sampling an already represented pattern.
    penalty=min(60,self.seen_on_host[(host,f)]*5) if x[2]=='external' else min(12 if f=='main.award-detail' else 60,self.seen[f]*3)
    return x[3]+penalty,x[0]
   chosen=min((x for x in candidates if urllib.parse.urlsplit(x[0]).hostname not in cooling),key=score,default=None)
   row=chosen[:3] if chosen else None
   if row:self.db.execute('UPDATE queue SET state="fetching" WHERE url=?',(row[0],));self.db.commit()
   return row
 def inspect(self,row):
  url,origin,scope=row;record={'id':hashlib.sha256(url.encode()).hexdigest()[:16],'url':url,'discovered_from':origin,'scope':scope,'family':family(url),'observed_at':now(),'inspection_level':'not_observed','visual_inspection':'not_run','interaction_validation':'not_run','skill_extraction':'pending','family_assignment':'URL pattern hint; individual page design requires review','rights':'Reference metadata only; no copied code, imagery or full text redistribution'}
  r,proof=self.policy(url);record['robots']=proof
  if not r.allowed(url):record['status']='robots_disallowed' if proof['policy']=='rules' else 'robots_unavailable';return record
  try:
   code,headers,body,truncated=self.request(url);record.update({'http_status':code,'status':'http_observed' if 200<=code<300 else ('http_blocked' if code in (401,403,429) else 'http_unavailable'),'bytes_read':len(body),'truncated':truncated})
   if 300<=code<400 and headers.get('Location'):
    target=normalize(headers['Location'],url);record['redirect_to']=target
    if target and (same_site(url,target) or scope=='external'):self.add(target,url,scope,3)
    record['status']='redirect';return record
   if code in (404,410):record['status']='http_not_found'
   elif code<200 or code>=300:return record
   content_type=next((v for k,v in headers.items() if k.lower()=='content-type'),'');record['content_type']=content_type
   if not any(s in content_type.lower() for s in ('html','xhtml')):record['status']='non_html';return record
   sha=hashlib.sha256(body).hexdigest();record['source_sha256']=sha;(self.raw/(record['id']+'.html')).write_bytes(body)
   parser=Structure();parser.feed(body.decode('utf-8','replace'));record.update({'inspection_level':'partial_http_dom' if truncated else 'http_dom','title':' '.join(parser.title.split()[:14])[:180],'structure':{'headings':dict(parser.headings),'forms':parser.tags['form'],'input_types':dict(parser.inputs),'navigation_regions':parser.tags['nav'],'main_regions':parser.tags['main'],'sections':parser.tags['section'],'articles':parser.tags['article'],'tables':parser.tags['table'],'dialogs':parser.tags['dialog'],'canvases':parser.tags['canvas'],'videos':parser.tags['video'],'roles':dict(parser.roles),'anchor_count':len(parser.links)}})
   if parser.canonical:record['declared_canonical']=normalize(parser.canonical,url)
   record['content_state_hint']=content_state_hint(parser.title,parser.heading_texts)
   if code in (404,410) and record['content_state_hint']=='unclassified':record['content_state_hint']='http_not_found_reference'
   record['content_state_method']='Title/heading text only; requires rendered review. Unclassified does not prove normal content.'
   root=urllib.parse.urlsplit(url).hostname
   with self.lock:known={h for (h,) in self.db.execute('SELECT host FROM roots')}
   links=[];winners=[];external_pages=[]
   for a in parser.links:
    target=normalize(a['href'],url)
    if not target:continue
    th=urllib.parse.urlsplit(target).hostname
    if th==MAIN and root==MAIN:
     f=family(target);priority=5 if f not in ('main.creator-profile','main.category-list','main.award-detail') else (15 if f=='main.category-list' else (4 if f=='main.award-detail' else 35))
     # Award-list pagination is traversed before repetitive detail records.
     if '?page=' in target:priority=12
     self.add(target,url,'main',priority);links.append(target)
    elif root==MAIN and record['family']=='main.award-detail' and th.removeprefix('www.') not in SOCIAL:
     if 'toolbar-bts__item' in a['class'] or a['text'].strip().lower()=='visit site':
      with self.lock:self.db.execute('INSERT OR IGNORE INTO roots(host,official_url)VALUES(?,?)',(th,url));self.db.commit()
      self.add(target,url,'external',1);winners.append(target)
     elif 'figure-rollover__bt' in a['class']:
      self.add(target,url,'external',4);external_pages.append(target)
    elif scope=='external' and (same_site(target,url) or th in known):
     self.add(target,url,'external',7 if family(target)!='external.other' else 20);links.append(target)
   record['discovered_same_scope_links']=len(set(links));record['external_winner_roots']=sorted(set(winners));record['explicit_external_inner_pages']=sorted(set(external_pages));return record
  except Exception as e:record.update({'status':'request_error','error_type':type(e).__name__,'error':str(e)[:180]});return record
 def worker(self):
  row=self.claim()
  if not row:return False
  record=self.inspect(row)
  with self.lock:
   self.db.execute('UPDATE queue SET state="done",record=? WHERE url=?',(json.dumps(record,ensure_ascii=False),row[0]));self.db.commit()
   if record.get('inspection_level')=='http_dom':
    self.seen[record['family']]+=1;self.seen_on_host[(urllib.parse.urlsplit(record['url']).hostname,record['family'])]+=1
  return True
 def export(self):
  with self.lock:
   rows=[json.loads(r) for (r,) in self.db.execute('SELECT record FROM queue WHERE record IS NOT NULL ORDER BY url')];counts=dict(self.db.execute('SELECT state,COUNT(*)FROM queue GROUP BY state'));roots=[{'host':h,'official_url':u,'award_status':'not_independently_verified'} for h,u in self.db.execute('SELECT host,official_url FROM roots ORDER BY host')];pending=[{'url':u,'scope':s,'family':family(u)} for u,s in self.db.execute('SELECT url,scope FROM queue WHERE state!="done" ORDER BY priority,url')]
  statuses=Counter(r['status'] for r in rows);families=Counter(r['family'] for r in rows if r['inspection_level']=='http_dom');summary={'snapshot_at':now(),'goal':'Convert Awwwards main-site and awarded external-site page patterns into reusable skills','status':'in_progress','scope':['Awwwards public page families and concrete pages','Awarded external websites and their reachable inner pages'],'queue':counts,'observed_records':len(rows),'observed_complete_http_dom':sum(r['inspection_level']=='http_dom' for r in rows),'statuses':dict(statuses),'families_http_dom':dict(sorted(families.items())),'awarded_external_hosts_discovered':len(roots),'not_claimed':['Exhaustive discovery of every historical award','All external websites fully traversed','Visual or interaction completion from HTTP DOM','Skill completion solely from URL counts'],'raw_content_distribution':'not included','robots_respected':True}
  summary['http_dom_content_state_hints']=dict(sorted(Counter(r.get('content_state_hint','unclassified') for r in rows if r['inspection_level']=='http_dom').items()))
  summary['content_state_hint_note']='Title/heading heuristics only. Unclassified is not normal UI proof; complete HTTP DOM includes readable HTTP-error references.'
  summary['awwwards_linked_external_hosts_discovered']=len(roots)
  summary['external_host_count_note']='The legacy awarded_external_hosts_discovered field counts explicit work-detail-linked hosts; winning status is not independently verified per host.'
  summary['pending_sample_count']=min(200,len(pending));summary['pending_sample_is_exhaustive']=len(pending)<=200
  summary['pending_families']=dict(sorted(Counter(p['family'] for p in pending).items()))
  for name,data in [('sources.jsonl',rows),('pending-pages.jsonl',pending[:200]),('external-targets.jsonl',roots)]:
   temp=self.out/(name+'.tmp');temp.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in data),encoding='utf-8',newline='\n');temp.replace(self.out/name)
  temp=self.out/'coverage.json.tmp';temp.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');temp.replace(self.out/'coverage.json');return summary
 def crawl(self,limit,workers):
  # A previous killed process can leave claims behind; only the explicit resume
  # flag in the CLI resets them, after the operator checks the old owner.
  done=0
  with concurrent.futures.ThreadPoolExecutor(workers) as pool:
   while done<limit:
    futures=[pool.submit(self.worker) for _ in range(min(workers,limit-done))];results=[f.result() for f in futures];n=sum(results);done+=n
    if not n:break
    if done%9<workers:summary=self.export();print(json.dumps({'batch_done':done,'records':summary['observed_records'],'queue':summary['queue'],'external_hosts':summary['awarded_external_hosts_discovered']}),flush=True)
  return self.export()
def main():
 p=argparse.ArgumentParser();p.add_argument('--state',required=True);p.add_argument('--out',required=True);p.add_argument('--raw',required=True);p.add_argument('--legacy');p.add_argument('--limit',type=int,default=120);p.add_argument('--workers',type=int,default=3);p.add_argument('--resume-abandoned',action='store_true',help='Reset in-flight claims only after confirming previous owner stopped');a=p.parse_args()
 if not 1<=a.workers<=4 or not 1<=a.limit<=100000:raise SystemExit('Invalid bounds')
 c=Collector(a.state,a.out,a.raw);c.initialize(a.legacy)
 if a.resume_abandoned:
  with c.lock:c.db.execute('UPDATE queue SET state="pending" WHERE state="fetching"');c.db.commit()
 summary=c.crawl(a.limit,a.workers);print(json.dumps(summary,ensure_ascii=True),flush=True)
if __name__=='__main__':main()
