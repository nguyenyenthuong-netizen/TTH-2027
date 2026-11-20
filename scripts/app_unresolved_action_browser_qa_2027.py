#!/usr/bin/env python3
"""Browser test for unresolved App links: visible honest fallback, no fake route.
Desktop and mobile; explicitly not a test of all 120 App buttons.
"""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
path=(root/"healthcare-app"/"index.html").resolve()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 for w,h in [(1440,900),(390,844)]:
  page=browser.new_page(viewport={"width":w,"height":h},locale="vi-VN")
  errors=[];page.on("pageerror",lambda exc:errors.append(str(exc)))
  page.goto(path.as_uri()+"?demo=1",wait_until="domcontentloaded")
  catalog=page.locator("#catalog");catalog.click()
  page.locator("#find").fill("BatDau_DongY")
  page.locator("#pages button").first.click()
  page.frame_locator("iframe").locator('a[href="#"]').first.click()
  notice=page.frame_locator("iframe").locator("#tth-app-action-notice")
  notice.wait_for(state="visible",timeout=6000)
  content=notice.inner_text()
  if "chưa được tích hợp" not in content:raise SystemExit("Legal link incorrectly claims working document "+repr(content))
  if "BatDau_DongY.html" not in page.url:raise SystemExit("Unresolved anchor unexpectedly navigated")
  if errors:raise SystemExit("Browser JS error "+repr(errors[:3]))
  results.append({"viewport":[w,h],"legal_notice":True,"unchanged_route":True,"errors":0})
  page.close()
 browser.close()
print("APP_UNRESOLVED_BROWSER_QA",json.dumps(results,ensure_ascii=False))
