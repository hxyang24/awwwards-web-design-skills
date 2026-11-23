"""Render full original reference content; never retrieves or copies source-site media."""
from pathlib import Path
import json,re,html,hashlib
def render(folder=None):
 folder=Path(folder) if folder else Path(__file__).resolve().parent;p=folder/'reference.json'
 if p.stat().st_size>1048576:raise ValueError('Shard reference data beyond1MiB')
 d=json.loads(p.read_text(encoding='utf-8'));e=html.escape
 def ident(x):
  if not re.fullmatch(r'[a-z][a-z0-9-]{0,49}',x):raise ValueError('Invalid reference identity')
  return x
 for t in d['tags']:ident(t)
 if len(d['related'])>30 or len(d['transcript'])>30:raise ValueError('Bounded reference content required')
 values={'TAGS':''.join('<li>'+e(t)+'</li>'for t in d['tags']),'TOPICS':''.join('<option value="'+t+'">'+e(t.capitalize())+'</option>'for t in d['tags']),'TRANSCRIPT':'<ol class="description">'+''.join('<li><time>'+str(x['start'])+'–'+str(x['end'])+' seconds</time><div><h3>'+e(x['title'])+'</h3><p>'+e(x['text'])+'</p></div></li>'for x in d['transcript'])+'</ol>',
 'RELATED':''.join('<li class="related-card" data-note="'+ident(x['id'])+'"><span class="number" aria-hidden="true">0'+str(i)+'</span><h3><a href="#note-'+x['id']+'">'+e(x['title'])+'</a></h3><p>'+e(x['summary'])+'</p><p>'+e(' / '.join(x['tags']))+'</p></li>'for i,x in enumerate(d['related'],1)),
 'READINGS':''.join('<article class="reading" id="note-'+ident(x['id'])+'" tabindex="-1"><h3>'+e(x['title'])+'</h3><p>'+e(x['body'])+'</p><a href="#related">Back to related notes</a></article>'for x in d['related'])}
 target=folder/'index.html';s=target.read_text(encoding='utf-8')
 for name,value in values.items():
  start='<!-- '+name+'_START -->';end='<!-- '+name+'_END -->';s=s[:s.index(start)+len(start)]+value+s[s.index(end):]
 for tag,id,value in [('h1','reference-title',d['title']),('p','summary',d['summary']),('span','creator',d['creator'])]:s=re.sub(r'(<'+tag+r'\b[^>]*\bid="'+id+r'"[^>]*>).*?(</'+tag+'>)',lambda m:m[1]+e(value)+m[2],s)
 source=d['source'];href='#project-note'
 if source['url'] is not None:
  from urllib.parse import urlsplit
  u=urlsplit(source['url'])
  if u.scheme not in ['http','https'] or not u.netloc or u.username or u.password or len(source['url'])>2048:raise ValueError('Public safe source URL required')
  href=source['url']
 s=re.sub(r'<a id="source-link"[^>]*>.*?</a>',lambda m:'<a id="source-link" href="'+e(href,quote=True)+'"'+(' target="_blank" rel="noopener noreferrer"'if source['url']else'')+'>'+e(source['label'])+'</a>',s)
 s=re.sub(r'(<meta name="reference-data-sha256" content=")[^"]+',lambda m:m[1]+hashlib.sha256(p.read_bytes()).hexdigest(),s)
 s=re.sub(r'All (three|\d+) original notes are available below\.',f'All {len(d["related"])} original notes are available below.',s)
 target.write_text(s,encoding='utf-8',newline='\n');return{'transcript_segments':len(d['transcript']),'related_notes':len(d['related'])}
if __name__=='__main__':print(json.dumps(render()))
