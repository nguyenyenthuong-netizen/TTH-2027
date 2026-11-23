#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys
path=(Path(sys.argv[1])/"khung-marketing"/"index.html").resolve().as_uri()
with sync_playwright() as p:
 browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 for width in (1600,1280,390):
  page=browser.new_page(viewport={"width":width,"height":900})
  errs=[];page.on("pageerror",lambda e:errs.append(str(e)))
  page.goto(path,wait_until="domcontentloaded",timeout=30000)
  page.locator('.tab[data-target="org"]').click()
  left=page.locator("#v-org .org-left.mkt-cvt-branch")
  right=page.locator("#v-org .org-right.mkt-cvt-branch")
  assert left.count()==right.count()==1
  assert left.locator('[data-jd="cvt"]').count()==1
  assert right.locator('[data-jd="cvt-2"]').count()==1
  assert left.locator(".mkt-cvt-connector").inner_text().find("01 tổ")>=0
  assert right.locator(".mkt-cvt-connector").inner_text().find("02 tổ")>=0
  assert right.locator(".org-right-teams>.col").count()==2
  assert page.locator("#v-org .mkt-org-local-row").count()==1
  geom=page.evaluate("""() => {
    let a=document.querySelector('#v-org .org-left.mkt-cvt-branch');
    let b=document.querySelector('#v-org .org-right.mkt-cvt-branch');
    let x=a.querySelector('[data-jd="cvt"]'), y=b.querySelector('[data-jd="cvt-2"]');
    let team=a.querySelector('details.grp'), teams=b.querySelector('.org-right-teams');
    let A=a.getBoundingClientRect(),B=b.getBoundingClientRect();
    return {branches:innerWidth<=1100?B.top>=A.bottom-4:B.left>=A.right-3,
      left:team.getBoundingClientRect().top>x.getBoundingClientRect().bottom,
      right:teams.getBoundingClientRect().top>y.getBoundingClientRect().bottom,
      noOverflow:document.documentElement.scrollWidth<=document.documentElement.clientWidth+4}
  }""")
  assert all(geom.values()),(width,geom)
  page.locator('#v-org .gbtn[data-g="2"]').click()
  assert left.is_visible() and right.is_visible()
  page.locator('#v-org .gbtn[data-g=""]').click()
  cvt=left.locator('[data-jd="cvt"]')
  cvt.click();assert cvt.get_attribute("aria-expanded")=="true"
  cvt.click();assert cvt.get_attribute("aria-expanded")=="false"
  assert not errs,(width,errs)
  page.close()
 browser.close()
print("PASS CVT visual hierarchy: 1 team + hospitals / 2 teams, filters and detail buttons, 3 viewports")
