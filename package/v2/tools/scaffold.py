#!/usr/bin/env python3
"""Export one V2 interaction template as a self-contained local project."""
import argparse,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2];KINDS=('enterprise','fintech','commerce','agent','mobile','studio')
def scaffold(kind,output):
 if kind not in KINDS:raise ValueError('Unknown template')
 target=Path(output).expanduser().resolve()
 if target==R or R in target.parents:raise ValueError('Choose a project directory outside the package')
 if target.exists() and any(target.iterdir()):raise ValueError('Output must be empty; existing files will not be overwritten')
 site=target/'v2';demo=site/'demos';demo.mkdir(parents=True,exist_ok=True)
 shutil.copytree(R/'v2/demos'/kind,demo/kind)
 shutil.copytree(R/'v2/demos/shared',demo/'shared')
 shutil.copy2(R/'v2/server.mjs',site/'server.mjs')
 if kind=='studio':shutil.copytree(R/'v2/vendor',site/'vendor')
 shutil.copy2(R/'LICENSE-V2.txt',target/'LICENSE-V2.txt')
 (demo/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Exported template</title><link rel="stylesheet" href="shared/style.css"></head><body><main id="main"><h1>Original V2 template</h1><p>Local fictional data; no external transactions or services.</p><a class="button primary" href="'+kind+'/">Open '+kind+' template</a></main></body></html>',encoding='utf-8')
 (target/'README.md').write_text('# V2 '+kind+' template\n\nRun `node v2/server.mjs`, then open http://127.0.0.1:4173/ . Node 20+ is required; no npm install is needed for the demo. Data is fictional, tab-local and cleared on refresh. No live backend, payments, trading or AI model is connected. The full source package contains focused tests and integration guidance.\n',encoding='utf-8')
 return {'kind':kind,'output':str(target),'start':'node v2/server.mjs','mode':'local_demo'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=KINDS,required=True);p.add_argument('--output',required=True);a=p.parse_args()
 try:print(json.dumps(scaffold(a.kind,a.output),ensure_ascii=True))
 except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
