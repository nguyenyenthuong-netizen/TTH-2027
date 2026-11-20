#!/usr/bin/env python3
"""Audit navigation and assistant search surfaces from all original App/Website HTML pages.
Read-only diagnostics; never alter marketing framework or invent services.
"""
from pathlib import Path
import sys,re,json,collections,html
from html.parser import HTMLParser
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
for directory,script_id in (("healthcare-app","pageData"),("healthcare-website","pagesData")):
 raw=(root/directory/"index.html").read_text("utf8")
 m=re.search(r'<script\b[^>]*\bid=["\']'+script_id+r'["\'][^>]*>(.*?)</script>',raw,re.S|re.I)
 if not m:raise SystemExit("Missing catalog "+directory)
 pages=json.loads(m.group(1))
 missing=collections.Counter(); counts=collections.Counter(); suspicious=[]
 forms=[]
 for name,doc in pages.items():
  clean=re.sub(r'data:image/[^"\' ]+','[ASSET]',doc)
  links=re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)',clean,re.I)
  for href in links:
   key=href.split("?")[0].split("#")[0].split("/")[-1]
   if key.endswith(".html") and key not in pages:missing[key]+=1
  btns=re.findall(r'<button\b[^>]*>',clean,re.I)
  counts["pages"]+=1;counts["buttons"]+=len(btns);counts["links"]+=len(links)
  counts["buttons_without_inline_handler"]+=sum(not re.search(r'onclick|data-(?:href|route)|type=["\']submit',b,re.I) for b in btns)
  if name in ("Main.html","Tim_NhuCau.html","HoTro_TroLy.html","TimKiem.html","Web_TroLy.html","HoTro_ChatTuVan.html"):
   terms=("Tìm kiếm","Hỏi Trợ lý","Trợ lý","Tìm bác sĩ","search","assistant","Đau bụng","<input","<form")
   excerpts=[]
   for term in terms:
    found=[m.start() for m in list(re.finditer(re.escape(term),clean,re.I))[:4]]
    for p in found:
     ex=clean[max(0,p-350):p+560].replace("\n"," ")
     ex=re.sub(r'data:[^"\' ]{60,}',"[ASSET]",ex)
     excerpts.append((term,ex[:850]))
   suspicious.append((name,len(doc),len(btns),excerpts[:26]))
  if name=="Main.html":
   for q in re.findall(r'<(?:input|button|a|form)\b[^>]*>',clean,re.I):
    if re.search("search|trợ lý|tim|hỏi|q=|submit|placeholder",q,re.I):forms.append(q[:500])
 print("AUDIT",directory,"COUNTS",dict(counts),"BROKEN_LINKS",missing.most_common(18))
 for name,length,bcount,excerpts in suspicious:
  print("APP_SURFACE",directory,name,"len",length,"buttons",bcount)
  for key,ex in excerpts[:18]:print("  TERM",key,ex[:850])
 print("MAIN_FORM_ELEMENTS",directory,forms[:25])
