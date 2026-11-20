#!/usr/bin/env python3
"""Temporary public Website Hotline route diagnosis; never modifies artifacts."""
import re,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
p=root/'healthcare-website'/'index.html'
s=p.read_text('utf-8')
m=re.search(r'<script\b[^>]*\bid=["\']pagesData["\'][^>]*>(.*?)</script>',s,re.I|re.S)
pages=json.loads(m.group(1))
print('HOTLINE_ROUTE_CATALOG',json.dumps([k for k in pages if 'hotline' in k.lower() or k.lower() in ['main.html','index.html','trangchu.html']],ensure_ascii=False))
for k,v in pages.items():
 if 'hotline' not in k.lower():continue
 for q in ('Hotline','1900 2675','modal','backdrop'):
  i=v.find(q)
  if i>=0:print('HOTLINE_DOC_SNIPPET',k,q,repr(v[max(0,i-1100):i+1400]))
with sync_playwright() as pw:
 br=pw.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=br.new_page(viewport={'width':1440,'height':900})
 errs=[];page.on('pageerror',lambda e:errs.append(str(e)[:160]))
 page.goto(p.resolve().as_uri(),wait_until='domcontentloaded')
 page.wait_for_timeout(600)
 def report(label):
  outer=page.evaluate('''()=>({url:location.href,title:document.title,hash:location.hash,
   frame:document.querySelector('iframe')?.getAttribute('src'),
   content:document.body.innerText.slice(0,280)})''')
  inner=page.frame_locator('iframe').locator('body').evaluate('''b=>{
   let els=[...b.querySelectorAll('a,button')].filter(x=>/hotline|tổng đài/i.test(x.textContent+' '+x.getAttribute('title')+' '+x.getAttribute('aria-label')));
   let heads=[...b.querySelectorAll('h1,h2,h3,h4,strong')].filter(x=>x.textContent.trim()==='Hotline');
   let mains=[...b.querySelectorAll('main')].map(x=>({text:x.innerText.slice(0,100),visible:x.getBoundingClientRect().height>0}));
   return {title:document.title,els:els.slice(0,10).map(x=>({tag:x.tagName,outer:x.outerHTML.slice(0,700)})),
     heads:heads.slice(0,4).map(x=>x.parentElement?.outerHTML.slice(0,1700)),mains,
     body:document.body.innerText.slice(0,320),html:document.body.outerHTML.length}
  }''')
  print('HOTLINE_BROWSER_'+label,json.dumps({'outer':outer,'inner':inner,'errors':errs},ensure_ascii=False))
 report('BEFORE')
 try:
  frame=page.frame_locator('iframe')
  q=frame.locator('.fab.tth-cta-fixed a.fabx').all()
  print('HOTLINE_CTA_COUNT',len(q))
  for i,item in enumerate(q):
   print('HOTLINE_CTA',i,item.evaluate('x=>x.outerHTML.slice(0,1000)'))
  clicked=False
  for item in q:
   desc=item.evaluate('x=>x.outerHTML.slice(0,700)')
   if re.search('hotline|Tổng đài|phone|Gọi',desc,re.I):
    item.click(force=True,timeout=3000);clicked=True;break
  print('HOTLINE_TRIGGER_CLICKED',clicked)
  page.wait_for_timeout(250)
  report('AFTER')
 except Exception as e:print('HOTLINE_BROWSER_ERROR',repr(e))
 br.close()
