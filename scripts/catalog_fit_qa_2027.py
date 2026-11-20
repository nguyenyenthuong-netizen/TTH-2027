#!/usr/bin/env python3
"""Regression gate for the TTH Group one-screen Vercel link directory.
Checks original logo, branding, no old search strip, five Vercel links and viewport fit.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import re,sys,json
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
pagefile=root/"index.html"
assert pagefile.is_file(),"Missing catalog index"
html=pagefile.read_text("utf-8")
assert "TTH Group <span>· Marketing toàn hệ thống</span>" in html,"Wrong Group title"
assert "TTH Healthcare · Marketing toàn hệ thống" not in html,"Outdated brand header"
assert "Tìm tên giao diện" not in html and 'type="search"' not in html,"Obsolete search bar"
assert "tth-marketing-2027-slide.vercel.app" not in html,"Duplicate presentation link is forbidden"
assert "Phần mềm quản trị Marketing</strong>" not in html and "tth-quan-tri-marketing-16112026" not in html and 'href="quan-tri-marketing/"' not in html,"Marketing software must not appear in GitHub catalog"
assert (root/"trinh-chieu-marketing"/"assets"/"tth-logo.png").stat().st_size>1000,"Original TTH Group logo asset unavailable"
from urllib.parse import urlparse
with sync_playwright() as p:
 browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 checks=[]
 for width,height in [(1440,900),(1280,720),(390,844),(375,667)]:
  page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
  errs=[]
  page.on("pageerror",lambda error:errs.append(str(error)))
  page.goto(pagefile.resolve().as_uri(),wait_until="load")
  page.wait_for_timeout(100)
  result=page.evaluate("""() => {
   const logo=document.querySelector('.brand img');
   const cards=[...document.querySelectorAll('a.tile')];
   const main=document.querySelector('main');
   return {title:document.title,viewport:[innerWidth,innerHeight],
     scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,
     cards:cards.length,validUrls:cards.every(a=>/^https:\\/\\/[^/]+\\.vercel\\.app\\/$/.test(a.href)),
     logoLoaded:!!(logo&&logo.complete&&logo.naturalWidth>0),
     logoInside:!!(logo&&logo.getBoundingClientRect().width>0),
     clippedCards:cards.filter(c=>c.scrollHeight>c.clientHeight+2||c.scrollWidth>c.clientWidth+2)
       .map(c=>c.textContent.trim().slice(0,55)),
     bottom:Math.round(document.querySelector('footer').getBoundingClientRect().bottom)};
  }""")
  if errs or not result["logoLoaded"] or not result["logoInside"]:
   raise AssertionError(f"Catalog image/JS error at {width}x{height}: {result} {errs}")
  if result["cards"]!=5 or not result["validUrls"]:
   raise AssertionError(f"Incorrect five Vercel destinations: {result}")
  if result["scrollHeight"]>height+1 or result["scrollWidth"]>width+1 or result["bottom"]>height+1:
   raise AssertionError(f"Catalog not contained in one viewport at {width}x{height}: {result}")
  if result["clippedCards"]:
   raise AssertionError(f"Catalog card text clipped at {width}x{height}: {result}")
  out=root.parent/"artifacts"/"tth-catalog";out.mkdir(parents=True,exist_ok=True)
  page.screenshot(path=str(out/f"catalog-{width}x{height}.png"),full_page=False)
  print("CATALOG_SCREEN_QA",json.dumps(result,ensure_ascii=False))
  checks.append(result)
  page.close()
 browser.close()
print("TTH_CATALOG_OK",len(checks),"viewport sizes; original Group logo; five Vercel links; no scroll")
