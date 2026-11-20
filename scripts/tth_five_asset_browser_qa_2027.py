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
      if name in ('healthcare-app','healthcare-website'):
       test_question='Tôi muốn hỏi cách chuẩn bị trước khi khám'
       field_sel='#tth-app-inline-question' if name=='healthcare-app' else 'header.gh .gsrch input.tth-ai-question'
       promptfield=frame.locator(field_sel).first
       if promptfield.count()==0:
        failed.append(name+' '+str(size)+': assistant input absent; clicking old search still redirects')
       else:
        original_url=page.url
        promptfield.click(timeout=6000)
        page.wait_for_timeout(100)
        if page.url!=original_url:failed.append(name+': search field click navigated before question was submitted')
        promptfield.fill(test_question)
        page.wait_for_timeout(100)
        if page.url!=original_url:failed.append(name+': typing question triggered a result-page redirect')
        submit=frame.locator('[data-tth-assistant-submit="1"]').first
        if submit.count()==0:failed.append(name+': assistant-only icon submit missing')
        else:
         submit.click(timeout=6000)
         if name=='healthcare-app':
          route='HoTro_TroLy.html'
          try:page.wait_for_function('(expected)=>decodeURIComponent(location.hash).includes(expected)',arg=route,timeout=6000)
          except Exception:failed.append(name+': assistant icon did not route to '+route)
          page.wait_for_timeout(220)
          prefill=frame.locator('input').evaluate_all('''(els,q)=>els.some(e=>e.value===q)''',test_question)
          if not prefill:failed.append(name+': App assistant did not receive the submitted question')
         else:
          panel=frame.locator('#tth-web-assistant-panel')
          if not panel.is_visible():failed.append(name+': assistant panel did not open in place')
          elif test_question not in panel.inner_text():failed.append(name+': submitted question missing from inline assistant')
          if page.url!=original_url:failed.append(name+': Website assistant unexpectedly redirected to another page')
         if test_question in page.url:failed.append(name+': sensitive question leaked into URL')
        # Reset the original home screen before standard responsive / catalog QA.
        page.goto(path.as_uri()+('?demo=1' if name=='healthcare-app' else ''),wait_until='domcontentloaded',timeout=45000)
        page.wait_for_timeout(260)
        frame=page.frame_locator('iframe')
      if name=='healthcare-app':
       app_catalog=page.evaluate('''() => {
        const pages=JSON.parse(document.getElementById('pageData').textContent);
        return {count:Object.keys(pages).length,allScroll:Object.values(pages).every(d=>d.includes('tth-app-all-pages-scroll-2027')),allSwipe:Object.values(pages).every(d=>d.includes('tth-app-all-pages-scroll-script-2027')),counter:document.getElementById('catalog')?.textContent||'',shell:!!document.getElementById('tth-app-catalog-full-2027')};
       }''')
       if app_catalog['count']<102:failed.append(name+': app screen count unexpectedly decreased '+str(app_catalog))
       if not app_catalog['allScroll'] or not app_catalog['allSwipe']:failed.append(name+': some app screens lack complete long-scroll / swipe behavior '+str(app_catalog))
       if str(app_catalog['count']) not in app_catalog['counter'] or not app_catalog['shell']:failed.append(name+': full app catalog and count unavailable '+str(app_catalog))
       info['app_carousel_toolbars_main']=frame.locator('.tth-app-hscroll-tools').count()
       info['app_native_hscroll_main']=frame.locator('.tth-app-hscroll-track').count()
       if info['app_carousel_toolbars_main']!=0:
        failed.append(name+': internal horizontal-scroll instruction buttons still visible')
       if info['app_native_hscroll_main']<1:
        failed.append(name+': horizontal cards lost native swipe/drag scrolling')
       page.locator('#catalog').click(timeout=5000)
       if page.locator('#drawer[hidden]').count()>0:failed.append(name+': app screen catalog did not open')
       page.locator('#find').fill('Tim_NhuCau')
       if page.locator('#pages button').count()!=1:failed.append(name+': Tim_NhuCau page not found in complete catalog')
       else:
        page.locator('#pages button').first.click(timeout=5000)
        page.wait_for_timeout(220)
        if 'Tim_NhuCau.html' not in page.url:failed.append(name+': app screen chooser did not navigate')
        if frame.locator('#tth-app-all-pages-scroll-2027').count()==0:failed.append(name+': need-based screen scrolling repair missing')
       print('APP_CATALOG_QA',str(size),str(app_catalog),'native-scroll-tracks',info['app_native_hscroll_main'],'internal-buttons',info['app_carousel_toolbars_main'])
      if name=='healthcare-website':
       layout=frame.locator('body').evaluate('''() => {
        const main=document.querySelector('#app main'),fab=document.querySelector('.fab.tth-cta-fixed');
        const rect=el=>{if(!el)return null;const r=el.getBoundingClientRect(),s=getComputedStyle(el);return {left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width),maxWidth:s.maxWidth,tag:el.tagName,cls:String(el.className).slice(0,80)}};
        const items=main?[main,...main.children,...[...main.children].flatMap(el=>[...el.children])].filter(el=>el.getBoundingClientRect().width>Math.min(innerWidth*.45,350)).slice(0,8).map(rect):[];
        const changed=[...document.querySelectorAll('[data-tth-wide-content-2027="1"]')].map(rect);
        const ctaRect=rect(fab);
        return {hasMain:!!main,main:rect(main),cta:ctaRect,expanded:fab?.dataset.collapsed!=='true',widened:changed.length,candidates:items,selected:changed.slice(0,5)};
       }''')
       print('WEBSITE_WIDE_LAYOUT_AUDIT',str(size),json.dumps(layout,ensure_ascii=False))
       if size[0]>=981:
        if layout['hasMain'] and layout['main']['left']>48:
         failed.append(name+': excessive Website left margin after widening '+str(layout['main']))
        if layout['cta'] and layout['main'] and layout['main']['right']>layout['cta']['left']-8:
         failed.append(name+': main content overlaps right CTA '+str(layout))
        for box in layout['selected']:
         if box['right']>size[0]-55:failed.append(name+': widened content reaches too close to CTA / viewport '+str(box))
        # Regression for the previously fixed 1320px cap on wide monitors.
        page.set_viewport_size({'width':1920,'height':1080})
        page.wait_for_timeout(180)
        wide=frame.locator('#app main').evaluate('''el => {const r=el.getBoundingClientRect(),cta=document.querySelector('.fab.tth-cta-fixed')?.getBoundingClientRect();return {width:Math.round(r.width),left:Math.round(r.left),right:Math.round(r.right),ctaLeft:cta?Math.round(cta.left):null}}''')
        print('WEBSITE_WIDE_1920_QA',json.dumps(wide,ensure_ascii=False))
        if wide['width']<1500 or wide['left']>52:
         failed.append(name+': Website content still constrained to narrow center column at 1920 '+str(wide))
        if wide['ctaLeft'] is not None and wide['right']>wide['ctaLeft']-8:
         failed.append(name+': Website content overlaps CTA at 1920 '+str(wide))
        page.set_viewport_size({'width':size[0],'height':size[1]})
        page.wait_for_timeout(110)
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
    if name=='crm-da-kenh':
     if info['slides']!=7:failed.append(name+': CRM must have exactly 7 slides, got '+str(info['slides']))
     nav=page.locator('#sideNav button')
     if nav.count()!=7:failed.append(name+': CRM seventh slide missing from sidebar '+str(nav.count()))
     elif page.locator('#s7').count()!=1:failed.append(name+': CRM internal agreement screen absent')
     else:
      nav.nth(2).evaluate('(el)=>el.click()')
      page.wait_for_timeout(120)
      tabs=page.locator('#flowTabs .flowbtn')
      if tabs.count()<2:failed.append(name+': missing second HIS identification workflow tab')
      else:
       tabs.nth(1).evaluate('(el)=>el.click()')
       page.wait_for_timeout(150)
       title=page.locator('#crmFlowMetaToggle').inner_text()
       if 'CRM' not in title or 'HIS' not in title:failed.append(name+': HIS example help label missing')
       page.locator('#crmFlowMetaToggle').evaluate('(el)=>el.click()')
       page.wait_for_timeout(120)
       sample=page.locator('#s3 .tth-his-example')
       if not sample.is_visible():failed.append(name+': fictional CRM to HIS patient-ID example not visible')
       else:
        sample_text=sample.inner_text()
        for expected in ('CRM-00125','BN-00876','BN-00444','Chờ xác minh','không tự gộp'):
         if expected not in sample_text:failed.append(name+': missing HIS linkage example: '+expected)
        layout=sample.evaluate('''e=>({width:e.scrollWidth,client:e.clientWidth,height:e.scrollHeight,visible:e.getBoundingClientRect().height})''')
        if layout['width']>layout['client']+24:failed.append(name+': CRM/HIS example horizontally clipped '+str(layout))
        print('CRM_HIS_EXAMPLE_QA',str(size),json.dumps(layout,ensure_ascii=False))
       page.locator('#crmFlowMetaToggle').evaluate('(el)=>el.click()')
      launcher=page.locator('#ux-search-launch')
      if launcher.count()==0:failed.append(name+': CRM advanced search launcher missing')
      else:
       launcher.evaluate('(el)=>el.click()')
       page.wait_for_timeout(120)
       dialog=page.locator('#ux-search-panel')
       if not dialog.is_visible():failed.append(name+': advanced search did not open')
       else:
        search_metrics=dialog.evaluate('''e=>{
          const q=(s)=>e.querySelector(s);
          const font=(s)=>q(s)?parseFloat(getComputedStyle(q(s)).fontSize):null;
          return {width:Math.round(e.getBoundingClientRect().width),
            maxWidth:Math.round(innerWidth-16),
            overflow:e.scrollWidth-e.clientWidth,
            heading:font('.ux-hd strong'),
            title:font('.ux-res .ux-title')};
        }''')
        if search_metrics['width']>search_metrics['maxWidth']+2:failed.append(name+': advanced search extends beyond viewport')
        if search_metrics['overflow']>20:failed.append(name+': advanced search clips content horizontally')
        if search_metrics['heading'] is None or search_metrics['heading']<16:failed.append(name+': advanced search header font too small')
        query=dialog.locator('.ux-fields input:not([type="checkbox"])').first
        if query.count():
         query.fill('liên kết hồ sơ')
         page.wait_for_timeout(260)
         results=dialog.locator('.ux-res button')
         if results.count()==0:failed.append(name+': search query returned no results for HIS linkage text')
         else:
          title_font=results.first.locator('.ux-title').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')
          if title_font<15:failed.append(name+': result titles still too small')
        print('CRM_ADVANCED_SEARCH_QA',str(size),json.dumps(search_metrics,ensure_ascii=False))
        dialog.locator('.ux-exit').first.evaluate('(el)=>el.click()')
      nav.nth(3).evaluate('(el)=>el.click()')
      page.wait_for_timeout(140)
      cm=page.locator('#s4').evaluate('''root=>{
        const read=sel=>{const el=root.querySelector(sel);if(!el)return {exists:false};
          const r=el.getBoundingClientRect();return {exists:true,px:parseFloat(getComputedStyle(el).fontSize),
          visible:r.width>0&&r.height>0,sw:el.scrollWidth,cw:el.clientWidth,sh:el.scrollHeight,ch:el.clientHeight}};
        return {active:root.classList.contains('active'),
          rule:read('.role-rule>strong'),flow:read('.tier-example-flow>span'),
          label:read('.tier-example-label'),except:read('.tier-example>p'),
          horizontal:root.scrollWidth-root.clientWidth};
      }''')
      if not cm['active']:failed.append(name+': slide 04 did not open before font QA')
      for part,minimum in [('rule',16),('flow',15),('label',14),('except',14)]:
       obj=cm[part]
       if not obj.get('exists') or not obj.get('visible') or obj.get('px',0)<minimum:
        failed.append(name+' '+str(size)+': CRM slide04 text still too small '+part+' '+str(obj))
      if cm['horizontal']>35:failed.append(name+' '+str(size)+': slide04 width overflow after font growth '+str(cm))
      print('CRM_S4_FONTS_QA',str(size),json.dumps(cm,ensure_ascii=False))
      nav.nth(6).evaluate('(el)=>el.click()')
      page.wait_for_timeout(160)
      if page.locator('#s7.active').count()!=1:failed.append(name+': CRM sidebar could not open seventh slide')
      if page.locator('#pageCount').inner_text().strip()!='07 / 07':failed.append(name+': CRM counter not updated to 07 / 07')
      if page.locator('#s7 .crm-internal-table tbody tr').count()!=6:failed.append(name+': CRM needs exactly six internal service rows')
      page.locator('#prev').evaluate('(el)=>el.click()')
      if page.locator('#s6.active').count()!=1:failed.append(name+': CRM previous button does not return to roadmap slide')
      page.locator('#next').evaluate('(el)=>el.click()')
      if page.locator('#s7.active').count()!=1:failed.append(name+': CRM next button does not navigate back to internal slide')
      overflow=page.locator('#s7').evaluate('(el)=>({sw:el.scrollWidth,cw:el.clientWidth,sh:el.scrollHeight,ch:el.clientHeight})')
      if overflow['sw']>overflow['cw']+30:failed.append(name+': seventh slide horizontally clipped '+str(overflow))

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
