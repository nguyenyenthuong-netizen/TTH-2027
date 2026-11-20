#!/usr/bin/env python3
"""Exercise actual Website home iframe, Hotline popup and responsive cards in Chromium."""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
site=(Path(sys.argv[1] if len(sys.argv)>1 else '_site')/'healthcare-website'/'index.html').resolve()
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={'width':w,'height':h},locale='vi-VN')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)[:240]))
  page.goto(site.as_uri(),wait_until='domcontentloaded',timeout=45000)
  page.wait_for_timeout(450)
  frame=page.frame_locator('iframe#frame')
  home=frame.locator('#app main')
  assert home.count()==1,(w,'Home content missing')
  text=home.inner_text(timeout=6000)
  assert len(text)>300,(w,'Home content too short')
  original=home.evaluate('''e=>({top:e.getBoundingClientRect().top,text:e.innerText.slice(0,160)})''')
  route=page.url
  opener=frame.locator('a[href="TienIch_Hotline.html"]').first
  assert opener.count()>0,(w,'Hotline trigger missing')
  opener.evaluate('(el)=>el.click()')
  page.wait_for_timeout(250)
  popup=frame.locator('#tth-hotline-popup-2027')
  assert popup.is_visible(),(w,'Hotline popup did not open')
  assert page.url==route,(w,'Hotline changed route',page.url)
  assert home.is_visible() and home.inner_text()==text,(w,'Home content replaced when Hotline opened')
  current=home.evaluate('''e=>({top:e.getBoundingClientRect().top,text:e.innerText.slice(0,160)})''')
  assert abs(current['top']-original['top'])<3 and current['text']==original['text'],(w,'Home layout changed')
  assert popup.get_attribute('aria-modal')=='false',(w,'Blocking/dimming modal returned')
  popup.locator('[aria-label="Đóng"]').evaluate('(el)=>el.click()')
  page.wait_for_timeout(80)
  assert not popup.is_visible(),(w,'Close X failed')
  assert page.url==route and home.inner_text()==text,(w,'Home content changed after close')
  opener.evaluate('(el)=>el.click()');page.wait_for_timeout(120)
  assert popup.is_visible(),(w,'Hotline did not reopen')
  page.keyboard.press('Escape');page.wait_for_timeout(100)
  assert not popup.is_visible(),(w,'Escape did not close')
  cards=frame.locator('#app main article.card')
  if cards.count():
   sizes=cards.evaluate_all('''xs=>xs.filter(e=>e.getBoundingClientRect().width>0).map(e=>Math.round(e.getBoundingClientRect().width))''')
   assert sizes and max(sizes)<=(370 if w>1000 else w-8),(w,'Cards stretched',sizes[:8])
  if w>1000:
   ims=frame.locator('#app main article.card img[alt*="16:9"]').evaluate_all('''xs=>xs.map(e=>({fit:getComputedStyle(e).objectFit,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}))''')
   assert all(x['fit']=='cover' and x['height']>0 for x in ims),(w,'Images stretched',ims[:4])
  assert not errors,(w,'Uncaught JavaScript',errors[:3])
  print('REAL_WEBSITE_HOTLINE_LAYOUT_QA',json.dumps({'size':[w,h],'home_length':len(text),'popup_no_route':True,'background_unchanged':True,'close_reopen_escape':True,'card_count':cards.count()},ensure_ascii=False))
  page.close()
 browser.close()
