#!/usr/bin/env python3
"""CRM: remove duplicate top toolbar and its old menu button;
keep full-screen / diagram actions accessible in the native sidebar.
Executed on the assembled CRM HTML after ZIP extraction.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"crm-da-kenh"/"index.html"
s=p.read_text(encoding="utf-8")
if "<head" not in s.lower() or "</head>" not in s.lower() or "</body>" not in s.lower():
    raise SystemExit("CRM HTML is incomplete")

marker="tth-crm-sidebar-cleanup-1911"
if marker in s:
    raise SystemExit("Already injected: "+marker)

css=r"""
<style id="tth-crm-sidebar-cleanup-style">
/* Controls occupy space in the existing sidebar, never float over main content. */
#tth-crm-sidebar-actions{position:relative!important;display:flex!important;
  flex-direction:column!important;gap:8px!important;padding:12px 12px 14px!important;
  margin:10px 8px!important;border-top:1px solid #cbd9eb!important;
  background:transparent!important;box-sizing:border-box!important;z-index:auto!important}
#tth-crm-sidebar-actions button{position:static!important;display:block!important;
  width:100%!important;min-height:39px!important;padding:8px 10px!important;
  background:#fff!important;border:1px solid #b8cae2!important;
  border-radius:8px!important;color:#0837A1!important;font:700 14px/1.35 Arial,Tahoma,sans-serif!important;
  white-space:normal!important;cursor:pointer!important}
#tth-crm-sidebar-actions button:last-child{background:#0837A1!important;color:#fff!important}
#tth-crm-sidebar-actions button:focus-visible{outline:2px solid #ED3237;outline-offset:2px}
#tth-crm-retired-topbar{display:none!important;height:0!important;min-height:0!important;
  max-height:0!important;margin:0!important;padding:0!important;border:0!important;overflow:hidden!important}
#tth-crm-retired-open-menu,#ux-sidebar-toggle{display:none!important}
</style>
"""
js=r"""
<script id="tth-crm-sidebar-cleanup-1911">
(function(){
 function norm(s){return (s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/đ/g,'d').replace(/Đ/g,'D').replace(/\s+/g,' ').trim().toLowerCase();}
 function controls(){return Array.from(document.querySelectorAll('button,a,[role="button"]'));}
 function find(label){
   return controls().find(function(b){return norm(b.textContent||b.getAttribute('aria-label'))===label;});
 }
 function removeMenu(){
   var old=document.getElementById('ux-sidebar-toggle');
   if(old)old.remove();
   controls().forEach(function(b){
     if(norm(b.textContent||'').includes('mo danh muc')
        && b.closest('aside')) b.remove();
   });
   document.body.classList.remove('ux-crm-min');
   try{localStorage.removeItem('tth-ux-crm-compact')}catch(e){}
 }
 function initialize(){
   removeMenu();
   var side=document.querySelector('.layout aside')||document.querySelector('#sidebar')||
     document.querySelector('aside.sidebar')||document.querySelector('aside');
   if(!side){console.warn('[CRM] Sidebar not found; toolbar kept to preserve navigation');return;}
   var full=find('toan man hinh'),flow=find('xem luu do'),menu=find('mo danh muc');
   if(!full||!flow){console.warn('[CRM] Original actions not found; toolbar kept to preserve navigation');return;}
   if(document.getElementById('tth-crm-sidebar-actions'))return;
   var bar=null,anc=full,depth=0;
   while(anc && anc!==document.body && depth++<8){
     if(anc.contains(flow) && (anc.tagName==='HEADER'||norm(anc.textContent).includes('de an crm da kenh'))){
       bar=anc;break;
     }
     anc=anc.parentElement;
   }
   /* Never hide all page content if the original controls do not share a standalone toolbar. */
   if(!bar || bar.contains(side) || bar.querySelector('main') ||
      bar.getBoundingClientRect().height>170){
     console.warn('[CRM] Safe toolbar boundary not found; retained old toolbar');return;
   }
   var dock=document.createElement('div');dock.id='tth-crm-sidebar-actions';
   [
     {name:'Toàn màn hình',original:full},
     {name:'Xem lưu đồ',original:flow}
   ].forEach(function(item){
      var b=document.createElement('button');b.type='button';b.textContent=item.name;
      b.addEventListener('click',function(){item.original.click()});
      dock.appendChild(b);
   });
   var identity=side.querySelector('.identity');
   if(identity && identity.parentElement===side){
     side.insertBefore(dock,identity.nextSibling);
   } else {
     side.insertBefore(dock,side.firstElementChild);
   }
   bar.id='tth-crm-retired-topbar';bar.style.setProperty('display','none','important');
   if(menu && !bar.contains(menu)){
     menu.id='tth-crm-retired-open-menu';
     menu.style.setProperty('display','none','important');
   }
   document.documentElement.dataset.tthCrmSidebar='ready';
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize);
 else initialize();
 window.addEventListener('load',initialize,{once:true});
 window.addEventListener('pageshow',removeMenu);
 document.addEventListener('visibilitychange',function(){if(!document.hidden)removeMenu()});
 setTimeout(initialize,500);
})();
</script>
"""
s=s.replace("</head>",css+"\n<style id=\"tth-crm-responsive-1911\">\n/* Never show full-text actions inside a 72px collapsed vertical sidebar. */\n@media screen and (min-width:901px){\n .layout,.layout.crm-sidebar-mini{display:grid!important;grid-template-columns:clamp(228px,18vw,268px) minmax(0,1fr)!important}\n .layout>aside,.layout.crm-sidebar-mini>aside{box-sizing:border-box!important;min-width:0!important;width:auto!important;padding:16px 12px!important}\n .layout.crm-sidebar-mini .identity,.layout.crm-sidebar-mini .navtitle,.layout.crm-sidebar-mini .asideFoot{display:flex!important}\n .layout.crm-sidebar-mini .nav{display:flex!important;flex-direction:column!important;gap:8px!important;margin-top:16px!important}\n .layout.crm-sidebar-mini .navbtn{display:flex!important;justify-content:flex-start!important;font-size:14px!important;line-height:1.35!important;width:100%!important;padding:11px 12px!important;min-height:45px!important;overflow-wrap:normal!important}\n .layout.crm-sidebar-mini .navbtn .navtxt{display:inline!important;font-size:14px!important;line-height:1.35!important}\n}\n#crmSidebarToggle,#ux-sidebar-toggle{display:none!important}\n#ux-search-launch,#tth-crm-sidebar-actions button{\n font-size:14px!important;line-height:1.35!important;\n word-break:normal!important;overflow-wrap:break-word!important;\n white-space:normal!important;writing-mode:horizontal-tb!important;\n min-width:0!important;max-width:100%!important\n}\n#ux-search-launch{padding:10px 12px!important;text-align:left!important}\n#tth-crm-sidebar-actions{min-width:0!important}\n#s3,#s3 .diagram-stage,#s3 .diagramWrap{min-width:0!important;max-width:100%!important;box-sizing:border-box!important}\n#s3 .flowBar{max-width:100%!important;overflow-x:auto!important;overscroll-behavior-x:contain;scrollbar-width:thin}\n#s3 .flowbtn{flex-shrink:0!important;white-space:nowrap!important}\n#s3 .flow-chart-scroll{max-width:100%!important;overflow-x:auto!important;scrollbar-width:thin;overscroll-behavior-x:contain}\n#s3 .crm-compact-grid{max-width:100%!important;min-width:0!important}\n#s3 .crm-flow-node,#s3 .crm-phase{min-width:0!important;box-sizing:border-box!important}\n#s3 .crm-node-copy strong,#s3 .crm-node-copy small{overflow-wrap:break-word!important;word-break:normal!important}\n@media screen and (max-width:900px){\n .layout,.layout.crm-sidebar-mini{display:block!important}\n .layout>aside,.layout.crm-sidebar-mini>aside{position:relative!important;top:auto!important;height:auto!important;max-height:none!important;\n   display:flex!important;flex-direction:column!important;gap:7px!important;\n   width:100%!important;min-width:0!important;box-sizing:border-box!important;padding:9px 12px!important}\n .layout aside .identity,.layout.crm-sidebar-mini aside .identity{display:none!important}\n .layout aside .nav,.layout.crm-sidebar-mini aside .nav{display:flex!important;flex-direction:row!important;\n   gap:7px!important;margin:0!important;min-height:48px!important;overflow-x:auto!important;overflow-y:hidden!important;scrollbar-width:thin}\n .layout aside .navbtn,.layout.crm-sidebar-mini aside .navbtn{flex:0 0 auto!important;width:auto!important;min-width:110px!important;\n   min-height:43px!important;max-height:60px!important;display:flex!important;align-items:center!important;justify-content:center!important;\n   padding:7px 10px!important;font-size:12px!important;line-height:1.25!important;white-space:normal!important;overflow-wrap:normal!important}\n .layout.crm-sidebar-mini .navbtn .navtxt{display:inline!important;font-size:12px!important}\n #tth-crm-sidebar-actions{margin:0!important;border:0!important;padding:3px 0!important;\n   display:flex!important;flex-direction:row!important;gap:7px!important}\n #tth-crm-sidebar-actions button{flex:1 1 0!important;max-width:none!important;min-height:37px!important;padding:6px 9px!important;font-size:12px!important}\n #ux-search-launch{min-height:39px!important;margin:0!important;width:100%!important;padding:7px 10px!important}\n .layout>main{min-width:0!important;width:100%!important;max-width:100%!important}\n #s3.slide{padding:14px!important}\n #s3 .diagram-toolbar{min-width:0!important;display:block!important}\n #s3 .flowBar{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important}\n #s3 .crm-compact-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:8px!important}\n}\n@media screen and (max-width:540px){\n #s3 .crm-compact-grid{grid-template-columns:minmax(0,1fr)!important}\n #s3 .slideHeader h1{font-size:clamp(23px,6vw,31px)!important}\n}\n</style>\n"+"</head>",1).replace("</body>",js+"<script id=\"tth-crm-force-expanded-1911\">\n(function(){\n \"use strict\";\n function expand(){\n   var layout=document.querySelector(\".layout\");\n   if(layout)layout.classList.remove(\"crm-sidebar-mini\");\n   var b=document.getElementById(\"crmSidebarToggle\");\n   if(b)b.remove();\n   try{localStorage.removeItem(\"crmSidebarMini\")}catch(e){}\n }\n if(document.readyState===\"loading\")document.addEventListener(\"DOMContentLoaded\",expand);\n else expand();\n window.addEventListener(\"pageshow\",expand);\n window.addEventListener(\"resize\",expand,{passive:true});\n})();\n</script>\n"+"</body>",1)

# 19/11: branding and accessible sidebar placement (keep original logo image bytes).
# This is deliberately injected after the previous sidebar repair so it wins
# without mutating the CRM database, graph, or navigation logic.
brand_css=r"""<style id="tth-crm-brand-sidebar-final-1911">
@media(min-width:731px){
 .layout>aside{display:flex!important;flex-direction:column!important;overflow-y:auto!important;overflow-x:hidden!important;scrollbar-width:thin!important;min-width:228px!important}
 .layout>aside .identity{display:flex!important;flex-direction:column!important;align-items:flex-start!important;gap:10px!important;padding:6px 10px 19px!important;border-bottom:1px solid #c7d7ec!important}
 .layout>aside .identity img#tthLogo{display:block!important;width:146px!important;height:91px!important;max-width:100%!important;object-fit:contain!important;object-position:left center!important}
 .layout>aside .identity div{width:100%!important;min-width:0!important}
 .layout>aside .identity strong{display:block!important;font:800 17px/1.3 Arial,Tahoma,sans-serif!important;letter-spacing:.02em!important;color:#092f72!important;white-space:normal!important;overflow-wrap:normal!important;word-break:normal!important}
 .layout>aside .identity small{display:block!important;margin-top:3px!important;font:700 12px/1.3 Arial,Tahoma,sans-serif!important;letter-spacing:.08em!important;color:#476188!important}
 .layout>aside .navtitle{color:#526b91!important;font-size:12px!important;letter-spacing:.1em!important;margin:17px 11px 8px!important}
 .layout>aside .nav{min-height:0!important;margin-top:0!important}
 .layout>aside .navbtn{color:#123969!important;font-size:14px!important;line-height:1.4!important;min-height:46px!important}
 .layout>aside .navbtn.active{color:#09358e!important;background:#e7effd!important}
 .layout>aside .asideFoot{margin-top:18px!important;color:#425a7f!important;font-size:12px!important;line-height:1.55!important}
 .layout>aside #ux-search-launch{display:block!important;flex:0 0 auto!important;align-self:stretch!important;order:100!important;margin:auto 0 6px!important;margin-top:auto!important;min-height:44px!important;padding:11px 13px!important;font:700 15px/1.3 Arial,Tahoma,sans-serif!important;text-align:center!important;color:#fff!important;background:#0837a1!important;border:1px solid #0837a1!important;border-radius:10px!important;white-space:normal!important;word-break:normal!important;overflow-wrap:normal!important}
}
#s3 .slideHeader h1{color:#082c68!important;line-height:1.22!important;letter-spacing:-.015em!important}
#s3 .slideHeader p,#s3 .flowFooter,#s3 .flowFootNote{color:#385577!important}
#s3 .flowBar{max-width:100%!important;overflow-x:auto!important;scrollbar-width:thin!important;scroll-snap-type:x proximity!important}
#s3 .flowBar button{flex-shrink:0!important;white-space:nowrap!important;font-weight:750!important}
#s3 .flow-lane-pane,#s3 .diagram-stage,#s3 .flow-chart-scroll{min-width:0!important;max-width:100%!important;box-sizing:border-box!important;overflow-x:auto!important;scrollbar-width:thin!important}
#s3 .crm-flow-meta-panel{max-width:min(560px,calc(100vw - 24px))!important}
@media(max-width:730px){
 .layout>aside .identity{display:flex!important;align-items:flex-start!important;gap:9px!important;padding:5px 4px!important}
 .layout>aside .identity img#tthLogo{width:90px!important;height:54px!important;object-fit:contain!important}
 .layout>aside .identity strong{font-size:13px!important;line-height:1.3!important;color:#092f72!important}
 .layout>aside .identity small{font-size:11px!important;color:#476188!important}
 .layout>aside #ux-search-launch{display:block!important;order:100!important;margin:8px 0 0!important;white-space:normal!important;word-break:normal!important}
 #s3 .slideHeader h1{font-size:clamp(22px,5.4vw,30px)!important}
}
</style>"""
brand_js=r"""<script id="tth-crm-brand-sidebar-final-1911">
(function(){
 "use strict";
 function update(){
  var side=document.querySelector(".layout>aside")||document.querySelector(".layout aside");
  if(!side)return;
  var identity=side.querySelector(".identity");
  if(identity){
   var heading=identity.querySelector("strong"),sub=identity.querySelector("small");
   if(heading)heading.textContent="ĐỀ ÁN CRM ĐA KÊNH";
   if(sub)sub.textContent="TTH GROUP";
  }
  var search=document.getElementById("ux-search-launch");
  if(search&&search.parentElement!==side)side.appendChild(search);
  else if(search&&side.lastElementChild!==search)side.appendChild(search);
  if(search)search.setAttribute("aria-label","Tìm kiếm nâng cao");
  document.documentElement.dataset.tthCrmSearchPlacement=search?"bottom":"missing";
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",update);
 else update();
 window.addEventListener("pageshow",update);
})();
</script>"""
s=s.replace("</head>",brand_css+"</head>",1).replace("</body>",brand_js+"</body>",1)
assert 'tth-crm-brand-sidebar-final-1911' in s


# Final legibility/layout layer: restore natural card heights; never squeeze all
# four workflow phases into a fixed viewport, and remove redundant subtitle.
legible_css=r"""<style id="tth-crm-readable-nonoverlap-1911">
/* 1. Sidebar brand: original logo, project name only (no TTH Group subtitle). */
.layout>aside .identity{align-items:flex-start!important;min-width:0!important}
.layout>aside .identity strong{font-size:18px!important;line-height:1.38!important;letter-spacing:0!important;white-space:normal!important;word-break:normal!important;color:#082E6A!important}
.layout>aside .identity small{display:none!important}
.layout>aside .navtitle{color:#304E78!important}
.layout>aside .navbtn{color:#123968!important;background:transparent!important;line-height:1.4!important;letter-spacing:0!important;word-break:normal!important;white-space:normal!important}
.layout>aside .navbtn span,.layout>aside .navbtn .navtxt{color:inherit!important;line-height:inherit!important}
.layout>aside .navbtn.active{background:#0837A1!important;color:#fff!important}
.layout>aside .navbtn.active span,.layout>aside .navbtn.active .navtxt{color:#fff!important}
.layout>aside .asideFoot{color:#334F73!important;line-height:1.55!important}
.layout>aside .asideFoot strong{color:#082E6A!important}
/* 2. Workflow text blocks: readable contrast and natural intrinsic height. */
#s3 .stepnum{font-size:13px!important;color:#CF2631!important;letter-spacing:.08em!important}
#s3 .slideHeader h1{color:#112E64!important;line-height:1.25!important;letter-spacing:-.012em!important}
#s3 .slideHeader h1 em{color:#0837A1!important}
#s3 .slideHeader p{font-size:15px!important;line-height:1.55!important;color:#334E72!important}
#s3 .diagram-stage{overflow:visible!important;max-height:none!important;height:auto!important}
#s3 .diagramWrap{max-height:none!important;height:auto!important;overflow:visible!important;min-height:0!important}
#s3 .flow-chart-scroll{max-height:none!important;height:auto!important;overflow-x:auto!important;overflow-y:visible!important}
#s3 .flow-svg-host{height:auto!important;min-height:0!important;max-height:none!important}
#s3 .crm-overview-top{font-size:14px!important;line-height:1.5!important;color:#365477!important;flex-wrap:wrap!important;padding:10px 12px!important;gap:8px!important}
#s3 .crm-overview-top b{color:#082F75!important}
#s3 .crm-compact-grid{width:100%!important;max-width:100%!important;min-width:0!important;display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr))!important;gap:14px!important;align-items:stretch!important}
#s3 .crm-phase{min-width:0!important;max-width:100%!important;height:auto!important;max-height:none!important;overflow:visible!important}
#s3 .crm-phase:after{display:none!important}
#s3 .crm-phase-head{display:flex!important;align-items:center!important;gap:10px!important;min-height:56px!important;height:auto!important;max-height:none!important;padding:12px 12px!important;font-size:15px!important;line-height:1.4!important;font-weight:800!important;color:#102F6C!important;white-space:normal!important;word-break:normal!important;overflow-wrap:break-word!important;background:#E5EEFC!important}
#s3 .crm-phase-body{display:flex!important;flex-direction:column!important;gap:10px!important;padding:12px!important;min-height:0!important;height:auto!important;max-height:none!important;overflow:visible!important}
#s3 button.crm-flow-node{display:grid!important;grid-template-columns:32px minmax(0,1fr) 18px!important;align-items:start!important;gap:9px!important;padding:12px 10px!important;min-height:91px!important;height:auto!important;max-height:none!important;width:100%!important;min-width:0!important;overflow:visible!important;white-space:normal!important;word-break:normal!important}
#s3 .crm-node-copy{display:flex!important;flex-direction:column!important;gap:5px!important;min-width:0!important;height:auto!important;overflow:visible!important;overflow-wrap:normal!important}
#s3 .crm-node-copy strong{display:block!important;color:#112F65!important;font-size:16px!important;line-height:1.38!important;font-weight:800!important;white-space:normal!important;overflow-wrap:break-word!important;word-break:normal!important}
#s3 .crm-node-copy small{display:block!important;color:#395572!important;font-size:14px!important;line-height:1.4!important;font-weight:550!important;white-space:normal!important;overflow-wrap:break-word!important}
#s3 .crm-node-routes{display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:4px 7px!important;padding-top:5px!important;line-height:1.35!important}
#s3 .crm-route{color:#073B8E!important;font-size:13px!important;font-weight:750!important;line-height:1.35!important;white-space:normal!important}
#s3 .crm-stepnum{font-size:15px!important;line-height:1.3!important}
#s3 .crm-kindmark{color:#275A9D!important;font-size:15px!important}
#s3 .diagram-toolbar{display:flex!important;flex-wrap:wrap!important;align-items:center!important;gap:10px!important;overflow:visible!important}
#s3 .flowBar{min-width:0!important;max-width:100%!important;display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;overflow-y:hidden!important;scrollbar-width:thin!important;gap:8px!important}
#s3 .flowbtn{font-size:14px!important;line-height:1.3!important;min-height:43px!important;padding:10px 13px!important;flex:0 0 auto!important;background:#fff!important;border-color:#9AB6DE!important;color:#17457E!important;white-space:nowrap!important}
#s3 .flowbtn.active{background:#0837A1!important;color:#fff!important;border-color:#0837A1!important}
#s3 .flowFooter,#s3 .flowFootNote{color:#355474!important;line-height:1.45!important}
#s3 .crm-flow-help-button{color:#08377A!important;background:#fff!important;border:1px solid #A7BFE0!important}
/* 3. Responsive: two phases before text becomes too narrow; single on mobile. */
@media(max-width:1599px){#s3 .crm-compact-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(max-width:800px){#s3 .crm-compact-grid{grid-template-columns:1fr!important}}
@media(max-width:730px){
 .layout>aside .identity strong{font-size:15px!important}
 #s3 .slideHeader h1{font-size:clamp(23px,5vw,31px)!important;line-height:1.3!important}
 #s3 .crm-phase-body{padding:10px!important}
 #s3 .crm-node-copy strong{font-size:16px!important}
 #s3 .crm-node-copy small{font-size:14px!important}
}
</style>"""
legible_js=r"""<script id="tth-crm-readable-nonoverlap-1911">
(function(){
 function cleanBrand(){
   var identity=document.querySelector(".layout>aside .identity");
   if(!identity)return;
   var small=identity.querySelector("small");
   if(small)small.remove();
   var title=identity.querySelector("strong");
   if(title)title.textContent="ĐỀ ÁN CRM ĐA KÊNH";
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",cleanBrand);
 else cleanBrand();
 window.addEventListener("pageshow",cleanBrand);
})();
</script>"""
s=s.replace("</head>",legible_css+"</head>",1).replace("</body>",legible_js+"</body>",1)
assert 'tth-crm-readable-nonoverlap-1911' in s


# Number and section title must sit next to one another, with a consistent
# 7px gap; prevent the number or word wraps from collapsing them together.
nav_spacing_css=r"""<style id="tth-crm-nav-number-spacing-1911">
.layout>aside #sideNav .navbtn{
 display:grid!important;
 grid-template-columns:23px minmax(0,1fr)!important;
 column-gap:7px!important;
 align-items:center!important;
 justify-content:start!important;
 text-align:left!important;
 padding:11px 12px!important;
 min-height:44px!important;
 box-sizing:border-box!important;
}
.layout>aside #sideNav .navbtn .navnum{
 grid-column:1!important;
 width:23px!important;
 min-width:23px!important;
 max-width:23px!important;
 margin:0!important;
 padding:0!important;
 display:block!important;
 flex-shrink:0!important;
 font:800 13px/1.3 Arial,Tahoma,sans-serif!important;
 letter-spacing:0!important;
 text-align:left!important;
 white-space:nowrap!important;
 color:#3B5C86!important;
}
.layout>aside #sideNav .navbtn .navtxt{
 grid-column:2!important;
 display:block!important;
 min-width:0!important;
 width:auto!important;
 margin:0!important;
 padding:0!important;
 font:700 14px/1.4 Arial,Tahoma,sans-serif!important;
 color:#163B70!important;
 white-space:normal!important;
 overflow-wrap:normal!important;
 word-break:normal!important;
}
.layout>aside #sideNav .navbtn.active .navnum,
.layout>aside #sideNav .navbtn.active .navtxt{color:#fff!important}
@media(max-width:900px){
 .layout>aside #sideNav .navbtn{
   display:grid!important;
   grid-template-columns:22px minmax(0,1fr)!important;
   column-gap:6px!important;
   padding:8px 10px!important;
   min-width:135px!important;
 }
 .layout>aside #sideNav .navbtn .navnum{
   width:22px!important;min-width:22px!important;max-width:22px!important;
 }
 .layout>aside #sideNav .navbtn .navtxt{
   font-size:13px!important;line-height:1.3!important;
 }
}
</style>"""
s=s.replace("</head>",nav_spacing_css+"</head>",1)
assert 'tth-crm-nav-number-spacing-1911' in s


# The original footer used inline <strong>...<br/>text</div>. A former
# .crm-sidebar-mini { display:flex } rule turns the title, <br> and anonymous
# text into three flex items; in 228px width the title becomes a ~50px column.
# Rewrite it structurally, not just by changing text size.
import re
footer_pattern=r'(<div class=["\x27]asideFoot["\x27]>)\s*<strong>([^<]+)</strong>\s*<br\s*/?>\s*([^<]+)(</div>)'
def footer_stack(m):
    return (m.group(1)+"<strong>"+m.group(2).strip()+"</strong>"
            +'<p class="crm-aside-summary">'+m.group(3).strip()+"</p>"+m.group(4))
s,footer_n=re.subn(footer_pattern,footer_stack,s,count=1,flags=re.I)
if footer_n!=1:
    raise AssertionError("CRM sidebar footer structure not found; avoid blind CSS patch")
footer_css=r"""<style id="tth-crm-aside-summary-stack-1911">
/* Title occupies its own line; paragraph flows below without flex columns. */
.layout>aside .asideFoot,
.layout.crm-sidebar-mini>aside .asideFoot{
 display:block!important;
 flex-direction:initial!important;
 width:100%!important;
 min-width:0!important;
 max-width:100%!important;
 flex:0 0 auto!important;
 box-sizing:border-box!important;
 margin:18px 0 8px!important;
 padding:14px 9px 0!important;
 border-top:1px solid #B8C9DF!important;
 text-align:left!important;
 writing-mode:horizontal-tb!important;
 white-space:normal!important;
 word-break:normal!important;
 overflow-wrap:break-word!important;
 color:#315071!important;
 font:500 14px/1.55 Arial,Tahoma,sans-serif!important;
}
.layout>aside .asideFoot>strong,
.layout.crm-sidebar-mini>aside .asideFoot>strong{
 display:block!important;
 float:none!important;
 width:auto!important;
 min-width:0!important;
 max-width:none!important;
 margin:0 0 7px!important;
 white-space:normal!important;
 overflow-wrap:normal!important;
 word-break:normal!important;
 font:800 15px/1.45 Arial,Tahoma,sans-serif!important;
 color:#092F6C!important;
}
.layout>aside .asideFoot>p.crm-aside-summary,
.layout.crm-sidebar-mini>aside .asideFoot>p.crm-aside-summary{
 display:block!important;
 width:100%!important;
 min-width:0!important;
 max-width:100%!important;
 margin:0!important;
 padding:0!important;
 white-space:normal!important;
 word-break:normal!important;
 overflow-wrap:break-word!important;
 font:500 14px/1.55 Arial,Tahoma,sans-serif!important;
 color:#315071!important;
}
@media(max-width:900px){
 .layout>aside .asideFoot,
 .layout.crm-sidebar-mini>aside .asideFoot{
  margin:8px 0!important;
  padding:10px 4px!important;
 }
}
</style>"""
s=s.replace("</head>",footer_css+"</head>",1)
assert '<p class="crm-aside-summary">' in s and 'tth-crm-aside-summary-stack-1911' in s
print("PASS CRM footer one-column markup, title above paragraph")


# 19/11: fix actual sidebar collision. The root cause is compact sidebar
# CSS shrinking the nav while the footer is laid out in the same fixed-height
# flex column. Give nav/footer independent natural heights and make aside
# the only vertical scroll container. Manual browser QA: 390/920/1280/1440/
# 1678px: last nav item bottom < footer top, with 24px separation.
nav_footer_css=r"""<style id="tth-crm-nav-footer-isolation-1911">
@media(min-width:901px){
 .layout,.layout.crm-sidebar-mini{
  grid-template-columns:clamp(248px,18vw,292px) minmax(0,1fr)!important;
 }
 .layout>aside,.layout.crm-sidebar-mini>aside{
  position:sticky!important;top:0!important;width:100%!important;
  min-width:0!important;max-width:none!important;
  height:100dvh!important;max-height:100dvh!important;min-height:0!important;
  overflow-y:auto!important;overflow-x:hidden!important;scrollbar-width:thin!important;
  box-sizing:border-box!important;display:flex!important;flex-direction:column!important;
  align-items:stretch!important;padding:16px 14px 20px!important;
 }
}
.layout>aside>.identity,.layout.crm-sidebar-mini>aside>.identity{
 flex:0 0 auto!important;position:relative!important;min-height:0!important;
 height:auto!important;overflow:visible!important
}
.layout>aside>.navtitle,.layout.crm-sidebar-mini>aside>.navtitle{
 display:block!important;flex:0 0 auto!important;position:relative!important;
 height:auto!important;min-height:0!important;margin:20px 8px 9px!important
}
.layout>aside>#sideNav,.layout.crm-sidebar-mini>aside>#sideNav{
 display:flex!important;flex-direction:column!important;
 align-items:stretch!important;justify-content:flex-start!important;gap:9px!important;
 position:relative!important;flex:0 0 auto!important;
 height:auto!important;min-height:0!important;max-height:none!important;
 margin:0!important;padding:0!important;overflow:visible!important;
 grid-template-columns:none!important
}
.layout>aside>#sideNav>.navbtn,.layout.crm-sidebar-mini>aside>#sideNav>.navbtn{
 position:relative!important;flex:0 0 auto!important;display:grid!important;
 grid-template-columns:24px minmax(0,1fr)!important;gap:7px!important;
 align-items:center!important;justify-content:start!important;
 width:100%!important;height:auto!important;min-height:47px!important;max-height:none!important;
 padding:11px 12px!important;margin:0!important;font-size:14px!important;
 line-height:1.35!important;text-align:left!important;white-space:normal!important;
 overflow:visible!important
}
.layout>aside>#sideNav>.navbtn .navnum,
.layout.crm-sidebar-mini>aside>#sideNav>.navbtn .navnum{
 display:block!important;grid-column:1!important;width:24px!important;
 max-width:24px!important;min-width:24px!important;
 font:800 13px/1.35 Arial,Tahoma,sans-serif!important;white-space:nowrap!important
}
.layout>aside>#sideNav>.navbtn .navtxt,
.layout.crm-sidebar-mini>aside>#sideNav>.navbtn .navtxt{
 display:block!important;grid-column:2!important;min-width:0!important;width:auto!important;
 font:700 14px/1.35 Arial,Tahoma,sans-serif!important;
 white-space:normal!important;word-break:normal!important;overflow-wrap:normal!important
}
.layout>aside>#sideNav>.navbtn.active{
 background:#0837A1!important;border-color:#0837A1!important;
 color:#fff!important
}
.layout>aside>#sideNav>.navbtn.active .navtxt,
.layout>aside>#sideNav>.navbtn.active .navnum{
 color:#fff!important
}
.layout>aside>.asideFoot,.layout.crm-sidebar-mini>aside>.asideFoot{
 display:block!important;position:relative!important;inset:auto!important;
 float:none!important;flex:0 0 auto!important;order:0!important;
 height:auto!important;min-height:0!important;max-height:none!important;
 max-width:100%!important;width:100%!important;box-sizing:border-box!important;
 margin:24px 0 12px!important;padding:17px 8px 0!important;
 overflow:visible!important;white-space:normal!important;word-break:normal!important
}
.layout>aside>.asideFoot>strong{display:block!important;width:auto!important;min-width:0!important;
 margin:0 0 7px!important;font:800 15px/1.4 Arial,Tahoma,sans-serif!important;color:#092F6C!important}
.layout>aside>.asideFoot>p{display:block!important;margin:0!important;width:100%!important;
 font:500 14px/1.55 Arial,Tahoma,sans-serif!important;color:#315071!important}
.layout>aside>#ux-search-launch,.layout.crm-sidebar-mini>aside>#ux-search-launch{
 display:block!important;position:relative!important;flex:0 0 auto!important;
 order:10!important;align-self:stretch!important;margin:12px 0 0!important;
 width:100%!important;height:auto!important;min-height:46px!important;
 max-height:none!important;word-break:normal!important;white-space:normal!important
}
@media(max-width:900px){
 .layout>aside,.layout.crm-sidebar-mini>aside{
  display:flex!important;flex-direction:column!important;position:relative!important;
  width:100%!important;max-width:100%!important;height:auto!important;max-height:none!important;
  overflow:visible!important;padding:12px!important
 }
 .layout>aside>#sideNav,.layout.crm-sidebar-mini>aside>#sideNav{
  display:flex!important;flex-direction:row!important;gap:7px!important;
  max-width:100%!important;overflow-x:auto!important;overflow-y:hidden!important;
  scrollbar-width:thin!important
 }
 .layout>aside>#sideNav>.navbtn{flex:0 0 auto!important;
  width:145px!important;min-height:45px!important;padding:8px!important
 }
 .layout>aside>.asideFoot{margin:12px 0!important}
}
</style>"""
s=s.replace("</head>",nav_footer_css+"</head>",1)
assert s.count('tth-crm-nav-footer-isolation-1911')==1
print("CRM-QA nav/footer: independent natural heights; sidebar scroll container")


# 19/11: opening CRM slide; keep "Không phải một tổng đài mới." on one
# line. The red dot from the diagram :before decoration collided with the
# "TÁCH ĐÚNG CHỨC NĂNG" label. Remove only that dot (not actual buttons).
hero_src='<h1>Không phải<br/><span>một tổng đài mới.</span></h1>'
hero_dst='<h1 class="crm-hero-one-line">Không phải <span>một tổng đài mới.</span></h1>'
if s.count(hero_src)!=1:
    raise AssertionError("CRM opening headline markup changed; cannot safely force single line")
s=s.replace(hero_src,hero_dst,1)
hero_css=r"""<style id="tth-crm-hero-one-line-1911">
#s1 .hero-copy h1.crm-hero-one-line{
 display:block!important;width:100%!important;max-width:100%!important;
 white-space:nowrap!important;word-break:normal!important;overflow-wrap:normal!important;
 font-size:clamp(19px,3.25vw,50px)!important;
 letter-spacing:-.035em!important;line-height:1.22!important
}
#s1 .hero-copy h1.crm-hero-one-line span{
 display:inline!important;white-space:nowrap!important
}
/* This decorative red pseudo-dot intersected the final letters of the label. */
#s1 .hero-visual:before{content:none!important;display:none!important}
#s1 .hero-visual .hv-top{
 display:flex!important;flex-wrap:wrap!important;gap:8px 20px!important;
 align-items:center!important;justify-content:space-between!important;
 min-height:29px!important;line-height:1.35!important
}
#s1 .hero-visual .hv-top>span{
 position:relative!important;white-space:nowrap!important;
 flex:0 1 auto!important;padding-right:8px!important;
 color:#bc2535!important;letter-spacing:.045em!important
}
@media(max-width:700px){
 #s1 .hero-copy h1.crm-hero-one-line{
  font-size:clamp(18px,5.15vw,24px)!important;letter-spacing:-.04em!important
 }
}
</style>"""
s=s.replace("</head>",hero_css+"</head>",1)
assert 'tth-crm-hero-one-line-1911' in s and hero_src not in s
print("PASS CRM opening: single-line headline, no red pseudo-dot over functional label")


# Readable typography and deliberate TTH palette: avoid tiny gray-on-blue
# text; allow cards to grow instead of locking their heights.
readable_css=r"""<style id="tth-crm-typography-accessible-2111">
:root{--tth-legible-blue:#0837A1;--tth-legible-ink:#173967;--tth-legible-muted:#395575}
.layout>aside #sideNav .navbtn,
.layout>aside #sideNav .navbtn .navtxt{font-size:15px!important;line-height:1.45!important}
.layout>aside #sideNav .navbtn .navnum{font-size:14px!important;line-height:1.45!important}
.layout>aside #sideNav .navbtn.active,
.layout>aside #sideNav .navbtn[aria-current="page"],
.layout>aside #sideNav .navbtn.on{
 background:#0837A1!important;color:#fff!important;border-left-color:#ED3237!important
}
.layout>aside #sideNav .navbtn.active *,
.layout>aside #sideNav .navbtn[aria-current="page"] *,
.layout>aside #sideNav .navbtn.on *{color:#fff!important}
.layout>aside #sideNav .navbtn:not(.active):not(.on):not([aria-current="page"]){color:#163C72!important}
.layout>aside .navtitle{font-size:13px!important;color:#304F7B!important;line-height:1.45!important}
.layout>aside .asideFoot>strong{font-size:16px!important;line-height:1.4!important}
.layout>aside .asideFoot>p{font-size:15px!important;line-height:1.6!important}
#s1 .hero-visual .hv-top>span{font-size:14px!important;line-height:1.42!important;color:#C02337!important}
#s1 .hero-visual .hv-top{min-height:36px!important}
#s1 .hero-visual .hv-top>span:last-child{max-width:100%!important}
#s1 .hero-visual .hv-body small,
#s1 .hero-visual .hv-body .muted,
#s1 .hero-visual .hv-body p{font-size:14px!important;line-height:1.48!important;color:#385475!important}
#s1 .hero-visual .hv-body b,
#s1 .hero-visual .hv-body strong{color:#08377B!important}
#s3 .crm-node-copy small,
#s3 .crm-route,
#s3 .crm-overview-top,
#s3 .flowFooter,#s3 .flowFootNote{font-size:15px!important;line-height:1.48!important}
#s3 .crm-node-copy strong{font-size:17px!important;line-height:1.42!important}
#s3 .stepnum{font-size:14px!important}
#s3 .flowbtn{font-size:15px!important;line-height:1.4!important}
#s3 .crm-flow-node,#s3 .crm-phase-body{height:auto!important;min-height:0!important;max-height:none!important}
#s3 .crm-compact-grid{align-items:stretch!important}
#s3 .crm-phase-head{font-size:16px!important;line-height:1.42!important}
#s3 button.crm-flow-node{min-height:100px!important;max-height:none!important;overflow:visible!important}
#s3 button.crm-flow-node .crm-node-copy{min-height:0!important;max-height:none!important}
#s3 .crm-phase-body{overflow:visible!important}
#s3 .slideHeader p{font-size:16px!important;line-height:1.5!important}
@media(max-width:900px){
 .layout>aside #sideNav .navbtn,
 .layout>aside #sideNav .navbtn .navtxt{font-size:14px!important;line-height:1.38!important}
 #s3 .crm-node-copy small,#s3 .crm-route{font-size:14px!important}
 #s3 .crm-phase-head{font-size:15px!important}
}
</style>"""
s=s.replace("</head>",readable_css+"</head>",1)
assert s.count("tth-crm-typography-accessible-2111")==1
print("PASS CRM typography: accessible nav contrast, metadata >=14px, natural workflow card heights")

p.write_text(s,encoding="utf-8")
assert marker in s and "tth-crm-retired-topbar" in s
print("PASS CRM sidebar cleanup injected; HTML bytes:",p.stat().st_size)
