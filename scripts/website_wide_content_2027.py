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
/* Widen centered, fixed-max-width public page containers, never cards.
   CTA width is accounted for by the actual expanded/collapsed state. */
:root{--tth-website-left-gap:clamp(22px,2vw,38px);--tth-website-cta-gap:116px}
#app{max-width:100%!important;width:100%!important;box-sizing:border-box!important}
@media(min-width:981px){
 #app [data-tth-wide-content-2027="1"]{
  width:min(1720px,calc(100vw - var(--tth-website-left-gap) - var(--tth-website-cta-gap)))!important;
  max-width:min(1720px,calc(100vw - var(--tth-website-left-gap) - var(--tth-website-cta-gap)))!important;
  box-sizing:border-box!important;
 }
 #app [data-tth-wide-content-2027="1"][data-tth-wide-outer="1"]{
  margin-left:var(--tth-website-left-gap)!important;margin-right:0!important
 }
 #app [data-tth-wide-content-2027="1"][data-tth-wide-outer="0"]{
  margin-left:0!important;margin-right:0!important
 }
}
@media(max-width:980px){
 #app [data-tth-wide-content-2027="1"]{max-width:100%!important}
}
</style>"""
js=r"""<script id="tth-website-content-wide-js-2027">
(function(){
'use strict';
var root=document.documentElement,resizeTimer=0;
function resize(){
 if(window.innerWidth<981)return;
 var app=document.getElementById('app');if(!app)return;
 var main=app.querySelector('main');if(!main)return;
 var cta=app.querySelector('.fab.tth-cta-fixed');
 var expanded=!!cta&&cta.dataset.collapsed!=='true';
 var right=expanded?Math.min(300,Math.max(238,window.innerWidth*.155)):Math.min(146,Math.max(102,window.innerWidth*.075));
 var left=Math.min(38,Math.max(22,window.innerWidth*.02));
 var target=Math.min(1720,window.innerWidth-left-right);
 root.style.setProperty('--tth-website-left-gap',left+'px');
 root.style.setProperty('--tth-website-cta-gap',right+'px');
 // Evaluate existing layout geometry, not a generic max-width override on
 // every .container (which would distort cards and nested grid columns).
 var nodes=[main];
 var one=Array.from(main.children);
 one.forEach(function(el){nodes.push(el);Array.from(el.children).forEach(function(c){nodes.push(c)})});
 nodes.forEach(function(el){
  if(el.closest('.fab,.card,[role="dialog"],nav,aside,footer'))return;
  var box=el.getBoundingClientRect(),style=getComputedStyle(el);
  if(!box.width||box.width<window.innerWidth*.48||box.width>=target-35)return;
  if(box.left<left+42||window.innerWidth-box.right<right+30)return;
  var explicitMax=style.maxWidth!=='none'&&parseFloat(style.maxWidth)>400;
  var centered=Math.abs(box.left-(window.innerWidth-box.right))<Math.max(130,window.innerWidth*.085);
  if(!explicitMax&&!centered)return;
  var outer=el===main||el.parentElement===main||el.parentElement===app;
  // Never force a child wider than an already constrained multi-column parent.
  if(!outer){
   var parent=el.parentElement,ps=getComputedStyle(parent);
   if(parent.children.length>1 && (ps.display==='flex'||ps.display==='grid'))return;
  }
  el.setAttribute('data-tth-wide-content-2027','1');
  el.dataset.tthWideOuter=outer?'1':'0';
 });
}
function schedule(){clearTimeout(resizeTimer);resizeTimer=setTimeout(resize,40)}
window.addEventListener('resize',schedule,{passive:true});
window.addEventListener('load',schedule);
var fab=document.querySelector('.fab.tth-cta-fixed');
if(fab&&window.MutationObserver){
 new MutationObserver(schedule).observe(fab,{attributes:true,attributeFilter:['data-collapsed']});
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
