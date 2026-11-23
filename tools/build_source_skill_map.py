#!/usr/bin/env python3
"""Map observed metadata to candidate skills without declaring pages completed."""
from pathlib import Path
from collections import Counter
import datetime,json,hashlib
from reviewed_family import load_reviews,assign_family
R=Path(__file__).resolve().parents[1]

def build():
 registry=json.loads((R/'page_skills/registry.json').read_text(encoding='utf-8'))['skills']
 patterns=json.loads((R/'interaction_skills/registry.json').read_text(encoding='utf-8'))['skills']
 families={}
 for s in registry:
  for f in s['source_families']:families.setdefault(f,[]).append(s['skill'])
 selected={}
 for s in registry:
  c=json.loads((R/s['path']/'references/page-contract.json').read_text(encoding='utf-8'))
  for source in c['sources']:selected.setdefault(source['id'],[]).append(s['skill'])
 evidence={};variants={}
 for filename,key in [('visual-observations.json','observations'),('interaction-observations.json','observations'),('creative-page-observations.json','observations'),('pricing-page-observations.json','observations'),('editorial-page-observations.json','observations'),('product-page-observations.json','observations')]:
  file=R/'research/live_pages'/filename
  if not file.exists():continue
  file.stat()
  for view in json.loads(file.read_text(encoding='utf-8')).get(key,[]):
   source_id=view.get('source_id')
   if source_id:evidence.setdefault(source_id,[]).append({'record':view.get('id',str(view.get('viewport',{}))),'file':'research/live_pages/'+filename,'status':view.get('status'),'viewport':view.get('viewport'),'observed_state_changes':sum(a.get('observable_state_changed',False) for a in view.get('actions',[]))})
 counts=Counter();unmapped=Counter();rows=[];reviews=load_reviews(R)
 source=R/'research/live_pages/sources.jsonl';source.stat()
 with source.open(encoding='utf-8') as f:
  for line in f:
   s=json.loads(line);assignment=assign_family(s,reviews);s['family']=assignment['family'];candidates=families.get(s['family'],[])
   state='access_unresolved' if s['inspection_level']!='http_dom' else 'source_content_requires_review' if s.get('content_state_hint','unclassified')!='unclassified' else 'family_candidate_needs_page_review' if candidates else 'needs_skill_extraction'
   counts[state]+=1
   if state=='needs_skill_extraction':unmapped[s['family']]+=1
   if s['inspection_level']=='http_dom':
    structure=s['structure'];signature={k:structure.get(k,0) for k in ['forms','tables','dialogs','canvases','videos','navigation_regions']};signature['content_state_hint']=s.get('content_state_hint','unclassified');signature['input_types']=sorted(structure.get('input_types',{}));variant_id=hashlib.sha256(json.dumps([s['family'],signature],sort_keys=True).encode()).hexdigest()[:16]
    variant=variants.setdefault(variant_id,{'id':variant_id,'family_hint':s['family'],'observed_dom_signature':signature,'pages':0,'example_source_ids':[],'candidate_page_skills':candidates,'status':'requires_variant_review','not_claimed':'DOM element counts do not prove visible layout, technology, state or completed skill extraction'});variant['pages']+=1
    if len(variant['example_source_ids'])<5:variant['example_source_ids'].append(s['id'])
   rows.append({'source_id':s['id'],'url':s['url'],'family_hint':s['family'],'heuristic_family':assignment['heuristic'],'family_assignment':assignment['assignment'],'family_review':assignment.get('review'),'family_review_status':assignment.get('review_status'),'inspection_level':s['inspection_level'],'content_state_hint':s.get('content_state_hint','unclassified'),'candidate_page_skills':candidates,'included_contract_references':selected.get(s['id'],[]),'candidate_mechanisms':[p['skill'] for p in patterns if set(candidates)&set(p['supports_page_skills'])],'recorded_view_and_state_evidence':evidence.get(s['id'],[]),'extraction_state':state,'individual_page_design_complete':False})
 out=R/'research/skill_extraction';out.mkdir(exist_ok=True)
 with (out/'source-skill-map.jsonl').open('w',encoding='utf-8',newline='\n') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
 report={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'in_progress','recorded_sources':len(rows),'states':dict(counts),'unmapped_dom_families':dict(unmapped),'contract_reference_sources':len(selected),'sources_with_recorded_view_or_state_evidence':sum(bool(r['recorded_view_and_state_evidence']) for r in rows),'dom_signature_variant_candidates':len(variants),'all_pages_completed':False,'limitations':['A family match is a navigation aid, not completed individual-page analysis','A shared skill does not prove that every design variation has been extracted','Access-unresolved entries remain gaps even when a family can be guessed','The pending crawl queue is additional work, not included in recorded-source counts']}
 (out/'variant-backlog.json').write_text(json.dumps({'status':'in_progress','scope':'DOM signatures for prioritizing concrete variant inspections; not a completed pattern library','variants':list(variants.values())},ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 (out/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps(report,ensure_ascii=True));return report
if __name__=='__main__':build()
