#!/usr/bin/env python3
"""Copy complete skills into an explicitly chosen directory; never overwrite."""
import argparse,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def install(target):
 target=Path(target).expanduser().resolve()
 if target==R or R in target.parents:raise ValueError('Choose an installation directory outside the package')
 target.mkdir(parents=True,exist_ok=True);result=[]
 for source in sorted((R/'skills').iterdir()):
  if not (source/'SKILL.md').is_file():continue
  dest=target/source.name
  if dest.exists() or dest.is_symlink():result.append({'skill':source.name,'status':'skipped_existing'});continue
  shutil.copytree(source,dest)
  if source.name in NEW:
   (dest/'PACKAGE_LOCATION.json').write_text(json.dumps({'package_root':str(R),'version':'2.0.0'},indent=2)+'\n',encoding='utf-8')
  result.append({'skill':source.name,'status':'installed'})
 return result
NEW={'awwwards-'+x for x in ['page-library','enterprise','fintech','ecommerce','ai-agent','mobile','advanced-motion','3d-experience','design-intelligence','visual-reconstruction','visual-diff','acceptance-docs']}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--target');p.add_argument('--list',action='store_true');a=p.parse_args()
 if a.list:print(json.dumps(sorted(x.name for x in (R/'skills').iterdir() if (x/'SKILL.md').is_file()),indent=2))
 elif a.target:
  try:print(json.dumps(install(a.target),indent=2))
  except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
 else:p.error('--target or --list is required')
