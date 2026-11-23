"""Regenerate complete original static catalog and details from catalog.json."""
from pathlib import Path
import json,html,re
LABELS={'ready':'In stock','made':'Made to order','unknown':'Availability unknown','soldout':'Unavailable'}
def render(folder=None):
 folder=Path(folder) if folder else Path(__file__).resolve().parent;p=folder/'catalog.json'
 if p.stat().st_size>1048576:raise ValueError('Catalog exceeds the standalone study limit')
 data=json.loads(p.read_text(encoding='utf-8'));products=data['products'];categories={c['id']:c['label'] for c in data['categories']};e=html.escape
 if not 1<=len(products)<=1000 or len({p['id'] for p in products})!=len(products):raise ValueError('Invalid product identities')
 def price(p):
  value=p['price_cents']
  if value is None:return 'Price on request'
  if type(value) is not int or not 0<=value<=10000000:raise ValueError('Invalid integer cents')
  return '$'+str(value//100)+'.'+str(value%100).zfill(2)+' USD'
 def art(p):
  if not re.fullmatch(r'[a-z][a-z0-9-]{0,59}',p['id']) or p['shape'] not in ['lamp','vessel','bowl','cloth','book'] or p['finish'] not in ['sand','chalk','ink','rust']:raise ValueError('Invalid art or object identity')
  return '<div class="art '+p['shape']+' '+p['finish']+'" role="img" aria-label="Original abstract illustration: '+e(p['title'])+'"><span class="shape" aria-hidden="true"></span><span class="art-label" aria-hidden="true">FORM / '+str(p['rank']).zfill(2)+'</span></div>'
 cards=''.join('<li id="card-'+p['id']+'" tabindex="-1"><article class="card">'+art(p)+'<p class="category">'+e(categories[p['category']])+'</p><h3><a id="read-'+p['id']+'" data-item="'+p['id']+'" href="#object-'+p['id']+'">'+e(p['title'])+'</a></h3><p class="price">'+price(p)+'</p><p class="availability">'+LABELS[p['availability']]+'</p></article></li>' for p in products)
 details=''.join('<article class="static-object" id="object-'+p['id']+'" tabindex="-1"><h3>'+e(p['title'])+'</h3><p>'+e(p['description'])+'</p><p>'+e(p['detail'])+'</p><p>'+e(p['material'])+' · '+e(p['dimensions'])+' · '+LABELS[p['availability']]+' · '+price(p)+'</p><p>Fictional study only. Tax and delivery remain unknown; no purchase or reservation is offered.</p><a href="#catalog">Back to the collection</a></article>' for p in products)
 p=folder/'index.html';text=p.read_text(encoding='utf-8')
 for marker,value in [('CATALOG',cards),('DETAILS',details)]:
  start='<!-- '+marker+'_START -->';end='<!-- '+marker+'_END -->';text=text[:text.index(start)+len(start)]+value+text[text.index(end):]
 text=re.sub(r'All \d+ original objects are available below\.',f'All {len(products)} original objects are available below.',text)
 p.write_text(text,encoding='utf-8',newline='\n');return len(products)
if __name__=='__main__':print(json.dumps({'static_objects':render()}))
