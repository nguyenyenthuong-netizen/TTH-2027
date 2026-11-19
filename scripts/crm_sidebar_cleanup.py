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
s=s.replace("</head>",css+"</head>",1).replace("</body>",js+"</body>",1)
p.write_text(s,encoding="utf-8")
assert marker in s and "tth-crm-retired-topbar" in s
print("PASS CRM sidebar cleanup injected; HTML bytes:",p.stat().st_size)
