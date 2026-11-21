/* CMS workload additive ledger. Quantities undefined are unknown, never zero.
 * One original source record can be used by both website and App; only view checks repeat.
 * Minutes are scenario assumptions until signed off by source owner and process lead.
 */
const TTHCms=(()=>{
 const nums=x=>x!==undefined&&x!==null&&x!==''&&Number.isFinite(Number(x))&&Number(x)>=0?Number(x):null;
 const sum=a=>a.reduce((x,y)=>x+y,0);
 const months=Array.from({length:12},(_,i)=>i+1);
 const roles=u=>({
   intake:u.intake,
   editorial:u.group==='g1'?'bt-ac':'bt-b',
   visual:u.group==='g1'?'tk-a':'tk-b',
   media:u.group==='g1'?'md-ac':'md-b',
   reviewer:u.group==='g1'?'qlth-a':'qlth-bc',
   manager:'qlsps'
 });
 function simulate(cms,edits,consume){
  if(!cms)return {tasks:[],items:[],unknown:[],total:{initial:0,maint:0,external:0},activated:[]};
  const tasks=[],items=[],unknown=[],activated=[];
  const cfg=edits?.cms||{}, activation=edits?.cmsUnits||{};
  let initial=0,maint=0,external=0;
  const event=(row,m,actor,stage,perUnit,qty,kind,channel,control)=>{
    const internal=actor!=='nguon-doi-tac'&&actor!=='chu-du-lieu'&&actor!=='so-hoa'&&actor!=='cong-nghe';
    const h=qty===null?null:qty*perUnit/60;
    const rec={id:row.id+'-'+stage+'-'+kind,unit:row.unit,type:row.type,role:actor,stage,mins:perUnit,q:qty,m,
      h,kind,channel:channel||'CMS chung',control:control||'',internal};
    tasks.push(rec);
    if(h!=null&&h>0){
      if(!internal){external+=h;return;}
      const v=consume(actor,m);
      if(kind==='initial'){v.setup+=h;v.cmsInitial=(v.cmsInitial||0)+h;initial+=h;}
      else {v.maint+=h;v.cmsMaintain=(v.cmsMaintain||0)+h;maint+=h;}
      if(/Biên tập|Chuẩn bị|Nhập|Công bố/.test(stage))v.direct+=h;
      else if(/Kiểm|Đối chiếu/.test(stage))v.check+=h;
      else v.coord+=h;
    }
  };
  for(const u of cms.units){
    const activeStart=u.state==='dang-hoat-dong'?1:nums(activation[u.id]);
    const isActive=activeStart!==null&&activeStart>=1&&activeStart<=12;
    if(isActive)activated.push(u.id);
    const rt=roles(u);
    for(const type of cms.types){
      const id=u.id+'/'+type.id,chg=cfg[id]||{},start=Math.max(1,Math.min(12,Math.floor(nums(chg.month)??type.first)));
      const values={base:nums(chg.base),reuse:nums(chg.reuse),maint:nums(chg.maint),graphic:nums(chg.graphic),media:nums(chg.media)};
      const row={id,unit:u.id,unitName:u.name,group:u.group,type:type.id,typeName:type.name,active:isActive,month:start,values,source:u.state,
        owner:type.external,roles:rt,site:u.site,late:start>3};
      items.push(row);
      if(!isActive){unknown.push({id,unit:u.id,type:type.id,what:'Mốc vận hành/bàn giao chưa được xác nhận',owner:'Ban Giám đốc cơ sở/Quản lý thương hiệu'});continue;}
      for(const k of ['base','reuse','maint','graphic','media'])if(values[k]===null)
        unknown.push({id,unit:u.id,type:type.id,what:({base:'Số hồ sơ gốc phân biệt mã nguồn',reuse:'Số liên kết hồ sơ gốc dùng chung',maint:'Số sửa đổi thêm mới mỗi tháng NGOÀI sản lượng W đã tính',graphic:'Số đồ họa mới ngoài W thiết kế',media:'Số tư liệu mới ngoài W media'})[k],owner:'Đầu mối cơ sở/Quản lý thương hiệu/Quản lý sản phẩm số'});
      const month=Math.max(start,activeStart);
      // Every original record has one editorial/structural entry and one QA per platform.
      const actors=[rt.intake,rt.editorial,rt.manager,rt.reviewer,rt.manager,rt.manager,rt.manager,rt.intake];
      const check=['Đơn vị cung cấp dữ liệu nguồn đã xác nhận','Biên tập không xác nhận nguồn thay đơn vị','Mã hồ sơ, CMS chung; không nhân đôi website/App','Kiểm độc lập với người nhập','Kiểm hiển thị website riêng','Kiểm hiển thị App riêng','Đủ cửa duyệt mới công bố','Biên bản giao nhận của đơn vị'];
      type.mins.forEach((per,i)=>event(row,month,actors[i],cms.stages[i],per,values.base,'initial',
        i===4?'Website':i===5?'App':'CMS chung',check[i]));
      // Source confirmation is external to Marketing. This is a separate active-time estimate,
      // never counted as a Marketing seat.
      event(row,month,'chu-du-lieu','Xác nhận chuyên môn/giấy phép/giá của dữ liệu gốc (ngoài Marketing)',25,values.base,'initial','Nguồn đơn vị',type.external);
      const reuseStages=[['Tiếp nhận yêu cầu gắn địa điểm từ mã nguồn đã xác nhận',rt.intake,12],
        ['Gắn cơ sở vào CMS mà không biên tập lại hồ sơ gốc',rt.manager,17],
        ['Kiểm quy thuộc hồ sơ/cơ sở độc lập',rt.reviewer,12],
        ['Kiểm hiển thị địa điểm trên website',rt.manager,8],
        ['Kiểm hiển thị địa điểm trên App',rt.manager,8]];
      for(const [stage,role,per] of reuseStages)event(row,month,role,stage,per,values.reuse,'initial','CMS chung','Giữ mã hồ sơ gốc, kiểm mã cơ sở, không nhân sản phẩm gốc');
      event(row,month,rt.visual,'Chuẩn bị đồ họa CMS mới ngoài định mức thiết kế W',75,values.graphic,'initial','Kho tài sản số','Chỉ nhập khi có yêu cầu và chứng cứ KHÔNG tính trong W');
      event(row,month,rt.media,'Chuẩn bị ảnh/tư liệu CMS mới ngoài định mức Media W',90,values.media,'initial','Kho tư liệu','Không tính ảnh/video đã hạch toán trong W');
      // Recurrence starts no earlier than month 4, after the unit's validated handover.
      for(let m=Math.max(4,month+1);m<=12;m++){
       const maintStages=[rt.intake,rt.editorial,rt.manager,rt.reviewer,rt.manager,rt.manager,rt.manager,rt.intake];
       type.maint.forEach((per,i)=>event(row,m,maintStages[i],cms.stages[i]+' · cập nhật tăng thêm',per,values.maint,
         'maint',i===4?'Website':i===5?'App':'CMS chung','Chỉ công việc THÊM ngoài lượng trang web/SEO đang tính trong W'));
       event(row,m,'chu-du-lieu','Xác nhận nguồn cập nhật ngoài Marketing',15,values.maint,'maint','Nguồn đơn vị',type.external);
      }
    }
  }
  const totals={initial,maint,external};
  return {tasks,items,unknown,total:totals,activated};
 }
 return {simulate};
})();
if(typeof module!=='undefined'&&module.exports)module.exports=TTHCms;
