#!/usr/bin/env python3
import sys,json,argparse
from pathlib import Path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('path',type=Path);a=p.parse_args();d=json.loads(a.path.read_text(encoding='utf-8'));errs=[]
 for k in ('purpose','primary_dom_action','static_fallback','dispose_policy','reduced_motion','assets','budgets'):
  if not d.get(k):errs.append('missing: '+k)
 b=d.get('budgets',{})
 if b.get('max_device_pixel_ratio',0)>2:errs.append('DPR > 2')
 if b.get('target_fps',0)>60:errs.append('FPS > 60')
 if b.get('max_assets_mb',0)>30:errs.append('asset budget >30MB needs explicit exception')
 for a1 in d.get('assets',[]):
  if not a1.get('license_status') or not a1.get('owner'):errs.append('asset needs owner and license_status')
 print(json.dumps({'passed':not errs,'errors':errs},ensure_ascii=False,indent=2));sys.exit(bool(errs))
