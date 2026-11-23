#!/usr/bin/env python3
"""Keep work-detail title labels distinct from certified site/inner-page awards."""
from pathlib import Path
from collections import Counter
import datetime,json,re
R=Path(__file__).resolve().parents[1]

def build():
 source=R/'research/live_pages/sources.jsonl';source.stat();rows=[]
 with source.open(encoding='utf-8') as f:
  for line in f:
   s=json.loads(line)
   if s['family']!='main.award-detail' or s['inspection_level']!='http_dom':continue
   title=s.get('title','');label='sotd' if re.search(r'\bSOTD\b',title,re.I) else 'nominee' if re.search(r'\bNominee\b',title,re.I) else 'honorable_mention' if re.search(r'Honorable Mention',title,re.I) else 'undetermined'
   rows.append({'source_id':s['id'],'official_url':s['url'],'observed_title_label':label,'observed_at':s['observed_at'],'source_sha256':s['source_sha256'],'method':'Official HTML title from the timestamped HTTP observation','not_claimed':'Not a fresh live badge audit, a current version match, or an award for every linked inner page'})
 out=R/'research/skill_extraction';out.mkdir(exist_ok=True)
 with (out/'official-detail-title-labels.jsonl').open('w',encoding='utf-8',newline='\n') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
 report={'recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'official_detail_observations':len(rows),'observed_title_labels':dict(Counter(r['observed_title_label'] for r in rows)),'scope':'Counts official work-detail observations, not unique external hosts or awarded inner pages','source_eligibility_note':'Nominee is a nomination label and must not be counted as a confirmed award. SOTD/Honorable Mention title labels remain timestamped source reports; do not infer all current inner pages won.','all_awarded_sites_enumerated':False}
 (out/'award-provenance-coverage.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(report));return report
if __name__=='__main__':build()
