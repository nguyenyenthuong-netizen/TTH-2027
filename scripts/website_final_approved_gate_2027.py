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
# TTH Healthcare: distinguish the general hospital/clinic system from specialty brands.
tth_pairs=[
 ("Hệ thống bệnh viện và phòng khám","Hệ thống bệnh viện và phòng khám đa khoa"),
 ("System of hospitals and clinics","System of general hospitals and clinics"),
 ("Hospital and clinic system","General hospital and clinic system"),
 ("Hospital and Clinic System","General Hospital and Clinic System"),
 ("Network of hospitals and clinics","Network of general hospitals and clinics"),
]
tth_vi_count=0
for old,new in tth_pairs:
 for source,target in [(old,new),(json.dumps(old,ensure_ascii=True)[1:-1],json.dumps(new,ensure_ascii=True)[1:-1])]:
  if source==target: continue
  # Do not alter a phrase already qualified as general/multispecialty.
  suffix=(" "+("đa khoa" if old.startswith("Hệ") else "đa khoa"))
  if not old.startswith("Hệ"): suffix=" general"
  if source!=old: suffix=json.dumps(suffix,ensure_ascii=True)[1:-1]
  arch_text,n=re.subn(re.escape(source)+r"(?!"+re.escape(suffix)+r")",lambda m:target,arch_text)
  if n:
   changes.append({"old":old,"new":new,"count":n})
   if old.startswith("Hệ"):tth_vi_count+=n
assert tth_vi_count>0 or "Hệ thống bệnh viện và phòng khám đa khoa" in arch_text,"TTH Healthcare descriptor not found"
# Consolidated 27 November revision: all specialty brands share one naming and navigation standard.
for old,new in [
 ("Nhóm 2 · Thương hiệu y tế độc lập","Nhóm 2 · Hệ thống thương hiệu y tế độc lập"),
 ("Chuỗi bệnh viện","Hệ thống bệnh viện"),("Chuỗi Bệnh viện","Hệ thống Bệnh viện"),
 ("chuỗi bệnh viện","hệ thống bệnh viện"),("CHUỖI BỆNH VIỆN","HỆ THỐNG BỆNH VIỆN"),
 ("Chuỗi ·","Hệ thống ·"),("chuỗi ·","hệ thống ·"),
 ("Hospital Network","Hospital System"),("Hospital Chain","Hospital System"),
 ("hospital chain","hospital system"),("hospital network","hospital system"),
 ("Hệ thống bệnh viện theo địa phương","Hệ thống bệnh viện thành viên"),
 ("Hệ thống Bệnh viện Chuyên khoa Nguyên Bách","Hệ thống Bệnh viện Nguyên Bách"),
]:
 for source,target in [(old,new),(json.dumps(old,ensure_ascii=True)[1:-1],json.dumps(new,ensure_ascii=True)[1:-1])]:
  if source==target:continue
  n=arch_text.count(source)
  if n:
   arch_text=arch_text.replace(source,target)
   changes.append({"old":old,"new":new,"count":n})
# Operate on the live DOM after the existing renderer and locale controls, without replacing its routing.
ui_patch=r"""
<style id="tth-unified-ui-2711-css">
header details>summary .tth-menu-primary{color:inherit!important;font:inherit!important;text-decoration:none!important;display:inline-flex!important;align-items:center!important;white-space:nowrap}
header details>summary .tth-menu-primary:hover{text-decoration:underline!important;text-underline-offset:4px}
header details>summary .tth-menu-primary:focus-visible{outline:2px solid currentColor;outline-offset:3px}
header details>summary .un-chevron{cursor:pointer}
header details>summary:has(.tth-menu-toggle){display:flex!important;align-items:center!important;gap:3px!important}
header details>summary:has(.tth-menu-toggle)::after{display:none!important}
header details>summary .tth-menu-toggle{border:0;background:none;color:inherit;cursor:pointer;padding:4px;display:inline-flex;align-items:center;justify-content:center;min-width:22px;min-height:30px}
header details>summary .tth-menu-toggle:focus-visible{outline:2px solid currentColor;outline-offset:2px}
footer .tth-footer-address,footer .tth-footer-hotline{min-width:0;overflow-wrap:anywhere}
.tth-added-illustration{margin:0 0 12px;overflow:hidden;border-radius:6px}
.tth-added-illustration img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.tth-added-illustration figcaption{font-size:12px;color:inherit;padding:4px 0}
footer .tth-footer-address a{overflow-wrap:anywhere}
</style>
<script id="tth-unified-ui-2711">
(()=>{
 const names={bach:'Nguyên Bách',chau:'Nguyên Châu',tri:'Nguyên Trí',thao:'Nguyên Thảo',phuc:'Nguyên Phúc',tam:'Nguyên Tâm'};
 const enNames={bach:'Nguyen Bach',chau:'Nguyen Chau',tri:'Nguyen Tri',thao:'Nguyen Thao',phuc:'Nguyen Phuc',tam:'Nguyen Tam'};
 const specialty={bach:'Chuyên khoa chọn lọc',chau:'Mắt',tri:'Tai Mũi Họng',thao:'Răng Hàm Mặt',phuc:'Y học cổ truyền',tam:'Thẩm mỹ'};
 const specialtyEN={bach:'Selected specialties',chau:'Ophthalmology',tri:'Ear, Nose and Throat',thao:'Dentistry and Maxillofacial Care',phuc:'Traditional Medicine',tam:'Aesthetic Medicine'};
 const address={phuc:'Đại lộ 72m, phường Vinh Hưng, Nghệ An',tth:'28 Nguyễn Sỹ Sách, phường Thành Vinh, Nghệ An'};
 const addressEN={phuc:'72m Boulevard, Vinh Hung Ward, Nghe An',tth:'28 Nguyen Sy Sach Street, Thanh Vinh Ward, Nghe An'};
 const demoHotline={tri:'1900 0001',chau:'1900 0002',thao:'1900 0003',phuc:'1900 0004',tam:'1900 0005',tth:'1900 0006',bach:'1900 0007',elder:'1900 0008',group:'1900 0009'};
 function put(el,s){if(el&&el.textContent!==s)el.textContent=s}
 function apply(){
  const id=typeof active==='string'?active:'';
  const en=document.documentElement.lang==='en';
  const route=typeof currentHash==='string'?currentHash:'#home';
  // A dedicated text link and a dedicated chevron button are independent.
  document.querySelectorAll('header details>summary').forEach(s=>{
   if(s.querySelector('.tth-menu-primary')&&s.querySelector('.tth-menu-toggle'))return;
   const prior=s.querySelector('a[href^="#"]');
   const first=prior||s.parentElement.querySelector(':scope > :not(summary) a[href^="#"]');
   if(!first)return;
   const label=(prior?.textContent||s.textContent).trim().replace(/[⌄▾▼›]+$/,'').trim();
   if(!label)return;
   const a=document.createElement('a');a.className='v19-menulabel tth-menu-primary';a.href=first.getAttribute('href');a.textContent=label;
   const b=document.createElement('button');b.type='button';b.className='tth-menu-toggle';b.setAttribute('aria-label',en?'Open submenu':'Mở danh mục con');b.setAttribute('aria-expanded',String(s.parentElement.open));b.innerHTML='<svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="m3 6 5 5 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
   s.replaceChildren(a,b);s.parentElement.addEventListener('toggle',()=>b.setAttribute('aria-expanded',String(s.parentElement.open)));
  });
  const brand=document.querySelector('header .brand-name-stack');
  if(brand&&names[id]){
   const parts=brand.querySelectorAll(':scope > span');
   const m=route.match(/^#med-facility-(\d+)$/);
   const facility=m&&typeof GEO!=='undefined'?GEO[id]?.[Number(m[1])]:null;
   const main=facility?facility.name.replace(/\s+[–-]\s+/g,' '):(en?enNames[id]:names[id]).toUpperCase();
   const sub=facility?(id==='chau'&&Number(m[1])===1?(en?'Ophthalmology – Ear, Nose and Throat':'Mắt – Tai Mũi Họng'):(en?specialtyEN[id]:specialty[id])):(en?'Specialty hospital system':'Hệ thống bệnh viện chuyên khoa');
   if(parts.length>=2){put(parts[0],main);put(parts[1],sub)}
  }
  if(id==='chau'){
   // The two locations are explicitly illustrative; keep the different specialties visible.
   document.querySelectorAll('.loc-card[data-loc="Hà Tĩnh"]').forEach(c=>{
    c.dataset.spec='1,0';
    const chips=c.querySelector('.loc-chips');
    if(chips&&!chips.querySelector('[data-tth-ent]')){
     const chip=document.createElement('span');chip.className='loc-chip';chip.dataset.tthEnt='1';chip.textContent=en?'Ear, Nose and Throat':'Tai Mũi Họng';chips.append(chip);
    }
    const p=c.querySelector('.loc-copy p');if(p&&/1 chuyên khoa|1 specialty/i.test(p.textContent))put(p,en?'2 specialties · Illustrative facility':'2 chuyên khoa · Cơ sở minh họa');
   });
   if(route==='#med-facility-1'){
    const chips=document.querySelector('#app .loc-chips');
    if(chips&&!chips.querySelector('[data-tth-ent]')){const chip=document.createElement('span');chip.className='loc-chip';chip.dataset.tthEnt='1';chip.textContent=en?'Ear, Nose and Throat':'Tai Mũi Họng';chips.append(chip)}
   }
  }
  document.querySelectorAll('footer .final-footer-contact,footer .contact-compact').forEach(c=>{
   const cols=[...c.children];
   let a=cols.find(x=>/^(địa chỉ|address)$/i.test(x.querySelector('strong,h3,h4')?.textContent.trim()||''));
   const website=cols.find(x=>/^website$/i.test(x.querySelector('strong,h3,h4')?.textContent.trim()||''));
   if(website&&a)website.remove();
   if(!a){
    a=website||document.createElement('div');
    a.classList.add('tth-footer-address');
    a.replaceChildren();
    const h=document.createElement('strong');h.textContent=en?'Address':'Địa chỉ';a.append(h);
    if(!website)c.prepend(a);
    const text=document.createElement(names[id]&&!address[id]?'a':'span');text.className='footer-contact-link';text.dataset.tthAddress='1';a.append(text);
   }
   const target=a.querySelector('[data-tth-address]');
   if(target){
    put(a.querySelector('strong'),en?'Address':'Địa chỉ');
    const fixed=en?addressEN[id]:address[id];
    if(fixed)put(target,fixed);
    else {
     const m=route.match(/^#med-facility-(\d+)$/);
     const facility=m&&typeof GEO!=='undefined'?GEO[id]?.[Number(m[1])]:null;
     const loc=facility?.loc||'Vinh';
     const span=target.tagName==='A'?document.createElement('span'):target;
     if(span!==target){span.className='footer-contact-link';span.dataset.tthAddress='1';target.replaceWith(span);}
     put(span,en?'00 Illustration Street, '+loc+' (sample)':'Số 00, đường Minh Họa, '+loc+' (mẫu)');
    }
   }else if(a&&/chưa cập nhật|chưa xác nhận|not available|not yet confirmed/i.test(a.textContent)){
    const old=a.querySelector('a,span,p');if(old){const span=document.createElement('span');span.className='footer-contact-link';span.dataset.tthAddress='1';span.textContent=en?'00 Illustration Street, Vinh (sample)':'Số 00, đường Minh Họa, Vinh (mẫu)';old.replaceWith(span);}
   }
   let hot=[...c.children].find(x=>/^hotline$/i.test(x.querySelector('strong,h3,h4')?.textContent.trim()||''));
   if(!hot&&demoHotline[id]){hot=document.createElement('div');hot.innerHTML='<strong>Hotline</strong><span class="footer-contact-link"></span>';c.append(hot);}
   if(hot&&demoHotline[id]){
    let v=hot.querySelector('a,span,p');
    const value=v?.textContent.trim()||'';
    if(!value||/xxxx|chưa cập nhật|chưa xác nhận|not available|not yet confirmed|mẫu|minh họa|sample|illustrative/i.test(value)||hot.classList.contains('tth-footer-hotline')){
     if(!v||v.tagName==='A'){const span=document.createElement('span');span.className='footer-contact-link';if(v)v.replaceWith(span);else hot.append(span);v=span;}
     hot.classList.add('tth-footer-hotline');put(v,demoHotline[id]+(en?' (sample)':' (mẫu)'));
    }
   }
  });
  // Only reuse a relevant existing brand illustration; never fabricate a doctor's portrait or facility photograph.
  if(names[id]||id==='tth'||id==='elder'){
   const hero=document.querySelector('#app .hero img,#app .el-hero img')||document.querySelector('#tpl-home')?.content?.querySelector('.hero img,.el-hero img');
   const raw=hero?.getAttribute('src');
   if(raw&&raw.startsWith('data:image/')){
    document.querySelectorAll('#app .un-topic,#app .el-card,#app .nb-hospital-item').forEach(card=>{
     if(card.querySelector('img,figure,svg,.tth-added-illustration')||!card.querySelector('h3,strong'))return;
     const fig=document.createElement('figure');fig.className='tth-added-illustration';
     const img=document.createElement('img');img.src=raw;img.loading='lazy';img.alt=en?'General specialty illustration':'Hình minh họa chuyên khoa';
     const cap=document.createElement('figcaption');cap.textContent=en?'General illustration':'Hình minh họa chung';
     fig.append(img,cap);card.prepend(fig);
    });
   }
  }
 }
 window.addEventListener('click',e=>{
  const a=e.target.closest?.('header .tth-menu-primary'),b=e.target.closest?.('header .tth-menu-toggle');if(!a&&!b)return;
  if(a&&(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey))return;
  e.preventDefault();e.stopImmediatePropagation();
  const d=(a||b).closest('details');
  if(b){const open=!d.open;d.closest('header').querySelectorAll('details[open]').forEach(x=>{if(x!==d)x.open=false});d.open=open;b.setAttribute('aria-expanded',String(open));return;}
  const h=a.getAttribute('href');
  if(h&&typeof window.navRoute==='function'){d.open=false;currentHash=h;window.navRoute()}
  else if(h)location.hash=h;
 },true);
 window.addEventListener('pointerover',e=>{if(e.target.closest?.('header summary:has(.tth-menu-toggle)'))e.stopPropagation();},true);
 if(typeof GEO!=='undefined'&&GEO.chau?.[1])GEO.chau[1].spec=[1,0];
 if(typeof NORMALIZED!=='undefined'&&NORMALIZED.chau?.facilities?.[1])NORMALIZED.chau.facilities[1].spec=[1,0];
 if(typeof clinicalDictionary!=='undefined')Object.assign(clinicalDictionary,{'Hệ thống bệnh viện chuyên khoa':'Specialty hospital system','Hệ thống bệnh viện thành viên':'Member hospitals','Địa chỉ':'Address','Xem địa chỉ từng bệnh viện':'See addresses by hospital','Địa chỉ chưa xác nhận':'Address not yet confirmed','Hình minh họa chung':'General illustration'});
 let pending=false;
 function schedule(){if(pending)return;pending=true;requestAnimationFrame(()=>{pending=false;apply()})}
 new MutationObserver(schedule).observe(document.body,{subtree:true,childList:true,characterData:true});
 apply();
 window.tthUnifiedUI2711=apply;
})();
</script>
"""
assert arch_text.lower().count("</body>")>=1
idx=arch_text.lower().rfind("</body>")
arch_text=arch_text[:idx]+ui_patch+arch_text[idx:]
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
   if site in ("bach","tri","chau","thao","phuc","tam","tth","elder","group"):
    pg.wait_for_function("typeof window.tthUnifiedUI2711==='function'")
    pg.evaluate("window.tthUnifiedUI2711()")
    links=pg.locator("header details>summary .tth-menu-primary:visible")
    if w>=1000 and links.count():
     for i in range(links.count()):
      pg.evaluate("x=>tthRestoreState(x)",{"site":site,"route":"#home","lang":lang})
      pg.evaluate("window.tthUnifiedUI2711()")
      a=pg.locator("header details>summary .tth-menu-primary:visible").nth(i)
      href=a.get_attribute("href")
      a.click(timeout=10000)
      pg.wait_for_function("h=>currentHash===h",arg=href,timeout=10000)
     pg.evaluate("x=>tthRestoreState(x)",{"site":site,"route":"#home","lang":lang})
     pg.evaluate("window.tthUnifiedUI2711()")
    if w>=1000 and pg.locator("header .tth-menu-toggle:visible").count():
     arrow=pg.locator("header .tth-menu-toggle:visible").first
     arrow.click(timeout=10000)
     assert arrow.evaluate("e=>e.closest('details').open"),"Submenu did not open"
     arrow.click(timeout=10000)
     assert not arrow.evaluate("e=>e.closest('details').open"),"Submenu did not close"
    assert not pg.locator("footer .final-footer-contact > div").filter(has=pg.locator("strong",has_text=re.compile("^Website$",re.I))).count(),"Duplicate website footer"
    assert not pg.locator("footer .tth-footer-hotline a[href^='tel:']").count(),"Sample hotline must not dial"
    if site in ("bach","tri","chau","thao","phuc","tam"):
     assert pg.locator("header .brand-name-stack").count()>0
   row["unified_ui"]="checked"
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
