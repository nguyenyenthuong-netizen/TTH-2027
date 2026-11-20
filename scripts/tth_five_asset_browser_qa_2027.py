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
    page.goto(path.as_uri()+('?demo=1' if name=='healthcare-app' else ''),wait_until='domcontentloaded',timeout=45000)
    page.wait_for_timeout(800)
    info=page.evaluate('''() => ({title:document.title,body:document.body?.innerText?.length||0,slides:document.querySelectorAll('section.slide').length,buttons:[...document.querySelectorAll('button')].filter(x=>x.getBoundingClientRect().height>0).length,fr:document.querySelectorAll('iframe').length,width:document.documentElement.scrollWidth,viewport:innerWidth})''')
    if name=='trinh-chieu-marketing':
     nav=page.evaluate('''() => {
      const c=document.getElementById('controls'),v=document.getElementById('viewport');
      const cr=c?.getBoundingClientRect(),vr=v?.getBoundingClientRect();
      const visible=id=>{const el=document.getElementById(id);if(!el)return false;const r=el.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(el).visibility!=='hidden'&&getComputedStyle(el).display!=='none'};
      return {barVisible:visible('controls'),overview:visible('overview'),fullscreen:visible('fullscreen'),scrubber:visible('slideScrubber'),separate:!!(cr&&vr&&vr.bottom<=cr.top+2),max:document.getElementById('slideScrubber')?.max};
     }''')
     for key in ('barVisible','overview','fullscreen','scrubber','separate'):
      if not nav.get(key):failed.append(name+' '+str(size)+': slide navigation regression '+key+' '+str(nav))
     if str(nav['max'])!=str(info['slides']):failed.append(name+': scrubber range does not cover all slides '+str(nav))
     if nav['overview'] and nav['scrubber']:
      page.locator('#overview').click(timeout=5000)
      if not page.locator('#index.open').is_visible():failed.append(name+': slide index did not open')
      page.locator('#closeIndex').click(timeout=5000)
      page.locator('#slideScrubber').evaluate('''el => {el.value="3";el.dispatchEvent(new Event("input",{bubbles:true}));}''')
      page.wait_for_timeout(70)
      if not page.locator('#counter').inner_text().strip().startswith('3 /'):
       failed.append(name+': horizontal scrubber did not navigate')
    if name in ('healthcare-website','healthcare-app'):
     try:
      frame=page.frame_locator('iframe')
      inner=frame.locator('body').inner_text(timeout=7000)
      info['frame_chars']=len(inner.strip())
      if name=='healthcare-app':
       app_catalog=page.evaluate('''() => {
        const pages=JSON.parse(document.getElementById('pageData').textContent);
        return {count:Object.keys(pages).length,allScroll:Object.values(pages).every(d=>d.includes('tth-app-all-pages-scroll-2027')),allSwipe:Object.values(pages).every(d=>d.includes('tth-app-all-pages-scroll-script-2027')),counter:document.getElementById('catalog')?.textContent||'',shell:!!document.getElementById('tth-app-catalog-full-2027')};
       }''')
       if app_catalog['count']<102:failed.append(name+': app screen count unexpectedly decreased '+str(app_catalog))
       if not app_catalog['allScroll'] or not app_catalog['allSwipe']:failed.append(name+': some app screens lack complete long-scroll / swipe behavior '+str(app_catalog))
       if str(app_catalog['count']) not in app_catalog['counter'] or not app_catalog['shell']:failed.append(name+': full app catalog and count unavailable '+str(app_catalog))
       info['app_carousel_toolbars_main']=frame.locator('.tth-app-hscroll-tools').count()
       page.locator('#catalog').click(timeout=5000)
       if page.locator('#drawer[hidden]').count()>0:failed.append(name+': app screen catalog did not open')
       page.locator('#find').fill('Tim_NhuCau')
       if page.locator('#pages button').count()!=1:failed.append(name+': Tim_NhuCau page not found in complete catalog')
       else:
        page.locator('#pages button').first.click(timeout=5000)
        page.wait_for_timeout(220)
        if 'Tim_NhuCau.html' not in page.url:failed.append(name+': app screen chooser did not navigate')
        if frame.locator('#tth-app-all-pages-scroll-2027').count()==0:failed.append(name+': need-based screen scrolling repair missing')
       print('APP_CATALOG_QA',str(size),str(app_catalog),'main-carousel-bars',info['app_carousel_toolbars_main'])
      if frame.locator('#tth-embedded-vietnamese-font-2027').count()==0:failed.append(name+' '+str(size)+': Vietnamese font stylesheet missing inside embedded document')
      frame_metrics=frame.locator('body').evaluate('''el => ({scrollWidth:document.documentElement.scrollWidth, viewport:document.documentElement.clientWidth, scrollHeight:document.documentElement.scrollHeight, height:document.documentElement.clientHeight})''')
      info['frame_overflow']=frame_metrics['scrollWidth']-frame_metrics['viewport']
      info['frame_broken_images']=frame.locator('img').evaluate_all('''imgs => imgs.filter(i => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map(i => i.getAttribute('src')).slice(0,10)''')
      if info['frame_broken_images']:failed.append(name+' '+str(size)+': broken embedded images '+str(info['frame_broken_images']))
      if info['frame_overflow']>40:failed.append(name+' '+str(size)+': embedded horizontal overflow '+str(frame_metrics))
      if info['frame_chars']<70:failed.append(name+' '+str(size)+': empty embedded page')
     except Exception as ex:failed.append(name+' '+str(size)+': iframe could not be inspected '+str(ex)[:150])
    elif info['body']<50:failed.append(name+' '+str(size)+': empty body')
    if name=='trinh-chieu-marketing' and info['slides']<20:failed.append(name+': slide deck unexpectedly short; got '+str(info['slides']))
    if name=='crm-da-kenh' and info['slides']<5:failed.append(name+': CRM display missing')
    if name=='khung-marketing' and page.locator('#m-5-2').count()==0:failed.append(name+': missing staffing table')
    if name in ('healthcare-website','healthcare-app') and info['fr']==0:failed.append(name+': missing page frame')
    if info['width']>size[0]+40:failed.append(name+' '+str(size)+': horizontal overflow '+str(info))
    if errors:failed.append(name+' '+str(size)+': uncaught JavaScript errors '+str(errors[:3]))
    checks.append(dict(asset=name,screen=size,title=info['title'],body=info['body'],slides=info['slides'],buttons=info['buttons'],pageerrors=errors[:3],overflow=info['width']-size[0]))
   except Exception as ex:failed.append(name+': '+str(ex)[:250])
   finally:page.close()
 browser.close()
(root/'five-assets-browser-qa.json').write_text(json.dumps({'checks':checks,'failed':failed},ensure_ascii=False,indent=2),'utf8')
print('FIVE_ASSETS_BROWSER_QA',json.dumps({'checks':len(checks),'failures':failed},ensure_ascii=False))
if failed:raise SystemExit(2)
