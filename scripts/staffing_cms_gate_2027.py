#!/usr/bin/env python3
"""Pre-merge checks: 26 role staffing, CMS no zero defaults, planned assets, valid JS sources."""
from pathlib import Path
import json, subprocess, sys, tempfile
HERE=Path(__file__).resolve().parents[1]/"pages-overrides/2027-1911-final/dinh-bien"
sys.path.insert(0,str(HERE))
from operations import W,SEATS,SITES
from cms import build_cms,TYPES,UNITS
from register import PROFILES
C=build_cms()
assert len(SEATS)==26 and sum(SEATS.values())==36
assert len({w["id"] for w in W})==len(W)
assert set(x["role"] for x in W)==set(SEATS)
assert len(TYPES)==5 and len(UNITS)==14 and len([x for x in C["assets"] if x["kind"]=="Kênh số"])==30
assert sum(SEATS[k] for k in SEATS if k not in ('tn-a','tn-b','mdcs-a','mdcs-b','qhcs','dmpk'))==22
assert SEATS["dmpk"]==1 and SEATS["dl-2"]==SEATS["qlml"]==0
for u in UNITS:
  assert u["group"] in ("g1","g2") and u["state"] in ("dang-hoat-dong","can-xac-minh-moc","chua-kich-hoat")
for t in TYPES:
  assert len(t["mins"])==len(t["maint"])==len(C["stages"])==8
  assert all(isinstance(x,int) and x>0 for x in t["mins"]+t["maint"])
for path in ["cms_calc.js","cms_ui.js","calculate.js","view.js","deliverables.js"]:
  subprocess.run(["node","--check",str(HERE/path)],check=True)
# Test the very same closure assembled in production, including all panel functions:
source=(HERE/"cms_calc.js").read_text()+"\n"+(HERE/"calculate.js").read_text()+"\n"+\
  (HERE/"view.js").read_text().replace("/* EMBED_DELIVERABLES */",(HERE/"deliverables.js").read_text()).replace("/* EMBED_CMS_UI */",(HERE/"cms_ui.js").read_text())
with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",suffix=".js") as t:
  t.write(source); t.flush(); subprocess.run(["node","--check",t.name],check=True)
with tempfile.TemporaryDirectory() as td:
  data=Path(td)/"fixture.json"
  data.write_text(json.dumps({"cms":{"types":[TYPES[0]],"units":[UNITS[0]],"stages":C["stages"]},
      "roles":{k:{"to":"tct"} for k in SEATS},"sites":[],"docs":[],"work":[],
      "factors":{},"highSite":{},"highClinic":{},"highSite":{},"highClinic":{}},ensure_ascii=False))
  node=(HERE/"cms_calc.js").read_text()+"\n"+(HERE/"calculate.js").read_text()+r"""
const fs=require('fs'),assert=require('assert');
const model=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let r=TTHStaffing.simulate(model,'base',{});assert(r.cms.unknown.length>=5);
assert(!r.roles['bt-ac']); // unknown quantity MUST NOT generate zero-work claim
const k='vinh/bac-si';
r=TTHStaffing.simulate(model,'base',{cms:{[k]:{base:2,reuse:1,maint:1,graphic:0,media:0,month:2}}});
const year=x=>r.monthly([x]).map(z=>z.setup+z.maint);
assert(Math.abs(r.roles['bt-ac'][1].cmsInitial-2*model.cms.types[0].mins[1]/60)<1e-8);
assert(!r.roles['bt-ac'][0].cmsInitial);  // no silent work before February
assert(Math.abs(r.roles['bt-ac'][3].cmsMaintain-model.cms.types[0].maint[1]/60)<1e-8);
assert(r.cms.tasks.find(t=>t.stage==='Nhập CMS dữ liệu có cấu trúc').q===2);
assert(r.cms.tasks.filter(t=>t.channel==='Website'&&t.stage==='Kiểm hiển thị website').length===1);
assert(r.cms.tasks.filter(t=>t.channel==='App'&&t.stage==='Kiểm hiển thị App').length===1);
const last=r.roll(r.monthly(Object.keys(r.roles)));assert(Math.abs(last.total-(last.regular+last.incident+last.maint+last.setup))<1e-6);
assert(r.cms.total.initial>0&&r.cms.total.maint>0);console.log("PASS CMS monthly, steps, unknowns, two platform checks");
"""
  script=Path(td)/"test.js";script.write_text(node,encoding="utf-8")
  subprocess.run(["node",str(script),str(data)],check=True)
print("PASS: 26 roles; 36 seats; 30 channel placeholders; 14 CMS units; syntax+monthly CMS formulas")
