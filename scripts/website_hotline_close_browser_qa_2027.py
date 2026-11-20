#!/usr/bin/env python3
"""Website Hotline modal QA: both nested and separate-backdrop cases, with preserved page content."""
import json,re,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
s=(root/'healthcare-website'/'index.html').read_text('utf-8')
m=re.search(r'<script\b[^>]*\bid=["\']pagesData["\'][^>]*>(.*?)</script>',s,re.I|re.S)
if not m:raise SystemExit('Website page data missing')
pages=json.loads(m.group(1))
docs=[v for v in pages.values() if 'id="tth-hotline-close-handler-2027"' in v]
if len(docs)<100:raise SystemExit('Hotline fix missing on public pages: '+str(len(docs)))
script=re.search(r'(<style id="tth-hotline-close-style-2027">.*?</script>)',docs[0],re.S)
if not script:raise SystemExit('Hotline script not embedded')
patch=script.group(1)
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844)]:
  for mode in ('nested','separate'):
   page=browser.new_page(viewport={'width':w,'height':h})
   errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   styles='''body{margin:0;font-family:Arial;background:white}
   #launcher{position:fixed;z-index:3;left:10px;top:10px}
   #site-content{position:relative;padding:100px 20px;background:white;color:#0837A1;min-height:100vh}
   #shade{position:fixed;inset:0;background:rgba(23,36,60,.48);z-index:10}
   #popup{width:min(475px,calc(100vw - 24px));height:min(620px,calc(100vh - 48px));box-sizing:border-box;
    background:white;border-radius:16px;padding:22px;position:fixed;z-index:20;left:50%;top:50%;transform:translate(-50%,-50%)}
   #dismiss{position:absolute;right:22px;top:22px;border:1px solid #468bff;border-radius:50%;width:40px;height:40px;background:#fff}
   '''
   # For nested mode, the full-screen fixed shade wraps its white panel.
   if mode=='nested':
    styles+='''#shade{display:flex;align-items:center;justify-content:center}
    #popup{position:relative;left:auto;top:auto;transform:none}'''
   popup='<section id="popup"><h2>Hotline</h2><button id="dismiss">×</button><p>Tổng đài TTH Healthcare — 1900 2675</p></section>'
   overlay=('<div id="shade">'+popup+'</div>') if mode=='nested' else ('<div id="shade"></div>'+popup)
   fixture='''<!doctype html><html><head><meta charset="utf-8"><style>'''+styles+'''</style></head>
   <body><button id="launcher" aria-label="Hotline">Hotline</button>
   <main id="site-content"><h1>Nội dung Website TTH Healthcare</h1>
    <p>Trang chủ phải được giữ nguyên kể cả sau khi đóng Hotline.</p>
    <button id="content-action" onclick="this.dataset.clicked='true'">Tương tác trang chủ</button>
   </main>'''+overlay+patch+'''</body></html>'''
   page.set_content(fixture,wait_until='domcontentloaded')
   shade=page.locator('#shade');panel=page.locator('#popup')
   assert shade.is_visible() and panel.is_visible(),(w,mode,'modal initially hidden')
   page.wait_for_function("getComputedStyle(document.querySelector('#shade')).backgroundColor === 'rgba(0, 0, 0, 0)' || getComputedStyle(document.querySelector('#shade')).backgroundColor === 'rgb(0, 0, 0)'",timeout=4000)
   assert page.locator('#site-content').is_visible(),(w,mode,'Website content not present when Hotline open')
   assert page.evaluate("getComputedStyle(document.querySelector('#shade')).pointerEvents")=='none',(w,mode,'Hotline shade still blocks page')

   page.locator('#dismiss').click()
   assert not shade.is_visible() and not panel.is_visible(),(w,mode,'× left panel or gray backdrop visible')
   assert page.locator('#site-content').is_visible(),(w,mode,'Website content hidden')
   page.locator('#content-action').click()
   assert page.locator('#content-action').get_attribute('data-clicked')=='true',(w,mode,'Website content blocked after dismissal')
   assert page.evaluate('document.body.style.overflow')!='hidden',(w,mode,'scroll locked')
   page.locator('#launcher').click()
   assert shade.is_visible() and panel.is_visible(),(w,mode,'Hotline failed to reopen')
   page.mouse.click(4,h//2)
   assert not shade.is_visible() and not panel.is_visible(),(w,mode,'outside click left gray backdrop')
   page.locator('#launcher').click()
   assert shade.is_visible() and panel.is_visible(),(w,mode,'Hotline did not reopen after backdrop')
   page.keyboard.press('Escape')
   assert not shade.is_visible() and not panel.is_visible(),(w,mode,'Escape left gray backdrop')
   assert page.locator('#site-content').is_visible(),(w,mode,'Website content lost after Escape')
   assert not errors,(w,mode,'JavaScript errors '+str(errors))
   print('WEBSITE_HOTLINE_BROWSER_QA',w,h,mode,'panel-and-backdrop ×/outside/Escape/reopen; website-content-preserved PASS')
   page.close()
 browser.close()
