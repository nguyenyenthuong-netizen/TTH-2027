#!/usr/bin/env python3
"""Read-only audit of currently published mockups. No forms submitted, no release."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

out = Path("artifacts/healthcare-live-audit")
out.mkdir(parents=True, exist_ok=True)
urls = {
    "github": "https://nguyenyenthuong-netizen.github.io/TTH-2027/healthcare-website/",
    "vercel": "https://tth-healthcare-website.vercel.app/"
}
sizes = [(390,844),(768,1024),(1024,768),(1440,900)]
targets = ["HeThongYTe.html","BacSi_DanhSach.html","DichVu_DanhSach.html","KienThuc_TrangChu.html","HuongDan_TrangChu.html","Microsite_TTHVinh.html","TimKiem.html"]
inspect = r"""() => {
 const visible=e=>{let r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'};
 const label=e=>(e.innerText||e.getAttribute('aria-label')||e.getAttribute('title')||'').trim().replace(/\s+/g,' ');
 const rect=e=>{let r=e.getBoundingClientRect();return {x:Math.round(r.x),y:Math.round(r.y),width:Math.round(r.width),height:Math.round(r.height),right:Math.round(r.right)}};
 const head=document.querySelector('#app header.gh,header.gh,header'), main=document.querySelector('#app main,main'), footer=document.querySelector('#app footer,footer');
 const collect=e=>e?[...e.querySelectorAll('a,button,[role=button]')].filter(visible).map(x=>({label:label(x),href:x.getAttribute('href'),box:rect(x)})):[];
 const nav=head&&head.querySelector('nav'); const a=collect(nav||head); const body=collect(main); const f=collect(footer);
 const duplicates=xs=>{let m={};for(const x of xs){let k=x.label+'|'+(x.href||'');if(x.label&&x.href)m[k]=(m[k]||0)+1}return Object.entries(m).filter(([k,v])=>v>1)};
 const imgs=[...document.querySelectorAll('img')].filter(visible);
 return {title:document.title,lang:document.documentElement.lang,viewport:[innerWidth,innerHeight],scrollWidth:document.documentElement.scrollWidth,
 header:head?rect(head):null,header_controls:collect(head),nav_duplicate:duplicates(a),
 main:main?rect(main):null,main_text_length:main?(main.innerText||'').length:0,main_duplicate_exact:duplicates(body),
 footer:footer?rect(footer):null,footer_contacts:f.filter(x=>/mailto:|tel:/.test(x.href||'')||/@|1900/.test(x.label)),
 placeholder_visible:[...document.querySelectorAll('a[href="#chua-co-trang"]')].filter(visible).map(label),
 language_controls:collect(head).filter(x=>/^(VN|VI|EN|VN\s*\|\s*EN|VI\s*\|\s*EN)$/i.test(x.label)),
 search_controls:collect(head).filter(x=>/tìm kiếm|search/i.test(x.label)),
 broken_loaded_images:imgs.filter(x=>x.complete&&!x.naturalWidth).map(x=>({alt:x.alt,src:(x.getAttribute('src')||'').slice(0,100)})),
 visible_image_count:imgs.length,head_text:head?(head.innerText||'').slice(0,1200):'',
 footer_text:footer?(footer.innerText||'').slice(0,1600):''}
}"""
def get_frame(page):
    try:
        page.locator("iframe#frame").wait_for(state="attached",timeout=5000)
        frame = page.locator("iframe#frame").element_handle().content_frame()
        if frame:
            frame.locator("#app main,main").first.wait_for(state="visible",timeout=20000)
            return frame
    except Exception:
        pass
    return page
report=[]
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for origin,url in urls.items():
        for w,h in sizes:
            page=browser.new_page(viewport={"width":w,"height":h},locale="vi-VN")
            errors=[]; http=[]
            page.on("pageerror",lambda e:errors.append(str(e)[:500]))
            page.on("response",lambda r:http.append({"status":r.status,"url":r.url[:500]}) if r.status>=400 else None)
            item={"origin":origin,"viewport":[w,h],"url":url,"routes":[]}
            try:
                resp=page.goto(url,wait_until="domcontentloaded",timeout=45000)
                item["status"]=resp.status if resp else None
                frame=get_frame(page)
                frame.locator("#app main,main").first.wait_for(state="visible",timeout=20000)
                item["home"]=frame.evaluate(inspect)
                item["final_url"]=page.url
                page.screenshot(path=str(out/f"{origin}-{w}-home.png"),timeout=20000,animations="disabled")
                foot=frame.locator("#app footer,footer").first
                if foot.count():
                    foot.scroll_into_view_if_needed(timeout=10000)
                    page.screenshot(path=str(out/f"{origin}-{w}-footer.png"),timeout=20000,animations="disabled")
                if origin=="github" and w in (390,1440):
                    for route in targets:
                        row={"target":route}
                        try:
                            page.goto(url,wait_until="domcontentloaded",timeout=45000)
                            frame=get_frame(page)
                            link=frame.locator(f'a[href="{route}"]').first
                            if not link.count():
                                row["status"]="not found from home"
                            else:
                                old=frame.evaluate("()=>document.querySelector('#app main,main')?.innerText?.slice(0,350)")
                                link.evaluate("e=>e.click()")
                                frame.wait_for_timeout(600)
                                frame=get_frame(page)
                                st=frame.evaluate(inspect)
                                new=frame.evaluate("()=>document.querySelector('#app main,main')?.innerText?.slice(0,350)")
                                row.update({"status":"content changed" if new!=old and new else "not confirmed","state":st,"outer_url":page.url})
                                page.screenshot(path=str(out/f"{origin}-{w}-{route.replace('.html','')}.png"),timeout=20000,animations="disabled")
                        except Exception as e:
                            row["error"]=str(e)[:400]
                        item["routes"].append(row)
            except Exception as e:
                item["error"]=str(e)[:700]
                try: page.screenshot(path=str(out/f"{origin}-{w}-error.png"),timeout=10000)
                except Exception: pass
            item["page_errors"]=errors
            item["http_errors"]=http
            report.append(item)
            (out/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
            print("HEALTHCARE_LIVE_AUDIT",json.dumps(item,ensure_ascii=False),flush=True)
            page.close()
    browser.close()
summary={"cases":len(report),"home_observed":sum("home" in r for r in report),"failed_to_observe":sum("home" not in r for r in report),"routes_observed":sum(x.get("status")=="content changed" for r in report for x in r["routes"])}
print("HEALTHCARE_LIVE_SUMMARY",json.dumps(summary),flush=True)
if not summary["home_observed"]:
    raise SystemExit("No live website could be inspected")
