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
     if(/(?:^|\\s)mo danh muc(?:\\s|$)/.test(norm(b.textContent||''))
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
p.write_text(s,encoding="utf-8")
assert marker in s and "tth-crm-retired-topbar" in s
print("PASS CRM sidebar cleanup injected; HTML bytes:",p.stat().st_size)
