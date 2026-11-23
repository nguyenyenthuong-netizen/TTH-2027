#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Browser regression for CRM / Marketing two-phase cards at real site output."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import sys
from playwright.sync_api import sync_playwright

site=Path(sys.argv[1] if len(sys.argv)>1 else "_site").resolve()
page_file=site/"ke-hoach-mkt-2027"/"index.html"
khung_file=site/"khung-marketing"/"index.html"
src=page_file.read_text("utf-8")
assert 'class="phase-summary"' in src, "Missing two-phase structured cards"
assert 'class="phase-gate"' in src, "Missing separate gate block"
assert "<small><b>Cổng chuyển:" not in src, "Legacy inline gate still in source"
assert "phase-exclusion" in src
assert "phase-summary" in khung_file.read_text("utf-8"), "Embedded Khung did not receive new two-phase cards"

handler=functools.partial(SimpleHTTPRequestHandler,directory=str(site))
server=ThreadingHTTPServer(("127.0.0.1",0),handler)
thread=Thread(target=server.serve_forever,daemon=True)
thread.start()
url="http://127.0.0.1:%s/ke-hoach-mkt-2027/"%server.server_port
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="chrome",headless=True,
            args=["--no-sandbox","--disable-dev-shm-usage"])
        for width,height in [(1600,900),(1280,850),(390,844)]:
            page=browser.new_page(viewport={"width":width,"height":height},locale="vi-VN")
            errors=[]
            page.on("pageerror",lambda err:errors.append(str(err)))
            page.goto(url,wait_until="domcontentloaded",timeout=30000)
            page.locator('.tab[data-tab="stages"]').click()
            cards=page.locator(".summary-grid .sectioncard")
            cards.first.wait_for(state="visible",timeout=30000)
            assert cards.count()==2,(width,cards.count())
            gate_count=page.locator(".summary-grid .phase-gate").count()
            assert gate_count==4,(width,gate_count)
            labels=page.locator(".summary-grid .phase-item .phase-title b").all_text_contents()
            assert labels==["Giai đoạn 1","Giai đoạn 2","Giai đoạn 1","Giai đoạn 2"],labels
            report=page.evaluate("""() => {
              const cards=[...document.querySelectorAll('.summary-grid .sectioncard')];
              const tol=1.5;
              return cards.map(card=>{
                const phases=[...card.querySelectorAll('.phase-item')];
                const footer=card.querySelector('.phase-exclusion');
                const records=phases.map((el,i)=>{
                  const title=el.querySelector('.phase-title');
                  const gate=el.querySelector('.phase-gate');
                  const t=title.getBoundingClientRect(),g=gate.getBoundingClientRect();
                  const next=phases[i+1]?.getBoundingClientRect();
                  return {title: title.innerText,gate:gate.innerText,
                    separated:getComputedStyle(gate).display==='block' && g.top>=t.bottom+4,
                    inBounds:g.left>=card.getBoundingClientRect().left-tol && g.right<=card.getBoundingClientRect().right+tol,
                    beforeNext: !next || g.bottom<=next.top+tol};
                });
                return {title:card.querySelector('h3').textContent,records,
                  footerAfterGate:footer.getBoundingClientRect().top>=phases.at(-1).getBoundingClientRect().bottom-1};
              });
            }""")
            for card in report:
                assert card["footerAfterGate"],(width,card)
                for item in card["records"]:
                    assert item["separated"] and item["inBounds"] and item["beforeNext"],(width,item)
                    assert "Cổng chuyển:" in item["gate"],(width,item)
            overflow=page.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            assert overflow<=3,(width,"horizontal overflow",overflow)
            assert not errors,(width,errors)
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
print("PASS two-phase cards: 4 separate transfer gates; 1600/1280/390; no collisions or missing text")
