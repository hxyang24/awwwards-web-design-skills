"""Regenerate the complete original technical sections and local text sheet."""
import html,json,re,hashlib
from pathlib import Path
def render(folder=None):
 folder=Path(folder) if folder else Path(__file__).resolve().parent;data=folder/'product.json'
 if data.stat().st_size>1048576:raise ValueError('Shard data beyond 1 MiB')
 p=json.loads(data.read_text(encoding='utf-8'));e=html.escape
 if p.get('mode')!='fictional_design_study':raise ValueError('Only original fictional study data is supported')
 def ident(x):
  if not re.fullmatch(r'[a-z][a-z0-9-]{0,49}',x):raise ValueError('Invalid identity')
  return x
 def dim(x):
  if x is None:return 'Not supplied'
  if type(x)is not int or not 0<x<=10000:raise ValueError('Invalid example millimetres')
  return str(x)+' mm · example'
 def metric(x):
  if x['basis']=='unknown' and x['value'] is None and x['reference'] is None:return 'Not verified'
  if x['basis'] not in ['example','documented'] or x['value'] is None:raise ValueError('Invalid performance evidence')
  return str(x['value'])+(' '+x['unit'] if x['unit'] else '')+' · '+('example' if x['basis']=='example' else 'documented input')
 def section(id,title,body):return '<article class="panel" id="technical-'+id+'" aria-labelledby="heading-'+id+'" tabindex="-1"><h3 id="heading-'+id+'">'+title+'</h3>'+body+'</article>'
 specs='<p>Illustrative dimensions for this original study. These values are not manufacturing instructions.</p><div class="specs"><dl class="spec-list">'+''.join('<div><dt>'+label+'</dt><dd data-dimension="'+key+'">'+dim(p['dimensions'][key])+'</dd></div>' for key,label in [('width_mm','Width'),('height_mm','Height'),('depth_mm','Depth')])+'</dl><div class="diagram"><svg viewBox="0 0 260 250" role="img" aria-label="Original elevation diagram, not to scale"><path d="M40 220V20H210V220ZM125 20V220M25 20V220M20 20H30M20 220H30M40 235H210M40 230V240M210 230V240" fill="none" stroke="currentColor" stroke-width="2"/></svg><p class="note">Elevation study · not to scale</p></div></div>'
 performance='<p>Unknown evidence stays unknown. A numeric zero is not a substitute for an unverified result.</p><ul class="metric-list">'+''.join('<li><span>'+e(x['label'])+'</span><strong data-metric="'+ident(x['id'])+'">'+e(metric(x))+'</strong><small>Evidence basis: '+e(x['basis'])+'. Confirm applicability and the underlying document before using a value.</small></li>' for x in p['performance'])+'</ul><p class="note">No certification, compliance or engineering approval is implied.</p>'
 options='<p>Choose an illustrative finish. Selection changes only this local original illustration.</p><fieldset><legend>Study finish</legend>'
 for i,x in enumerate(p['finishes']):
  if not re.fullmatch(r'#[a-fA-F0-9]{6}',x['color']):raise ValueError('Invalid swatch')
  options+='<label class="choice"><input type="radio" name="finish" value="'+ident(x['id'])+'"'+(' checked' if i==0 else '')+' disabled><span class="swatch" style="background:'+x['color']+'" aria-hidden="true"></span><span>'+e(x['label'])+'<small>'+e(x['description'])+'</small></span></label>'
 options+='</fieldset>'
 configs='<p>Choose a symbolic arrangement. This diagram describes panel count and a turn; it is not a CAD model or a working configurator.</p><fieldset><legend>Study layout</legend>'+''.join('<label class="choice"><input type="radio" name="layout" value="'+ident(x['id'])+'"'+(' checked' if i==0 else '')+' disabled><span>'+e(x['label'])+'<small>'+str(x['panels'])+' panels · '+str(x['turn'])+'° illustrative turn</small></span></label>' for i,x in enumerate(p['layouts']))+'</fieldset><div class="diagram"><svg id="plan" viewBox="0 0 260 160" role="img" aria-label="Original two-panel line plan, not to scale"><g fill="none" stroke="currentColor" stroke-width="7"><path d="M30 55H130M130 55H230"/></g></svg><p id="plan-caption" class="note">Two-panel line · not to scale</p></div>'
 values={'PANELS':section('specification','Technical specification',specs)+section('performance','Performance evidence',performance)+section('options','Finish options',options)+section('configurations','Configuration studies',configs),'FAQ':''.join('<details><summary>'+e(x['question'])+'</summary><p>'+e(x['answer'])+'</p></details>' for x in p['faq'])}
 target=folder/'index.html';text=target.read_text(encoding='utf-8')
 for name,value in values.items():
  start='<!-- '+name+'_START -->';end='<!-- '+name+'_END -->';text=text[:text.index(start)+len(start)]+value+text[text.index(end):]
 text=re.sub(r'(<meta name="study-data-sha256" content=")[^"]+',lambda m:m[1]+hashlib.sha256(data.read_bytes()).hexdigest(),text)
 text=re.sub(r'(<h1 id="title">).*?(</h1>)',lambda m:m[1]+e(p['title'])+m[2],text)
 text=re.sub(r'(<p id="summary">).*?(</p>)',lambda m:m[1]+e(p['summary'])+m[2],text)
 finish=p['finishes'][0];layout=p['layouts'][0]
 text=re.sub(r'(<div id="elevation"[^>]*>).*?(</div>)',lambda m:m[1]+''.join('<span></span>' for _ in range(layout['panels']))+m[2],text)
 text=re.sub(r'(id="elevation"[^>]*aria-label=")[^"]+',lambda m:m[1]+e('Original illustration: '+finish['label']+' / '+layout['label'],quote=True),text)
 text=re.sub(r'(<figcaption id="caption">).*?(</figcaption>)',lambda m:m[1]+e(finish['label']+' / '+layout['label']+' / symbolic illustration')+m[2],text)
 target.write_text(text,encoding='utf-8',newline='\n')
 lines=['ORIGINAL FICTIONAL DESIGN STUDY',p['title'],p['summary'],'Not an engineering specification, certification, quotation or order.']+[label+': '+dim(p['dimensions'][key]) for key,label in [('width_mm','Width'),('height_mm','Height'),('depth_mm','Depth')]]+['PERFORMANCE']+[x['label']+': '+metric(x) for x in p['performance']]+['FINISHES']+[x['label']+': '+x['description'] for x in p['finishes']]+['LAYOUTS']+[x['label'] for x in p['layouts']]+['Pricing, availability, installation and manufacturing remain unknown. No message is sent.']
 (folder/'concept-sheet.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n');return {'panels':4,'finishes':len(p['finishes']),'layouts':len(p['layouts'])}
if __name__=='__main__':print(json.dumps(render()))
