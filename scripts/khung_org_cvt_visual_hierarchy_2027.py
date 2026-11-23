#!/usr/bin/env python3
from pathlib import Path
import sys
p=Path(sys.argv[1])/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
assert 'id="tth-org-cvt-ownership-map-2027"' not in s
def change(old,new):
 global s
 assert s.count(old)==1,(old[:95],s.count(old))
 s=s.replace(old,new,1)
change('<div class="org-cols"><div class="org-left"><div class="col">',
       '<div class="org-cols mkt-cvt-map"><div class="org-left mkt-cvt-branch" role="group" aria-label="Chuyên viên trưởng quản lý Tổ Nội dung và Sáng tạo cùng mạng lưới bệnh viện">'+
       '<div class="mkt-cvt-branch-label"><b>01 TỔ CHUYÊN MÔN + MARKETING BỆNH VIỆN</b><span>Quản lý chuyên môn Tổ Nội dung và Sáng tạo; quản lý trực tiếp Trưởng nhóm Marketing bệnh viện thuộc cả hai nhóm thương hiệu</span></div><div class="col">')
change('<div class="org-right"><div class="mkt-org-cvt-2">',
       '<div class="org-right mkt-cvt-branch" role="group" aria-label="Chuyên viên trưởng quản lý hai tổ Truyền thông Thương hiệu và Tăng trưởng số">'+
       '<div class="mkt-cvt-branch-label"><b>02 TỔ CHUYÊN MÔN TẠI TỔNG CÔNG TY</b><span>Quản lý Tổ Truyền thông và Thương hiệu, Tổ Tăng trưởng số; phối hợp kiểm chuẩn nghiệp vụ cơ sở, không tạo cấp quản lý nhân sự thứ hai</span></div><div class="mkt-org-cvt-2">')
change('<small>Quản lý trực tiếp Trưởng nhóm Marketing bệnh viện · cả 2 nhóm</small>',
       '<small>Quản trị Tổ Nội dung và Sáng tạo (10) · quản lý trực tiếp Trưởng nhóm Marketing bệnh viện cả hai nhóm</small>')
change('<small>Quản lý 02 tổ: Truyền thông và Thương hiệu · Tăng trưởng số</small>',
       '<small>Quản trị Tổ Truyền thông và Thương hiệu (04) và Tổ Tăng trưởng số (05)</small>')
change('<div class="col-b">\n<details class="grp" open=""><summary>Tổ Nội dung và Sáng tạo (10)',
       '<div class="col-b"><div class="mkt-cvt-connector" aria-label="Một tổ trực thuộc Chuyên viên trưởng Nội dung và cơ sở"><span>↓</span><strong>01 tổ trực thuộc</strong></div>\n<details class="grp" open=""><summary>Tổ Nội dung và Sáng tạo (10)')
# Target each team's heading rather than source prose that is normalized at build time.
def change_team_small(prefix,description):
 global s
 assert s.count(prefix)==1,(prefix,s.count(prefix))
 a=s.index(prefix)+len(prefix)
 b=s.index("</small>",a)
 assert b>a
 s=s[:a]+description+s[b:]
change_team_small('<summary>Tổ Nội dung và Sáng tạo (10)<small>',
                  'Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở quản trị chuyên môn toàn tổ; Tổ trưởng kiêm nhiệm chỉ điều phối nhóm 1 trong phạm vi được giao')
change('<div class="org-right-teams"><div class="col">',
       '<div class="mkt-cvt-connector" aria-label="Hai tổ trực thuộc Chuyên viên trưởng Truyền thông và số"><span>↓</span><strong>02 tổ trực thuộc</strong></div><div class="org-right-teams"><div class="col">')
change_team_small('Tổ Tăng trưởng số (05)<small>',
                  'Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số quản lý; Tổ trưởng là Quản lý sản phẩm số (kiêm nhiệm)')
css="""
<style id="tth-org-cvt-ownership-map-2027">
#v-org .org-cols.mkt-cvt-map{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:18px!important;align-items:stretch!important;padding-top:24px!important;border-top:2px solid #0837a1}
#v-org .org-cols.mkt-cvt-map>.mkt-cvt-branch{display:flex!important;flex-direction:column!important;align-items:stretch!important;gap:12px!important;grid-column:auto!important;grid-row:auto!important;position:relative!important;min-width:0!important;width:auto!important;margin:0!important;padding:14px!important;border:1.5px solid #b9cde9!important;border-radius:14px!important;background:#f7faff!important}
#v-org .mkt-cvt-branch:before{content:"";position:absolute;top:-24px;left:50%;width:2px;height:22px;background:#0837a1;transform:translateX(-50%);pointer-events:none}
#v-org .mkt-cvt-branch-label{display:flex;flex-direction:column;gap:5px;margin:0 0 3px;color:#193967;line-height:1.48}
#v-org .mkt-cvt-branch-label b{font-size:15px;font-weight:800;color:#0837a1}
#v-org .mkt-cvt-branch-label span{font-size:13px;color:#415b7d;line-height:1.55}
#v-org .mkt-cvt-branch .pos-lead[data-jd="cvt"],#v-org .mkt-cvt-branch .pos-lead[data-jd="cvt-2"]{background:#0837a1!important;color:#fff!important;border-left:4px solid #ed3237!important;border-radius:10px!important;padding:15px!important;text-align:left!important;min-height:0!important;width:100%!important;line-height:1.48!important}
#v-org .mkt-cvt-branch .pos-lead[data-jd="cvt"]>small,#v-org .mkt-cvt-branch .pos-lead[data-jd="cvt-2"]>small{display:block!important;color:#f2f6ff!important;font-size:13px!important;opacity:1!important;margin-top:7px!important;line-height:1.5!important}
#v-org .mkt-cvt-branch .col,#v-org .mkt-cvt-branch .mkt-org-cvt-2,#v-org .mkt-cvt-branch .org-right-teams{min-width:0!important;max-width:100%!important;width:100%!important;margin:0!important;grid-column:auto!important;grid-row:auto!important}
#v-org .mkt-cvt-connector{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;text-align:center;font-size:12px;color:#0837a1;font-weight:750;line-height:1.35}
#v-org .mkt-cvt-connector span{font-size:24px;line-height:1}
#v-org .mkt-cvt-connector strong{padding:5px 10px;background:#fff;border:1px solid #b9cde9;border-radius:7px;color:#164782;font-size:12px}
#v-org .org-right>.org-right-teams{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:12px!important}
#v-org .mkt-cvt-branch .grp summary,#v-org .mkt-cvt-branch .org-right-teams .col-h{white-space:normal!important;overflow-wrap:break-word!important;line-height:1.5!important}
#v-org .mkt-cvt-branch .grp small,#v-org .mkt-cvt-branch .org-right-teams .col-h small{font-size:12.5px!important;line-height:1.55!important}
#v-org .mkt-org-local-row{margin-top:20px!important}
#v-org .mkt-org-local-heading{border-left:4px solid #0837a1!important}
@media(max-width:1100px){#v-org .org-cols.mkt-cvt-map{grid-template-columns:minmax(0,1fr)!important;gap:20px!important}#v-org .org-cols.mkt-cvt-map>.mkt-cvt-branch{padding:12px!important}}
@media(max-width:650px){#v-org .org-cols.mkt-cvt-map>.mkt-cvt-branch{padding:10px!important}#v-org .mkt-cvt-branch-label b{font-size:14px}}
</style>
"""
assert s.count("</head>")==1
s=s.replace("</head>",css+"</head>",1)
assert s.count('class="mkt-cvt-connector"')==2
p.write_text(s,"utf-8")
print("PASS: two visibly distinct CVT branches, 1+2 subordinate teams and one hospital-management line")
