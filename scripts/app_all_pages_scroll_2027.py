#!/usr/bin/env python3
"""Expose existing TTH App pages and preserve long content and native horizontal card scrolling.
Never adds sample medical records or changes page content, copy, logos, or routes.
Runs after other post-assembly App rewrites, before browser QA.
"""
import sys,re,json
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
file=root/'healthcare-app'/'index.html'
raw=file.read_text('utf-8')
match=re.search(r'(<script\b[^>]*\bid=["\']pageData["\'][^>]*>)(.*?)(</script>)',raw,re.I|re.S)
if not match:raise SystemExit('APP_PAGE_AUDIT: pageData missing')
pages=json.loads(match.group(2))
if not isinstance(pages,dict) or len(pages)<100:
 raise SystemExit('APP_PAGE_AUDIT: expected complete existing page catalog (>=100); got '+str(len(pages)))
if 'Main.html' not in pages or 'Tim_BacSi.html' not in pages or 'DatLich_XacNhan.html' not in pages:
 raise SystemExit('APP_PAGE_AUDIT: key application workflows missing')
styles=r"""<style id="tth-app-all-pages-scroll-2027">
/* App document itself must remain vertically navigable; no viewport cropping. */
html{height:auto!important;min-height:100%;overflow-y:auto!important;scroll-behavior:auto}
body{height:auto!important;min-height:100%;overflow-y:auto!important;overscroll-behavior-y:contain}
:where(main,.main,.page,.page-content,.content-wrap,.screen-content,.app-content)[data-tth-long-scroll="1"]{
  overflow-y:auto!important;overscroll-behavior-y:contain!important;-webkit-overflow-scrolling:touch;
  scrollbar-width:thin
}
.tth-app-hscroll-track{overflow-x:auto!important;overscroll-behavior-x:contain!important;
 scroll-behavior:smooth!important;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
.tth-app-hscroll-track>*{flex-shrink:0}

</style>"""
logic=r"""<script id="tth-app-all-pages-scroll-script-2027">
(function(){
'use strict';
function longScroll(){
 document.querySelectorAll('main,.main,.page,.page-content,.content-wrap,.screen-content,.app-content').forEach(function(el){
  if(el.dataset.tthLongScroll)return;
  var st=getComputedStyle(el);
  if(st.display==='none'||st.position==='fixed'||el.clientHeight<80)return;
  if(el.scrollHeight>el.clientHeight+48&&/hidden|clip/.test(st.overflowY)){
   el.dataset.tthLongScroll='1';
  }
 });
}
function horizontal(){
 var all=document.querySelectorAll('div,section,ul');
 var n=0;
 all.forEach(function(el){
  if(n>=12||el.dataset.tthHscrollDone||!el.parentNode||el.children.length<2)return;
  if(el.closest('header,footer,nav,aside,[role="dialog"]'))return;
  var st=getComputedStyle(el), width=el.clientWidth;
  if(st.display==='none'||width<130||el.scrollWidth<=width+28)return;
  var cls=String(el.className||'')+' '+String(el.id||'');
  var named=/carousel|slider|swiper|scroller|horizontal|card[s-]|rail|track|swipe|goi-kham|service|nhu-cau|need[s-]/i.test(cls);
  var row=(st.display.includes('flex')&&st.flexDirection==='row')||
          (st.display.includes('grid')&&st.gridAutoFlow.includes('column'));
  if(!named&&!(row&&el.children.length>=3))return;
  if(el.parentElement&&el.parentElement.classList.contains('tth-app-hscroll-track'))return;
  el.dataset.tthHscrollDone='1';el.classList.add('tth-app-hscroll-track');
  // Native touch scroll and unobtrusive mouse drag only; no internal instruction buttons.
  var start=null;
  el.addEventListener('pointerdown',function(ev){
   if(ev.pointerType!=='mouse'||ev.button!==0||ev.target.closest('a,button,input,select,textarea'))return;
   start={x:ev.clientX,left:el.scrollLeft};
  });
  el.addEventListener('pointermove',function(ev){
   if(!start||!(ev.buttons&1))return;
   if(Math.abs(ev.clientX-start.x)>5)el.scrollLeft=start.left+start.x-ev.clientX;
  });
  ['pointerup','pointercancel','pointerleave'].forEach(function(type){
    el.addEventListener(type,function(){start=null});
  });
  n++;
 });
}
function run(){longScroll();horizontal()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
window.addEventListener('load',function(){run();setTimeout(run,450)});
window.addEventListener('resize',run,{passive:true});
})();
</script>"""
revised={}
lengths={}
for name,doc in pages.items():
 if not isinstance(doc,str):raise SystemExit('Nontext page '+name)
 lengths[name]=len(re.sub(r'<[^>]*>','',doc))
 if not re.search(r'<(?:body|main|div|section)\b',doc,re.I):
  raise SystemExit('Missing page body: '+name)
 if 'id="tth-app-all-pages-scroll-2027"' not in doc:
  if re.search(r'</head\s*>',doc,re.I):
   doc=re.sub(r'</head\s*>',lambda m:styles+m.group(0),doc,count=1,flags=re.I)
  else:doc=styles+doc
 if 'id="tth-app-all-pages-scroll-script-2027"' not in doc:
  if re.search(r'</body\s*>',doc,re.I):
   doc=re.sub(r'</body\s*>',lambda m:logic+m.group(0),doc,count=1,flags=re.I)
  else:doc+=logic
 revised[name]=doc
encoded=json.dumps(revised,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
output=raw[:match.start(2)]+encoded+raw[match.end(2):]
shellstyle=r"""<style id="tth-app-catalog-full-2027">
#drawer:not([hidden]){overflow-y:auto!important;overflow-x:hidden!important;
 max-height:min(78dvh,760px)!important;overscroll-behavior:contain!important;scrollbar-width:thin}
#drawer #pages{max-height:min(60dvh,600px)!important;overflow-y:auto!important;scrollbar-width:thin}
#tth-app-total-pages{color:#0837A1;font:700 14px/1.3 Arial,sans-serif;
 margin:8px 0;padding:5px 0}
</style>"""
shellscript=r"""<script id="tth-app-catalog-full-script-2027">
(function(){
 var data=document.getElementById('pageData'),btn=document.getElementById('catalog'),
 drawer=document.getElementById('drawer');
 if(!data||!btn||!drawer)return;
 var n=Object.keys(JSON.parse(data.textContent)).length;
 btn.textContent='☰ '+n+' màn hình';
 btn.setAttribute('aria-label','Danh mục '+n+' màn hình ứng dụng');
 var label=document.createElement('div');label.id='tth-app-total-pages';
 label.textContent='Danh mục đầy đủ: '+n+' màn hình';
 var hdr=drawer.querySelector('.ux-drawer-header');if(hdr)hdr.insertAdjacentElement('afterend',label);
})();
</script>"""
if 'id="tth-app-catalog-full-2027"' not in output:output=output.replace('</head>',shellstyle+'</head>',1)
if 'id="tth-app-catalog-full-script-2027"' not in output:output=output.replace('</body>',shellscript+'</body>',1)
if set(json.loads(encoded))!=set(pages):raise SystemExit('Page catalog altered unexpectedly')
file.write_text(output,'utf-8')
report={'page_count':len(pages),'pages_with_long_scroll_and_swipe':len(revised),
        'shortest_existing_pages':sorted(lengths.items(),key=lambda v:v[1])[:12],
        'routes':list(pages.keys()),
        'notes':'All original page documents kept; content scroll and eligible horizontal carousels unlocked; no medical data added'}
(root/'app-page-coverage-2027.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8')
print('APP-ALL-PAGES-2027','pages',len(pages),'scroll+native-swipe',len(revised),
      'shortest',report['shortest_existing_pages'][:4])
