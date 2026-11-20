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
  iframe=page.locator("iframe").element_handle().content_frame()
  before_url=iframe.url
  # Chỉ thử liên kết thật sự chưa có trình xử lý; liên kết đã có onclick
  # được quyền xử lý trước, không phải trường hợp thông báo dự phòng.
  anchors=page.frame_locator("iframe").locator(
      'a[href="#"]:not([onclick]):not([data-route]):not([data-href])')
  if anchors.count()==0:raise SystemExit("Không có liên kết thiếu đích phù hợp để thử trên trang đồng ý")
  anchor=anchors.first
  label=anchor.inner_text().strip()
  anchor.click()
  notice=page.frame_locator("iframe").locator("#tth-app-action-notice")
  notice.wait_for(state="visible",timeout=6000)
  content=notice.inner_text()
  if not any(p in content for p in ("chưa được tích hợp","chưa kết nối","chưa có màn hình đích","chỉ đang được minh họa")):
      raise SystemExit("Liên kết thiếu đích không có thông báo trung thực: "+repr(content))
  if iframe.url!=before_url:
      raise SystemExit("Unresolved anchor unexpectedly navigated: "+repr((before_url,iframe.url)))
  if errors:raise SystemExit("Browser JS error "+repr(errors[:3]))
  results.append({"viewport":[w,h],"legal_notice":True,"unchanged_route":True,"errors":0})
  page.close()
 browser.close()
print("APP_UNRESOLVED_BROWSER_QA",json.dumps(results,ensure_ascii=False))
