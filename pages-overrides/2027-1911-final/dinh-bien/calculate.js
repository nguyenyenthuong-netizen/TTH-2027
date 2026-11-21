/* Calculations are independent of the interface. Monthly buckets are the source for every total. */
const TTHStaffing = (() => {
  const scenarios=['base','high','opt'];
  const months=Array.from({length:12},(_,i)=>i+1);
  const peak=m=>[4,9,11].includes(m);
  const sum=a=>a.reduce((x,y)=>x+y,0);
  const empty=()=>({direct:0,coord:0,check:0,fix:0,travel:0,regular:0,incident:0,setup:0,maint:0,lead:0,next:0,external:0});
  const timeKeys=['direct','coord','check','fix','travel'];
  const hqVideoPlan={g1:{short:9,complex:4,film:2},g2:{short:6,complex:3,film:1}};
  function capacity(settings={}){
    const weekly=settings.week??47, days=settings.days??6, leave=settings.leave??24, share=(settings.share??75)/100;
    const gross=(365/7*weekly-leave*weekly/days)/12, plan=gross*share;
    if(!(weekly>0&&days>0&&days<=7&&leave>=0&&gross>0&&share>0&&share<=1))throw Error('Thông số giờ khả dụng chưa hợp lệ.');
    return {gross,plan,share,reserve:gross-plan};
  }
  function periods(period,m){
    if(period==='m')return 1;
    if(period==='q')return m%3===0?1:0;
    if(period==='qs')return m%3===1?1:0;
    if(period.startsWith('y'))return m===Number(period.slice(1))?1:0;
    let count=0;
    // 52 weekly Tuesday closes, 26 fortnightly closes in the model calendar for 2027.
    for(let offset=0;offset<365;offset++){
      const d=new Date(Date.UTC(2027,0,1+offset));
      if(d.getUTCMonth()===m-1&&d.getUTCDay()===2&&(period==='w'||Math.floor(offset/7)%2===0))count++;
    }
    return count;
  }
  function compareHours(row,planLimit,totalLimit,includeSetup=true){
    const planned=row.regular+row.maint+(includeSetup?row.setup:0);
    const all=planned+row.incident;
    const excess=Math.max(0,planned-planLimit,all-totalLimit);
    return {planned,all,excess:excess<1e-7?0:excess};
  }
  function reviewPosition(run,keys,seats,clinicHours){
    const monthly=run.monthly(keys),annual=run.roll(monthly);
    const isClinic=keys.some(k=>k.endsWith('@clinic'));
    const planLimit=isClinic?clinicHours:seats*run.cap.plan;
    const totalLimit=isClinic?clinicHours:seats*run.cap.gross;
    const result={annual,avgHours:annual.total/12,planLimit,totalLimit,periods:[],peak:null,annualExcess:null};
    if(planLimit==null||totalLimit==null||seats===0)return result;
    result.annualExcess=compareHours(annual,planLimit*12,totalLimit*12).excess;
    result.periods=monthly.map((v,i)=>{
      const full=compareHours(v,planLimit,totalLimit);
      const ongoing=compareHours(v,planLimit,totalLimit,false);
      return {m:i+1,...full,ongoing:ongoing.excess,setup:full.excess-ongoing.excess};
    });
    result.peak=result.periods.reduce((best,next)=>next.excess>best.excess?next:best);
    return result;
  }
  const periodMap={};['m','w','2w','q','qs','y9','y12'].forEach(p=>{periodMap[p]=months.map(m=>periods(p,m))});
  function simulate(data,scenario='base',edits={}){
    const cap=capacity(edits.capacity), roles={};const consume=(r,m)=>{if(!roles[r])roles[r]=months.map(empty);return roles[r][m-1]};
    const drivers=(s,m)=>Object.fromEntries(Object.entries(s.inputs).map(([k,v])=>[k,(edits.sites?.[s.id]?.[k]??v)+(scenario==='high'&&peak(m)?(s.group==='clinic'?data.highClinic:data.highSite)[k]||0:0)]));
    const siteInputs=Object.fromEntries(data.sites.map(s=>[s.id,months.map(m=>drivers(s,m))]));
    const siteRoles=s=>s.group==='clinic'?['dmpk']:s.group==='g1'?['tn-a','mdcs-a','qhcs']:['tn-b','mdcs-b'];
    const key=(role,site)=>site?role+'@'+site:role;
    const works=[]; const resolveQ=(q,site,m)=>{
      if(typeof q==='number')return q;
      if(q[0]==='@'){
        const v=siteInputs[site][m-1], k=q.slice(1);
        return k==='lot'?v.v1+v.v2+v.v3+v.photo+v.evt:v[k];
      }
      const [g,k]=q.split(':');const count=cat=>sum(data.sites.filter(s=>s.group===g).map(s=>siteInputs[s.id][m-1][cat]));
      const plus=scenario==='high'&&peak(m)?1:0;
      const planned=type=>(edits.hqVideo?.[g]?.[type]??hqVideoPlan[g][type])+plus;
      const review=count('v2')+count('v3');
      if(k==='review')return review;
      if(k==='script')return review+planned('short')+planned('complex')+planned('film');
      return planned(k);
    };
    for(const item of data.work){
      const isLocal=data.roles[item.role].to==='coso';
      const sites=isLocal?data.sites.filter(s=>siteRoles(s).includes(item.role)).map(s=>s.id):[null];
      for(const site of sites){
        const id=key(item.id,site),rid=key(item.role,site),override=edits.work?.[id]||{},t=override.t??item.t;
        const row={id,rid,item,site,qty:[],hours:[],segments:[],t};
        for(const m of months){
          const v=consume(rid,m);const freq=periodMap[item.period][m-1];
          // A regional transfer needs a new authority and a corresponding reduction at the former manager.
          const q=item.kind==='G'?0:((override.q??resolveQ(item.q,site,m))+(scenario==='high'&&peak(m)?item.extra:0))*freq;
          const parts=t.map(min=>q*min/60);
          // Only the confirmed eligible subset changes rate. No blanket AI/software productivity credit.
          if(scenario==='opt'&&item.code==='c1'&&edits.eligible?.[item.role]){
            const eligible=Math.min(q,edits.eligible[item.role]);parts[0]-=eligible*Math.max(0,t[0]-12)/60;
          }
          const hours=sum(parts);row.qty.push(q);row.hours.push(hours);row.segments.push(parts);
          v[item.kind==='U'?'incident':'regular']+=hours;
          if(item.kind==='T')v.lead+=hours;
          timeKeys.forEach((k,i)=>v[k]+=parts[i]);
        }
        works.push(row);
      }
    }
    const docs=[];
    // Resolve prerequisites independently from the order in which the catalogue is displayed.
    const dependencies={'M-6':['B-1','B-2'],'QC-1':['B-1'],'QC-2':['B-2'],'B-3':['B-1','B-2'],'B-4':['B-1','B-2'],'B-5':['B-1','B-2'],'B-7':['QC-4'],'MAU-QC':['M-6'],'ND-WEB1':['YC-WEB'],'ND-WEB2':['YC-WEB']};
    const finishes=new Map();
    function startMonth(d){
      const start=edits.docs?.[d.id]?.month??d.month;
      return Math.min(12,Math.max(start,...(dependencies[d.code]||[]).map(code=>finishMonth(code)+1)));
    }
    function finishMonth(code){
      if(!finishes.has(code)){
        const end=data.docs.filter(d=>d.code===code).map(d=>{
          const units=edits.docs?.[d.id]?.count??d.count;
          const window=Math.max(0,Math.min(2,(d.deadline??12)-startMonth(d)));
          const lastOffset=scenario==='opt'?(units>1?Math.min(window,units-1):d.order%(window+1)):0;
          return units?Math.min(12,startMonth(d)+lastOffset):0;
        });finishes.set(code,Math.max(0,...end));
      }
      return finishes.get(code);
    }
    for(const d of data.docs){
      const change=edits.docs?.[d.id]||{};const action=d.link?'link':(change.action??d.action), units=change.count??d.count;
      const m0=change.month??d.month, scheduled=startMonth(d), rate=data.factors[action], p=d.profile, monthly=months.map(()=>[]);
      const add=(m,r,stage,h,type)=>{
        if(!(h>0))return;
        const internal=Object.hasOwn(data.roles,r.split('@')[0]);
        monthly[m-1].push({r,stage,h,type,internal});if(internal)consume(r,m)[type]+=h;
      };
      const mayMaintain=!['link','bo','soat'].includes(action);
      for(let i=0;i<units;i++){
        // Each unit closes after its stages. In the optimized scenario deliver independent lots over up to three months.
        const window=Math.max(0,Math.min(2,(d.deadline??12)-scheduled));
        const closeMonth=scenario==='opt'?Math.min(12,scheduled+((units>1?i:d.order)%(window+1))):scheduled;
        if(i===0&&d.link)continue;
        const stages=[['Đối chiếu bản gốc',d.owner],['Soạn hoặc cập nhật bản gốc',d.writer],['Kiểm chuẩn độc lập',d.reviewer],['Thử áp dụng',d.tester],['Trình và ký theo thẩm quyền','ky'],['Bàn giao, lưu phiên bản',d.owner]];
        stages.forEach(([label,r],j)=>add(closeMonth,r,label,p[j]*rate[j]/60,'setup'));
        for(const [r,minutes,label] of d.coauthors)add(closeMonth,r,label,minutes*rate[1]/60,'setup');
        if(mayMaintain){
          for(let j=1;j<=d.freq;j++){
            const due=Math.ceil(12*j/d.freq);
            if(action==='giu'||due>closeMonth)add(due,d.owner,'Rà phiên bản sau bàn giao',p[6]/60,'maint');
            add(due,d.owner,'Rà soát trong một năm vận hành đủ kỳ',p[6]/60,'next');
          }
        }
      }
      const closeMonths=monthly.flatMap((a,i)=>a.some(x=>x.type==='setup')?[i+1]:[]);
      const finish=closeMonths.length?Math.max(...closeMonths):null;
      docs.push({d,action,units,monthly,m0,scheduled,finish,deadline:d.deadline??null,late:finish!==null&&d.deadline!=null&&finish>d.deadline,depends:dependencies[d.code]||[]});
    }
    function monthly(keys){return months.map((m)=>{
      const v=empty();for(const k of keys){const x=roles[k]?.[m-1];if(x)for(const field in v)v[field]+=x[field]};return v;
    });}
    function roll(array){
      const v=empty();for(const x of array)for(const field in v)v[field]+=x[field];
      const p=v.regular+v.maint,u=v.incident;v.total=p+u+v.setup;v.run=p+u;
      const req=(p,u,n)=>Math.max(p/(cap.plan*n),(p+u)/(cap.gross*n));
      v.fteRun=req(p,u,array.length);v.fte=req(p+v.setup,u,array.length);
      v.fteNext=req(v.regular+v.next,u,array.length);v.fteProject=v.fte-v.fteRun;
      const peaks=array.map(x=>req(x.regular+x.maint+x.setup,x.incident,1));v.peak=Math.max(...peaks);v.peakIndex=peaks.indexOf(v.peak);return v;
    }
    return {scenario,cap,works,docs,roles,monthly,roll,siteInputs,siteRoles};
  }
  return {simulate,capacity,scenarios,sum,months,hqVideoPlan,reviewPosition};
})();
if(typeof module!=='undefined'&&module.exports)module.exports=TTHStaffing;
