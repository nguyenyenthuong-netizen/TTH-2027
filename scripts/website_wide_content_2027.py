#!/usr/bin/env python3
"""Widen real TTH Healthcare website page content, with room for the right CTA.
Applies only to embedded public Website pages; keeps App, CRM and Khung unchanged.
"""
from pathlib import Path
import json,re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('_site')
file=root/'healthcare-website'/'index.html'
s=file.read_text('utf-8')
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',s,re.I|re.S)
if not m:raise SystemExit('Missing Website page catalog')
pages=json.loads(m.group(2))
css=r"""<style id="tth-website-content-wide-2027">
/* Full-width public layout, leaving only a measured clearance for the CTA.
   The original 1320px cap created oversized margins on wide desktop screens. */
:root{--tth-website-left-gap:clamp(22px,2vw,38px);--tth-website-cta-gap:104px}
#app{width:100%!important;max-width:100%!important;box-sizing:border-box!important}
@media(min-width:981px){
 #app main,
 #app header.gh > div:first-child,
 #app footer > div:first-child{
  box-sizing:border-box!important;
  width:min(1810px,calc(100vw - var(--tth-website-left-gap) - var(--tth-website-cta-gap)))!important;
  max-width:min(1810px,calc(100vw - var(--tth-website-left-gap) - var(--tth-website-cta-gap)))!important;
  margin-left:var(--tth-website-left-gap)!important;
  margin-right:auto!important
 }
}
/* The header has its own symmetric gutters; CTA clearance applies to page content,
   not to the navigation bar. Keep logo and first navigation item separated. */
@media(min-width:1180px){
 #app header.gh > div:first-child{column-gap:clamp(10px,1vw,19px)!important}
 #app header.gh > div:first-child > :first-child{
  margin-right:clamp(16px,1.3vw,27px)!important;flex-shrink:0!important
 }
}
/* At intermediate laptop widths, keep the search field compact instead of
   letting the booking button protrude past the balanced right gutter. */
@media(min-width:1180px) and (max-width:1550px){
 #app header.gh .gsrch{width:clamp(200px,16vw,240px)!important;
  max-width:240px!important;min-width:200px!important;flex:0 1 auto!important}
}
@media(max-width:980px){
 #app main{max-width:100%!important}
}
</style>"""
js=r"""<script id="tth-website-content-wide-js-2027">
(function(){
'use strict';
var root=document.documentElement,resizeTimer=0;
function isVisible(el){
 if(!el)return false;
 var s=getComputedStyle(el),r=el.getBoundingClientRect();
 if(s.display==='none'||s.visibility!=='visible'||Number(s.opacity)<.08)return false;
 if(r.width<4||r.height<4)return false;
 var p=el.parentElement;
 while(p&&p!==document.body){
  var ps=getComputedStyle(p);
  if(ps.display==='none'||ps.visibility==='hidden'||Number(ps.opacity)<.08)return false;
  p=p.parentElement;
 }
 return true;
}
function resize(){
 var app=document.getElementById('app');if(!app)return;
 if(window.innerWidth<981){
  ['main','header.gh > div:first-child','footer > div:first-child'].forEach(function(sel){
   var el=app.querySelector(sel);if(!el)return;
   ['width','max-width','margin-left','margin-right','gap'].forEach(function(prop){el.style.removeProperty(prop)});
  });
  return;
 }
 var cta=app.querySelector('.fab.tth-cta-fixed');
 var left=Math.min(38,Math.max(22,window.innerWidth*.02));
 var right=104;
 if(cta){
  var nodes=[cta].concat(Array.from(cta.querySelectorAll('a.fabx,.tth-cta-toggle,.tth-cta-stack')));
  var leftmost=window.innerWidth;
  nodes.forEach(function(el){
   if(!isVisible(el))return;
   leftmost=Math.min(leftmost,el.getBoundingClientRect().left);
  });
  if(leftmost<window.innerWidth)right=Math.max(92,Math.min(320,Math.ceil(window.innerWidth-leftmost+20)));
 }
 root.style.setProperty('--tth-website-left-gap',left+'px');
 root.style.setProperty('--tth-website-cta-gap',right+'px');
 // The source design has a literal 1320px cap on main. Some pages also apply
 // it inline after their head stylesheet; set the actual layout element itself.
 var width=Math.min(1810,window.innerWidth-left-right);
 function widen(el){
  if(!el)return;
  el.style.setProperty('width',width+'px','important');
  el.style.setProperty('max-width',width+'px','important');
  el.style.setProperty('margin-left',left+'px','important');
  el.style.setProperty('margin-right','auto','important');
  el.style.setProperty('box-sizing','border-box','important');
 }
 widen(app.querySelector('main'));
 // Header navigation must have equal free space on both sides, independent
 // of the floating CTA's expanded/collapsed state.
 var head=app.querySelector('header.gh > div:first-child');
 if(head){
  var edge=Math.min(64,Math.max(24,window.innerWidth*.028));
  var headWidth=Math.min(1920,window.innerWidth-2*edge);
  head.style.setProperty('width',headWidth+'px','important');
  head.style.setProperty('max-width',headWidth+'px','important');
  head.style.setProperty('margin-left','auto','important');
  head.style.setProperty('margin-right','auto','important');
  head.style.setProperty('box-sizing','border-box','important');
 }
 widen(app.querySelector('footer > div:first-child'));
}
function schedule(){clearTimeout(resizeTimer);resizeTimer=setTimeout(resize,35)}
window.addEventListener('resize',schedule,{passive:true});
window.addEventListener('load',schedule);
var fab=document.querySelector('.fab.tth-cta-fixed');
if(fab&&window.MutationObserver){
 new MutationObserver(schedule).observe(fab,{attributes:true,attributeFilter:['data-collapsed','style','class']});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});
else schedule();
})();
</script>"""
changed=0
for name,doc in pages.items():
 if 'id="app"' not in doc or 'class="gh"' not in doc:continue
 if 'tth-website-content-wide-2027' in doc:raise SystemExit('Double application on '+name)
 if '</head>' not in doc or '</body>' not in doc:raise SystemExit('Invalid Website page '+name)
 pages[name]=doc.replace('</head>',css+'</head>',1).replace('</body>',js+'</body>',1)
 changed+=1
if changed<100:raise SystemExit('Expected at least 100 public Website pages; found '+str(changed))
packed=json.dumps(pages,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
s=s[:m.start(2)]+packed+s[m.end(2):]
file.write_text(s,'utf-8')
print('WEBSITE_WIDE_CONTENT_2027','public_pages',changed,'total_pages',len(pages),'cta_space_responsive',True)
