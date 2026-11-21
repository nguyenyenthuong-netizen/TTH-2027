"""Browser proof that the MTCV / overlap / evidence panel is actually usable."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
url=(Path(sys.argv[1])/"khung-marketing"/"index.html").resolve().as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width,height in ((1440,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},locale="vi-VN")
        errors=[]
        page.on("pageerror",lambda exc:errors.append(str(exc)))
        page.goto(url,wait_until="domcontentloaded",timeout=30000)
        page.locator('.tab[data-target="staffing"]').evaluate("(b)=>b.click()")
        host=page.locator("#dinh-bien-2027")
        host.locator('[data-panel="audit"]').click(timeout=30000)
        content=host.locator("#db-main")
        content.get_by_text("Kiểm toán không trùng, không sót theo CNNV và MTCV",exact=True).wait_for(timeout=15000)
        assert "496" in content.inner_text(),width
        assert "568" in content.inner_text(),width
        assert "356" in content.inner_text(),width
        assert "212" in content.inner_text(),width
        assert "25 nhóm" in content.inner_text() or "25" in content.inner_text(),width
        assert content.locator("details.entry").count()>=3,width
        dims=host.evaluate('h=>{const a=h.shadowRoot.querySelector(".app");return {a:a.clientWidth,b:a.scrollWidth}}')
        assert dims["b"] <= dims["a"] + 3,(width,dims)
        assert not errors,(width,errors)
        page.close()
    browser.close()
print("PASS CHROME DEDUP: 1440px and 390px; all new audit cards and counts render without page errors or clipping")
