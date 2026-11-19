#!/usr/bin/env python3
import sys,re,json,html
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
sites=['khung-marketing','trinh-chieu-marketing','crm-da-kenh','healthcare-website','healthcare-app']
checks=[];failed=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for size in [(1440,900),(390,844)]:
  for name in sites:
   page=browser.new_page(viewport={'width':size[0],'height':size[1]},locale='vi-VN')
   errors=[];page.on('pageerror',lambda e,arr=errors:arr.append(str(e)[:200]))
   try:
    path=(root/name/'index.html').resolve()
    page.goto(path.as_uri(),wait_until='domcontentloaded',timeout=45000)
    page.wait_for_timeout(800)
    info=page.evaluate('''() => ({title:document.title,body:document.body?.innerText?.length||0,slides:document.querySelectorAll('section.slide').length,buttons:[...document.querySelectorAll('button')].filter(x=>x.getBoundingClientRect().height>0).length,fr:document.querySelectorAll('iframe').length,width:document.documentElement.scrollWidth,viewport:innerWidth})''')
    if info['body']<50:failed.append(name+' '+str(size)+': empty body')
    if name=='trinh-chieu-marketing' and info['slides']!=28:failed.append(name+': should have 28 slides; got '+str(info['slides']))
    if name=='crm-da-kenh' and info['slides']<5:failed.append(name+': CRM display missing')
    if name=='khung-marketing' and page.locator('#m-5-2').count()==0:failed.append(name+': missing staffing table')
    if name in ('healthcare-website','healthcare-app') and info['fr']==0:failed.append(name+': missing page frame')
    if info['width']>size[0]+40:failed.append(name+' '+str(size)+': horizontal overflow '+str(info))
    checks.append(dict(asset=name,screen=size,title=info['title'],body=info['body'],slides=info['slides'],buttons=info['buttons'],pageerrors=errors[:3],overflow=info['width']-size[0]))
   except Exception as ex:failed.append(name+': '+str(ex)[:250])
   finally:page.close()
 browser.close()
(root/'five-assets-browser-qa.json').write_text(json.dumps({'checks':checks,'failed':failed},ensure_ascii=False,indent=2),'utf8')
print('FIVE_ASSETS_BROWSER_QA',json.dumps({'checks':len(checks),'failures':failed},ensure_ascii=False))
if failed:raise SystemExit(2)
