#!/usr/bin/env python3
"""Audit factual and editorial contracts; cannot independently verify marketing claims."""
import argparse,json,re,sys
from pathlib import Path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();d=json.loads(a.path.read_text(encoding='utf-8'));errors=[]
 if not d.get('site_name'):errors.append('site_name missing')
 paths=set()
 for r in d.get('routes',[]):
  path=r.get('path')
  if not path or path in paths:errors.append('missing/duplicate route path')
  paths.add(path)
  for k in ('title','description','h1','primary_cta'):
   if not isinstance(r.get(k),str) or len(r[k].strip())<3:errors.append(f'{path}: missing {k}')
  if len(r.get('title',''))>72:errors.append(f'{path}: title too long')
  if len(r.get('description',''))>180:errors.append(f'{path}: meta description too long')
  for img in r.get('images',[]):
   if not img.get('src') or 'alt' not in img:errors.append(f'{path}: image src/alt missing')
  for field in ('title','description','h1','primary_cta'):
   if re.search(r'(?i)lorem ipsum|placeholder|todo|待填写|测试文案',r.get(field,'')):errors.append(f'{path}: placeholder in {field}')
  for claim in r.get('public_claims',[]):
   if not claim.get('source') and not claim.get('verified_by_owner'):errors.append(f'{path}: unsourced claim: {claim.get("text","")[:30]}')
 if not d.get('routes'):errors.append('no routes')
 print(json.dumps({'passed':not errors,'route_count':len(d.get('routes',[])),'errors':errors,'limitations':['声明的真实来源仍需人为验证','不验证外部链接当前可用性']},ensure_ascii=False,indent=2));sys.exit(bool(errors))
