#!/usr/bin/env python3
"""Append cases in a new dataset; reject unsupported facts and ID replacement."""
import argparse,json,sys
from pathlib import Path
from case_tool import validate
BASE=Path(__file__).resolve().parents[3]/'research/cases/representative_30.json'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--incoming',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():p.error('output exists')
 d=json.loads(BASE.read_text(encoding='utf-8'));v=json.loads(a.incoming.read_text(encoding='utf-8'))
 if isinstance(v,dict):v=v.get('cases',[])
 if not isinstance(v,list):p.error('incoming must list cases')
 issues=validate(v);oldids={x['case_id'] for x in d['cases']};issues.extend(f'existing case {x.get("case_id")}' for x in v if x.get('case_id') in oldids)
 if issues:
  print(json.dumps({'passed':False,'errors':issues},ensure_ascii=False,indent=2));sys.exit(1)
 d['cases'].extend(v);d['case_count']=len(d['cases']);d['derived_from']='bundled reference; new cases appended, not silently rewritten'
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'passed':True,'created':str(a.output),'cases':len(d['cases'])},ensure_ascii=False))
