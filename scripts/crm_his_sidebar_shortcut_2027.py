#!/usr/bin/env python3
"""Direct, discoverable sidebar action for existing CRM/HIS linkage example.
It opens slide 03, workflow 02 and the example immediately. No fake HIS connection.
"""
from pathlib import Path
import sys
p=(Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"crm-da-kenh"/"index.html")
s=p.read_text("utf-8")
for key in ("id=\"sideNav\"","id=\"flowTabs\"","id=\"crmFlowMetaToggle\"","id=\"crmFlowMetaPanel\"","CRM-00125","BN-00876"):
 if key not in s:raise SystemExit("CRM_HIS_SHORTCUT missing prerequisite: "+key)
if 'id="tth-crm-his-shortcut-script-2027"' in s:raise SystemExit("CRM_HIS_SHORTCUT duplicate")
css=r'''<style id="tth-crm-his-shortcut-style-2027">
/* Separate from 7 slide controls. Always in layout flow, never over content. */
#tth-crm-his-shortcut{position:relative!important;display:flex!important;
  align-items:center!important;justify-content:flex-start!important;gap:9px!important;
  width:calc(100% - 16px)!important;min-width:0!important;max-width:none!important;
  margin:9px 8px 14px!important;min-height:54px!important;padding:10px 11px!important;
  box-sizing:border-box!important;background:#EAF2FF!important;color:#0837A1!important;
  border:1px solid #A8C2E9!important;border-left:4px solid #ED3237!important;
  border-radius:10px!important;font:800 14px/1.36 Arial,"Segoe UI",Tahoma,sans-serif!important;
  text-align:left!important;white-space:normal!important;overflow-wrap:break-word!important;
  writing-mode:horizontal-tb!important;cursor:pointer!important;box-shadow:none!important}
#tth-crm-his-shortcut .tth-his-shortcut-icon{font-size:20px!important;line-height:1!important;
  flex:0 0 auto!important;color:#ED3237!important}
#tth-crm-his-shortcut:hover{background:#DCEAFF!important;border-color:#6697D7!important}
#tth-crm-his-shortcut:focus-visible{outline:3px solid #ED3237!important;outline-offset:2px!important}
#s3 #flowDescription .tth-his-example-head b{font-size:18px!important;line-height:1.46!important}
#s3 #flowDescription .tth-his-item span{font-size:15px!important;line-height:1.5!important}
#s3 #flowDescription .tth-his-example p{font-size:15px!important;line-height:1.55!important}
#s3 #flowDescription .tth-his-example p.tth-his-foot{font-size:14px!important}
@media(max-width:850px){
  #tth-crm-his-shortcut{font-size:13px!important;padding:9px!important}
}
</style>'''
js=r'''<script id="tth-crm-his-shortcut-script-2027">
(function(){
 "use strict";
 function showMapping(){
  var nav=document.querySelectorAll('#sideNav button');
  if(nav.length<3)return false;
  nav[2].click();
  var tabs=document.querySelectorAll('#flowTabs .flowbtn');
  if(tabs.length<2)return false;
  tabs[1].click();
  var toggle=document.getElementById('crmFlowMetaToggle');
  var panel=document.getElementById('crmFlowMetaPanel');
  if(!toggle||!panel)return false;
  if(panel.hidden)toggle.click();
  // Show the mapping in the existing business flow context and take keyboard focus to it.
  window.requestAnimationFrame(function(){
   var example=panel.querySelector('.tth-his-example');
   if(example){
    example.setAttribute('tabindex','-1');
    example.scrollIntoView({block:'nearest',inline:'nearest',behavior:'auto'});
    example.focus({preventScroll:true});
   }
  });
  return true;
 }
 function initialize(){
  if(document.getElementById('tth-crm-his-shortcut'))return;
  var aside=document.querySelector('.layout>aside');
  var nav=document.getElementById('sideNav');
  if(!aside||!nav||!nav.parentNode)return;
  var b=document.createElement('button');
  b.type='button';b.id='tth-crm-his-shortcut';
  b.setAttribute('aria-label','Mở trực tiếp ví dụ liên kết hồ sơ CRM với mã bệnh nhân HIS');
  b.setAttribute('title','Mở Lưu đồ 02 và ví dụ CRM-00125 liên kết BN-00876');
  var icon=document.createElement('span');icon.className='tth-his-shortcut-icon';icon.setAttribute('aria-hidden','true');icon.textContent='↔';
  var label=document.createElement('span');label.textContent='Liên kết hồ sơ CRM – mã HIS';
  b.append(icon,label);
  b.addEventListener('click',function(){
   if(!showMapping())console.warn('[CRM] Cannot open HIS linkage example; original navigation retained');
  });
  nav.parentNode.insertBefore(b,nav);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',initialize,{once:true});
 else initialize();
})();
</script>'''
if s.count("</head>")!=1 or s.count("</body>")!=1:raise SystemExit("CRM_HIS_SHORTCUT malformed html")
s=s.replace("</head>",css+"</head>",1).replace("</body>",js+"</body>",1)
p.write_text(s,"utf-8")
print("CRM_HIS_SHORTCUT_OK direct sidebar path -> slide 03 -> workflow 02 -> mapping panel, no slide count changes")
