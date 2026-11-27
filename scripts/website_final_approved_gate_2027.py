#!/usr/bin/env python3
"""Install only two approved, byte-exact website HTML files; preserve every other generated route."""
from pathlib import Path
import hashlib, json, re, sys, zipfile, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright

root=Path(sys.argv[1]).resolve()
incoming=Path("release-final-2027")
specs=[
 ("TTH-FINAL-kien-truc.zip","kien-truc-thuong-hieu","9de4f2729e1aa64547f91b7429ff34fe2ddf652348d17b35b545b091cc7825f5","b8499f4f774baff7904a453a9d17f8c8106ebf4fc57724ade191fc5633793571",34527312),
 ("TTH-FINAL-healthcare.zip","healthcare-website","1753d06e704f7c58881feb5f46b0dc9c960147451bb9d573305b029c3fde7a0b","4326f4c79e1e66b4cc550221cc6ba39d2e2e7ddd7b6861797b3030800b3c9367",35406360)]
def digest(b):return hashlib.sha256(b).hexdigest()
out=Path("artifacts/tth-final-release");out.mkdir(parents=True,exist_ok=True)
report={"files":[],"cases":[]}
def persist():
 (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
raw_root=Path("_release-approved")
raw_present=[(raw_root/route/"index.html").is_file() for _,route,*_ in specs]
present=[(incoming/name).is_file() for name,*_ in specs]
if not any(present) and not any(raw_present):
 print("FINAL_GATE: approved files not supplied; keep existing V8 release")
 sys.exit(0)
assert all(raw_present) or all(present),"FINAL_GATE: both approved files required"
payloads={}
for name,route,zsha,hsha,size in specs:
 if all(raw_present):
  b=(raw_root/route/"index.html").read_bytes()
 else:
  z=incoming/name
  assert digest(z.read_bytes())==zsha,(name,"archive checksum mismatch")
  with zipfile.ZipFile(z) as f:
   assert f.namelist()==["index.html"] and f.testzip() is None,name
   b=f.read("index.html")
 assert len(b)==size and digest(b)==hsha,(name,"HTML checksum mismatch")
 payloads[route]=b
 report["files"].append({"route":route,"sha256":hsha,"size":size})
# 27/11/2026: user-approved naming correction, applied only after original checksum verification.
# Keep the approved source immutable and record the derivative checksum separately.
route="kien-truc-thuong-hieu"
arch_before=payloads[route]
arch_text=arch_before.decode("utf-8")
rename_pairs=[
 ("Chuỗi bệnh viện đa chuyên khoa Nguyên Bách","Hệ thống Bệnh viện Chuyên khoa Nguyên Bách"),
 ("Chuỗi Bệnh viện Đa chuyên khoa Nguyên Bách","Hệ thống Bệnh viện Chuyên khoa Nguyên Bách"),
 ("Chuỗi Bệnh viện Đa Chuyên Khoa Nguyên Bách","Hệ thống Bệnh viện Chuyên khoa Nguyên Bách"),
 ("Hệ thống bệnh viện chuyên khoa; mỗi bệnh viện thành viên từ 03 chuyên khoa trở lên","Hệ thống bệnh viện phát triển theo mô hình tích hợp nhiều chuyên khoa chọn lọc, với mỗi bệnh viện thành viên có từ 03 chuyên khoa trở lên."),
 ("Nguyen Bach Multi-specialty Hospital Chain","Nguyen Bach Specialty Hospital System"),
 ("Nguyen Bach Multispecialty Hospital Chain","Nguyen Bach Specialty Hospital System"),
 ("Nguyen Bach Multi-Specialty Hospital Chain","Nguyen Bach Specialty Hospital System"),
 ("Nguyen Bach Multi-specialty Hospitals","Nguyen Bach Specialty Hospital System"),
 ("Nguyen Bach Multi-specialty Hospital System","Nguyen Bach Specialty Hospital System"),
 ("Nguyen Bach multi-specialty hospital chain","Nguyen Bach Specialty Hospital System"),
 ("Multi-specialty Hospital Chain Nguyen Bach","Nguyen Bach Specialty Hospital System"),
]
changes=[]
title_count=0
for old,new in rename_pairs:
 for source,target in [(old,new),(json.dumps(old,ensure_ascii=True)[1:-1],json.dumps(new,ensure_ascii=True)[1:-1])]:
  if source==target: continue
  count=arch_text.count(source)
  if count:
   arch_text=arch_text.replace(source,target)
   changes.append({"old":old,"new":new,"count":count})
   if old.casefold().startswith("chuỗi bệnh viện"):title_count+=count
assert title_count>0,"Nguyen Bach naming correction: exact old Vietnamese title not found; no release"
assert "Chuỗi bệnh viện đa chuyên khoa Nguyên Bách".casefold() not in arch_text.casefold()
payloads[route]=arch_text.encode("utf-8")
assert payloads[route]!=arch_before
report["naming_correction"]={"route":route,"original_sha256":digest(arch_before),"published_sha256":digest(payloads[route]),"changes":changes}
print("FINAL_NGUYEN_BACH_CORRECTION",json.dumps(report["naming_correction"],ensure_ascii=False),flush=True)
hc=payloads["healthcare-website"].decode("utf-8")
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',hc,re.S|re.I)
assert m and len(json.loads(m.group(2)))==126
assert "Demo_ChiTiet.html" in json.loads(m.group(2))
arch=payloads["kien-truc-thuong-hieu"].decode("utf-8")
assert "https://tth-healthcare-website.vercel.app/" in arch
# Fingerprint the rest of the site before changing the two entry points.
targets={root/route/"index.html" for route in payloads}
def other_files():
 return {str(p.relative_to(root)):digest(p.read_bytes()) for p in root.rglob("*") if p.is_file() and p not in targets}
before=other_files()
for route,b in payloads.items():
 dest=root/route/"index.html"
 assert dest.is_file(),route
 dest.write_bytes(b)
assert other_files()==before,"Unrelated route changed"
report["unchanged_other_files"]=len(before);persist()
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
srv=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(root)))
threading.Thread(target=srv.serve_forever,daemon=True).start()
base=f"http://127.0.0.1:{srv.server_port}"
def check(pg,route,w,lang=None,site=None):
 errors=[];failed=[]
 onerr=lambda e:errors.append(str(e)[:200])
 onresp=lambda r:failed.append([r.status,r.url]) if r.status>=400 and r.url.startswith(base) else None
 pg.on("pageerror",onerr);pg.on("response",onresp)
 row={"route":route,"viewport":w,"site":site,"lang":lang}
 try:
  response=pg.goto(base+"/"+route+"/",wait_until="domcontentloaded",timeout=90000)
  assert response and response.status==200
  if route=="kien-truc-thuong-hieu":
   pg.wait_for_function("typeof tthRestoreState==='function'",timeout=30000)
   pg.evaluate("x=>tthRestoreState(x)",{"site":site,"route":"#home","lang":lang})
   pg.wait_for_timeout(400)
   row.update(pg.evaluate("""()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,text:document.body.innerText.trim().length,broken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).length})"""))
   assert row["text"]>250
  else:
   f=pg.frame_locator("#frame")
   f.locator("#app main").first.wait_for(timeout=30000)
   pg.wait_for_timeout(500)
   row.update(f.locator("html").evaluate("""e=>({width:innerWidth,scroll:e.scrollWidth,text:document.body.innerText.trim().length,broken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).length})"""))
   assert row["text"]>250
  assert row["scroll"]<=row["width"]+2,row
  assert not errors and not failed,(errors,failed)
  row["result"]="pass"
  if (site in ("group","tam","elder") or route=="healthcare-website") and lang in (None,"vi"):
   pg.screenshot(path=str(out/f'{site or "healthcare"}-{w}.png'),timeout=30000)
 except Exception as e:
  row.update(result="fail",error=str(e)[:1000])
 row["errors"]=errors;row["failed_http"]=failed
 report["cases"].append(row);persist()
 pg.remove_listener("pageerror",onerr);pg.remove_listener("response",onresp)
 print("FINAL_GATE_CASE",json.dumps(row,ensure_ascii=False),flush=True)
with sync_playwright() as p:
 browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 for w,h in [(390,844),(1440,900)]:
  pg=browser.new_page(viewport={"width":w,"height":h})
  for site in ("group","bach","tri","chau","thao","phuc","tam","tth","elder"):
   for lang in ("vi","en"):check(pg,"kien-truc-thuong-hieu",w,lang,site)
  check(pg,"healthcare-website",w)
  # Actual hosted sample of the new interactive service detail.
  errors=[];pg.on("pageerror",lambda e:errors.append(str(e)[:200]))
  row={"route":"healthcare-service-demo","viewport":w}
  try:
   f=pg.frame_locator("#frame")
   f.locator('a[href="DichVu_DanhSach.html"]').first.evaluate("e=>e.click()")
   f.locator('a[data-tth-mockup-detail="service"]').first.wait_for(timeout=20000)
   import urllib.parse
   links=f.locator('a[data-tth-mockup-detail="service"]')
   opts=links.evaluate_all("xs=>xs.map(a=>a.getAttribute('href'))")
   opts=[(i,json.loads(urllib.parse.parse_qs(urllib.parse.urlsplit(x).query)["item"][0])) for i,x in enumerate(opts)]
   i,d=next(((i,d) for i,d in opts if "thai sản" in d["title"].casefold()),opts[0])
   links.nth(i).evaluate("e=>e.click()")
   f.locator("#tth-demo-title").wait_for(timeout=20000)
   assert f.locator("#tth-demo-title").inner_text()==d["title"]
   f.locator('#tth-demo-action select').select_option(index=1)
   f.locator('#tth-demo-action button[type="submit"]').click()
   assert "DEMO-001" in f.locator('#tth-demo-action [role="status"]').inner_text()
   assert not errors,errors
   row.update(result="pass",title=d["title"])
   pg.screenshot(path=str(out/f"service-demo-{w}.png"),timeout=30000)
  except Exception as e:row.update(result="fail",error=str(e)[:1000])
  report["cases"].append(row);persist()
  print("FINAL_GATE_CASE",json.dumps(row,ensure_ascii=False),flush=True)
  pg.close()
 browser.close()
srv.shutdown()
assert other_files()==before
assert all((root/route/"index.html").read_bytes()==b for route,b in payloads.items())
assert digest(payloads["healthcare-website"])==next(hsha for _,route,_,hsha,_ in specs if route=="healthcare-website")
report["summary"]={"cases":len(report["cases"]),"pass":sum(x["result"]=="pass" for x in report["cases"])}
persist()
print("FINAL_GATE_SUMMARY",json.dumps(report["summary"]),flush=True)
assert all(x["result"]=="pass" for x in report["cases"]),"FINAL release blocked by smoke test"
