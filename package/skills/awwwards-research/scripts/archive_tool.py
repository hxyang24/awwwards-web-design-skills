#!/usr/bin/env python3
"""Query bundled official archive with strict evidence and unknown-month semantics."""
import argparse,json
from collections import Counter
from pathlib import Path
DATA=Path(__file__).resolve().parents[3]/'research/archive/sites_of_the_month.json'
COV=Path(__file__).resolve().parents[3]/'research/coverage/coverage_summary.json'
def load():return json.loads(DATA.read_text(encoding='utf-8'))
def month(r):return f"{r['award_year']}-{r['award_month']:02d}" if isinstance(r.get('award_month'),int) else 'UNKNOWN'
def sub(r,k):return [x.get('value',x.get('name','')) for x in r.get('taxonomy',{}).get(k,[])]
def main():
 a=argparse.ArgumentParser(); sp=a.add_subparsers(dest='cmd',required=True);sp.add_parser('stats');sp.add_parser('missing');sp.add_parser('validate')
 q=sp.add_parser('search');q.add_argument('--year',type=int);q.add_argument('--month',type=int);q.add_argument('--keyword');q.add_argument('--industry');q.add_argument('--technology');q.add_argument('--status');q.add_argument('--limit',type=int,default=100);q.add_argument('--json',action='store_true')
 s=sp.add_parser('show');s.add_argument('--id',required=True);opt=a.parse_args();rows=load()['rows'];cov=json.loads(COV.read_text(encoding='utf-8'))
 if opt.cmd=='stats':
  print(json.dumps({'sites':len(rows),'years':dict(sorted(Counter(x['award_year'] for x in rows).items())),'known_months':sum(isinstance(x.get('award_month'),int) for x in rows),'unknown_months':sum(x.get('award_month') is None for x in rows),'classification_counts':cov.get('classification_completeness',{}),'month_status_counts':cov.get('month_status_counts',{})},ensure_ascii=False,indent=2));return
 if opt.cmd=='missing':
  print(json.dumps({'missing_evidence_months':cov['missing_evidence_months'],'conflicting_months':cov['conflicting_months'],'unresolved_month_cases':cov['unresolved_month_cases']},ensure_ascii=False,indent=2));return
 if opt.cmd=='validate':
  ids=[r['id'] for r in rows];err=[]
  if len(ids)!=len(set(ids)):err.append('duplicate ID')
  if len(rows)!=load()['record_count']:err.append('count mismatch')
  for r in rows:
   if r.get('award_month') is not None and not 1<=r['award_month']<=12:err.append('bad month: '+r['id'])
   if not r.get('official_url') or not r.get('source_url'):err.append('source missing: '+r['id'])
  print(json.dumps({'ok':not err,'errors':err},ensure_ascii=False));raise SystemExit(bool(err))
 if opt.cmd=='show':
  d=next((r for r in rows if r['id']==opt.id),None)
  if not d:raise SystemExit('ID not found')
  print(json.dumps(d,ensure_ascii=False,indent=2));return
 if opt.cmd=='search':
  for attr,v in [('award_year',opt.year),('award_month',opt.month),('month_verification',opt.status)]:
   if v is not None: rows=[x for x in rows if x.get(attr)==v]
  if opt.keyword: rows=[x for x in rows if opt.keyword.lower() in (x['name']+' '+x['id']).lower()]
  if opt.industry: rows=[x for x in rows if any(opt.industry.lower() in y.lower() for y in sub(x,'industry'))]
  if opt.technology: rows=[x for x in rows if any(opt.technology.lower() in y.lower() for y in sub(x,'technology'))]
  if opt.json:print(json.dumps(rows[:opt.limit],ensure_ascii=False,indent=2))
  else:
   for r in rows[:opt.limit]:print(f"{month(r):7} {r['id'][:38]:38} {r['name']} [{r.get('month_verification') or 'unknown'}]")
   print(f'SHOWING {min(opt.limit,len(rows))}/{len(rows)}')
if __name__=='__main__':main()
