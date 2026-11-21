/* Report actual baseline/high loads from the exact embedded Mục 05 model, by seat and month. */
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(process.argv[2],'utf8');
const match=html.match(/<script id="csdl" type="application\/json">([\s\S]*?)<\/script>/);
assert(match,'Embedded source missing');
const db=JSON.parse(match[1]);
const model=db.dinh_bien_theo_dau_ra_2027;
assert(model&&Object.keys(model.roles).length===26&&Object.values(model.seats).reduce((a,b)=>a+b,0)===36);
const TTHCms=require('../pages-overrides/2027-1911-final/dinh-bien/cms_calc.js');
const TTHStaffing=require('../pages-overrides/2027-1911-final/dinh-bien/calculate.js');
const sum=TTHStaffing.sum,months=TTHStaffing.months;
const edits={capacity:{week:47,days:6,leave:24,share:75},clinic:null,eligible:{},sites:{},hqVideo:{},splits:{},docs:{},work:{}};
const u={chiefSeat:'a'};
const scopeKeys=(r,role,site)=>Object.keys(r.roles).filter(k=>(!role||k.split('@')[0]===role)&&(!site||k.endsWith('@'+site)));
const roleKeys=(r,id,pool=false)=>{const ids=scopeKeys(r,id);return pool&&id==='dl-1'?[...ids,...scopeKeys(r,'dl-2')]:ids;};
const ctx={model,db,edits,u,scopeKeys,roleKeys,TTHStaffing,sum,months};
const dfile='pages-overrides/2027-1911-final/dinh-bien/deliverables.js';
vm.runInNewContext(fs.readFileSync(dfile,'utf8')+'\n globalThis.audit={poolReviews,seatMonths,slotShare,slotDoc,splitSeats};',ctx,{filename:dfile});
const {poolReviews,seatMonths,splitSeats}=ctx.audit;
for(const scenario of ['base','high','opt']){
 const run=TTHStaffing.simulate(model,scenario,edits);
 const pos=poolReviews(run);
 const enough=pos.filter(x=>x.review.annualExcess!==null);
 const peak=pos.filter(x=>x.review.periods?.some(z=>z.excess>0));
 const annual=pos.filter(x=>x.review.annualExcess>0);
 const missingCms=run.cms.unknown.length;
 const hr=run.roll(run.monthly(Object.keys(run.roles)));
 const records=peak.map(x=>({
   position:db.vi_tri.find(y=>y.id===x.id)?.ten||x.id,
   id:x.id,site:x.site||'TCT',seat:x.slot||null,
   annualHours:Math.round(x.review.annual.total*10)/10,
   annualExcess:Math.round(x.review.annualExcess*10)/10,
   monthLimit:x.review.planLimit,
   excessMonths:x.review.periods.filter(z=>z.excess>0).map(z=>({
      month:z.m,hours:Math.round(z.all*10)/10,
      excess:Math.round(z.excess*10)/10,
      dueToSetup:Math.round(z.setup*10)/10
   }))
 }));
 console.log('AUDIT_SCENARIO',scenario,JSON.stringify({
   positions:pos.length,compared:enough.length,monthlyOverload:peak.length,
   annualOverload:annual.length,unknownCms:missingCms,
   yearKnownHours:Math.round(hr.total),knownSetup:Math.round(hr.setup),knownMaint:Math.round(hr.maint),
   monthPlanHours:Math.round(run.cap.plan*10)/10,monthlyGrossHours:Math.round(run.cap.gross*10)/10,
   overloads:records
 }));
 if(scenario==='base'){
  const row=pos.find(x=>x.id==='qc-a'&&x.slot==='b');
  if(row) console.log('SPLIT_SEAT_QC_HOSPITAL',JSON.stringify({annualExcess:row.review.annualExcess,peak:row.review.peak}));
  const summary=pos.map(x=>({
   id:x.id,site:x.site,slot:x.slot,annualHours:Math.round(x.review.annual.total),
   annualExcess:x.review.annualExcess,peak:x.review.peak?.excess,
   incomplete:x.review.annualExcess===null}));
  console.log('ALL_POSITIONS_BASE',JSON.stringify(summary));
 }
}
const sample='vinh/bac-si';
const edited={...edits,cms:{[sample]:{base:40,reuse:4,maint:3,graphic:0,media:0,month:2}}};
const newrun=TTHStaffing.simulate(model,'base',edited),split=seatMonths(newrun,'bt-ac','b');
const row=newrun.monthly(['bt-ac']);
assert(split[1].cmsInitial>0,'CMS hours lost in individual seat');
assert(split[3].cmsMaintain>0,'CMS maint lost in individual seat');
const a=seatMonths(newrun,'bt-ac','a'),b=seatMonths(newrun,'bt-ac','b');
for(let m=0;m<12;m++)
 for(const k of ['regular','incident','setup','maint','cmsInitial','cmsMaintain']){
   assert(Math.abs(a[m][k]+b[m][k]-row[m][k])<1e-6,'Split mismatch '+k+' month '+(m+1));
 }
console.log('SPLIT_CMS_CHECK_PASS',JSON.stringify({initialB:split[1].cmsInitial,maintB:split[3].cmsMaintain}));
