#!/usr/bin/env python3
"""Giữ nhất quán quy chuẩn tiêu đề always-on đã có trong Khung Marketing 2027.

Thực hiện cuối pipeline để không bị các lớp CSS cũ ghi đè. Không thay đổi
nội dung, màu nhận diện gốc, bố cục cơ cấu hoặc quyền nghiệp vụ.
"""
from pathlib import Path
import re, sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
marker='tth-title-always-on-unified-2027'
if marker in s:
    raise ValueError("Duplicate always-on title style: refusing second insertion")
if '<main id="main">' not in s:
    raise ValueError("Main marketing framework content missing")
if s.count('class="view-h"')!=12:
    raise ValueError("Expected 12 main section headers, found "+str(s.count('class="view-h"')))
for t in ('class="sec-h"','class="jd-head"','class="card-h"','class="col-h"','class="tbl"'):
    if t not in s: raise ValueError("Heading family missing: "+t)

# Inherit agreed glass standard from existing readability styling.
# Keep blue group headers blue; don't turn these into pale document headings.
css=r"""
<style id="tth-title-always-on-unified-2027">
/* Single title specification (same background tint and blur at every sticky/open state).
   Maintain the existing TTH glass colors, not a redesigned title treatment. */
#main{
 --tth-title-glass:rgba(245,249,255,.985);
 --tth-title-border:rgba(8,55,161,.20);
 --tth-title-shadow:0 5px 15px rgba(8,42,104,.105);
 --tth-title-blue-glass:rgba(8,55,161,.985);
 --tth-title-blur:blur(16px);
}
#main :is(.view-h,.doc-sec>.sec-h,.card-h,.jd-head,.pp-h,.std-head,.scope-card>h3,.mkt-one-line h3){
 background:var(--tth-title-glass)!important;
 border-color:var(--tth-title-border)!important;
 border-left:4px solid #0837A1!important;
 box-shadow:var(--tth-title-shadow)!important;
 -webkit-backdrop-filter:var(--tth-title-blur)!important;
 backdrop-filter:var(--tth-title-blur)!important;
 opacity:1!important;filter:none!important;
 box-sizing:border-box!important;
 height:auto!important;min-height:0!important;max-height:none!important;
 min-width:0!important;max-width:100%!important;
 white-space:normal!important;text-overflow:clip!important;
 overflow-wrap:break-word!important;word-break:normal!important;
 line-height:1.5!important;letter-spacing:normal!important;
}
#main :is(.view-h,.doc-sec>.sec-h,.card-h,.jd-head,.pp-h,.std-head) :is(h1,h2,h3,h4,h5,h6,b,span,p,small){
 max-height:none!important;white-space:normal!important;
 overflow-wrap:break-word!important;word-break:normal!important;
 text-overflow:clip!important;letter-spacing:normal!important;
 opacity:1!important;
}
#main :is(.view-h,.doc-sec>.sec-h,.card-h,.jd-head,.pp-h,.std-head){
 padding:11px 14px!important;margin-block-start:0!important;
}
#main .doc-sec>.sec-h{
 display:flex!important;align-items:flex-start!important;
 flex-wrap:wrap!important;gap:8px 12px!important;
}
#main .doc-sec>.sec-h .sec-num{
 flex:0 0 auto!important;align-self:flex-start!important;
 white-space:nowrap!important;line-height:1.5!important;
}
/* "Always on" is sticky only for title types that are already sticky in the
   application's interaction model. The rest remain in normal flow to avoid
   multiple overlapping title strips while reading 12 sections. */
#main .jd-d[open]>.jd-head,#main .pp-h{
 position:sticky!important;top:0!important;z-index:12!important;
 background:var(--tth-title-glass)!important;
 border-color:var(--tth-title-border)!important;
 box-shadow:var(--tth-title-shadow)!important;
 -webkit-backdrop-filter:var(--tth-title-blur)!important;
 backdrop-filter:var(--tth-title-blur)!important;
}
#main .jd-d:not([open])>.jd-head{
 position:relative!important;top:auto!important;z-index:auto!important;
}
#main .jd-head{display:flex!important;flex-wrap:wrap!important;align-items:flex-start!important;gap:10px 12px!important}
#main .jd-head .jd-tt{flex:1 1 300px!important;min-width:0!important}
#main .jd-head .jd-name{display:block!important;line-height:1.5!important}
#main .pp-h{display:flex!important;flex-wrap:wrap!important;align-items:flex-start!important;gap:10px!important}
#main .pp-h>div{min-width:0!important;flex:1 1 280px!important}
#main .pp-h button{flex:0 0 auto!important}
#main :is(.col-h,.mkt-org-cvt-2 .col-h){
 background:var(--tth-title-blue-glass)!important;color:#fff!important;
 -webkit-backdrop-filter:var(--tth-title-blur)!important;
 backdrop-filter:var(--tth-title-blur)!important;
 height:auto!important;min-height:0!important;max-height:none!important;
 white-space:normal!important;overflow-wrap:break-word!important;
 opacity:1!important;line-height:1.48!important;
}
/* All table heading rows adopt one light blue glass tint. No squeezed,
   clipped columns or changing darkness between standard and scroll tables. */
#main :is(.tbl,.std-table,.rel-scroll){
 max-width:100%!important;min-width:0!important;
 overflow-x:auto!important;-webkit-overflow-scrolling:touch;
}
#main :is(.tbl,.std-table,.rel-scroll) :is(thead th,.fhead th),
#main .fhead th{
 background:rgba(235,243,255,.985)!important;
 -webkit-backdrop-filter:var(--tth-title-blur)!important;
 backdrop-filter:var(--tth-title-blur)!important;
 color:#17365c!important;
 opacity:1!important;filter:none!important;
 white-space:normal!important;overflow-wrap:break-word!important;
 word-break:normal!important;height:auto!important;
 min-height:0!important;max-height:none!important;
 padding:10px 12px!important;line-height:1.5!important;
 text-overflow:clip!important;vertical-align:top!important;
}
#main :is(.tbl,.std-table) thead th{position:static!important;z-index:auto!important}
/* Keep text and its background on the same title line when zoomed.
   All headings wrap; never center vertically on a fixed-height card. */
#main :is(.view-h,.doc-sec,.card,.jd,.jd-head,.std-review,.pp-h){
 min-width:0!important;
}
@media(max-width:900px){
 #main .jd-d[open]>.jd-head,#main .pp-h{
  top:108px!important;max-width:100%!important;
 }
 #main :is(.view-h,.doc-sec>.sec-h,.card-h,.jd-head,.pp-h,.std-head){
  padding:10px 12px!important;
 }
 #main .jd-head .jd-tt{flex-basis:210px!important}
}
@media print{
 #main .jd-d[open]>.jd-head,#main .pp-h{
  position:static!important;top:auto!important;
 }
 #main :is(.view-h,.doc-sec>.sec-h,.card-h,.jd-head,.pp-h,.std-head){
  background:#fff!important;box-shadow:none!important;
  -webkit-backdrop-filter:none!important;backdrop-filter:none!important;
 }
}
</style>
"""
if "</head>" not in s: raise ValueError("Missing closing head")
s=s.replace("</head>",css+"</head>",1)
assert s.count(marker)==1
assert s.count('class="view-h"')==12
p.write_text(s,"utf-8")
print("TITLE-ALWAYS-ON-UNIFIED PASS; 12/12 main titles; glass 0.985; blur 16px; open JD and panels sticky; other headings normal flow")
