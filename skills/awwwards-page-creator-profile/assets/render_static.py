"""Regenerate complete original public profile and every work, without fetching media."""
from pathlib import Path
import html,json,re,hashlib
LABELS={'selected':'Study selection','entry':'Study entry','unknown':'Label unknown'}
UNAVAILABLE='<section class="unavailable"><h1 id="profile-title" tabindex="-1">Profile unavailable</h1><p>This profile is not available here. No identity, works or private details are displayed.</p><a href="#top">Return to the directory header</a></section>'
def render(folder=None):
 folder=Path(folder) if folder else Path(__file__).resolve().parent;p=folder/'profile.json'
 if p.stat().st_size>1048576:raise ValueError('Shard public data beyond1MiB')
 d=json.loads(p.read_text(encoding='utf-8'));e=html.escape
 def identity(x):
  if not isinstance(x,str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,49}',x):raise ValueError('Invalid work identity')
  return x
 def art(w):
  if w['art']not in ['grid','arc','type']:raise ValueError('Unsupported original illustration')
  return '<div class="art '+w['art']+'" role="img" aria-label="Original abstract study: '+e(w['title'],quote=True)+'"><span aria-hidden="true"></span></div>'
 public=d.get('visibility')=='public'
 if not public and (d!={'schema_version':1,'visibility':'unavailable'}):raise ValueError('Unavailable profile must contain no identity fields')
 if public:
  identity(d['id']);works=d['works']
  if not 1<=len(works)<=500 or len({identity(w['id'])for w in works})!=len(works):raise ValueError('Bounded unique works required')
  metrics=''
  for x in d['reported_metrics']:
   value=x['value']
   if value is not None and(type(value)is not int or not 0<=value<=1000000):raise ValueError('Unknown and zero reports are distinct')
   metrics+='<div><dt>'+e(x['label'])+'<small class="report-date">'+e('Report date: '+x['observed_at']if x['observed_at']else'Report date not supplied')+'</small></dt><dd>'+('Not supplied'if value is None else str(value))+'</dd></div>'
  links=''
  for x in d['public_links']:
   if x['url']is None:links+='<li>'+e(x['label'])+' · Not supplied</li>';continue
   from urllib.parse import urlsplit
   u=urlsplit(x['url'])
   if u.scheme not in ['http','https']or not u.netloc or u.username or u.password:raise ValueError('Public URL required')
   links+='<li><a href="'+e(x['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(x['label'])+' ↗</a></li>'
  profile='<section class="profile" aria-labelledby="profile-title"><div><p class="eyebrow">Original fictional '+e(d['entity_type'])+'</p><h1 id="profile-title">'+e(d['name'])+'</h1><p class="profile-meta">'+e(d['location']or'Location not supplied')+'</p><p class="bio">'+e(d['bio'])+'</p><ul class="services">'+''.join('<li>'+e(x)+'</li>'for x in d['services'])+'</ul><button id="shortlist" aria-pressed="false" disabled>Keep on this device</button><p id="shortlist-status" role="status">Nothing saved. Optional shortlist controls are loading.</p><ul class="public-links">'+links+'</ul></div><aside aria-labelledby="report-title"><div class="identity-mark" role="img" aria-label="Original abstract Common Room study mark"><span aria-hidden="true">cr.</span></div><h2 id="report-title">Fictional provider report</h2><dl class="metrics">'+metrics+'</dl><p class="report-scope">These are supplied fictional report values, not a count of visible cards or verified awards. Each supplied report date is shown separately. The complete local study contains '+str(len(works))+' works.</p></aside></section>'
  cards=''.join('<li class="work-card" id="card-'+w['id']+'">'+art(w)+'<div><p class="work-meta">'+e(w['category'].capitalize())+' / '+e(w['date']or'Date not supplied')+'</p><h3><a id="read-'+w['id']+'" data-work="'+w['id']+'" href="#work-'+w['id']+'">'+e(w['title'])+'</a></h3><p>'+e(w['summary'])+'</p><p class="work-meta">'+LABELS[w['recognition']]+'</p></div></li>'for w in works)
  readings=''.join('<article class="reading" id="work-'+w['id']+'" tabindex="-1"><h3>'+e(w['title'])+'</h3><p>'+e(w['summary'])+'</p><p class="contribution">Contribution: '+e(w['contribution'])+'</p><p>'+e(w['body'])+'</p><a href="#works">Back to the work archive</a></article>'for w in works)
 else:profile=UNAVAILABLE;cards='';readings='';works=[]
 target=folder/'index.html';s=target.read_text(encoding='utf-8')
 for name,value in [('PROFILE',profile),('WORKS',cards),('READINGS',readings)]:
  start='<!-- '+name+'_START -->';end='<!-- '+name+'_END -->';s=s[:s.index(start)+len(start)]+value+s[s.index(end):]
 s=re.sub(r'<title>.*?</title>',lambda m:'<title>'+e(d['name']if public else'Profile unavailable')+' / original study</title>',s)
 for pattern in [r'(<section id="work-section")([^>]*)(>)',r'(<section class="context" id="context")([^>]*)(>)']:
  def section_state(m):
   attrs=re.sub(r'\s+hidden(?=\s|$)','',m[2]).strip()
   return m[1]+(' hidden'if not public else'')+(' '+attrs if attrs else'')+'>'
  s=re.sub(pattern,section_state,s)
 s=re.sub(r'All (eight|\d+) original works and complete descriptions are available below\.',f'All {len(works)} original works and complete descriptions are available below.',s)
 s=re.sub(r'(<meta name="creator-data-sha256" content=")[^"]+',lambda m:m[1]+hashlib.sha256(p.read_bytes()).hexdigest(),s)
 target.write_text(s,encoding='utf-8',newline='\n');return{'public':public,'complete_works':len(works),'identity_in_unavailable':False}
if __name__=='__main__':print(json.dumps(render()))
