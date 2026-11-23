#!/usr/bin/env python3
"""Map observed metadata to candidate skills without declaring pages completed."""
from pathlib import Path
from collections import Counter
import datetime,json
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
 counts=Counter();unmapped=Counter();rows=[]
 source=R/'research/live_pages/sources.jsonl';source.stat()
 with source.open(encoding='utf-8') as f:
  for line in f:
   s=json.loads(line);candidates=families.get(s['family'],[])
   state='access_unresolved' if s['inspection_level']!='http_dom' else 'family_candidate_needs_page_review' if candidates else 'needs_skill_extraction'
   counts[state]+=1
   if state=='needs_skill_extraction':unmapped[s['family']]+=1
   rows.append({'source_id':s['id'],'url':s['url'],'family_hint':s['family'],'family_assignment':'URL heuristic; not a reviewed design conclusion','inspection_level':s['inspection_level'],'candidate_page_skills':candidates,'included_contract_references':selected.get(s['id'],[]),'candidate_mechanisms':[p['skill'] for p in patterns if set(candidates)&set(p['supports_page_skills'])],'extraction_state':state,'individual_page_design_complete':False})
 out=R/'research/skill_extraction';out.mkdir(exist_ok=True)
 with (out/'source-skill-map.jsonl').open('w',encoding='utf-8',newline='\n') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
 report={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'in_progress','recorded_sources':len(rows),'states':dict(counts),'unmapped_dom_families':dict(unmapped),'contract_reference_sources':len(selected),'all_pages_completed':False,'limitations':['A family match is a navigation aid, not completed individual-page analysis','A shared skill does not prove that every design variation has been extracted','Access-unresolved entries remain gaps even when a family can be guessed','The pending crawl queue is additional work, not included in recorded-source counts']}
 (out/'coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps(report,ensure_ascii=True));return report
if __name__=='__main__':build()
