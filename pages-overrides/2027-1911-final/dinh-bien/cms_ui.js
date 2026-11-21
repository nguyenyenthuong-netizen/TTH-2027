/* In-framework evidence ledger: quantities not supplied are UNKNOWN, not zero. */
const cmsOptional=(k,v)=>'<input type="number" min="0" max="99999" step="1" name="'+e(k)+'" value="'+e(v)+'">';
function cmsPanel(){
 const run=getRun(),catalog=model.cms,unit=catalog.units.find(x=>x.id===u.cmsUnit)||catalog.units[0],
 type=catalog.types.find(x=>x.id===u.cmsType)||catalog.types[0],key=unit.id+'/'+type.id,
 item=run.cms.items.find(x=>x.id===key),cv=edits.cms?.[key]||{},
 active=unit.state==='dang-hoat-dong'||edits.cmsUnits?.[unit.id]!=null,
 selected=run.cms.tasks.filter(x=>x.unit===unit.id&&x.type===type.id&&(!u.period||x.m===u.period));
 const val=k=>cv[k]==null?'':cv[k];
 const data=selected.map(x=>[e('T'+x.m+' · '+(x.kind==='initial'?'Ban đầu':'Duy trì')),
   e(x.stage),e(name(x.role)),e(x.channel),nu(x.mins),
   x.q==null?'<b>CHƯA XÁC NHẬN</b>':nu(x.q),x.h==null?'Chưa tính':nu(x.h),e(x.control)]);
 const missing=run.cms.unknown.filter(x=>x.id===key);
 const overview=catalog.units.map(x=>{const t=run.cms.tasks.filter(z=>z.unit===x.id&&z.internal&&z.h!=null);
 return [btn(x.name,'cms',x.id),e(x.group==='g1'?'Nhóm thương hiệu 1':'Nhóm thương hiệu 2'),e(x.state),
  nu(sum(t.filter(z=>z.kind==='initial').map(z=>z.h))),
  nu(sum(t.filter(z=>z.kind==='maint').map(z=>z.h))),
  e(String(run.cms.unknown.filter(z=>z.unit===x.id).length)+' trường chưa xác nhận')];});
 const controls='<div class="control">'+fLabel('Đơn vị','<select data-set="cmsUnit">'+opt(Object.fromEntries(catalog.units.map(x=>[x.id,x.name])),u.cmsUnit)+'</select>')+
 fLabel('Loại hồ sơ','<select data-set="cmsType">'+opt(Object.fromEntries(catalog.types.map(x=>[x.id,x.name])),u.cmsType)+'</select>')+selPeriod()+'</div>';
 const form='<form class="form" data-cms-row="'+e(key)+'">'+
 fLabel('Số hồ sơ GỐC có mã duy nhất',cmsOptional('base',val('base')))+
 fLabel('Số liên kết với cơ sở từ mã hồ sơ gốc có sẵn',cmsOptional('reuse',val('reuse')))+
 fLabel('Số hồ sơ cần cập nhật THÊM mỗi tháng, ngoài khối lượng W',cmsOptional('maint',val('maint')))+
 fLabel('Số đồ họa mới NGOÀI công việc thiết kế W',cmsOptional('graphic',val('graphic')))+
 fLabel('Số tư liệu mới NGOÀI công việc Media W',cmsOptional('media',val('media')))+
 fLabel('Tháng hoàn tất đợt đầu','<select name="month">'+opt(Object.fromEntries(months.map(m=>[m,'Tháng '+m])),String(cv.month??type.first))+'</select>')+
 apply+'</form>';
 const activation=active?'':'<form class="form" data-cms-activate="'+e(unit.id)+'"><p>Đơn vị chưa có thời điểm bắt đầu được xác nhận. Chọn tháng khi có căn cứ phân công/bàn giao để mở phép tính.</p>'+fLabel('Tháng bắt đầu','<select name="month"><option value="">Chưa xác minh</option>'+months.map(m=>'<option value="'+m+'">Tháng '+m+'</option>').join('')+'</select>')+apply+'</form>';
 return '<h3>CMS Website và App – số hồ sơ và giờ từng công đoạn</h3>'+
 '<p class="note"><b>Số hồ sơ chưa được kiểm kê không được tính là 0.</b> Biên soạn/nhập dữ liệu chung một lần, kiểm website và App tính riêng. Dữ liệu chuyên môn, giấy phép và giá do chủ nguồn xác nhận. Các định mức phút là giả định chờ đo thực tế.</p>'+
 metrics([[nu(run.cms.total.initial),'Giờ thiết lập CMS đã nhập'],[nu(run.cms.total.maint),'Giờ duy trì CMS đã nhập'],[nu(run.cms.unknown.length),'Trường CMS chưa có căn cứ']])+
 detail('Toàn bộ đơn vị – so giờ và dữ liệu còn thiếu',table(['Đơn vị','Nhóm','Trạng thái','Giờ thiết lập','Giờ duy trì','Phần chưa có số'],overview,[3,4]),true)+
 controls+'<h4>'+e(unit.name)+' · '+e(type.name)+'</h4>'+
 '<p><b>Chủ nguồn:</b> '+e(type.external)+'. <b>Người biên tập:</b> '+e(name(item.roles.editorial))+
 '. <b>Nhập/công bố CMS:</b> '+e(name(item.roles.manager))+'. <b>Kiểm độc lập:</b> '+e(name(item.roles.reviewer))+
 '. <b>Đầu mối:</b> '+e(name(item.roles.intake))+'.</p>'+activation+(active?form:'')+
 '<p class="fine">Để trống = chưa xác minh; nhập 0 = đã xác minh không phát sinh. Số hồ sơ bác sĩ có mặt tại nhiều cơ sở phải kiểm mã định danh: nguồn gốc chỉ tính một lần, gắn cơ sở là công đoạn riêng. Duy trì CMS chỉ nhập phần ngoài số trang đã có trong W và SEO, không cộng trùng.</p>'+
 detail('Sản lượng × phút từng bước = giờ theo người, CMS chung, website và App',table(
 ['Giai đoạn/tháng','Công đoạn','Người thực hiện','Nơi','Phút/lượt','Lượt','Giờ','Điểm kiểm soát'],data,[4,5,6]),true)+
 (missing.length?'<p class="note"><b>Thiếu:</b> '+e(missing.map(x=>x.what).join('; '))+'. Chủ cung cấp: đầu mối cơ sở, quản lý thương hiệu và chủ dữ liệu.</p>':'');
}
function assetsPanel(){
 const v=model.cms.assets.filter(x=>u.assetFilter==='all'||x.group===u.assetFilter);
 const rows=v.map(x=>[e(x.id),e(x.name),e(x.group==='g1'?'Nhóm thương hiệu 1':'Nhóm thương hiệu 2')+
 '<small>'+e(x.unit)+'</small>',e(x.owner)+'<small>Người giữ nghiệp vụ: '+e(name(x.keeper))+'</small>',
 e(x.status)+'<small>Ngày: '+e(x.date??'chưa xác minh')+'</small>',
 e(x.output)+'<small>Tránh trùng: '+e(x.counted_by)+'</small>']);
 return '<h3>Kiểm kê 30 kênh và toàn bộ nhóm tài sản nghiệp vụ</h3>'+
 '<p class="note"><b>30 là số kênh tổng hợp đã có trong sổ nguồn, chưa phải danh sách tài khoản kiểm chứng.</b> K-KK- là mã ô kiểm kê tạm. Mọi tài sản chưa xác nhận URL, chủ sở hữu, ngày hiệu lực, trạng thái và tần suất chăm sóc đều là khoản tải chưa kết luận.</p>'+
 metrics([[nu(model.cms.assets.filter(x=>x.kind==='Kênh số').length),'Ô kiểm kê 30 kênh'],[nu(model.cms.assets.length),'Ô tài sản và kênh'],[nu(model.cms.assets.filter(x=>x.status.includes('Chưa')).length),'Chưa xác minh trạng thái']])+
 '<div class="control">'+fLabel('Nhóm thương hiệu','<select data-set="assetFilter">'+opt({all:'Tất cả',g1:'Nhóm thương hiệu 1',g2:'Nhóm thương hiệu 2'},u.assetFilter)+'</select>')+'</div>'+
 table(['Mã','Tài sản/kênh','Phạm vi','Chủ sở hữu/người giữ','Trạng thái','Đầu ra và quy tắc tính'],rows)+
 '<p>Danh mục nguồn phải được đối chiếu với tài khoản thật, mã tài sản, điểm biển, màn hình, hệ thống số và lịch bàn giao. Chưa có thông tin đó, số giờ duy trì các tài sản này chưa đủ để khẳng định định biên.</p>';
}
function detailedPanel(){
 const run=getRun(),id=u.role,info=roleMap[id],
  keys=roleKeys(run,id,id==='dl-1'),works=run.works.filter(x=>x.item.role===id||(id==='dl-1'&&x.item.role==='dl-2')),
  cms=run.cms.tasks.filter(x=>x.internal&&(x.role.split('@')[0]===id||(id==='dl-1'&&x.role.split('@')[0]==='dl-2'))&&(!u.period||x.m===u.period)),
  dlist=run.docs.flatMap(x=>x.monthly.flatMap((a,i)=>(!u.period||i+1===u.period)?a.filter(z=>z.internal&&(z.r.split('@')[0]===id||(id==='dl-1'&&z.r.split('@')[0]==='dl-2'))&&z.type!=='next').map(z=>({d:x.d,act:z,m:i+1})):[])),
  capacity=id==='dmpk'?edits.clinic:id==='qlml'?null:model.seats[id]*run.cap.plan;
 const workload=months.filter(m=>!u.period||u.period===m).map(m=>{
  const z=run.monthly(keys)[m-1],
    docSetup=Math.max(0,z.setup-z.cmsInitial),docMaint=Math.max(0,z.maint-z.cmsMaintain),
    total=z.regular+z.incident+z.maint+z.setup,gap=capacity==null?null:Math.max(0,total-capacity);
  return ['T'+m,...[z.regular,docSetup,z.cmsInitial,docMaint,z.cmsMaintain,z.incident,total].map(nu),
    gap===null?'Chưa có quỹ giờ được duyệt':gap>0?'<b>Vượt '+format(gap)+' giờ</b>':'Phần đã lượng hóa nằm trong quỹ'];
 });
 const wrows=works.map(w=>{
  const q=u.period?w.qty[u.period-1]:sum(w.qty),h=u.period?w.hours[u.period-1]:sum(w.hours);
  return [btn(w.item.id+' · '+w.item.name,'roles',w.id),e(w.item.ref),
    e(w.site?siteTitle(w.site):'TCT / nhóm đúng MTCV'),nu(q),
    e(segment.map((x,i)=>x+': '+format(w.t[i])+' phút').join(' · ')),nu(h),e(name(w.rid))];
 });
 const drows=dlist.map(x=>['T'+x.m,btn(x.d.code+' · '+x.d.name,'docs',x.d.id),e(x.d.scope),e(x.act.stage),
 e(name(x.act.r)),nu(x.act.h*60),nu(x.act.h),'Kiểm: '+e(name(x.d.reviewer))+'; thử: '+e(name(x.d.tester))]);
 const crows=cms.map(x=>['T'+x.m,e(x.unit+' / '+x.type),e(x.stage),e(name(x.role)),
 x.q==null?'<b>Chưa xác minh</b>':nu(x.q),nu(x.mins),x.h==null?'Chưa tính':nu(x.h),e(x.control)]);
 const missing=cms.filter(x=>x.q==null).length;
 return '<h3>Toàn bộ sản phẩm, công đoạn, thời gian theo từng vị trí</h3>'+
 '<p>Chọn từng chức danh. Đầu ra chuyên môn, công đoạn xây dựng hệ thống và CMS đều truy vết đến MTCV, mã việc, người thực hiện, tháng và nguồn số lượng. Giờ CMS đã nằm trong tổng giờ; không cộng hai lần.</p>'+
 '<div class="control">'+roleSel()+selCase()+selPeriod()+'</div>'+
 '<h4>'+e(info.ten)+'</h4>'+
 stack([['Căn cứ MTCV/CNNV',e(info.phan_dinh_chu_tri_dau_ra||info.muc_dich)],
 ['Giới hạn trách nhiệm',e(info.phan_dinh_khong_thuoc_trach_nhiem)],
 ['Tuyến nhận/kiểm/duyệt',e(info.phan_dinh_ban_giao_dau_vao)+' · '+e(info.phan_dinh_kiem_duyet)],
 ['Suất cơ cấu / quỹ người thực có',id==='dl-2'?'Kiêm Đo lường; không có suất riêng':id==='qlml'?'Chưa kích hoạt':id==='dmpk'?'1 đầu mối kiêm nhiệm, giờ phân bổ chờ xác nhận':e(model.seats[id])+' suất; người thực có chờ Phòng Nhân lực xác minh'],
 ['Phạm vi tính thử',works.length+' sản phẩm chuyên môn; '+dlist.length+' công đoạn tài liệu; '+cms.length+' công đoạn CMS; '+missing+' công đoạn CMS chưa có số lượng']])+
 '<h4>I. Cân tải theo tháng (giờ)</h4>'+
 table(['Tháng','Chuyên môn / quản lý','Xây dựng hệ thống','CMS ban đầu','Duy trì tài liệu','CMS duy trì','Phát sinh','Tổng đã tính','Vượt quỹ kế hoạch'],workload,[1,2,3,4,5,6,7])+
 '<p class="note">Không coi giờ đã tính thấp hơn quỹ là bằng chứng đủ người khi còn đầu ra chưa có lượng, tài sản chưa kiểm, giờ Clinic/nhân sự thực có chưa đối chiếu. Chức danh 2 suất phải kiểm riêng phân công từng người.</p>'+
 detail('II. Toàn bộ đầu ra chuyên môn và 5 công đoạn (phút)',table(['Mã/đầu ra','Căn cứ','Đơn vị','Số lượng','Phút: làm, phối hợp, kiểm, sửa, đi','Giờ','Người thực hiện'],wrows,[3,5]),true)+
 detail('III. Lập, sửa, kiểm, thử, bàn giao tài liệu – giờ theo người',table(['Tháng','Mã/tên tài liệu','Phạm vi','Công đoạn','Người','Phút công đoạn','Giờ công đoạn','Kiểm và thử'],drows,[5,6]),true)+
 detail('IV. CMS – nguồn, biên tập, nhập, kiểm, công bố – giờ theo người',table(['Tháng','Đơn vị/hồ sơ','Công đoạn','Người','Lượng','Phút','Giờ','Căn cứ'],crows,[4,5,6]),true)+
 detail('V. Toàn bộ dòng MTCV gốc và đối chiếu phần thiếu',origOutputs(id))+
 '<p><strong>Điều kiện ra quyết định:</strong> phải chốt các trường chưa lượng hóa, người thực có, phút chuẩn và giờ khả dụng; không dùng số 0 cho dữ liệu thiếu, không xếp người vào việc ngoài MTCV.</p>';
}
/* Cảnh báo chuỗi tải: chỉ xét công đoạn nằm trên cùng tuyến phục vụ.
 * Không suy diễn thành sự cố đã xảy ra; dùng để chặn cam kết trước khi xác nhận.
 */
function cascadeExposurePanel(run,positions){
 const bottleneck=(role,month)=>positions.filter(x=>x.id===role&&x.review.periods?.some(p=>p.m===month&&p.excess>0));
 const chains=[
  {name:'Nhóm thương hiệu 1 – TTH',parts:[
    ['Định hướng/đặt hàng','qlth-a'],
    ['Biên tập nội dung','bt-ac'],
    ['Thiết kế','tk-a'],
    ['Media','md-ac'],
    ['Phát hành/kênh số','qc-a'],
    ['Đo lường','dl-1'],
    ['CMS website/App','qlsps']
  ]},
  {name:'Nhóm thương hiệu 2 – chuyên khoa và các thương hiệu còn lại',parts:[
    ['Định hướng/đặt hàng','qlth-bc'],
    ['Biên tập nội dung','bt-b'],
    ['Thiết kế','tk-b'],
    ['Media','md-b'],
    ['Phát hành/kênh số','qc-b'],
    ['Đo lường','dl-1'],
    ['CMS website/App','qlsps']
  ]}
 ];
 const rows=[];
 for(const month of months){
  const monthOver=positions.flatMap(x=>x.review.periods?.filter(p=>p.m===month&&p.excess>0).map(p=>({x,p}))||[]);
  const grossOver=monthOver.filter(({x,p})=>x.review.totalLimit!=null&&p.all>x.review.totalLimit+1e-7);
  const impacted=chains.map(chain=>{
   const parts=chain.parts.filter(([,id])=>bottleneck(id,month).length);
   return {chain,parts};
  }).filter(z=>z.parts.length);
  const downstream=impacted.filter(z=>z.parts.length>=2);
  const status=grossOver.length?'Ưu tiên xử lý ngay – vượt quỹ giờ tổng tham chiếu':
    downstream.length?'Nguy cơ dây chuyền – nhiều công đoạn cùng vượt quỹ kế hoạch':
    impacted.length?'Cảnh báo điểm nghẽn – cần điều phối trước khi nhận thêm việc':
    'Chưa phát hiện vượt trên phần đã lượng hóa';
  const causes=monthOver.sort((a,b)=>b.p.excess-a.p.excess).slice(0,4).map(({x,p})=>
    name(x.id)+(x.slot?' ('+slotLabel(x.slot)+')':x.site?' ('+siteTitle(x.site)+')':'')+
    ': +'+format(p.excess)+' giờ').join('; ');
  const chainLabel=impacted.map(z=>z.chain.name+': '+z.parts.map(([stage])=>stage).join(' + ')).join(' | ');
  rows.push(['T'+month,e(status),nu(monthOver.length),e(chainLabel||'Chưa xác định, vẫn thiếu kiểm kê tài sản/CMS'),
    e(causes||'Không có số vượt trong các khoản đã tính'),
    e(grossOver.length?'Tạm dừng cam kết việc bổ sung không khẩn cấp; với sự cố liên quan người bệnh hoặc truyền thông khẩn, kích hoạt người thay, nguồn lực dự phòng và phê duyệt ngoại lệ theo quyền.':
      downstream.length?'Ưu tiên giải phóng nút nghẽn theo công đoạn, kiểm lịch chéo và giờ người thay trước khi khóa mốc.':
      impacted.length?'Kiểm tuần cao điểm, người thay và quyền duyệt trước khi nhận thêm yêu cầu.':
      'Giữ dự phòng; chưa kết luận ổn định do số CMS/kênh/tài sản chưa chốt.')]);
 }
 return '<h4>3. Bản đồ nguy cơ ảnh hưởng dây chuyền theo tháng và nhóm thương hiệu</h4>'+
 '<p class="note">Khi nhiều công đoạn của cùng một luồng cùng vượt 141,4 giờ kế hoạch/người/tháng, cảnh báo <b>nguy cơ chậm dây chuyền</b>. Nếu bất kỳ vị trí nào vượt quỹ giờ tổng tham chiếu (188,6 giờ/người/tháng), ưu tiên giải quyết ngay. Các ngưỡng là giả định của mô hình và phải đối chiếu quy định giờ làm, lịch trực thực tế; không phải xác nhận đã có sự cố.</p>'+
 table(['Tháng','Cấp cảnh báo','Số suất vượt','Nhóm/thao tác có nguy cơ','Điểm nghẽn theo vị trí','Điều kiện điều phối'],rows,[2])+
 '<h4>4. Quy tắc chặn để tránh lan truyền chậm tiến độ</h4>'+
 table(['Cửa kiểm soát','Điều kiện cho phép đi tiếp','Khi chưa đạt'],[
 ['Nhận thêm việc, chiến dịch hoặc mở cơ sở','Phải có chỗ trong quỹ giờ của đúng vai, đúng tháng; đầu ra thường xuyên bắt buộc đã được bảo toàn và người thay có năng lực.','Không tự giao thêm bằng cách dùng dự phòng 25% như giờ thường xuyên; Trưởng phòng chủ trì điều chỉnh ưu tiên, thay người hoặc nguồn lực đúng thẩm quyền. Việc khẩn cấp phải xử lý theo tuyến sự cố, không trì hoãn vì chặn kế hoạch.'],
 ['Giao hạn sản xuất và chuyển công đoạn','Phiếu nhận có nguồn đầu vào, người nhận, thời gian làm/kiểm/sửa, mốc chốt; đầu ra của bước trước đạt chuẩn.','Không được phát hành thiếu hồ sơ; chuyển tín hiệu nghẽn về quản lý thương hiệu và chuyên viên trưởng đúng tuyến.'],
 ['Phát hành và công bố CMS','Nguồn y khoa/giá/giấy phép được xác nhận, kiểm độc lập, quyền công bố và kiểm website/App đã hoàn tất.','Dừng phát hành nội dung chưa đủ điều kiện; không đưa việc bị chặn thành sản lượng hoàn tất.'],
 ['Bàn giao nền tảng quý I','Tài liệu bắt buộc có phiên bản hợp lệ, đã thử, duyệt, hướng dẫn và nhận bàn giao; tải tháng 1–3 xử lý được.','Báo mốc bàn giao rủi ro và đề xuất điều phối có căn cứ; không tự dời mốc 31/03 hay bỏ hạng mục.'],
 ['Khóa kết luận định biên','Phải có số hồ sơ CMS/kênh/tài sản, M-6, giờ người thực có và sản lượng đã đối soát; không còn vượt tải không được xử lý.','Trạng thái quyết định vẫn là CHƯA ĐỦ CĂN CỨ; không kết luận 36 suất chắc chắn đủ/dư.']
 ])+
 '<p><strong>Tác động cần theo dõi:</strong> ngày trễ từng công đoạn, số yêu cầu bị trả lại, tỷ lệ làm lại, số sản phẩm đúng hạn, số lịch phát hành bị thay đổi, số tài liệu chậm nghiệm thu, chi phí tăng và các KPI bị ảnh hưởng. <strong>Chưa có số trễ thực tế thì không được tự gán</strong> số thiệt hại hoặc nguyên nhân.</p>';
}

function sufficiencyPanel(){
 const run=getRun(),all=poolReviews(run),
    known=run.roll(run.monthly(Object.keys(run.roles))),
    overload=all.filter(x=>x.review.periods?.some(q=>q.excess>0)),
    annual=all.filter(x=>x.review.annualExcess>0),
    confirmed=all.filter(x=>x.review.annualExcess!==null),
    other=all.filter(x=>x.review.annualExcess===null);
 const scenarioRows=['base','high','opt'].map(c=>{
    const roster=poolReviews(runs[c]);
    const p=roster.filter(x=>x.review.periods?.some(z=>z.excess>0));
    const y=roster.filter(x=>x.review.annualExcess>0);
    return [e(cases[c]),nu(runs[c].roll(runs[c].monthly(Object.keys(runs[c].roles))).total),
      nu(p.length),nu(y.length),
      nu(runs[c].cms.unknown.length),
      c===u.scenario?'<b>Đang xem</b>':'Chọn ở bộ lọc bên trên'];
 });
 const topRows=overload.map(x=>{
    const v=x.review,peak=v.periods.reduce((a,b)=>a.excess>=b.excess?a:b);
    return [positionLink(x),x.site?e(siteTitle(x.site)):'Tổng công ty',
      x.slot?e(slotLabel(x.slot)):String(x.seats)+' suất',
      nu(peak.m),nu(peak.all),nu(v.planLimit),nu(peak.excess),
      v.annualExcess>0?'<b>'+format(v.annualExcess)+' giờ/năm</b>':'Không vượt năm trên số đã tính'];
 }).sort((a,b)=>Number(String(b[6]).replace(/<[^>]+>/g,'').replace(',','.'))-Number(String(a[6]).replace(/<[^>]+>/g,'').replace(',','.')));
 const allRows=all.map(x=>{
    const unknown=run.cms.tasks.filter(t=>t.internal&&t.q==null&&x.keys.includes(t.role)).length,
        bad=x.review.periods?.filter(z=>z.excess>0)||[];
    return [positionLink(x),x.site?e(siteTitle(x.site)):'Tổng công ty',
      x.slot?e(slotLabel(x.slot)):String(x.seats),
      x.id==='dmpk'&&edits.clinic==null?'Chưa xác minh':nu(x.review.planLimit),
      bad.length?bad.map(z=>'T'+z.m+': +'+format(z.excess)+' giờ').join('; '):'Không vượt trên phần đã tính',
      nu(unknown),
      x.id==='qlml'?'Chưa kích hoạt':x.id==='dmpk'&&edits.clinic==null?'Chưa có quỹ Clinic':
      unknown?'Thiếu sản lượng CMS':bad.length?'Lấn quỹ dự phòng trong kịch bản':'Chưa đủ dữ liệu chốt đủ người'];
 });
 const critical='<p class="note"><b>KẾT LUẬN CHO BAN LÃNH ĐẠO: CHƯA ĐỦ CĂN CỨ XÁC NHẬN 36 SUẤT LÀ PHÙ HỢP.</b> Đã xuất hiện vị trí lấn quỹ dự phòng kế hoạch trong phần mô phỏng, trong khi sản lượng CMS, M-6, tài sản/kênh và nhân sự thực có chưa chốt. Đây là kết quả từ dữ liệu giả định theo MTCV, không phải chứng nhận đã đủ việc hoặc đủ người.</p>';
 const hasCmsUnknown=run.cms.unknown.length>0;
 const shortVerdict='<div class="note" style="border-left-color:#ed3237;background:#fff9f9">'+
 '<h4 style="margin:0 0 8px">Kết luận định biên: chưa đủ căn cứ ban hành cơ cấu 36 suất</h4>'+
 '<p><b>'+format(overload.length)+'/'+format(confirmed.length)+' đầu mối so được quỹ giờ có tháng vượt</b>; '+
 '<b>'+format(annual.length)+' đầu mối vượt kế hoạch cả năm</b>. Số còn lại chưa vượt trên phần việc đã định lượng, '+
 '<b>không có nghĩa là đã đủ người</b>. Quá tải theo tháng khác với thiếu biên chế dài hạn.</p>'+
 '<p>'+format(other.length)+' đầu mối chưa so được quỹ; '+
 (hasCmsUnknown?format(run.cms.unknown.length)+' trường CMS/chuyển giao còn thiếu số lượng và giờ thực tế.':'Sản lượng thực vẫn phải xác nhận.')+
 ' Chưa tính đủ việc xây mới, đào tạo SEO/CRM, duy trì hệ thống và người kiêm nhiệm nếu chưa gắn mã việc.</p></div>';
 const reserveCases=all.flatMap(x=>(x.review.periods||[]).filter(p=>p.excess>0).map(p=>{
  const plannedBeyond=Math.max(0,p.planned-x.review.planLimit);
  const grossBeyond=Math.max(0,p.all-x.review.totalLimit);
  const reserveUse=Math.max(0,Math.min(x.review.totalLimit-x.review.planLimit,p.all-x.review.planLimit));
  return {x,p,plannedBeyond,grossBeyond,reserveUse};
 })).sort((a,b)=>b.grossBeyond-a.grossBeyond||b.plannedBeyond-a.plannedBeyond);
 const reserveRows=reserveCases.map(({x,p,plannedBeyond,grossBeyond,reserveUse})=>[
    positionLink(x),e(x.site?siteTitle(x.site):'Tổng công ty'),e(x.slot?slotLabel(x.slot):String(x.seats)+' suất'),
    'T'+p.m,nu(p.planned),nu(p.all),nu(x.review.planLimit),nu(x.review.totalLimit),
    nu(reserveUse),nu(plannedBeyond),nu(grossBeyond),
    grossBeyond>0?'<b>Vượt tổng quỹ giờ tham chiếu</b>':plannedBeyond>0?'Việc kế hoạch lấn quỹ dự phòng':'Phát sinh dùng dự phòng'
 ]);
 const reserveExplanation='<h4>Giải thích quỹ 25% dự phòng</h4>'+
 '<p><b>Quỹ giờ khả dụng bình quân:</b> '+format(run.cap.gross)+' giờ/người/tháng. <b>75% dành cho kế hoạch:</b> '+format(run.cap.plan)+' giờ. <b>25% để dự phòng:</b> '+format(run.cap.reserve)+' giờ. Đây là 25% thời gian của cùng một người, không phải tăng thêm 25% suất nhân sự.</p>'+
 '<p class="note"><b>Cần phân biệt:</b> phần việc kế hoạch vượt ngưỡng 75% là <b>chiếm dụng dự phòng</b>, chưa phải vượt thời giờ làm việc. Tổng công việc, kể cả phát sinh, vượt ngưỡng 100% là <b>vượt quỹ giờ tổng tham chiếu</b> phải xử lý và kiểm lịch thực tế. Các ngưỡng là bình quân năm theo giả định, không phải lịch chấm công từng tháng.</p>'+
 detail('Mở bảng theo tháng: quỹ dự phòng đã dùng và giờ vượt quỹ tổng',
   reserveRows.length?table(['Chức danh','Đơn vị','Suất','Tháng','Giờ kế hoạch','Giờ tổng kể phát sinh','Ngưỡng 75%','Ngưỡng 100%','Dự phòng đã dùng','Việc kế hoạch lấn dự phòng','Vượt quỹ giờ tổng','Nhận định'],reserveRows,[4,5,6,7,8,9,10]):
    '<p>Chưa phát hiện giờ kế hoạch lấn dự phòng trên phạm vi đã tính; không đồng nghĩa đủ năng lực khi dữ liệu thiếu.</p>');

 const direct='<h4>Diễn giải nhanh: vượt giờ không đồng nghĩa phải tăng nhân sự ngay</h4>'+
 table(['Tình trạng hiện tại','Hiểu đúng','Hướng xử lý trước khi sửa định biên'],[
  ['Có vị trí vượt quỹ cả năm','Một đầu mối lấn quỹ 75% theo kịch bản; chưa có nghĩa đã vượt tổng quỹ giờ hoặc nhất thiết thiếu suất dài hạn.','Đo lại định mức, khử trùng công đoạn, kiểm tải đúng CNNV/MTCV; nếu vẫn vượt thì xác định năng lực cần bổ sung trong chính chuyên môn, không chuyển việc để cân giờ.'],
  ['Nhiều vị trí chỉ vượt tháng thiết lập','Công việc tạo mẫu, quy trình, đào tạo có thể đang dồn vào một kỳ, nhưng phải giữ hạn bàn giao bắt buộc.','Lập lịch tuần của chính vị trí; ưu tiên tài liệu bắt buộc, đối chiếu bản cũ, giảm sửa trùng; hỗ trợ chỉ trong phạm vi CNNV/MTCV và thẩm quyền đã có.'],
  ['Còn đầu vào CMS chưa lượng hóa','Bảng đang thiếu giờ chứ không chứng minh còn công suất trống.','Chốt mã hồ sơ bác sĩ/khoa/dịch vụ, khối lượng nhập/sửa, chủ nguồn, mốc bàn giao, người xử lý và số phút công đoạn.'],
  ['Chưa có đủ người thực tế','36 là số suất cơ cấu đề xuất, không tự động có 36 người đang làm.','Giao người phụ trách tạm có văn bản, bảo toàn quyền phê duyệt, đặt trần giờ và cơ chế ngừng việc không thiết yếu.']
 ])+
 '<p class="fine"><b>Quy tắc quyết định:</b> chỉ đề xuất điều chỉnh số suất hoặc tuyến chức năng sau khi đã khử trùng công đoạn, xác nhận đầu vào, đối chiếu tải 12 tháng và kiểm có người làm thay đủ quyền. Không cộng tổng giờ các đầu mối rồi chia bình quân để kết luận vì sản phẩm còn phụ thuộc chuyên môn và địa điểm.</p>';
 return '<h3>Quyết định định biên – nhìn ngay mức đủ tải và khoảng trống</h3>'+shortVerdict+reserveExplanation+
 '<div class="control">'+selCase()+'</div>'+
 metrics([[nu(overload.length),'Suất có tháng lấn quỹ dự phòng kế hoạch'],
          [nu(annual.length),'Suất lấn quỹ kế hoạch cả năm'],
          [nu(run.cms.unknown.length),'Trường điều kiện CMS chưa có số'],
          [nu(known.total,0),'Giờ mô hình đã tính/năm'],
          [nu(run.cap.plan),'Giờ kế hoạch 75%/một suất/tháng'],
          [nu(other.length),'Đầu mối chưa có quỹ/đang chờ kích hoạt']])+
 direct+
 detail('Mở bảng so sánh cả 3 kịch bản tính giờ',table(['Kịch bản','Giờ công mô phỏng/năm','Đầu mối vượt tháng','Suất vượt năm','Điều kiện CMS còn thiếu','Chuyển xem'],scenarioRows,[1,2,3,4]))+
 '<h4>Điểm nghẽn phải xử lý trước khi chốt cơ cấu</h4>'+
 (topRows.length?table(['Chức danh','Nơi làm','Suất','Tháng cao điểm','Giờ việc trong tháng','Quỹ giờ','Lấn quỹ 75%','Lấn quỹ 75% cả năm'],topRows,[3,4,5,6]):'<p>Chưa phát hiện vượt trên khối lượng đã tính; không đồng nghĩa đã đủ nhân sự.</p>')+
 detail('Mở đánh giá tác động dây chuyền khi thiếu người hoặc thiếu giờ',cascadeExposurePanel(run,all))+
 detail('Mở danh sách điều kiện chưa thể nghiệm thu phương án 36 suất',
 table(['Khoảng trống','Tình trạng và tác động','Nguồn xác nhận'],[
  ['CMS website/App','Chưa lượng hóa '+run.cms.unknown.length+' trường/điều kiện; sản lượng chưa chốt sẽ tăng giờ theo đúng người, đặc biệt khối biên tập và quản lý sản phẩm số.','Đầu mối cơ sở/Clinic; chủ dữ liệu y khoa, giá, giấy phép; Quản lý sản phẩm số'],
  ['Thư viện mẫu M-6','Mới có 6 nhóm; chưa xác định số file, kích thước, biến thể và thao tác sửa/kiểm. Không được coi công việc chưa lập danh sách là 0 giờ.','Tổ Thiết kế, Media; Chuyên viên trưởng đúng tuyến; quản lý thương hiệu'],
  ['30 kênh và tài sản','30 kênh mới là số tổng hợp, chưa đủ mã thật, đơn vị giữ, trạng thái, ngày kích hoạt và lịch bảo trì; biển, màn hình và tài sản số cần kiểm thêm.','Quảng cáo và kênh số; Truyền thông; cơ sở; Phòng Công nghệ/Số hóa theo quyền'],
  ['Người thực có và Clinic','36 là suất trong phương án, không phải danh sách người nhận việc. Quỹ giờ của đầu mối Clinic chưa có số chính thức.','Phòng Nhân lực, BGĐ cơ sở và Trưởng phòng Marketing'],
  ['Lịch giai đoạn, phát sinh, bản cũ','Mốc bàn giao quý I, lịch mở thương hiệu, phát sinh và hiệu lực quy trình/mẫu cũ chưa được xác nhận đủ để bảo đảm bàn giao từ quý II.','Chủ nghiệp vụ, Quản lý chất lượng, quản lý thương hiệu, các đơn vị liên quan']
 ]))+
 detail('Mở toàn bộ 26 chức danh, 37 dòng suất/đầu mối và 12 tháng để kiểm từng người',
   table(['Chức danh','Đơn vị','Suất/phân công','Quỹ tháng','Tháng vượt','CMS thiếu số','Trạng thái'],allRows,[5]))+
 '<h4>7. Cách xử lý vượt tải và điều kiện kết luận</h4>'+
 '<p>Truy ngược từng mã việc, công đoạn và người chịu tải; phân bổ lại <b>đúng CNNV/MTCV</b> trước khi đề xuất người mới. Tách phần duy trì và phần xây dựng hệ thống trong quý I; chỉ điều chỉnh lịch mẫu khi phê duyệt và không được tự lùi mốc 31/03. Kiểm thử định mức thực tế, danh mục dùng chung để tránh cộng trùng, tính cả công việc ngoài kế hoạch và yêu cầu hiện diện tại cơ sở. Chỉ chuyển trạng thái sang “Đủ căn cứ chốt” khi từng khoản thiếu được đối soát, có người cung cấp, bằng chứng nguồn và giờ công đã xác minh.</p>';
}
