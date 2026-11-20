#!/usr/bin/env python3
"""Browser QA of the exact Hotline patch embedded in Website page data."""
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
  page=browser.new_page(viewport={'width':w,'height':h})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  fixture='''<!doctype html><html><head><meta charset="utf-8"><style>
  body{margin:0;font-family:Arial}#launcher{position:fixed;z-index:3;left:10px;top:10px}
  #shade{position:fixed;inset:0;background:rgba(23,36,60,.48);z-index:10;display:flex;align-items:center;justify-content:center}
  #popup{width:min(475px,calc(100vw - 24px));height:min(620px,calc(100vh - 48px));box-sizing:border-box;
   background:white;border-radius:16px;padding:22px;position:relative}
  #dismiss{position:absolute;right:22px;top:22px;border:1px solid #468bff;border-radius:50%;width:40px;height:40px;background:#fff}
  </style></head><body><button id="launcher" aria-label="Hotline">Hotline</button>
  <div id="shade"><section id="popup"><h2>Hotline</h2><button id="dismiss">×</button>
  <p>Tổng đài TTH Healthcare — 1900 2675</p></section></div>
  '''+patch+'''</body></html>'''
  page.set_content(fixture,wait_until='domcontentloaded')
  overlay=page.locator('#shade')
  assert overlay.is_visible(),(w,'modal initially hidden')
  page.locator('#dismiss').click()
  assert not overlay.is_visible(),(w,'× did not close')
  assert page.evaluate('document.body.style.overflow')!='hidden',(w,'scroll locked')
  page.locator('#launcher').click()
  assert overlay.is_visible(),(w,'Hotline did not reopen')
  page.mouse.click(4,h//2)
  assert not overlay.is_visible(),(w,'outside click did not close')
  page.locator('#launcher').click()
  assert overlay.is_visible(),(w,'Hotline did not reopen after backdrop')
  page.keyboard.press('Escape')
  assert not overlay.is_visible(),(w,'Escape did not close')
  assert not errors,(w,'JavaScript errors '+str(errors))
  print('WEBSITE_HOTLINE_BROWSER_QA',w,h,'×/outside/Escape/reopen PASS')
  page.close()
 browser.close()
