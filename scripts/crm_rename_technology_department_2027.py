#!/usr/bin/env python3
"""Apply the approved organization-unit name 'Phòng Công nghệ' to displayed CRM.
Preserve HIS, PBX, API and all business-flow relationships and links.
"""
from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
path=root/"crm-da-kenh"/"index.html"
html=path.read_text("utf-8")
if "Phòng Công nghệ" in html and not re.search(r'(?<![\w])CNTT(?![\w])',html):
 print("CRM_TECH_DEPARTMENT_OK already normalized")
 raise SystemExit(0)
pattern=re.compile(r"(?<![\w])CNTT(?![\w])",re.U)
matches=list(pattern.finditer(html))
if not matches:
 raise SystemExit("CRM_TECH_DEPARTMENT: no CNTT occurrences; inspect assembled source instead of silently passing")
print("CRM_TECH_DEPARTMENT_BEFORE",len(matches))
for m in matches[:15]:
 print("CRM_TECH_DEPARTMENT_CONTEXT",repr(html[max(0,m.start()-80):m.end()+100]))
# Avoid ambiguous concatenations around HIS in joint function and responsibility labels.
html=html.replace("Phòng CNTT","Phòng Công nghệ")
html=html.replace("CNTT / chủ quản HIS","Phòng Công nghệ / đầu mối HIS")
html=html.replace("CNTT/HIS","Phòng Công nghệ / HIS")
html=pattern.sub("Phòng Công nghệ",html)
if pattern.search(html):
 raise SystemExit("CRM_TECH_DEPARTMENT: untranslated CNTT remains")
if "Phòng Phòng Công nghệ" in html:
 raise SystemExit("CRM_TECH_DEPARTMENT: duplicated department prefix")
if not all(x in html for x in ("HIS","CRM","Call Center")):
 raise SystemExit("CRM_TECH_DEPARTMENT: critical system references disappeared")
path.write_text(html,"utf-8")
print("CRM_TECH_DEPARTMENT_OK",len(matches),"occurrences normalized; unit name=Phòng Công nghệ; HIS/CRM/Call Center retained")
