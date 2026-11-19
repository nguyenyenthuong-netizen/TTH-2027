#!/usr/bin/env python3
"""Inspect the deployed assembly (all five pages), without mutating business facts.
Emit concise audit records in GitHub Actions logs for verification.
"""
from pathlib import Path
import re,sys,html

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
pages={name:(root/name/"index.html").read_text("utf-8") for name in
 ("khung-marketing","trinh-chieu-marketing","crm-da-kenh","healthcare-app","healthcare-website")}
def txt(src):
 src=re.sub(r'src=["\']data:[^"\']+["\']',"",src,flags=re.I)
 src=re.sub(r"<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>"," ",src,flags=re.I)
 src=re.sub(r"<[^>]+>"," ",src)
 return html.unescape(re.sub(r"\s+"," ",src)).strip()
for name,src in pages.items():
 t=txt(src)
 print("AUDIT-PAGE",name,"length",len(src),"visible-text",len(t),"fontstyle",'tth-vietnamese-font' in src or 'tth-final-pages-guard' in src)
 for word in ("34 suất","36 suất","36 nhân sự","Contact Center","không thuộc Marketing","quản lý trực tiếp","Trưởng nhóm Marketing","kịch bản dịch vụ"):
  hits=[m.start() for m in re.finditer(re.escape(word),t,flags=re.I)]
  if hits: print("AUDIT-TERM",name,word,len(hits),repr(t[max(0,hits[0]-100):hits[0]+155]))
 if name=="crm-da-kenh":
  for term in ("Mở danh mục","Toàn màn hình","Xem lưu đồ","ĐỀ ÁN CRM ĐA KÊNH"):
   a=src.lower().find(term.lower())
   print("AUDIT-CRM-CONTROL",term, "pos",a,repr(src[max(0,a-420):a+360]) if a>=0 else "")
  print("AUDIT-CRM-FIX-INJECTED", "tth-crm-sidebar-cleanup-1911" in src)
print("AUDIT-CRITICAL-SLIDES",pages["trinh-chieu-marketing"].count('<section class="slide'))
print("AUDIT-DONE")
