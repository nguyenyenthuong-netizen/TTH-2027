#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sửa chữ bị chia cột trong bảng tth-card ở toàn Khung Marketing TTH.

Nguyên nhân: mỗi <td> dùng display:grid với ::before làm nhãn, còn text node,
<a>, <span class=pend> được tự động tách thành nhiều grid item. Ký hiệu
(CN-1, ...), dấu ngoặc và nhãn chờ duyệt vì thế rơi sang cột trái.
Giải pháp: bọc nội dung gốc trong một vùng grid duy nhất, giữ nguyên DOM
con (liên kết, nhãn pháp lý, nội dung và dữ liệu) và theo dõi các lần render.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
page = root / "khung-marketing" / "index.html"
s = page.read_text("utf-8")
marker = "tth-grid-cell-inline-integrity-2027"
assert marker not in s, "Không chạy chồng bản sửa lỗi dàn trang"
assert 'table.tth-card' in s and 'data-tth-title' in s
assert s.count("</head>") == 1 and s.count("</body>") == 1

style = """
<style id="tth-grid-cell-inline-integrity-2027">
/* Các ô dạng thẻ có đúng hai thành phần lưới: nhãn và vùng văn bản. */
#main table.tth-card>tbody>tr>td:not(:has(details,table,.tbl))::before,
#main table.tth-card>tbody>tr>th:not(:has(details,table,.tbl))::before {
  grid-column:1!important;grid-row:1!important;align-self:start!important;
}
#main table.tth-card>tbody>tr>td>.tth-grid-value,
#main table.tth-card>tbody>tr>th>.tth-grid-value {
  grid-column:2!important;grid-row:1!important;display:block!important;
  min-width:0!important;max-width:100%!important;
  font:inherit!important;color:inherit!important;
  line-height:1.57!important;white-space:normal!important;
  overflow-wrap:break-word!important;word-break:normal!important;
}
#main table.tth-card .tth-grid-value .pend {
  display:inline!important;position:static!important;
  padding:1px 6px!important;border-radius:5px!important;
  white-space:normal!important;line-height:inherit!important;
  vertical-align:baseline!important;box-decoration-break:clone;
  -webkit-box-decoration-break:clone;
}
#main table.tth-card .tth-grid-value a {
  display:inline!important;position:static!important;float:none!important;
  white-space:normal!important;vertical-align:baseline!important;
}
#main table.tth-card .tth-grid-value :is(.xref,.hf-gloss) {
  overflow-wrap:normal!important;word-break:normal!important;
}
@media (max-width:760px) {
  #main table.tth-card>tbody>tr>td>.tth-grid-value,
  #main table.tth-card>tbody>tr>th>.tth-grid-value {line-height:1.54!important}
}
</style>
"""
js = """
<script id="tth-grid-cell-inline-integrity-script-2027">
(function(){
 'use strict';
 if(window.__TTH_GRID_CELL_INLINE_INTEGRITY_2027__)return;
 window.__TTH_GRID_CELL_INLINE_INTEGRITY_2027__=true;
 const root=document.getElementById('main');
 if(!root)return;
 const cells='#main table.tth-card>tbody>tr>td, #main table.tth-card>tbody>tr>th';
 function repair(){
  let changed=0;
  for(const cell of document.querySelectorAll(cells)){
   // Bảng, biểu mẫu và details lồng nhau có bố cục riêng: không di chuyển.
   if(cell.querySelector('details,table,.tbl'))continue;
   const nodes=Array.from(cell.childNodes);
   let value=Array.from(cell.children).find(x=>x.classList.contains('tth-grid-value'));
   if(value && nodes.length===1 && nodes[0]===value)continue;
   if(!value){
    value=document.createElement('span');
    value.className='tth-grid-value';
   }
   for(const node of nodes){if(node!==value)value.appendChild(node)}
   if(value.parentNode!==cell)cell.appendChild(value);
   changed++;
  }
  return changed;
 }
 let queued=false;
 function schedule(){
  if(queued)return;queued=true;
  requestAnimationFrame(function(){queued=false;repair()});
 }
 if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',schedule,{once:true});
 }else schedule();
 // Phần mềm còn dựng bảng/cập nhật data-csdl sau lần tải đầu tiên.
 // Dùng appendChild để giữ nguyên node, sự kiện liên kết và trạng thái.
 const observer=new MutationObserver(function(records){
  if(records.some(function(m){
   if(m.type==='attributes')return m.target.tagName==='TABLE';
   return m.addedNodes.length>0 || m.removedNodes.length>0;
  }))schedule();
 });
 observer.observe(root,{subtree:true,childList:true,attributes:true,attributeFilter:['class']});
 window.addEventListener('resize',schedule,{passive:true});
 document.addEventListener('click',function(e){
  if(e.target.closest('.tab,summary,[data-view],button'))schedule();
 },true);
})();
</script>
"""
s = s.replace("</head>", style + "</head>", 1)
s = s.replace("</body>", js + "</body>", 1)
assert s.count('id="tth-grid-cell-inline-integrity-2027"') == 1
assert s.count('id="tth-grid-cell-inline-integrity-script-2027"') == 1
assert "window.__TTH_GRID_CELL_INLINE_INTEGRITY_2027__=true" in s
page.write_text(s, "utf-8")
print("PASS inline grid cell repair: card labels and all source content kept together")
