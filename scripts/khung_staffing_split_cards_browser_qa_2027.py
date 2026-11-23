#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real Chrome acceptance for four grouped staffing split editors.

Checks actual Muc 05 UI: labels, value fields, submit and preserved calculations,
responsive display, independent values for all 2-seat positions.
"""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

page_path=(Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"khung-marketing"/"index.html").resolve()
source=page_path.read_text("utf-8")
assert "splitQuantityEditor" in source, "Split editor must be included in built site"
assert ".split-metric" in source, "Split styles must be included in built site"
roles={"bt-ac":(10,3),"tk-a":(6,2),"md-ac":(4,2),"qc-a":(8,2)}
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width,height in ((1440,900),(900,850),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1,locale="vi-VN")
        errors=[]
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(page_path.as_uri(),wait_until="domcontentloaded",timeout=30000)
        page.locator('.tab[data-target="staffing"]').evaluate("(b)=>b.click()")
        host=page.locator("#dinh-bien-2027")
        host.locator('[data-panel="roadmap"]').click()
        for role,(expected,groups) in roles.items():
            host.locator('[data-set="deliveryRole"]').select_option(role)
            expander=host.get_by_text("Căn cứ phân sản phẩm giữa hệ thống và bệnh viện",exact=True)
            expander.click()
            form=host.locator('form[data-split-role="'+role+'"]')
            form.wait_for(state="visible")
            cards=form.locator(".split-metric")
            assert cards.count()==expected,(width,role,cards.count(),expected)
            headings=form.locator(".split-group-title")
            assert headings.count()==groups,(width,role,headings.count(),groups)
            assert form.locator(".split-actions .action").count()==1
            assert form.locator("input[type=number]").count()==expected
            assert len(form.locator("input[name]").evaluate_all("(xs)=>xs.map(x=>x.name)"))==expected
            assert form.locator("input[name]").evaluate_all("(xs)=>xs.every(x=>x.required && x.hasAttribute('min') && x.hasAttribute('max'))")
            assert form.locator("input[name]").evaluate_all("(xs)=>new Set(xs.map(x=>x.name)).size===xs.length")
            geometry=form.evaluate("""f=>{
                const grid=f.querySelector('.split-grid'),css=getComputedStyle(grid);
                const cards=[...f.querySelectorAll('.split-metric')];
                const action=f.querySelector('.split-actions');
                const groups=[...f.querySelectorAll('.split-group')];
                const close=(a,b)=>Math.abs(a-b)<=1.5;
                const boxes=cards.map(c=>c.getBoundingClientRect());
                const noOverlap=boxes.every((r,i)=>boxes.every((s,j)=>i===j||
                    r.right<=s.left+1||s.right<=r.left+1||
                    r.bottom<=s.top+1||s.bottom<=r.top+1));
                return {columns:css.gridTemplateColumns.split(' ').length,noOverlap,
                    allInBounds:groups.every(g=>{
                      const outer=g.getBoundingClientRect();
                      return [...g.querySelectorAll('.split-metric')].every(c=>{
                        const r=c.getBoundingClientRect();
                        return r.left>=outer.left-1.5 && r.right<=outer.right+1.5;
                      });
                    }),
                    actionAtBottom:action.getBoundingClientRect().top>=groups.at(-1).getBoundingClientRect().bottom-1,
                    labelSize:getComputedStyle(cards[0].querySelector('.split-metric-title')).fontSize};
            }""")
            target_cols=1 if width<=690 else 2 if width<=1160 else 3
            assert geometry["columns"]==target_cols,(width,role,geometry)
            assert geometry["noOverlap"] and geometry["allInBounds"] and geometry["actionAtBottom"],(width,role,geometry)
            assert float(geometry["labelSize"].replace("px",""))>=15,(width,role,geometry)
            if role=="bt-ac":
                assert headings.all_text_contents()==["Nội dung chính","Kiểm duyệt và phối hợp","Nội dung hỗ trợ"]
                assert form.locator("input[name=kt]").input_value()=="9",(width,"original draft value should be 9")
                assert host.locator('[data-set="chiefSeat"]').count()==1
                if width==1440:
                    form.locator("input[name=kt]").fill("8")
                    form.locator(".split-actions .action").click()
                    form=host.locator('form[data-split-role="bt-ac"]')
                    assert form.locator("input[name=kt]").input_value()=="8","Submit did not persist test edit"
            outer=host.locator(".app").evaluate("(el)=>({client:el.clientWidth,scroll:el.scrollWidth})")
            assert outer["scroll"]<=outer["client"]+3,(width,role,outer)
        assert not errors,(width,errors[:5])
        page.close()
    browser.close()
print("PASS: 4 split editors, numeric state and recompute, role-specific groups, 1440/900/390px no overlap")
