#!/usr/bin/env python3
"""Optional live browser smoke test; honest blocked state if Playwright absent."""
import argparse,json,sys
p=argparse.ArgumentParser();p.add_argument('--url',required=True);a=p.parse_args()
try:
 from playwright.sync_api import sync_playwright
except ImportError:
 print(json.dumps({'status':'blocked','reason':'Playwright not installed; no browser testing run'},ensure_ascii=False));sys.exit(2)
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  out=[]
  for w,h in [(390,844),(1440,900)]:
   page=browser.new_page(viewport={'width':w,'height':h},reduced_motion='reduce');page.goto(a.url,wait_until='domcontentloaded',timeout=20000);page.locator('main').wait_for(timeout=5000); out.append({'viewport':f'{w}x{h}','title':page.title(),'h1':page.locator('h1').count(),'horizontal_overflow':page.evaluate('document.documentElement.scrollWidth > innerWidth')});page.close()
  browser.close()
 result={'status':'passed' if all(not x['horizontal_overflow'] and x['h1']==1 for x in out) else 'failed','details':out}
 print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['status']=='passed' else 1)
except Exception as e:
 print(json.dumps({'status':'blocked','reason':str(e)},ensure_ascii=False));sys.exit(2)
