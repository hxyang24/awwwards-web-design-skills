#!/usr/bin/env python3
"""Actual headless Chromium DOM/layout behavior by injecting local assets via set_content.

No navigation/HTTP or module-loader test is implied. Environment blocks goto() URLs.
"""
import argparse,json,re,sys
from pathlib import Path
from datetime import datetime,timezone
try:
 from playwright.sync_api import sync_playwright
except ImportError:
 print(json.dumps({'status':'blocked','reason':'Playwright unavailable'},ensure_ascii=False));sys.exit(2)

def main():
 p=argparse.ArgumentParser();p.add_argument('--examples',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--screenshots',type=Path);a=p.parse_args()
 root=a.examples;out=[];a.output.parent.mkdir(parents=True,exist_ok=True)
 css=(root/'saas/assets/styles.css').read_text(encoding='utf-8');common=(root/'saas/assets/common.js').read_text(encoding='utf-8').replace('export function ','function ')
 if a.screenshots:a.screenshots.mkdir(parents=True,exist_ok=True)
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
   for kind in ('saas','commerce','dashboard','portfolio','editorial','immersive'):
    html=(root/kind/'index.html').read_text(encoding='utf-8')
    main_js=(root/kind/'main.js').read_text(encoding='utf-8')
    main_js=re.sub(r'import\s*\{[^}]*\}\s*from\s*[\'\"]\./assets/common\.js[\'\"]\s*;?', '',main_js)
    for viewport in (390,1440):
     page=browser.new_page(viewport={'width':viewport,'height':900},reduced_motion='reduce' if viewport==390 else 'no-preference')
     errs=[];page.on('pageerror',lambda err:errs.append(str(err)))
     page.set_content(html,wait_until='domcontentloaded')
     page.add_style_tag(content=css)
     page.add_script_tag(content=common+'\n'+main_js)
     page.wait_for_timeout(100)
     w=page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1')
     title=page.title();h1=page.locator('h1').count();main=page.locator('main').count()
     if not w:errs.append('horizontal overflow')
     if h1!=1 or main!=1:errs.append('landmark counts')
     if viewport==390:
      btn=page.locator('#menu-toggle');nav=page.locator('#primary-nav')
      if not btn.is_visible():errs.append('mobile menu toggle not visible')
      btn.click();
      if nav.is_hidden():errs.append('mobile menu did not open')
      page.keyboard.press('Escape')
      if nav.is_visible():errs.append('mobile menu did not close on Escape')
      if not btn.evaluate('(el)=>document.activeElement===el'):errs.append('Escape focus not restored')
     else:
      if page.locator('#primary-nav').is_hidden():errs.append('desktop navigation hidden')
      if kind=='saas':
       page.locator('#name').fill('演示用户');page.locator('#email').fill('demo@example.com');page.locator('#reason').fill('我们需要一个清晰的财务分析演示。');page.locator('#contact-form button').click()
       if '未发送' not in page.locator('#form-status').inner_text():errs.append('form preview honesty missing')
       page.locator('#name').fill('新用户')
       if page.locator('#form-status').inner_text():errs.append('stale form success not cleared')
      if kind=='commerce':
       page.get_by_role('button',name='照明').click()
       if page.locator('[data-category]:visible').count()!=1:errs.append('filter does not select one item')
       page.locator('[data-category]:visible [data-view-product]').click()
       if not page.locator('#product-dialog').evaluate('(el)=>el.open'):errs.append('dialog not open')
       page.locator('#close-dialog').click()
       if page.locator('#product-dialog').evaluate('(el)=>el.open'):errs.append('dialog not closed')
      if kind=='dashboard':
       page.locator('#search-records').fill('不存在')
       if '没有符合' not in page.locator('#record-status').inner_text():errs.append('no-result message missing')
       page.locator('#search-records').fill('服务')
       if page.locator('#record-body tr:visible').count()!=1:errs.append('search not filtering')
     if a.screenshots:
      page.screenshot(path=str(a.screenshots/f'{kind}-{viewport}.png'),full_page=True,animations='disabled')
     out.append({'kind':kind,'viewport':viewport,'title':title,'dom_h1':h1,'dom_main':main,'no_horizontal_overflow':w,'status':'passed' if not errs else 'failed','errors':errs})
     page.close()
   browser.close()
 except Exception as e:
  result={'status':'blocked','reason':str(e),'method':'Chromium set_content with local CSS and transformed module source injection','cases':out}
  a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False));sys.exit(2)
 result={'status':'passed' if all(x['status']=='passed' for x in out) else 'failed','tested_at':datetime.now(timezone.utc).isoformat(),'method':'Headless Chromium set_content + local CSS and concatenated JS. This validates DOM/layout/behavior, not HTTP routing, module imports, network performance, or actual GPU scenes.','cases':out}
 a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({'status':result['status'],'cases':len(out),'failures':[x for x in out if x['status']!='passed']},ensure_ascii=False,indent=2));sys.exit(0 if result['status']=='passed' else 1)
if __name__=='__main__':main()
