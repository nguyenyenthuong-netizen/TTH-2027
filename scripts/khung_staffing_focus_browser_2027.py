"""Real Chrome smoke test for report ledger and a non-cramped, reversible focus window."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
p=(Path(sys.argv[1])/'khung-marketing'/'index.html').resolve()
url=p.as_uri()
with sync_playwright() as playwright:
    browser=playwright.chromium.launch(channel='chrome',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
    for width,height in [(1440,900),(390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        errors=[]
        page.on('pageerror',lambda exc:errors.append(str(exc)))
        page.goto(url,wait_until='domcontentloaded',timeout=30000)
        page.locator('.tab[data-target="staffing"]').evaluate('(b)=>b.click()')
        host=page.locator('#dinh-bien-2027')
        host.locator('.app').wait_for(state='visible',timeout=30000)
        host.locator('[data-panel="docs"]').click()
        assert host.get_by_text('0,7 giờ kiểm chuẩn',exact=False).count()>=1
        button=host.locator('[data-wide="toggle"]')
        button.click()
        app=host.locator('.app')
        assert 'reader-wide' in app.get_attribute('class')
        bounds=app.bounding_box()
        assert bounds and bounds['width']>=width-40,(width,bounds)
        assert bounds['height']>=height-40,(height,bounds)
        assert app.evaluate('(a)=>a.scrollWidth <= a.clientWidth + 3'), 'Window spills horizontally'
        assert host.locator('.tbl.doc-responsibility').count()>=1
        page.keyboard.press('Escape')
        assert 'reader-wide' not in app.get_attribute('class')
        assert button.inner_text()=='Mở rộng bảng'
        assert not errors,(width,errors)
        page.close()
    browser.close()
print('PASS: Chrome desktop 1440 / mobile 390; report note, focus width, Esc, no clipping errors')
