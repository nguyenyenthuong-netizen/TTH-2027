#!/usr/bin/env python3
"""Final non-destructive presentation guard. Runs AFTER latest overrides are copied.
No changes to business content, approval rights or operational rules.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
targets = {
    "khung-marketing": """
/* 2027 two-branch organization tree: one Chief plus their team(s) per column.
   Hospital Marketing is outside the two-column tree in a full-width band. */
#v-org .org-cols{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr)!important;grid-template-rows:auto!important;grid-auto-flow:row!important;align-items:start!important;gap:16px!important}
#v-org .org-cols>.org-left,#v-org .org-cols>.org-right{display:flex!important;flex-direction:column!important;gap:12px!important;grid-column:auto!important;grid-row:auto!important;min-width:0!important;width:auto!important}
#v-org .org-right-teams{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:12px!important}
#v-org .org-cols .col,#v-org .org-cols .mkt-org-cvt-2{min-width:0!important;width:100%!important;grid-column:auto!important;grid-row:auto!important;align-self:start!important}
#v-org .org-cols .col-h{display:block!important;box-sizing:border-box!important;height:auto!important;min-height:0!important;white-space:normal!important;overflow-wrap:break-word!important;padding:14px 16px!important}
#v-org .mkt-org-local-row{width:100%!important;min-width:0!important;clear:both}
#v-org .mkt-org-local-row .hosp-grid{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))!important}
@media(max-width:1100px){#v-org .org-cols{grid-template-columns:minmax(0,1fr)!important}}
#v-org .col-b,#v-org .grp,#v-org .hosp,#v-org .pos{min-width:0!important}
#v-org .pos-n{overflow-wrap:break-word!important;word-break:normal!important}
/* Balanced data table columns: long descriptions receive real room.
   Do not apply to specialized matrices with their own colgroup widths. */
#main .tbl table{table-layout:auto!important}
#main .tbl table th,#main .tbl table td{min-width:85px}
#main .tbl table th:first-child,#main .tbl table td:first-child{min-width:155px}
#main .tbl{max-width:100%;overflow-x:auto!important}
/* Legible Vietnamese text, while retaining natural widths. */
#main{font-family:Arial,"Segoe UI",Tahoma,sans-serif;font-size:16px}
#main table.t,#main .tbl table{font-size:15px!important;line-height:1.5!important}
#main .pos,#main .jd-body,#main .grp{font-size:15px}
#side .tab{font-size:14px}
/* Wide data tables are scrollable, never compressed into tiny characters. */
#main .tbl,#main .rel-scroll{overflow-x:auto!important;max-width:100%!important;scrollbar-width:thin}
/* Khung: permit wide tables to scroll instead of clipping their cells. */
html,body{max-width:100%;overflow-x:hidden}
main,section,article,.view,.card,.doc-sec{min-width:0}
table{max-width:100%}
table th,table td{overflow-wrap:anywhere;word-break:normal;vertical-align:top}
img,svg,video,iframe{max-width:100%}
:where(button,a,input,select,textarea):focus-visible{outline:2px solid #0837A1;outline-offset:2px}
""",
    "trinh-chieu-marketing": """
/* Navigation uses a dedicated side gutter, not content overlay. */
@media screen and (min-width:850px){
 #viewport{left:64px!important;width:calc(100vw - 64px)!important;right:0!important}
 .tth-floating-arrows{left:0!important;right:auto!important;bottom:12px!important;width:58px!important;display:flex!important;flex-direction:column!important;align-items:center!important;gap:9px!important}
 .tth-floating-arrow{flex:0 0 42px!important}
}
@media screen and (max-width:849px){
 #viewport{bottom:64px!important;height:calc(100dvh - 64px)!important}
 .tth-floating-arrows{right:10px!important;bottom:8px!important}
}
.slide .bodycopy{font-family:Arial,"Segoe UI",Tahoma,sans-serif}
.slide .head h2{font-size:32px!important}
.slide .head p{font-size:16px!important}
/* Slide: protect titles and text from clipping; retain the native arrows. */
html,body{max-width:100%}
.slide{box-sizing:border-box}
.slide h1,.slide h2,.slide h3,.slide p,.slide li{overflow-wrap:break-word}
.slide img,.slide svg,.slide video{max-width:100%}
:where(button,a):focus-visible{outline:2px solid #0837A1;outline-offset:2px}
"""
}
font_guard = """
/* UTF-8 Vietnamese fallback without external font requests. */
html,body,button,input,select,textarea{
 font-family:Arial,"Segoe UI",Tahoma,"DejaVu Sans",sans-serif;
}
:where(h1,h2,h3,h4,h5,h6){text-rendering:optimizeLegibility}
:where(p,li,td,th,button,label){overflow-wrap:break-word}
"""
# Do not override icon-font classes: those glyphs may depend on their own font.
for page in ("crm-da-kenh","healthcare-app","healthcare-website"):
    p=root/page/"index.html"
    if not p.exists(): raise ValueError(f"Missing page: {page}")
    s=p.read_text("utf-8")
    if "</head>" not in s: raise ValueError(f"Missing head: {page}")
    s=s.replace("</head>",'<style id="tth-vietnamese-font-1911">'+font_guard+"</style></head>",1)
    p.write_text(s,"utf-8")
    print("PASS font:",page)
for page, css in targets.items():
    p = root / page / "index.html"
    s = p.read_text(encoding="utf-8")
    start = '<style id="tth-final-pages-guard">'
    if start in s:
        a=s.index(start)
        b=s.index("</style>",a)+len("</style>")
        s=s[:a]+s[b:]
    if "</head>" not in s:
        raise ValueError(f"{page}: missing head tag")
    s=s.replace("</head>",start+font_guard+css+"</style></head>",1)
    if page == "khung-marketing":
        for term in ("Chuyên viên trưởng Nội dung", "KB-DV12", "tth-org-layout-rebuild-2027", "mkt-org-local-row", "mkt-org-line-to-local", "Tuyến quản lý trực tiếp", "tth-org-skills-controls-1911", "function buildOrgShortDetails()", "Chưa chỉ định cố định; Trưởng phòng Marketing phân công"):
            if term not in s:
                raise ValueError(f"{page}: critical baseline not found: {term}")
    else:
        if s.count('<section class="slide') != 27:
            raise ValueError("Slide count changed; expected 27")
    p.write_text(s,encoding="utf-8")
    print(f"PASS final QA: {page}, {len(s)} chars")
