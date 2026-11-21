"""Mục 05: nghiệp thu goc nhin quan tri / van hanh da nen tang tren Chrome.
Bao toan toan bo 30 o kenh du kien va 224 gio/thang W, khong phan bo gia so cho 4 nen tang gop.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys

file=(Path(sys.argv[1])/"khung-marketing"/"index.html").resolve()
source=file.read_text("utf-8")
assert "tth-platform-ops-dual-view-2027" in source
assert "assets:platformOperationsPanel" in source
assert "tth-platform-ops-dual-view-2027" in source
url=file.as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width,height in ((1440,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},locale="vi-VN")
        errors=[]
        page.on("pageerror",lambda err:errors.append(str(err)))
        page.goto(url,wait_until="domcontentloaded",timeout=30000)
        page.locator('.tab[data-target="staffing"]').evaluate("(e)=>e.click()")
        host=page.locator("#dinh-bien-2027")
        host.locator('[data-panel="assets"]').click(timeout=15000)
        body=host.locator("#db-main")
        body.get_by_text("Quản trị và vận hành đa nền tảng",exact=True).wait_for(timeout=15000)
        view=body.inner_text()
        for required in ["224","30","14","Facebook","TikTok","CHƯA TÁCH 4 NỀN TẢNG"]:
            assert required in view,(width,"admin",required)
        # Changing the presentation must not alter the role workload or invent distinct channel counts.
        host.locator('[data-set="platformMode"]').select_option("operate")
        body.get_by_text("Luồng giao việc 6 bước, một mã nguồn xuyên suốt").wait_for(timeout=10000)
        assert "Facebook" in body.inner_text()
        host.locator('[data-set="platformFilter"]').select_option("youtube")
        assert "CHƯA phân bổ riêng YouTube" in body.inner_text(),width
        host.locator('[data-set="platformGroup"]').select_option("g2")
        assert "Nhóm thương hiệu 2" in body.inner_text(),width
        host.locator('[data-set="platformFilter"]').select_option("zalo")
        assert "Zalo OA" in body.inner_text(),width
        host.locator('[data-set="platformMode"]').select_option("manage")
        assert "224" in body.inner_text(),width
        assert not errors,(width,errors)
        dims=host.evaluate('(h)=>{const a=h.shadowRoot.querySelector(".app");return [a.scrollWidth,a.clientWidth]}')
        assert dims[0]<=dims[1]+4,(width,dims)
        page.close()
    browser.close()
print("PASS PLATFORM UX: 30 channel slots, 224 hours/month, 2 user modes, 6 platforms, no invented platform counts, desktop/mobile")
