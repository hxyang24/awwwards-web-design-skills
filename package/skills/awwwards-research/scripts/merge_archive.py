#!/usr/bin/env python3
"""Non-destructive merge of explicitly sourced SOTM claims into a NEW dataset."""
import argparse,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[3]/'research/archive/sites_of_the_month.json'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--incoming',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():p.error('output exists; refuses overwrite')
 d=json.loads(BASE.read_text(encoding='utf-8'));incoming=json.loads(a.incoming.read_text(encoding='utf-8'))
 if not isinstance(incoming,list):p.error('incoming must be JSON array')
 byid={x['id']:x for x in d['rows']};issues=[];added=0;conflicts=0
 for r in incoming:
  if not isinstance(r,dict):issues.append('non-object incoming record');continue
  if not r.get('id') or not r.get('name') or not r.get('official_url') or not r.get('source_url') or r.get('retrieved_at') is None:issues.append('record missing identity/source/retrieved_at');continue
  if r.get('award_month') is not None and (not isinstance(r['award_month'],int) or not 1<=r['award_month']<=12):issues.append('invalid month for '+r['id']);continue
  if r['id'] not in byid:
   r['award_type']='SOTM';r.setdefault('month_claims',[]);r['month_verification']='primary_month_claim' if r.get('award_month') else 'unknown';d['rows'].append(r);byid[r['id']]=r;added+=1
  else:
   o=byid[r['id']]
   if isinstance(r.get('award_month'),int) and o.get('award_month') is not None and o['award_month']!=r['award_month']:
    o.setdefault('candidate_month_claims',[]).append({'year':r.get('award_year'),'month':r['award_month'],'source_url':r['source_url'],'confidence':'review_required'});o['month_verification']='conflicting_claims';conflicts+=1
   elif o.get('award_month') is None and r.get('award_month') is not None:
    # Do not automatically fill unknown; preserve an explicit review candidate.
    o.setdefault('candidate_month_claims',[]).append({'year':r.get('award_year'),'month':r['award_month'],'source_url':r['source_url'],'confidence':'review_required'});
 d['record_count']=len(d['rows']);d['derived_from']='bundled archive; merged candidates do not constitute official approval';a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'created':str(a.output),'added':added,'conflicts':conflicts,'problems':issues,'review_required':True},ensure_ascii=False,indent=2));sys.exit(bool(issues))
