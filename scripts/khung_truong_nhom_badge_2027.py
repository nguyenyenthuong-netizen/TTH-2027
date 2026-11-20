#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tô nhãn vai trò Trưởng nhóm trong 05 ô sơ đồ Marketing bệnh viện.
Giữ nguyên tên chức danh, người thay và nội dung, sử dụng màu đỏ TTH #ED3237.
"""
from pathlib import Path
import re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
# CSS dùng cùng hệ nhãn lead màu đỏ chữ trắng với Tổ trưởng.
badge_css = """
<style id="tth-badge-truong-nhom-2027">
#v-org .hosp button.pos[data-jd="tn-a"] > .lead.tth-truong-nhom,
#v-org .hosp button.pos[data-jd="tn-b"] > .lead.tth-truong-nhom {
  display:inline-flex!important;align-self:center!important;align-items:center!important;
  justify-content:center!important;flex:0 1 auto!important;width:auto!important;
  max-width:100%!important;min-width:0!important;padding:3px 9px!important;
  min-height:22px!important;background:#ED3237!important;color:#FFFFFF!important;
  border:1px solid #ED3237!important;border-radius:6px!important;
  font-size:11px!important;font-weight:800!important;line-height:1.35!important;
  overflow-wrap:anywhere!important;white-space:normal!important;text-align:center!important;
  box-shadow:none!important;text-shadow:none!important;opacity:1!important;visibility:visible!important;
}
@media print {
  #v-org .hosp button.pos[data-jd="tn-a"] > .lead.tth-truong-nhom,
  #v-org .hosp button.pos[data-jd="tn-b"] > .lead.tth-truong-nhom {
    -webkit-print-color-adjust:exact!important; print-color-adjust:exact!important;
  }
}
</style>"""
if 'id="tth-badge-truong-nhom-2027"' in s:
    raise RuntimeError("Nhãn Trưởng nhóm đã có – không chèn trùng")
pat=re.compile(r'(<button\b(?=[^>]*\bclass="pos")(?=[^>]*\bdata-jd="(?:tn-a|tn-b)")[^>]*>\s*<span class="pos-n">[^<]+</span>)(?!\s*<span class="lead tth-truong-nhom">)')
s,n=pat.subn(r'\1<span class="lead tth-truong-nhom">Trưởng nhóm</span>',s)
assert n==5, "Cần đúng 5 ô Trưởng nhóm bệnh viện, thấy "+str(n)
assert s.count('<span class="lead tth-truong-nhom">Trưởng nhóm</span>')==5
assert s.count('data-view="org"')>=1
assert s.count('<button class="tab"')==12
s=s.replace('</head>',badge_css+'</head>',1)
p.write_text(s,'utf-8')
print("PASS TRUONG NHOM BADGES: 5/5 red #ED3237 white #FFFFFF; same 12 tabs")
