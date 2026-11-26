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

    # Protect shared template detail routes from presenting unrelated clinical content.
    if ('DichVu_ChiTiet.html' in doc or 'KienThuc_BaiViet.html' in doc) and '</head>' in doc:
        doc=doc.replace('</head>', "<script id=\"tth-review-detail-identity-guard\">\n(function(){\n\"use strict\";\nconst rules={\"DichVu_ChiTiet.html\":{kind:\"service\",expected:\"khám sức khỏe tổng quát\"},\"KienThuc_BaiViet.html\":{kind:\"article\",expected:\"tăng huyết áp\"}};\nfunction plain(s){return (s||\"\").trim().replace(/\\s+/g,\" \")}\nfunction cardFor(a){return a.closest(\"article.card,article,.card\")}\nfunction titleOf(card){const e=card.querySelector(\"h1,h2,h3,h4,h5\");if(e&&plain(e.textContent))return plain(e.textContent);return card.innerText.split(/\\n+/).map(plain).find(x=>x&&!/^(gói khám|dịch vụ|bài viết|video|kiến thức|xem chi tiết|đọc bài)$/i.test(x))||\"\"}\nfunction show(card,title,rule){\n const existing=document.getElementById(\"tth-review-detail\");if(existing)existing.remove();\n const d=document.createElement(\"dialog\");d.id=\"tth-review-detail\";d.setAttribute(\"aria-labelledby\",\"tth-review-detail-title\");\n d.style.cssText=\"box-sizing:border-box;width:min(560px,calc(100vw - 32px));max-height:calc(100dvh - 40px);overflow:auto;padding:24px;border:1px solid #b8cbe7;border-radius:12px;background:white;color:#16345b;box-shadow:0 12px 44px #142c5a40;font:16px/1.5 Arial,sans-serif\";\n const close=document.createElement(\"button\");close.type=\"button\";close.textContent=\"Đóng\";close.style.cssText=\"float:right;border:1px solid #0837A1;color:#0837A1;background:#fff;padding:8px 14px;border-radius:6px;cursor:pointer\";close.onclick=()=>d.close();\n const heading=document.createElement(\"h2\");heading.id=\"tth-review-detail-title\";heading.textContent=title;heading.style.cssText=\"margin:12px 0;color:#0837A1;font-size:23px;clear:both\";\n d.append(close,heading);\n const description=Array.from(card.querySelectorAll(\"p\")).map(e=>plain(e.textContent)).find(s=>s&&s!==title);\n if(description){const body=document.createElement(\"p\");body.textContent=description;d.append(body)}\n const note=document.createElement(\"p\");note.textContent=rule.kind===\"service\"?\"Thông tin chi tiết và chi phí của dịch vụ này chưa được cập nhật. Vui lòng liên hệ cơ sở để được tư vấn.\":\"Nội dung đầy đủ của bài viết này chưa được cập nhật.\";d.append(note);\n if(rule.kind===\"service\"){const a=document.createElement(\"a\");a.href=\"tel:19002675\";a.textContent=\"Tư vấn: 1900 2675\";a.style.cssText=\"display:inline-block;padding:10px 15px;background:#0837A1;color:#fff;text-decoration:none;border-radius:6px\";d.append(a)}\n document.body.append(d);d.addEventListener(\"close\",()=>d.remove(),{once:true});d.showModal();\n}\nwindow.addEventListener(\"click\",function(e){\n const a=e.target.closest&&e.target.closest(\"a[href]\");if(!a)return;\n const rule=rules[a.getAttribute(\"href\")];if(!rule)return;\n const c=cardFor(a);if(!c)return;\n const title=titleOf(c);if(!title)return;\n // Only preserve the source's exact demonstrated detail identity.\n if(title.toLocaleLowerCase(\"vi\").includes(rule.expected))return;\n e.preventDefault();e.stopImmediatePropagation();show(c,title,rule);\n},true);\n})();\n</script>"+'</head>',1)
        report.setdefault("detail_guard_pages",[]).append(n)
    if n.startswith("EN_"):
        doc,lang_count=re.subn(r'(<html\b[^>]*\blang=["\'])vi(["\'])',r'\g<1>en\2',doc,count=1,flags=re.I)
        if lang_count:report.setdefault("english_language_fixed",[]).append(n)
        # Add a return only to an actual, unambiguous Vietnamese home route.
        if n=="EN_TrangChu.html":
            homes=[x for x in pages if x in ("TrangChu.html","Home.html","Index.html","index.html")]
            report["vi_home_candidates"]=homes
            if len(homes)==1 and not re.search(r'href=["\']'+re.escape(homes[0])+r'["\']',doc):
                doc=doc.replace('</body>', '<a href="'+homes[0]+'" aria-label="Tiếng Việt" style="position:fixed;top:8px;right:12px;z-index:10000;border:1px solid #0837A1;background:#fff;color:#0837A1;padding:8px 12px;border-radius:6px;text-decoration:none">VN | EN</a></body>',1)
                report["vi_return_added"]=homes[0]
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
                if links.count()<=i:
                    result["available_actions"]=f.locator("#app main").evaluate("""e=>[...e.querySelectorAll('a,button')].map(x=>({href:x.getAttribute('href'),label:(x.innerText||x.getAttribute('aria-label')||'').trim()})).filter(x=>x.label).slice(0,65)""")
                    break
                a=links.nth(i)
                sample=a.evaluate("""e=>({href:e.getAttribute('href'),context:(e.closest('article')||e.parentElement.parentElement).innerText.slice(0,300)})""")
                a.evaluate("e=>e.click()")
                page.wait_for_timeout(500)
                dialog=f.locator("#tth-review-detail")
                sample["guarded"]=dialog.count()>0 and dialog.is_visible()
                sample["detail_text"]=(dialog.inner_text() if sample["guarded"] else f.locator("#app main").first.inner_text())[:1600]
                result["samples"].append(sample)
            ss=result["samples"]
            result["status"]="not enough samples" if len(ss)<2 else ("same detail content" if ss[0]["detail_text"]==ss[1]["detail_text"] else "distinct detail content")
        except Exception as e: result["error"]=str(e)[:500]
        identity.append(result)
    report["identity_checks"]=identity
    for entry in identity:
        if entry["list"] in ("DichVu_DanhSach.html","KienThuc_TrangChu.html") and len(entry["samples"])==2:
            assert entry["status"]=="distinct detail content" and entry["samples"][1].get("guarded"),entry
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
