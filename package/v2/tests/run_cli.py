#!/usr/bin/env python3
"""Run reproducible focused CLI checks, retaining stdout and exit status."""
from pathlib import Path
import subprocess,os,json,sys,datetime
V=Path(__file__).resolve().parents[1];rows=[]
env=dict(os.environ);env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8';env['PYTHONDONTWRITEBYTECODE']='1'
def run(name,args,expected=0):
 p=subprocess.run(args,cwd=V,capture_output=True,text=True,encoding='utf-8',errors='replace',env=env,timeout=90)
 rows.append({'name':name,'command':args,'expected_exit':expected,'actual_exit':p.returncode,'status':'passed' if p.returncode==expected else 'failed','stdout':p.stdout[-16000:],'stderr':p.stderr[-6000:]})
run('Node domain, image and transport tests',['node','--test','tests/unit.test.mjs'])
run('Installer and contract unit tests',[sys.executable,'tests/tools_test.py'])
run('Package structure, original V1 hashes and skill references',[sys.executable,'tools/verify.py','--structure-only'])
run('Reference contract example',[sys.executable,'tools/validate_contract.py','reference','contracts/reference-brief.example.json'])
run('Unrun acceptance remains structurally valid',[sys.executable,'tools/validate_contract.py','acceptance','contracts/acceptance.example.json'])
if (V/'evidence/reference.png').exists():
 run('PNG analysis on actual browser screenshot',['node','tools/inspect_image.mjs','evidence/reference.png','evidence/image-analysis.json'])
 run('Visual CLI same screenshot passes',['node','tools/visual_diff.mjs','evidence/reference.png','evidence/reference-repeat.png','evidence/cli-identical'])
 run('Visual CLI changed heading fails',['node','tools/visual_diff.mjs','evidence/reference.png','evidence/reference-changed.png','evidence/cli-changed'],1)
 if env.get('PLAYWRIGHT_EXECUTABLE'):
  # This script starts its own short-lived local server; it never submits external forms.
  server=subprocess.Popen(['node','server.mjs'],cwd=V,env={**env,'PORT':'4199'},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  try:run('Capture CLI on local original reference',['node','tools/capture.mjs','http://127.0.0.1:4199/v2/demos/reference/','evidence/cli-capture.png','1440','1000'])
  finally:server.terminate();server.wait(timeout=10)
syntax=[]
for p in sorted((V.parent/'skills').rglob('*.py')):
 try:
  if p.stat().st_size>262144:raise ValueError('Unexpected large script')
  compile(p.read_text(encoding='utf-8'),str(p),'exec');syntax.append({'path':p.relative_to(V.parent).as_posix(),'status':'passed'})
 except Exception as ex:syntax.append({'path':p.relative_to(V.parent).as_posix(),'status':'failed','error':str(ex)})
report={'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed' if all(r['status']=='passed' for r in rows+syntax) else 'failed','checks':rows,'python_skill_syntax':syntax,'limitations':['CLI group counts are not individual assertion counts','Structure validation does not verify semantic design decisions or production integrations']}
(V/'evidence/cli-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'groups':len(rows),'python_scripts':len(syntax),'failed':[r['name'] for r in rows if r['status']!='passed']},ensure_ascii=True));raise SystemExit(report['status']!='passed')
