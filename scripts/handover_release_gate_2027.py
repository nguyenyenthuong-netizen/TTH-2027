#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gate for the stakeholder handover hub: five links, route integrity, honest statuses.
This checks a shareable review package, not live HIS/CRM/API functionality.
"""
import json,os,re,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
catalog=root/"index.html"
handover=root/"bo-ho-so"/"index.html"
expected={
 "https://tth-khung-marketing-14112026.vercel.app/",
 "https://tth-marketing-2027-trinh-chieu.vercel.app/",
 "https://tth-crm-da-kenh.vercel.app/",
 "https://tth-healthcare-website.vercel.app/",
 "https://tth-healthcare-app.vercel.app/",
}
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=="a":self.links.append(dict(attrs).get("href",""))
def links(p):
 assert p.is_file(),f"Missing {p}"
 parser=Links();parser.feed(p.read_text("utf-8"));return parser.links
cl=links(catalog);hl=links(handover)
catalog_urls=[u for u in cl if u.startswith("https://")]
handover_urls=[u for u in hl if u.startswith("https://")]
assert len(expected)==5
catalog_expected=expected|{"https://tth-duc-tho-ke-hoach-marketing-2027.vercel.app/"}
assert len(catalog_urls)==len(catalog_expected) and set(catalog_urls)==catalog_expected,"Catalog destinations mismatch"
assert len(handover_urls)==len(expected) and set(handover_urls)==expected,"Handover destinations mismatch"
assert "kien-truc-thuong-hieu/" in cl and (root/"kien-truc-thuong-hieu"/"index.html").is_file(),"Missing architecture route"
assert "bo-ho-so/" in cl,"Catalog must expose stakeholder handover"
assert all("quan-tri-marketing" not in u for u in cl+hl),"GitHub catalog/handover may not list Marketing software"
assert all("tth-marketing-2027-slide.vercel.app" not in u for u in cl+hl),"Duplicate presentation must not be listed"
assert "Phương án vận hành Marketing toàn hệ thống TTH Group 2027" in handover.read_text("utf-8"),"Official presentation title does not match catalog"
assert "../" in hl,"Handover must link back to catalog"
assert (root/"khung-marketing"/"nghiem-thu"/"index.html").is_file(),"Missing pre-issuance matrix"
assert (root/"khung-marketing"/"doi-chieu-quy-trinh"/"index.html").is_file(),"Missing process crosswalk"
for u in hl:
 if not u.startswith("https://") and u not in ("../",):
  local=(handover.parent/u).resolve()
  assert local.is_file() or (local.is_dir() and (local/"index.html").is_file()),f"Broken local handover link: {u}"
content=handover.read_text("utf-8")
for term in ("Ban Tổng Giám đốc","Phòng Nhân lực","Phòng Công nghệ","Contact Center","không xác nhận","60 luồng","568 đầu ra","chưa chứng minh","HIS","nghiệm thu"):
 assert term.lower() in content.lower(),f"Handover missing governance statement: {term}"
assert "đã liên thông dữ liệu thật" not in content.lower()
report={
 "document":"Ho so phoi hop va doi soat TTH 2027",
 "date":"2026-11-20",
 "revision_sha":os.environ.get("GITHUB_SHA","local"),
 "interfaces":len(catalog_expected)+1,
 "handover_vercel_links":len(expected),
 "catalog_consistent":True,
 "supporting_pages_present":True,
 "integration_claimed":False,
 "scope":"Kiểm tra trang danh mục, đường dẫn và hồ sơ; không xác nhận tích hợp HIS, CRM hoặc ban hành quy trình."
}
(handover.parent/"ket-qua-kiem-tra.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
print("PASS_HANDOVER_GATE",json.dumps(report,ensure_ascii=False))
