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
 if directory=="healthcare-app":
  onclick_pages=[]
  all_button_samples=[]
  placeholder_links=[]
  for pname,pdoc in pages.items():
   for m2 in re.finditer(r'<button\b[^>]*>[\s\S]*?<\/button>',pdoc,re.I):
    frag=re.sub(r'<[^>]*>',' ',m2.group(0))
    label=html.unescape(' '.join(frag.split()))[:72]
    attrs=m2.group(0).split('>')[0][:170]
    all_button_samples.append((pname,label,attrs))
   for m2 in re.finditer(r'<a\b[^>]*\bhref=["\']#["\'][^>]*>[\s\S]*?<\/a>',pdoc,re.I):
    label=html.unescape(' '.join(re.sub(r'<[^>]*>',' ',m2.group(0)).split()))[:72]
    placeholder_links.append((pname,label))
  print('APP_BUTTON_MAP',all_button_samples[:120])
  print('APP_PLACEHOLDER_LINKS',len(placeholder_links),placeholder_links)
 print("AUDIT",directory,"COUNTS",dict(counts),"BROKEN_LINKS",missing.most_common(18))
 for name,length,bcount,excerpts in suspicious:
  print("APP_SURFACE",directory,name,"len",length,"buttons",bcount)
  for key,ex in excerpts[:18]:print("  TERM",key,ex[:850])
 print("MAIN_FORM_ELEMENTS",directory,forms[:25])
 if directory=="healthcare-app":
  # Report action coverage separately from page navigation. A button is not
  # considered functional merely because the containing screen opens.
  groups=collections.Counter();items=[]
  for pname,pdoc in pages.items():
   for mm in re.finditer(r'<button\\b[^>]*>[\\s\\S]*?<\\/button>',pdoc,re.I):
    frag=mm.group(0);tag=frag.split('>',1)[0]
    label=html.unescape(' '.join(re.sub(r'<[^>]*>',' ',frag).split()))[:100]
    if re.search(r'onclick\\s*=|data-(?:href|route)\\s*=',tag,re.I):kind="explicit_handler"
    elif re.search(r'type\\s*=\\s*["\\']submit["\\']',tag,re.I):kind="form_submit_requires_browser_test"
    elif re.search(r'\\b(disabled|aria-disabled)\\b',tag,re.I):kind="disabled"
    elif re.search(r'\\b(filter|loc|ngày|giờ|chọn|bật|tắt|đổi|xem thêm|tiếp tục)\\b',label,re.I):kind="local_state_candidate_unverified"
    else:kind="unverified_no_inline_handler"
    groups[kind]+=1;items.append({"page":pname,"label":label,"class":kind})
  placeholders=[]
  for pname,pdoc in pages.items():
   for mm in re.finditer(r'<a\\b[^>]*\\bhref=["\\']#["\\'][^>]*>[\\s\\S]*?<\\/a>',pdoc,re.I):
    frag=mm.group(0);label=html.unescape(' '.join(re.sub(r'<[^>]*>',' ',frag).split()))[:100]
    placeholders.append({"page":pname,"label":label,"class":"unresolved_not_a_valid_navigation"})
  report={"screens":len(pages),"buttons":len(items),"button_classifications":dict(groups),
          "placeholders":len(placeholders),"button_inventory":items,"placeholder_inventory":placeholders,
          "interpretation":"Static inventory only: no claim of button interaction or HIS/CRM integration"}
  dest=root.parent/"artifacts"/"app-action-inventory.json"
  dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
  print("APP_ACTION_COVERAGE",json.dumps({"screens":len(pages),"buttons":len(items),
   "button_classes":dict(groups),"unresolved_links":len(placeholders),"artifact":str(dest)},ensure_ascii=False))

