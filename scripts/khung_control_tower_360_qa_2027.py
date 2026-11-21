#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Release gate for the 360 control tower: source integrity, all-month ledgers, real browser."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
import json, re, subprocess, sys
root=Path(sys.argv[1])
path=root/"khung-marketing"/"index.html"
html=path.read_text("utf-8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',html)
assert m
model=json.loads(m.group(1))["dinh_bien_theo_dau_ra_2027"]
c=model["control_360_2027"]
assert len(model["roles"])==26 and sum(model["seats"].values())==36
assert c["outcomesDraft"]==7 and c["unapprovedResultKpis"]==25
assert c["projectsInPlan"]==24 and c["highlightOutputs"]==132 and c["highlightSteps"]==660
assert c["highlightBooking"]=="CHUA_CHO_PHEP_CONG_TAI"
assert "tth-control-tower-360-2027" in html
assert "executive:controlTower360" in html
assert len(model["dedup_scope_audit_2027"]["openItems"])>=8

script_dir=Path("pages-overrides/2027-1911-final/dinh-bien")
module=(script_dir/"cms_calc.js").read_text("utf-8")+"\n"+(script_dir/"calculate.js").read_text("utf-8")
node_test=r"""
const fs=require('fs');
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf-8')).dinh_bien_theo_dau_ra_2027;
for(const scenario of ['base','high','opt']){
 const run=TTHStaffing.simulate(d,scenario,{});
 for(let m=1;m<=12;m++){
  const split={R:0,H:0,K:0,T:0,U:0,G:0};
  for(const w of run.works)split[w.item.kind]+=w.hours[m-1];
  const total=run.roll(run.monthly(Object.keys(run.roles)).slice(m-1,m))[0]||null;
  // roll returns an object, not an array.
 }
 const months=run.monthly(Object.keys(run.roles));
 for(let m=1;m<=12;m++){
  const byKind={R:0,H:0,K:0,T:0,U:0,G:0};
  for(const w of run.works)byKind[w.item.kind]+=w.hours[m-1];
  const ledger=months[m-1];
  const actual=Object.values(byKind).reduce((a,b)=>a+b,0);
  if(Math.abs(actual-ledger.regular-ledger.incident)>1e-6)
   throw Error('W 360 mismatch '+scenario+' T'+m+' '+actual+'/'+ledger.regular+'/'+ledger.incident);
  const workDirect=byKind.R+byKind.H+byKind.K+byKind.T+byKind.G;
  if(Math.abs(workDirect-ledger.regular)>1e-6)throw Error('R/H/K/T wrong '+scenario+' T'+m);
 }
 console.log('PASS CONTROL 360 LEDGER '+scenario+' 12 months: all stages match chargeable W without double counting');
}
"""
# Remove a dead branch in the test before execution; keep one clearly checked monthly path.
node_test=node_test.replace(
 " for(let m=1;m<=12;m++){\n  const split={R:0,H:0,K:0,T:0,U:0,G:0};\n  for(const w of run.works)split[w.item.kind]+=w.hours[m-1];\n  const total=run.roll(run.monthly(Object.keys(run.roles)).slice(m-1,m))[0]||null;\n  // roll returns an object, not an array.\n }\n","")
with TemporaryDirectory() as t:
 test=Path(t)/"test.cjs"
 test.write_text(module+"\n"+node_test,"utf-8")
 data=Path(t)/"data.json"
 data.write_text(json.dumps({"dinh_bien_theo_dau_ra_2027":model},ensure_ascii=False),"utf-8")
 proc=subprocess.run(["node",str(test),str(data)],capture_output=True,text=True)
 assert proc.returncode==0,proc.stderr
 print(proc.stdout)

with sync_playwright() as p:
 browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 for width,height in ((1440,900),(390,844)):
  page=browser.new_page(viewport={"width":width,"height":height},locale="vi-VN")
  errors=[]
  page.on("pageerror",lambda exc:errors.append(str(exc)))
  page.goto(path.resolve().as_uri(),wait_until="domcontentloaded",timeout=30000)
  page.locator('.tab[data-target="staffing"]').evaluate("(x)=>x.click()")
  host=page.locator("#dinh-bien-2027")
  host.locator('[data-panel="executive"]').click(timeout=15000)
  view=host.locator("#db-main")
  view.get_by_text("Điều hành Marketing 360° – hiệu quả, công việc và quỹ giờ",exact=True).wait_for(timeout=10000)
  for term in ["24 dự án","132 đầu ra","Định biên và dự phòng","Chưa thể chứng minh","Giờ kênh số bình quân/tháng"]:
   assert term in view.inner_text(),(width,term)
  metrics=host.locator(".metric b").all_text_contents()
  assert len(metrics)==6,metrics
  assert metrics[1].strip().replace(".","").isdigit(),metrics
  host.locator('[data-set="towerFilter"]').select_option("all")
  assert "Tất cả điểm phân công" in host.locator('[data-set="towerFilter"]').inner_text()
  host.locator('[data-set="period"]').select_option("4")
  assert "tháng 4" in view.inner_text()
  host.locator('[data-set="scenario"]').select_option("high")
  assert "Kịch bản" in view.inner_text()
  host.locator('[data-set="scenario"]').select_option("base")
  host.locator('[data-set="towerFilter"]').select_option("unknown")
  assert "CHƯA CÓ QUỸ GIỜ" in view.inner_text(),width
  host.locator('[data-set="towerFilter"]').select_option("priority")
  host.locator('button[data-go="assets"]').first.click()
  assert host.get_by_text("Quản trị và vận hành đa nền tảng",exact=True).is_visible()
  host.locator('[data-panel="executive"]').click()
  assert not errors,(width,errors)
  dims=host.evaluate('(h)=>{const a=h.shadowRoot.querySelector(".app");return [a.scrollWidth,a.clientWidth]}')
  assert dims[0] <= dims[1]+3,(width,dims)
  page.close()
 browser.close()
print("PASS CONTROL 360 CHROME: six decision areas, 3 scenarios, 12 months, view switch, desktop/mobile")
