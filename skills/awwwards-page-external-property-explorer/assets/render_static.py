"""Regenerate a complete fictional catalogue and local notes, without network."""
import json,re,html,hashlib
from pathlib import Path
def render(folder=None):
 p=Path(folder or Path(__file__).parent);raw=(p/'catalogue.json').read_bytes();d=json.loads(raw);e=lambda x:html.escape(str(x),quote=True)
 assert d['schema_version']==1 and d['origin']=='original_fictional_study' and 2<=len(d['units'])<=48
 assert len({x['id'] for x in d['units']})==len(d['units']) and len({(x['building'],x['floor'],x['bay']) for x in d['units']})==len(d['units'])
 area=lambda v:'Not supplied' if v is None else f'{v/100:g} m²'
 rooms=lambda v:'Not supplied' if v is None else f'{v/2:g} '+('room' if v==2 else 'rooms')
 status=lambda v:'Availability not supplied' if v is None else 'Example '+v
 rows=[];notes=[d['title']+' / Original fictional study','Catalogue revision '+d['revision'],'Geometry, area and daylight are illustrative. Prices and real availability are not supplied. No inquiry is submitted.','']
 for u in d['units']:
  assert re.fullmatch('[a-z][a-z0-9-]{0,39}',u['id']) and u['building'] in ('east','west') and 0<=u['floor']<=5 and 0<=u['bay']<=3
  assert u['area_hundredths'] is None or isinstance(u['area_hundredths'],int) and 1<=u['area_hundredths']<=500000
  floor='Ground' if u['floor']==0 else f"{u['floor']:02d}"
  facts=[('Area',area(u['area_hundredths'])),('Room units',rooms(u['rooms_half'])),('Floor',floor),('Price','Not supplied')]
  rows.append('<li class="static-space" id="space-'+e(u['id'])+'"><p class="meta">'+e(u['type'].upper()+' / '+u['building'].upper())+'</p><h3>'+e(u['label'])+'</h3><p class="availability">'+e(status(u['availability']))+'</p><dl>'+''.join('<dt>'+e(k)+'</dt><dd>'+e(v)+'</dd>' for k,v in facts)+'</dl><details><summary>Read the original space note</summary><p>'+e(u['description'])+'</p><p>Features: '+e(', '.join(u['features']) or 'None in this study')+'</p></details></li>')
  notes.extend([u['label']+' / '+u['type']+' / '+u['building'],status(u['availability'])]+[k+': '+v for k,v in facts]+[u['description'],''])
 s=(p/'index.html').read_text(encoding='utf-8');s=re.sub(r'(<!-- SPACES_START -->).*?(<!-- SPACES_END -->)',lambda m:m[1]+''.join(rows)+m[2],s,flags=re.S)
 s=re.sub(r'(<meta name="catalogue-data-sha256" content=")[^"]+',lambda m:m[1]+hashlib.sha256(raw).hexdigest(),s)
 for tag,name,value in [('h1','project-title',d['title']),('p','project-summary',d['summary'])]:s=re.sub(r'(<'+tag+' id="'+name+'"[^>]*>).*?(</'+tag+'>)',lambda m:m[1]+e(value)+m[2],s,flags=re.S)
 options='<option value="all">Any room count</option><option value="unknown">Not supplied</option>'+''.join('<option value="'+str(n)+'">'+f'{n/2:g}'+(' room' if n==2 else ' rooms')+'</option>' for n in range(1,13))
 s=re.sub(r'(<select id="rooms"[^>]*>).*?(</select>)',lambda m:m[1]+options+m[2],s,flags=re.S)
 (p/'index.html').write_text(s,encoding='utf-8',newline='\n');(p/'study-notes.txt').write_text('\n'.join(notes),encoding='utf-8',newline='\n');return {'complete_spaces':len(rows),'unknown_area':sum(x['area_hundredths'] is None for x in d['units'])}
if __name__=='__main__':print(json.dumps(render()))
