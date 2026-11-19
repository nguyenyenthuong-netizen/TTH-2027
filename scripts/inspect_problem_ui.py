#!/usr/bin/env python3
"""One-time safe inspection: dump bounded markup around user-reported UI defects."""
from pathlib import Path
import re,sys,html
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
pages=["index.html","khung-marketing/index.html","crm-da-kenh/index.html","healthcare-app/index.html","healthcare-website/index.html","trinh-chieu-marketing/index.html"]
queries={
"index.html":["TTH HEALTHCARE","TTH GROUP","Danh mục 5","<main","<body","</body>"],
"khung-marketing/index.html":["Người thay chính:","bt-ac|","class=\"org-cols\"","mkt-bgd-link","mkt-bao-cao-quan-ly-02-cvt","<td>Chuyên viên trưởng</td>"],
"crm-da-kenh/index.html":["Mở danh mục","ux-sidebar-toggle","<aside","Toàn màn hình","Xem lưu đồ"],
"healthcare-app/index.html":["Tìm theo nhu cầu","Dịch vụ, kỹ thuật","Nguy cơ đột quỵ","toptools","<iframe","srcdoc=","Toàn màn hình"],
"healthcare-website/index.html":["Gói khám","Dịch vụ, kỹ thuật","Ưu đãi đang chạy","Đặt lịch khám","id=\"tools\"","<iframe","srcdoc=","Trang chủ"],
"trinh-chieu-marketing/index.html":["Chuyên viên trưởng","Contact Center","34 người","36 người","<section class=\"slide"]
}
for page in pages:
 s=(root/page).read_text("utf-8")
 print("INSPECT-PAGE",page,len(s),"head",s[:310].replace("\n"," "))
 for needle in queries[page]:
  matches=list(re.finditer(re.escape(needle),s,re.I))
  print("INSPECT-TERM",page,repr(needle),"hits",len(matches))
  for m in matches[:2]:
   a=max(0,m.start()-850);b=min(len(s),m.end()+1800)
   v=s[a:b].replace("\n"," ").replace("\t"," ")
   v=re.sub(r'(?:data:image|data:font)/[^"\'\\s]+','[embedded-asset]',v)
   print("INSPECT-HTML",page,needle,repr(v[:2750]))
 print("INSPECT-ENDPAGE",page)
