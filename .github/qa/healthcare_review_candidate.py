#!/usr/bin/env python3
"""Prepare a review copy only from the exact live Healthcare HTML, without changing published content."""
from pathlib import Path
from urllib.request import urlopen,Request
from hashlib import sha256
import json,re
from playwright.sync_api import sync_playwright

url="https://nguyenyenthuong-netizen.github.io/TTH-2027/healthcare-website/"
out=Path("artifacts/healthcare-review")
out.mkdir(parents=True,exist_ok=True)
with urlopen(Request(url,headers={"User-Agent":"TTH-2027-review/1.0"}),timeout=90) as r:
    raw=r.read()
source=raw.decode("utf-8")
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',source,re.S|re.I)
assert m,"Live source missing embedded page catalog"
pages=json.loads(m.group(2))
assert len(pages)==125,("Unexpected live catalog size",len(pages))
report={"source_url":url,"source_sha256":sha256(raw).hexdigest(),"pages":len(pages),"route_inventory":sorted(pages),"changes":{"footer_email":[],"symmetric_layout":[],"az_links":[]},"browser":[],"unresolved":[]}
def persist():
    (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
persist()
# Choose only an existing list page. A generic detail or placeholder is not an acceptable target.
candidate_names=[n for n in pages if re.search(r'(?i)^ChuyenKhoa_(?:DanhSach|TrangChu|AZ|A_Z|TongQuan|DanhMuc)\.html$',n)]
report["az_candidates"]=candidate_names
az=candidate_names[0] if len(candidate_names)==1 else None
if az is None: report["unresolved"].append("A–Z: no unique existing specialist directory route identified; no invented target")
az_anchor=re.compile(r'(<a\b[^>]*\bhref=["\'])#chua-co-trang(["\'][^>]*>)([^<]*(?:Tất cả chuyên khoa|All specialties)[^<]*)(</a>)',re.I)
email_anchor=re.compile(r'<a\b[^>]*href=["\']mailto:cskh@tthhealthcare\.com["\'][^>]*>.*?</a>',re.I|re.S)
for n,doc in list(pages.items()):
    before=doc
    # Remove the source-production note from customer-facing specialty directory.
    internal_note="Tên khoa tại từng cơ sở được giữ theo dữ liệu đang thể hiện trong bộ trang gốc."
    if internal_note in doc:
        doc=doc.replace(" "+internal_note,"").replace(internal_note,"")
        report.setdefault("removed_internal_note",[]).append(n)
    if az:
        doc,ct=az_anchor.subn(lambda x:x.group(1)+az+x.group(2)+x.group(3)+x.group(4),doc)
        if ct: report["changes"]["az_links"].append({"page":n,"count":ct,"target":az})
    # Keep the existing customer service mailbox and add the approved general brand mailbox separately.
    def footer(m):
        f=m.group(0)
        if "info@tthhealthcare.com" in f.lower(): return f
        a=email_anchor.search(f)
        if not a:return f
        original=a.group(0)
        clone=re.sub(r'cskh@tthhealthcare\.com','info@tthhealthcare.com',original,flags=re.I)
        return f[:a.end()]+"\n"+clone+f[a.end():]
    doc2=re.sub(r'<footer\b[^>]*>.*?</footer>',footer,doc,flags=re.I|re.S)
    if doc2!=doc:report["changes"]["footer_email"].append(n)
    doc=doc2
    # Modify only the known deployed width controller, not general navigation or content.
    style=re.search(r'<style id="tth-website-content-wide-2027">.*?</style>',doc,re.S)
    js=re.search(r'<script id="tth-website-content-wide-js-2027">.*?</script>',doc,re.S)
    if style and js:
        old=js.group(0)
        marker=" root.style.setProperty('--tth-website-left-gap',left+'px');"
        ml="el.style.setProperty('margin-left',left+'px','important');"
        if old.count(marker)==1 and old.count(ml)==1:
            new=old.replace(marker," left=right;\n"+marker).replace(ml,"el.style.setProperty('margin-left','auto','important');")
            doc=doc.replace(old,new,1)
            oldcss=style.group(0)
            newcss=oldcss.replace("100vw - var(--tth-website-left-gap) - var(--tth-website-cta-gap)","100vw - 2 * var(--tth-website-cta-gap)").replace("margin-left:var(--tth-website-left-gap)!important","margin-left:auto!important")
            doc=doc.replace(oldcss,newcss,1)
            report["changes"]["symmetric_layout"].append(n)
    pages[n]=doc
assert len(pages)==125
packed=json.dumps(pages,ensure_ascii=False,separators=(",",":")).replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026")
review=source[:m.start(2)]+packed+source[m.end(2):]
if not re.search(r'<meta[^>]+name=["\']robots["\']',review,re.I):
    review=review.replace("</head>",'<meta name="robots" content="noindex,nofollow"></head>',1)
path=out/"TTH-Healthcare-ban-duyet.html"
path.write_text(review,encoding="utf-8")
report["candidate_sha256"]=sha256(path.read_bytes()).hexdigest()
report["unresolved"]+=["Tablet header: requires separate menu behavior verification before any changes","Song ngữ: inspect top utility strip, no unsupported translation changes","Per-doctor and per-service detail routing: requires identity-level verification"]
persist()
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for w,h in [(390,844),(768,1024),(1024,768),(1440,900)]:
        page=browser.new_page(viewport={"width":w,"height":h})
        errors=[];page.on("pageerror",lambda e:errors.append(str(e)[:300]))
        row={"viewport":[w,h]}
        try:
            page.goto(path.resolve().as_uri(),wait_until="domcontentloaded",timeout=60000)
            frame=page.frame_locator("iframe#frame")
            main=frame.locator("#app main").first
            main.wait_for(state="visible",timeout=25000)
            page.wait_for_timeout(500)
            row.update(main.evaluate("""e=>({left:e.getBoundingClientRect().left,right:innerWidth-e.getBoundingClientRect().right,scrollWidth:document.documentElement.scrollWidth,viewport:innerWidth,homeText:e.innerText.length,languageControls:[...document.querySelectorAll('a,button')].filter(x=>/Chuyển ngôn ngữ|VI\\s*\\|\\s*EN|VN\\s*\\|\\s*EN/i.test((x.getAttribute('aria-label')||'')+' '+x.innerText)).map(x=>({text:x.innerText,href:x.getAttribute('href'),visible:x.getBoundingClientRect().width>0})),email:[...document.querySelectorAll('footer a[href^="mailto:"]')].map(x=>x.getAttribute('href'))})"""))
            page.screenshot(path=str(out/f"{w}-home.png"),timeout=30000,animations="disabled")
            foot=frame.locator("#app footer").first
            if foot.count():
                foot.scroll_into_view_if_needed(timeout=15000)
                page.screenshot(path=str(out/f"{w}-footer.png"),timeout=30000,animations="disabled")
            assert row["scrollWidth"]<=w+2 and row["homeText"]>300,row
            if w>=981 and report["changes"]["symmetric_layout"]:
                assert abs(row["left"]-row["right"])<=3,row
            if report["changes"]["footer_email"]:
                assert "mailto:info@tthhealthcare.com" in row["email"],row
                assert "mailto:cskh@tthhealthcare.com" in row["email"],row
            if az:
                a=frame.locator(f'a[href="{az}"]').filter(has_text=re.compile("Tất cả chuyên khoa|All specialties",re.I)).first
                if a.count():
                    a.evaluate("(e)=>e.click()")
                    page.wait_for_timeout(700)
                    row["az_after"]=frame.locator("#app main").first.inner_text()[:300]
                    assert "chuyên khoa" in row["az_after"].lower() or "specialt" in row["az_after"].lower(),row
            assert not errors,errors
            row["result"]="pass"
        except Exception as e:row.update(result="not passed",error=str(e)[:1000])
        row["page_errors"]=errors
        report["browser"].append(row);persist()
        print("HEALTHCARE_REVIEW_CASE",json.dumps(row,ensure_ascii=False),flush=True)
        page.close()
    # Check whether different card links resolve to distinct content, without submitting forms.
    identity=[]
    page=browser.new_page(viewport={"width":1440,"height":900})
    def home():
        page.goto(path.resolve().as_uri(),wait_until="domcontentloaded",timeout=60000)
        f=page.frame_locator("iframe#frame")
        f.locator("#app main").first.wait_for(state="visible",timeout=25000)
        return f
    for list_route, detail in [("BacSi_DanhSach.html","BacSi_HoSo.html"),("DichVu_DanhSach.html","DichVu_ChiTiet.html"),("KienThuc_TrangChu.html","KienThuc_BaiViet.html")]:
        result={"list":list_route,"detail":detail,"samples":[]}
        try:
            for i in range(2):
                f=home()
                f.locator(f'a[href="{list_route}"]').first.evaluate("e=>e.click()")
                page.wait_for_timeout(500)
                links=f.locator(f'#app main a[href^="{detail}"]')
                if links.count()<=i:break
                a=links.nth(i)
                sample=a.evaluate("""e=>({href:e.getAttribute('href'),context:(e.closest('article')||e.parentElement.parentElement).innerText.slice(0,300)})""")
                a.evaluate("e=>e.click()")
                page.wait_for_timeout(500)
                sample["detail_text"]=f.locator("#app main").first.inner_text()[:1600]
                result["samples"].append(sample)
            ss=result["samples"]
            result["status"]="not enough samples" if len(ss)<2 else ("same detail content" if ss[0]["detail_text"]==ss[1]["detail_text"] else "distinct detail content")
        except Exception as e: result["error"]=str(e)[:500]
        identity.append(result)
    report["identity_checks"]=identity
    print("HEALTHCARE_IDENTITY_QA",json.dumps(identity,ensure_ascii=False),flush=True)
    language={}
    try:
        f=home()
        a=f.locator('a[href="EN_TrangChu.html"]').first
        language["vi_label"]=a.inner_text()
        a.evaluate("e=>e.click()")
        page.wait_for_timeout(600)
        language["en_text"]=f.locator("#app main").first.inner_text()[:600]
        language["en_lang"]=f.locator("html").get_attribute("lang")
        language["return_links"]=f.locator('a[href="TrangChu.html"]').count()
        page.screenshot(path=str(out/"1440-english-home.png"),timeout=30000)
    except Exception as e:language["error"]=str(e)[:500]
    report["language_check"]=language
    print("HEALTHCARE_LANGUAGE_QA",json.dumps(language,ensure_ascii=False),flush=True)
    page.close()
    persist()
    browser.close()
print("HEALTHCARE_REVIEW_SUMMARY",json.dumps({"source_sha256":report["source_sha256"],"candidate_sha256":report["candidate_sha256"],"pages":report["pages"],"changes":{k:len(v) for k,v in report["changes"].items()},"az_candidates":candidate_names,"unresolved":report["unresolved"],"passes":sum(x["result"]=="pass" for x in report["browser"]),"cases":len(report["browser"])},ensure_ascii=False),flush=True)
if any(x["result"]!="pass" for x in report["browser"]):raise SystemExit("Review candidate not accepted; screenshots preserved")
