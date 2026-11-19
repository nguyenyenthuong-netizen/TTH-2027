#!/usr/bin/env python3
"""Accessible content-only text zoom for the Marketing 2027 framework.

Must run after the final framework HTML override and final display guard.
Only changes font sizes. Never transform/zoom the entire page or its table frames.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
html=p.read_text("utf-8")
marker="tth-readability-controls-2027"
if marker in html:
    raise SystemExit("Duplicate readability control; refusing to insert twice")
needle='<div class="search"><input aria-label="Tìm trong khung: vị trí, việc, mục, KPI; phím tắt /"'
if needle not in html or 'id="main"' not in html:
    raise SystemExit("Framework HTML changed: missing sidebar search/main")
# Put the controls in the existing sidebar, not in a floating toolbar.
panel='''<div class="tth-text-tools" id="tth-readability-controls-2027" role="group" aria-label="Điều chỉnh cỡ chữ nội dung">
  <span class="tth-text-tools-caption">Cỡ chữ nội dung</span>
  <div class="tth-text-buttons">
    <button type="button" data-tth-font="minus" aria-label="Giảm cỡ chữ">A−</button>
    <output id="tth-text-percent" aria-live="polite" aria-atomic="true">100%</output>
    <button type="button" data-tth-font="plus" aria-label="Tăng cỡ chữ">A+</button>
    <button type="button" data-tth-font="reset" aria-label="Khôi phục cỡ chữ mặc định" title="Cỡ chữ mặc định">Mặc định</button>
  </div>
</div>
'''
# Insert before navigation; the search div closes directly before it.
anchor='</div></div>\n<nav aria-label="12 phần của đề án"'
if anchor not in html:
    raise SystemExit("Framework sidebar nav anchor missing")
html=html.replace(anchor,'</div></div>\n'+panel+'<nav aria-label="12 phần của đề án"',1)
css=r'''
<style id="tth-readability-style-2027">
/* Controls are in the sidebar normal flow, not overlapping the document. */
#side .tth-text-tools{padding:10px 12px 12px;border-block:1px solid #d7e4f4;background:#f8fbff;min-width:0}
#side .tth-text-tools-caption{display:block;margin-bottom:7px;color:#223d68;font:700 12px/1.3 Arial,Tahoma,sans-serif}
#side .tth-text-buttons{display:grid;grid-template-columns:minmax(40px,1fr) minmax(44px,.85fr) minmax(40px,1fr) minmax(70px,1.3fr);align-items:stretch;gap:5px}
#side .tth-text-buttons button{cursor:pointer;min-width:0;padding:8px 3px;border:1px solid #b5cdec;border-radius:7px;background:#fff;color:#0837A1;font:750 13px/1.3 Arial,Tahoma,sans-serif;white-space:normal}
#side .tth-text-buttons button:hover{background:#eaf2ff}
#side .tth-text-buttons button:focus-visible{outline:2px solid #ED3237;outline-offset:1px}
#side #tth-text-percent{display:grid;place-items:center;white-space:nowrap;color:#203d66;font:700 12px/1.25 Arial,Tahoma,sans-serif}
#side .tth-text-buttons [data-tth-font="reset"]{font-size:11px}

/* Scale text only. No CSS transform, zoom, fixed heights or width inflation. */
#main{--tth-readable-factor:1;min-width:0}
#main :is(p,li,dd,dt,.lede,.grel-sum,.acceptance-note,.sc-n,.scope-nonbrand){
 font-size:calc(15px * var(--tth-readable-factor))!important;
 line-height:1.56!important;max-height:none!important;overflow-wrap:break-word
}
#main :is(.tbl table th,.tbl table td,.std-table table th,.std-table table td){
 font-size:calc(14px * var(--tth-readable-factor))!important;
 line-height:1.52!important;
 height:auto!important;max-height:none!important;white-space:normal!important;
 overflow-wrap:break-word!important;word-break:normal!important;
 vertical-align:top!important
}
#main :is(.pos,.grel-it,.org-card .grp summary,.pos-n,.pos-sub,.col-h){
 font-size:calc(14px * var(--tth-readable-factor))!important;
 line-height:1.45!important;max-height:none!important;min-width:0!important
}
#main :is(.pos-sub span,.pos-sub i,.grel-it span,.grel-it b,.mkt-bgd-party small){
 font-size:calc(13px * var(--tth-readable-factor))!important;
 line-height:1.5!important;overflow-wrap:break-word!important
}
#main :is(.sec-h,.card-h,.org-card h3,.mkt-one-line h3){
 font-size:calc(19px * var(--tth-readable-factor))!important;
 line-height:1.35!important
}
#main .view-h .vt{font-size:clamp(24px,calc(30px * var(--tth-readable-factor)),42px)!important;line-height:1.3!important}
#main .scope-card h3{font-size:calc(18px * var(--tth-readable-factor))!important}
#main .scope-status .pills span{font-size:calc(13px * var(--tth-readable-factor))!important}

/* Table wrappers preserve horizontal scroll at 125%-135% and small screens. */
#main :is(.tbl,.std-table,.rel-scroll){max-width:100%!important;overflow-x:auto!important;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch}
#main :is(.tbl table,.std-table table){table-layout:auto!important;width:100%;border-collapse:separate!important;border-spacing:0!important}
#main :is(.tbl table,.std-table table) td,
#main :is(.tbl table,.std-table table) th{box-sizing:border-box!important;min-width:0!important;padding:9px 10px!important}
#main .tbl table.wide{min-width:900px!important}
#main .tbl table.mid{min-width:680px!important}
#main .card.meta .tbl table{table-layout:fixed!important;min-width:0!important;width:100%!important}
#main .card.meta .tbl table tr>*:first-child{width:18%!important;min-width:0!important}
#main .card.meta .tbl table tr>*:nth-child(2){width:82%!important;min-width:0!important}

/* Visually distinguish each of four columns, without heavy colored fills. */
#main .tbl table:has(>thead>tr>:nth-child(4):last-child) tr>*:nth-child(2),
#main .tbl table:has(>thead>tr>:nth-child(4):last-child) tr>*:nth-child(4){background:#f5f8fd}
#main .tbl table:has(>thead>tr>:nth-child(4):last-child) tbody tr>*+*{border-left:1px solid #cedbed!important}
#main .tbl table:has(>thead>tr>:nth-child(4):last-child) thead th{background:#e8f0fb!important;border-bottom:2px solid #afc6e6!important}
#main .tbl table:has(>thead>tr>:nth-child(4):last-child){min-width:750px!important}
#main .card,#main .doc-sec,#main .view,#main .org-cols,#main .col,#main .col-b,#main .hosp-grid{min-width:0!important}
#main .org-cols{align-items:start!important}
#main :is(.pos,.pos-sub,.grel-it,.hosp,.mkt-one-line-grid>div){height:auto!important;max-height:none!important}
@media(max-width:800px){
 #main .card.meta .tbl table tr>*:first-child{width:24%!important}
 #main .card.meta .tbl table tr>*:nth-child(2){width:76%!important}
 #main .scope-grid{grid-template-columns:1fr!important}
}
@media(max-width:520px){#main .card.meta .tbl table tr>*{font-size:calc(13px * var(--tth-readable-factor))!important}}
</style>'''
if "</head>" not in html: raise SystemExit("Missing head")
html=html.replace("</head>",css+"</head>",1)
js=r'''
<script id="tth-readability-script-2027">
(function(){
  "use strict";
  const main=document.getElementById("main");
  const group=document.getElementById("tth-readability-controls-2027");
  const output=document.getElementById("tth-text-percent");
  if(!main||!group||!output)return;
  const steps=[90,100,110,120,130,135];
  let current=100;
  try{
    const saved=Number(localStorage.getItem("tth-framework-text-size"));
    if(steps.includes(saved))current=saved;
  }catch(e){}
  function apply(value){
    current=steps.includes(value)?value:100;
    main.style.setProperty("--tth-readable-factor",String(current/100));
    main.dataset.tthTextZoom=String(current);
    output.textContent=current+"%";
    group.querySelectorAll("button").forEach(btn=>{
      const direction=btn.dataset.tthFont;
      btn.disabled=(direction==="plus"&&current===steps[steps.length-1])||(direction==="minus"&&current===steps[0]);
    });
    try{localStorage.setItem("tth-framework-text-size",String(current))}catch(e){}
  }
  group.addEventListener("click",function(event){
    const button=event.target.closest("button[data-tth-font]");
    if(!button)return;
    const type=button.dataset.tthFont;
    const idx=steps.indexOf(current);
    if(type==="plus")apply(steps[Math.min(idx+1,steps.length-1)]);
    else if(type==="minus")apply(steps[Math.max(idx-1,0)]);
    else if(type==="reset")apply(100);
  });
  apply(current);
})();
</script>'''
if "</body>" not in html: raise SystemExit("Missing body end")
html=html.replace("</body>",js+"</body>",1)
assert html.count(marker)==1
assert html.count("tth-readability-script-2027")==1
p.write_text(html,"utf-8")
print("PASS font controls: six levels 90-135%; table-safe scroll; 4-col visual separation",len(html))
