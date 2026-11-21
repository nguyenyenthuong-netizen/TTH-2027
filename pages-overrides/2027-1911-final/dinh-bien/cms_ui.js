/* In-framework evidence ledger: quantities not supplied are UNKNOWN, not zero. */
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
 fLabel('Số hồ sơ GỐC có mã duy nhất',input('base',val('base'),0,99999,'1'))+
 fLabel('Số liên kết với cơ sở từ mã hồ sơ gốc có sẵn',input('reuse',val('reuse'),0,99999,'1'))+
 fLabel('Số hồ sơ cần cập nhật THÊM mỗi tháng, ngoài khối lượng W',input('maint',val('maint'),0,99999,'1'))+
 fLabel('Số đồ họa mới NGOÀI công việc thiết kế W',input('graphic',val('graphic'),0,99999,'1'))+
 fLabel('Số tư liệu mới NGOÀI công việc Media W',input('media',val('media'),0,99999,'1'))+
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
 e(name(x.act.r)),nu(x.act.h),'Kiểm: '+e(name(x.d.reviewer))+'; thử: '+e(name(x.d.tester))]);
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
 detail('III. Lập, sửa, kiểm, thử, bàn giao tài liệu – giờ theo người',table(['Tháng','Mã/tên tài liệu','Phạm vi','Công đoạn','Người','Giờ','Kiểm và thử'],drows,[5]),true)+
 detail('IV. CMS – nguồn, biên tập, nhập, kiểm, công bố – giờ theo người',table(['Tháng','Đơn vị/hồ sơ','Công đoạn','Người','Lượng','Phút','Giờ','Căn cứ'],crows,[4,5,6]),true)+
 detail('V. Toàn bộ dòng MTCV gốc và đối chiếu phần thiếu',origOutputs(id))+
 '<p><strong>Điều kiện ra quyết định:</strong> phải chốt các trường chưa lượng hóa, người thực có, phút chuẩn và giờ khả dụng; không dùng số 0 cho dữ liệu thiếu, không xếp người vào việc ngoài MTCV.</p>';
}
function sufficiencyPanel(){
 const run=getRun(),rows=poolReviews(run).map(x=>{
 const unknown=run.cms.tasks.filter(t=>t.internal&&t.q==null&&x.keys.includes(t.role)).length,
 monthsBad=x.review.periods?.filter(z=>z.excess>0)||[];
 return [positionLink(x),x.site?e(siteTitle(x.site)):'Tổng công ty',x.slot?e(slotLabel(x.slot)):String(x.seats),
 x.id==='dmpk'&&edits.clinic==null?'Chưa xác minh':nu(x.review.planLimit),
 monthsBad.length?monthsBad.map(z=>'T'+z.m+': +'+format(z.excess)+' giờ').join('; '):'Không vượt trong phần đã tính',
 nu(unknown),
 x.id==='qlml'?'Chưa kích hoạt':x.id==='dmpk'&&edits.clinic==null?'Chưa có quỹ Clinic':
 x.slot?'Chưa phân đủ tải CMS giữa các suất':
 unknown?'Chưa đủ lượng CMS':monthsBad.length?'Vượt tải cần xử lý':'Chưa được kết luận đủ người'];
 });
 return '<h3>Kiểm tra đủ sức xử lý công việc theo từng tháng và suất</h3>'+
 '<p class="note"><b>Không kết luận đủ/dư người chỉ từ 36 suất.</b> Phải đủ sản lượng thực tế, công đoạn, hệ thống giai đoạn đầu, CMS, kiểm tài sản/kênh, giờ thực có và kế hoạch phát sinh. Kịch bản vượt giờ phải chỉ rõ tháng, vị trí và hướng xử lý; không ngầm kéo dài hạn bàn giao.</p>'+
 '<div class="control">'+selCase()+'</div>'+
 metrics([[nu(rows.length),'Tuyến/suất đang đối chiếu'],[nu(poolReviews(run).filter(z=>z.review.periods?.some(q=>q.excess>0)).length),'Có tháng vượt tải đã tính'],[nu(run.cms.unknown.length),'Điều kiện CMS còn thiếu']])+
 table(['Chức danh','Đơn vị','Suất/phân công','Giờ kế hoạch/tháng','Tháng vượt','Lượng CMS còn thiếu','Kết luận hiện tại'],rows,[5])+
 '<h4>Phương án khi vượt giờ</h4><p>Đối chiếu đúng mã việc gây vượt; loại bỏ việc trùng hoặc ngoài CNNV qua quyết định; chuẩn hóa mẫu có kiểm thời gian trước/sau; cân người đúng kỹ năng và thời hạn; tổ chức hỗ trợ theo tuyến quản lý; thuê ngoài đúng thẩm quyền hoặc trình điều chỉnh định biên. Trường hợp quá tải quý I cần báo rõ mốc 31/03 chưa khả thi, không tự đổi hạn hoặc cắt việc.</p>';
}
