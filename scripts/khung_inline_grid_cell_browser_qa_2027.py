#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chrome regression: links and parentheses in III.0 / 7.3 remain in value column."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys

url=(Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"khung-marketing"/"index.html").resolve().as_uri()

with sync_playwright() as driver:
    browser=driver.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width,height in [(1440,900),(390,844)]:
        page=browser.new_page(viewport={"width":width,"height":height},locale="vi-VN")
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.goto(url,wait_until="domcontentloaded",timeout=30000)
        page.locator('.tab[data-target="jd"]').evaluate("(el)=>el.click()")
        # III.0 is initially closed. Test the real table after opening details.
        page.locator("#m-III-0").evaluate("(section)=>section.closest('details').open=true")
        row=page.locator("#m-III-0 table.t tbody tr").first
        row.wait_for(timeout=20000)
        page.wait_for_function("""() => {
            const tr=document.querySelector('#m-III-0 table.t tbody tr');
            return tr && tr.closest('table').classList.contains('tth-card')
                && tr.cells[2].querySelector(':scope > .tth-grid-value');
        }""",timeout=20000)
        assert row.locator("td").count()==6,"III.0 has lost a column"
        s=row.locator("td").nth(2)
        assert "01 (đang trống, mục 28, số 29)" in " ".join(s.inner_text().split()),(width,s.inner_text())
        assert s.locator("a.xref").inner_text()=="28"
        assert s.locator("a.xref").get_attribute("href")=="#m-28"
        assert row.locator("td").nth(5).locator("a.xref").inner_text()=="24.2"
        # Check that no direct inline text/links remain separate grid items.
        data=page.evaluate("""() => {
          const td=document.querySelector('#m-III-0 table.t tbody tr td:nth-child(3)');
          const value=td.querySelector(':scope > .tth-grid-value');
          const link=td.querySelector('a.xref');
          const valueRect=value.getBoundingClientRect();
          const linkRect=link.getBoundingClientRect();
          const css=getComputedStyle(value);
          return {
           nodes:td.childNodes.length,
           onlyWrapped:td.childNodes.length===1 && td.firstChild===value,
           valueColumn:css.gridColumnStart,
           linkDisplay:getComputedStyle(link).display,
           left:valueRect.left,right:valueRect.right,
           linkLeft:linkRect.left,linkRight:linkRect.right,
           text:value.textContent
          };
        }""")
        assert data["onlyWrapped"],(width,data)
        assert data["valueColumn"]=="2",(width,data)
        assert data["linkDisplay"]=="inline",(width,data)
        assert data["linkLeft"]>=data["left"]-2 and data["linkRight"]<=data["right"]+2,(width,data)
        assert not errors,(width,errors[:5])
        page.close()
    browser.close()
print("PASS CHROME III.0: 1440/390; links 28/24.2, parentheses and all value text stay in right column")
