"""Regenerate the complete original guide and native downloads; no network."""
import hashlib,html,json,re
from pathlib import Path

def render(folder=None):
 p=Path(folder or Path(__file__).parent);raw=(p/'guide.json').read_bytes();d=json.loads(raw)
 e=lambda v:html.escape(str(v),quote=True)
 assert d['schema_version']==1 and d['origin']=='original_fictional_study'
 assert re.fullmatch('[A-Za-z0-9._-]{1,30}',d['version']) and re.fullmatch('[a-z][a-z0-9-]{0,39}',d['id'])
 for a in ('palette','symbols','motion'):assert 2<=len(d[a])<=32 and len({x['id'] for x in d[a]})==len(d[a])
 for x in d['palette']:assert re.fullmatch('[a-z][a-z0-9-]{0,39}',x['id']) and re.fullmatch('#[0-9a-fA-F]{6}',x['hex'])
 for x in d['symbols']:assert x['shape'] in ('orbit','window','steps','cross')
 for x in d['motion']:assert 100<=x['duration_ms']<=1800 and x['easing'] in ('linear','cubic-bezier(0.2, 0.8, 0.2, 1)')
 css='/* Original fictional '+d['id']+' palette / MIT / version '+d['version']+' */\n:root {\n'+'\n'.join('  --color-'+x['id']+': '+x['hex'].upper()+';' for x in d['palette'])+'\n}\n'
 exported={'schema_version':1,'id':d['id'],'version':d['version'],'license':'MIT','origin':d['origin'],'colors':{x['id']:x['hex'].upper() for x in d['palette']}}
 (p/'palette.css').write_text(css,encoding='utf-8',newline='\n');(p/'palette.json').write_text(json.dumps(exported,indent=2)+'\n',encoding='utf-8',newline='\n')
 s=(p/'index.html').read_text(encoding='utf-8')
 def block(name,value):
  nonlocal s
  s=re.sub(r'(<!-- '+name+'_START -->).*?(<!-- '+name+'_END -->)',lambda m:m[1]+value+m[2],s,flags=re.S)
 block('PALETTE',''.join('<li class="swatch"><div class="paint" style="background:'+x['hex']+'" aria-hidden="true"></div><div class="text"><h3>'+e(x['name'])+'</h3><code>'+e(x['hex'].upper())+'</code><button data-copy-color="'+e(x['id'])+'" disabled>Copy '+e(x['name'])+'</button></div></li>' for x in d['palette']))
 block('SYMBOLS',''.join('<li><span class="symbol '+e(x['shape'])+'" aria-hidden="true"></span><span>'+e(x['name'])+'</span></li>' for x in d['symbols']))
 block('MOTIONS',''.join('<option value="'+e(x['id'])+'">'+e(x['name'])+' / '+str(x['duration_ms'])+' ms</option>' for x in d['motion']))
 block('CSS',e(css));s=re.sub(r'(<meta name="guide-data-sha256" content=")[^"]+',lambda m:m[1]+hashlib.sha256(raw).hexdigest(),s)
 for tag,ident,value in [('h1','guide-title',d['title']),('p','summary',d['summary']),('span','version',d['version'])]:s=re.sub(r'(<'+tag+' id="'+ident+'"[^>]*>).*?(</'+tag+'>)',lambda m:m[1]+e(value)+m[2],s,flags=re.S)
 s=re.sub(r'<title>.*?</title>',lambda m:'<title>'+e(d['title'])+'</title>',s)
 (p/'index.html').write_text(s,encoding='utf-8',newline='\n');return {'colors':len(d['palette']),'symbols':len(d['symbols']),'transitions':len(d['motion'])}
if __name__=='__main__':print(json.dumps(render()))
