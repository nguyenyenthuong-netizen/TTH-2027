"""Acceptance gate for the stage-specific load ledger and scope audit.
Runs the actual production JS calculator on all 3 planning scenarios in Node.
Every hour must reconcile by role/site/month/category to its source row.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json,subprocess,re,sys

root=Path(sys.argv[1])
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s)
assert m,"Missing master framework data"
data=json.loads(m.group(1))
model=data["dinh_bien_theo_dau_ra_2027"]
audit=model["dedup_scope_audit_2027"]
assert audit["roles"]==26
assert audit["workflowOutputs"]==568
assert audit["workflowMarketing"]==356,(audit["workflowMarketing"],audit["workflowExternal"])
assert audit["workflowExternal"]==212
assert audit["mtcvLines"]==sum(len(x)-1 for x in model["jd"].values())
assert audit["mtcvNeedsVerification"]>=1
assert audit["channelsUnverified"]>0
assert len(audit["perRole"])==26
assert sum(1 for x in model["work"] if x["id"]=="tp/bc-tuan-kiem")==1
assert sum(model["seats"].values())==36
srcdir=Path("pages-overrides/2027-1911-final/dinh-bien")
js=srcdir.joinpath("cms_calc.js").read_text("utf-8")+"\n"+srcdir.joinpath("calculate.js").read_text("utf-8")
test=r"""
const fs=require('fs');
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8')).dinh_bien_theo_dau_ra_2027;
const buckets=new Map();
function add(r,m,cat,h){
  if(!(h>0))return;
  const key=r+'|'+m+'|'+cat;buckets.set(key,(buckets.get(key)||0)+h);
}
for(const scenario of ['base','high','opt']){
  buckets.clear();
  const run=TTHStaffing.simulate(d,scenario,{});
  // Operational ledger: one costed output/product role is charged once, by segment.
  for(const w of run.works){
    w.hours.forEach((h,i)=>add(w.rid,i+1,w.item.kind==='U'?'incident':'regular',h));
    w.hours.forEach((h,i)=>{
      const parts=w.segments[i].reduce((a,b)=>a+b,0);
      if(Math.abs(parts-h)>1e-6)throw Error('work parts mismatch '+w.id+' T'+(i+1));
    });
  }
  // Document setup / maintenance ledger, by the person responsible for that stage.
  for(const doc of run.docs)doc.monthly.forEach((items,i)=>{
    for(const x of items)if(x.internal&&x.type!=='next')add(x.r,i+1,x.type,x.h);
  });
  // CMS ledger, only activated known counts; NEVER invent missing quantities.
  for(const task of run.cms.tasks){
    if(task.internal && task.h!==null)
      add(task.role,task.m,task.kind==='initial'?'setup':'maint',task.h);
  }
  // Every accumulated hour must agree with the production calculator, not just all-up totals.
  for(const [rid,calendar] of Object.entries(run.roles)){
    calendar.forEach((v,i)=>{
      for(const cat of ['regular','incident','setup','maint']){
        const expected=buckets.get(rid+'|'+(i+1)+'|'+cat)||0;
        if(Math.abs(expected-v[cat])>1e-6)
          throw Error('ledger mismatch '+scenario+' '+rid+' T'+(i+1)+' '+cat+' = '+expected+' vs '+v[cat]);
      }
    });
  }
  for(const [key,value] of buckets){
    const [rid,m,cat]=key.split('|');
    if(!run.roles[rid])throw Error('orphan ledger '+key);
  }
  const total=Object.values(run.roles).flat().reduce((a,v)=>a+v.regular+v.incident+v.setup+v.maint,0);
  console.log('PASS LEDGER',scenario,'roles',Object.keys(run.roles).length,'hours',total.toFixed(1),'workEntries',run.works.length,'docEntries',run.docs.length,'unknownCMS',run.cms.unknown.length);
}
"""
assert 'function dedupAuditPanel2027()' in s
assert 'audit:dedupAuditPanel2027' in s
with TemporaryDirectory() as temp:
    testfile=Path(temp)/"ledger_qa.cjs"
    testfile.write_text(js+"\n"+test,"utf-8")
    infile=Path(temp)/"model.json"
    infile.write_text(json.dumps({"dinh_bien_theo_dau_ra_2027":model},ensure_ascii=False),"utf-8")
    check=subprocess.run(["node","--check",str(testfile)],capture_output=True,text=True)
    assert check.returncode==0,check.stderr
    result=subprocess.run(["node",str(testfile),str(infile)],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    print(result.stdout)
print('PASS MTCV: 26 roles, 568 workflow rows, 356 inside / 212 outside; stage ledger reconciled without double counting')
