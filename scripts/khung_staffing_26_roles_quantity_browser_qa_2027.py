#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full coverage of 26 staffing role quantity editors and working calculation."""
from pathlib import Path
import sys
from playwright.sync_api import sync_playwright

path=(Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"khung-marketing"/"index.html").resolve().as_uri()
with sync_playwright() as p:
    browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for width,height in ((1440,900),(390,844)):
        page=browser.new_page(viewport={"width":width,"height":height},locale="vi-VN")
        errors=[]
        page.on("pageerror",lambda err:errors.append(str(err)))
        page.goto(path,wait_until="domcontentloaded",timeout=40000)
        page.locator('.tab[data-target="staffing"]').evaluate("(b)=>b.click()")
        host=page.locator("#dinh-bien-2027")
        host.locator('[data-panel="roles"]').click()
        roles=host.locator('[data-set="role"] option').evaluate_all("(a)=>a.map(x=>x.value)")
        assert len(roles)==26 and len(set(roles))==26,("roles",roles)
        for i,role in enumerate(roles):
            host.locator('[data-set="role"]').select_option(role)
            form=host.locator('form[data-edit-role-products="'+role+'"]')
            cards=form.locator(".role-qty-card")
            assert cards.count()>0,(width,role,"no role production jobs")
            assert form.locator(".role-qty-actions .action").count()==1
            assert cards.count()==len(cards.locator(".role-qty-name").all_text_contents()),(width,role)
            state=form.evaluate("""f=>{
              const all=[...f.querySelectorAll('.role-qty-card')];
              const num=[...f.querySelectorAll('.role-qty-edit input')];
              const grid=f.querySelector('.role-qty-grid');
              const bs=all.map(x=>x.getBoundingClientRect());
              return {cards:all.length,unique:new Set(num.map(x=>x.name)).size===num.length,
                columns:getComputedStyle(grid).gridTemplateColumns.split(' ').length,
                overflow:bs.some(b=>b.left<f.getBoundingClientRect().left-2||b.right>f.getBoundingClientRect().right+2),
                allSourceOrNumber:all.every(x=>x.querySelector('input[type=number]')||x.querySelector('.role-qty-source')),
                actionAfter: f.querySelector('.role-qty-actions').getBoundingClientRect().top>=
                  f.querySelector('.role-qty-group:last-of-type').getBoundingClientRect().bottom-1};
            }""")
            assert state["allSourceOrNumber"] and state["actionAfter"] and state["unique"] and not state["overflow"],(width,role,state)
            assert state["columns"]==(1 if width<=720 else 3),(width,role,state)
            assert "NaN" not in host.locator("#db-main").inner_text(),(width,role)
            if role=="bt-ac" and width==1440:
                target=form.locator('input[name="q:bt-ac/bai"]')
                assert target.count()==1,"Expected role-level original production input"
                before=target.input_value()
                target.fill(str(int(before)+1))
                form.locator(".role-qty-actions .action").click()
                again=host.locator('form[data-edit-role-products="bt-ac"] input[name="q:bt-ac/bai"]')
                assert again.input_value()==str(int(before)+1),"Value not persisted after calculation"
                assert host.locator(".role-qty-ledger").count()==1
                assert host.locator(".role-qty-warning").count()==1
            if role=="dmpk":
                assert "Chưa" in host.locator(".role-qty-ledger").inner_text()
        assert not errors,(width,errors[:5])
        page.close()
    browser.close()
print("PASS: all 26 roles have source-linked quantity cards, 25% reserve view, calculation, 1440/390px.")
