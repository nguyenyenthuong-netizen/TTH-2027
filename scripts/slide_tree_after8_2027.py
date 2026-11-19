#!/usr/bin/env python3
"""Insert a 2027 Marketing organizational-tree slide after page 8.

Run after all source/framework validations (which still inspect the canonical
27-slide source). The published deck contains 28 slides with proper navigation
and footer numbering. Existing data-index attributes and selectors are NOT
renumbered so historical page-specific layout rules remain correct.
"""
from pathlib import Path
import re
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
path=root/"trinh-chieu-marketing"/"index.html"
s=path.read_text("utf-8")
if s.count('<section class="slide')!=27:
    raise SystemExit("Expected canonical 27 slides before inserting tree")
if "tth-organization-tree-after-8" in s:
    raise SystemExit("Tree slide already inserted")
m=re.search(r'<section class="slide" data-index="7">[\s\S]*?</section>',s)
if not m:
    raise SystemExit("Existing slide 8 not found")
old=m.group(0)
logo=re.search(r'<img\b[^>]*class="logo-head"[^>]*>',old)
if not logo:
    raise SystemExit("Official TTH logo in slide 8 missing")
official_logo=logo.group(0)
# Match the original head/footer structure, not the original document's
# experimental prototype navigation controls.
page=(
'<section class="slide tth-organization-tree-after-8" data-index="org-tree-after8">'
'<header class="head"><div class="kicker">SƠ ĐỒ TỔ CHỨC · MARKETING 2027</div>'
'<h2>Cơ cấu bộ máy Marketing toàn hệ thống</h2>'
'<p>Hai tuyến Chuyên viên trưởng · Ba tổ chuyên môn tại Tổng công ty · Một tuyến quản lý Marketing cơ sở</p>'
+official_logo+
'</header>'
'<main class="content tth-org-tree-body">'
' <div class="tth-tree-root">'
'   <strong>TRƯỞNG PHÒNG MARKETING TỔNG CÔNG TY</strong>'
'   <span>Điều hành toàn phòng · Quản lý hai Chuyên viên trưởng · Phê duyệt theo phân cấp</span>'
' </div>'
' <div class="tth-tree-junction"><i></i></div>'
' <div class="tth-tree-branches">'
'   <div class="tth-tree-branch tth-tree-left">'
'     <div class="tth-tree-chief">'
'       <strong>CHUYÊN VIÊN TRƯỞNG</strong>'
'       <b>Nội dung – Sáng tạo và Marketing cơ sở</b>'
'       <span>Quản lý trực tiếp Tổ Nội dung và Sáng tạo cùng các Trưởng nhóm Marketing cơ sở</span>'
'     </div>'
'     <div class="tth-tree-children">'
'       <div class="tth-tree-node">'
'         <b>TỔ NỘI DUNG VÀ SÁNG TẠO</b>'
'         <em>10 suất tại Tổng công ty</em>'
'         <span>Biên tập · Nội dung · Thiết kế · Media</span>'
'         <small>Tổ trưởng kiêm nhiệm theo phân công</small>'
'       </div>'
'       <div class="tth-tree-node tth-tree-local">'
'         <b>MARKETING CƠ SỞ</b>'
'         <em>14 suất tại bệnh viện</em>'
'         <span>Trưởng nhóm Marketing cơ sở của cả hai nhóm thương hiệu</span>'
'         <small>Tại bệnh viện chuyên khoa nhóm 2: Trưởng nhóm kiêm nhiệm truyền thông</small>'
'       </div>'
'     </div>'
'   </div>'
'   <div class="tth-tree-branch tth-tree-right">'
'     <div class="tth-tree-chief">'
'       <strong>CHUYÊN VIÊN TRƯỞNG</strong>'
'       <b>Truyền thông – Thương hiệu và Tăng trưởng số</b>'
'       <span>Quản lý hai tổ tại Tổng công ty; hướng dẫn nghiệp vụ cơ sở, không quản lý trực tiếp nhân sự cơ sở</span>'
'     </div>'
'     <div class="tth-tree-children">'
'       <div class="tth-tree-node">'
'         <b>TỔ TRUYỀN THÔNG VÀ THƯƠNG HIỆU</b>'
'         <em>04 suất tại Tổng công ty</em>'
'         <span>Quản lý thương hiệu · Truyền thông · PR · OOH</span>'
'         <small>Tổ trưởng kiêm nhiệm: Quản lý thương hiệu nhóm 2</small>'
'       </div>'
'       <div class="tth-tree-node">'
'         <b>TỔ TĂNG TRƯỞNG SỐ</b>'
'         <em>05 suất tại Tổng công ty</em>'
'         <span>Quảng cáo · Kênh số · Quản lý sản phẩm số</span>'
'         <small>Tổ trưởng kiêm nhiệm: Quản lý sản phẩm số</small>'
'       </div>'
'     </div>'
'   </div>'
' </div>'
' <div class="tth-tree-note">'
'   <b>36 suất = 22 Tổng công ty + 14 bệnh viện</b>'
'   <span>Hai nhóm thương hiệu là phạm vi phục vụ, không phải hai tuyến cấp trên. Hướng dẫn chuyên môn không tự tạo quyền duyệt hoặc quyền quản lý trực tiếp.</span>'
' </div>'
'</main>'
'<footer><span>TTH GROUP · MARKETING 2027</span><span>KHUNG CƠ CẤU VÀ VẬN HÀNH</span><b>9</b></footer>'
'</section>'
)
css=r"""<style id="tth-org-tree-slide-after8-style">
/* 1280x720 slide canvas. Clear role hierarchy with large legible labels. */
.slide.tth-organization-tree-after-8 .head{padding-top:17px!important}
.slide.tth-organization-tree-after-8 .head h2{
 font-size:31px!important;line-height:1.16!important;
 max-width:960px!important;letter-spacing:-.012em!important
}
.slide.tth-organization-tree-after-8 .head p{
 font-size:14px!important;color:#3c5474!important;line-height:1.4!important;
 max-width:960px!important
}
.slide.tth-organization-tree-after-8 .tth-org-tree-body{
 position:absolute!important;top:154px!important;left:36px!important;
 right:36px!important;bottom:40px!important;overflow:hidden!important;
 display:flex!important;flex-direction:column!important;gap:0!important;
 padding:7px 0 0!important;box-sizing:border-box!important
}
.tth-org-tree-body *{box-sizing:border-box}
.tth-tree-root{
 display:flex;flex-direction:column;align-items:center;justify-content:center;
 gap:4px;flex:0 0 68px;align-self:center;
 width:64%;min-width:0;background:#0837A1;color:#fff;
 border-radius:13px;padding:8px 16px;border-bottom:4px solid #ED3237;
 text-align:center
}
.tth-tree-root strong{font-size:19px;line-height:1.22;font-weight:800}
.tth-tree-root span{font-size:13px;line-height:1.3;color:#fff}
.tth-tree-junction{
 position:relative;flex:0 0 24px;width:50%;
 align-self:center;border-bottom:3px solid #92ADD2
}
.tth-tree-junction:before{
 content:"";position:absolute;left:50%;top:0;height:24px;
 border-left:3px solid #92ADD2
}
.tth-tree-junction:after{
 content:"";position:absolute;left:0;bottom:-9px;height:9px;
 border-left:3px solid #92ADD2
}
.tth-tree-junction i{
 position:absolute;right:0;bottom:-9px;height:9px;
 border-right:3px solid #92ADD2
}
.tth-tree-branches{
 display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
 flex:1 1 auto;min-height:0;gap:17px;padding-top:10px
}
.tth-tree-branch{
 display:flex;flex-direction:column;min-width:0;min-height:0;gap:12px
}
.tth-tree-chief{
 display:flex;flex-direction:column;gap:5px;
 border:1px solid #9AB9E0;border-left:7px solid #0837A1;
 border-radius:12px;background:#EAF2FD;
 min-height:110px;padding:12px 15px
}
.tth-tree-right .tth-tree-chief{border-left-color:#ED3237}
.tth-tree-chief strong{
 color:#0837A1;font-size:13px;font-weight:800;letter-spacing:.065em
}
.tth-tree-chief b{
 color:#092F6F;font-size:19px;line-height:1.18;font-weight:800
}
.tth-tree-chief span{
 color:#345273;font-size:13px;line-height:1.32
}
.tth-tree-children{
 display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
 gap:11px;flex:1 1 auto;min-height:0;
 border-top:3px solid #A5BBDD;padding-top:12px;
 position:relative
}
.tth-tree-children:before{
 content:"";position:absolute;top:0;left:50%;height:12px;
 border-left:3px solid #A5BBDD
}
.tth-tree-node{
 display:flex;flex-direction:column;gap:6px;min-height:0;
 border:1px solid #C7D9F0;border-top:5px solid #0837A1;
 border-radius:10px;background:#fff;padding:14px 12px 12px;
 box-shadow:0 3px 10px rgba(8,55,161,.05)
}
.tth-tree-right .tth-tree-node{border-top-color:#ED3237}
.tth-tree-node b{
 color:#0A347C;font-size:16px;line-height:1.25;font-weight:800
}
.tth-tree-node em{
 color:#B62935;font-size:13px;line-height:1.3;
 font-style:normal;font-weight:800
}
.tth-tree-node span{
 color:#294869;font-size:14px;line-height:1.35
}
.tth-tree-node small{
 color:#3C5778;font-size:12.5px;line-height:1.35;
 margin-top:auto
}
.tth-tree-local{background:#F8FBFF}
.tth-tree-note{
 flex:0 0 63px;display:flex;gap:14px;align-items:center;
 margin-top:11px;padding:8px 14px;
 border-radius:10px;border:1px solid #BFD0EA;background:#F2F7FD;
 color:#284666
}
.tth-tree-note b{
 color:#0837A1;font-size:15px;line-height:1.3;
 min-width:285px
}
.tth-tree-note span{font-size:13px;line-height:1.34}
</style>"""
# Preserve legacy CSS data-index selectors: later slides keep their original
# index, but the actual sequence order and footers are now 1..28.
s=s[:m.end()]+page+s[m.end():]
s=s.replace("</head>",css+"</head>",1)
sections=list(re.finditer(r'<section class="slide\b[\s\S]*?</section>',s))
if len(sections)!=28:
    raise SystemExit("Expected 28 slide sections after insertion; got "+str(len(sections)))
# footer is the audience-visible page number; only alter its own <b> token
# so content/data-index-specific styles are never re-keyed.
parts=[]
last=0
for number,match in enumerate(sections,1):
    parts.append(s[last:match.start()])
    piece=match.group(0)
    piece,count=re.subn(
       r'(<footer>[\s\S]*?<b>)\s*\d+\s*(</b>[\s\S]*?</footer>)',
       lambda z:z.group(1)+str(number)+z.group(2),
       piece,count=1
    )
    if count!=1:
        raise SystemExit("Footer number missing on slide "+str(number))
    parts.append(piece)
    last=match.end()
parts.append(s[last:])
s="".join(parts)
s=s.replace("Danh sách 27 slide","Danh sách 28 slide")
s=s.replace("Danh mục 27 slide","Danh mục 28 slide")
s=s.replace("27 trang trình chiếu","28 trang trình chiếu")
if s.count('<section class="slide')!=28:
    raise SystemExit("28-slide structural guard failed")
# Match exact literal opening tags. Dynamic templates can contain other
# <section class="slide-like"> tags; the three relevant slide tags are unique.
pos8=s.find('<section class="slide" data-index="7">')
pos_tree=s.find('<section class="slide tth-organization-tree-after-8" data-index="org-tree-after8">')
pos9=s.find('<section class="slide" data-index="8">')
if not (0<=pos8<pos_tree<pos9):
    raise SystemExit("Tree slide must appear after the actual slide 8 and before slide 9")
for title in (
    "Nội dung – Sáng tạo và Marketing cơ sở",
    "Truyền thông – Thương hiệu và Tăng trưởng số",
    "TỔ NỘI DUNG VÀ SÁNG TẠO",
    "TỔ TRUYỀN THÔNG VÀ THƯƠNG HIỆU",
    "TỔ TĂNG TRƯỞNG SỐ",
    "MARKETING CƠ SỞ",
    "36 suất = 22 Tổng công ty + 14 bệnh viện",
):
    if title not in s:
        raise SystemExit("Organization title missing: "+title)
path.write_text(s,"utf-8")
print("PASS 28 SLIDES: organizational tree inserted after slide 8; two chiefs, three teams, local direct line and footers 1..28")
