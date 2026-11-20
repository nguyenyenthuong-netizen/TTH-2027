/* Giai đoạn, đầu ra và quyết định dùng cùng một sổ giờ với 26 MTCV. */
const stages={
 prep:{title:'Chuẩn bị · đến 31/12/2026',months:[],scope:'Nhân sự hiện có. Trưởng phòng chuẩn bị phương án phân công và danh sách hai bệnh viện thí điểm.',gate:'Có văn bản giao phụ trách, danh sách người làm, phân quyền, mẫu yêu cầu và sổ nhận việc.'},
 q1:{title:'Quý I/2027 · thí điểm',months:[1,2,3],scope:'Hai bệnh viện, mỗi nhóm thương hiệu một bệnh viện. Các đơn vị còn lại thực hiện theo phân công hiện hành. Khe Tre bàn giao đầu mối từ 15/03 theo lộ trình.',gate:'Đối soát giờ từng người, ít nhất 90% yêu cầu đúng hạn theo ngưỡng thử tại Mục 29, kênh liên tục, có người xử lý hộp thư và đánh giá đạt của Ban Giám đốc bệnh viện.'},
 q2:{title:'Quý II/2027 · bàn giao từng đợt',months:[4,5,6],scope:'Tiếp nhận theo từng bệnh viện. Đích cuối quý là 5 bệnh viện và 2 phòng khám. Số lượng theo phạm vi mới chỉ giao kể từ mốc bàn giao của từng đơn vị.',gate:'Mỗi đơn vị có biên bản bàn giao kênh, quyền, kho tư liệu, người nhận, ngày hiệu lực và số liệu đánh giá cuối quý.'},
 q3:{title:'Quý III/2027 · ổn định vận hành',months:[7,8,9],scope:'Vận hành theo hai nhóm thương hiệu. Triển khai nhận diện, sản phẩm số và nội dung dịch vụ theo các hạng mục đã được giao.',gate:'Bộ mẫu hoặc hạng mục có phiên bản, bằng chứng thử và người nghiệm thu. Gói khai trương chỉ thực hiện khi có lịch và chủ trương.'},
 q4:{title:'Quý IV/2027 · tổng kết và bố trí năm sau',months:[10,11,12],scope:'Duy trì các hoạt động đã bàn giao. Chốt kết quả từng nhóm, đối soát dữ liệu, tổng hợp năm và rà phương án nhân sự.',gate:'Báo cáo năm có nguồn số liệu, giải thích chênh lệch, tải theo từng vị trí và phương án cho năm sau.'}
};
const phaseJobs={
 prep:[
 ['tp','01 bảng phân công theo chức danh và tuyến báo cáo','Trưởng phòng trình cấp có thẩm quyền, Phòng Nhân lực đối chiếu nhân sự.'],
 ['cvt','01 danh sách 2 bệnh viện thí điểm và lịch giao việc của tuyến cơ sở','Ban Giám đốc từng bệnh viện xác nhận người đầu mối và điều kiện tại chỗ.'],
 ['cvt-2','01 bảng điểm kiểm Truyền thông – Thương hiệu và Tăng trưởng số','Hai Tổ trưởng nhận phạm vi kiểm và tuyến chuyển yêu cầu.'],
 ['dl-1','01 sổ ghi sản lượng và giờ theo người, mã việc, địa điểm','Trưởng phòng nhận sổ và kỳ chốt.'],
 ['tk-a','Bản gốc nhận diện nhóm 1 và danh mục mẫu có thể dùng trong thí điểm','Hồ sơ có phiên bản và người duyệt trước khi nhân mẫu.']
 ],
 q1:[['qlth-a','Phiếu giao việc cho từng hạng mục nhóm 1','Một mã hạng mục, một người chịu mục tiêu, đầu ra và hạn bàn giao.'],['qlth-bc','Phiếu giao việc cho từng hạng mục nhóm 2','Cùng nguyên tắc, giao đúng chuyên môn thuộc nhóm.'],['cvt','Lịch xuống việc cho 2 Trưởng nhóm bệnh viện thí điểm','Trưởng nhóm xác nhận khối lượng, người thực hiện và giờ đã dùng.'],['cvt-2','Bảng kiểm mẫu nghiệp vụ của hai tổ','Gửi kết quả cho Tổ trưởng; yêu cầu đổi lịch cơ sở chuyển qua tuyến quản lý cơ sở.'],['dl-1','Bảng đối soát cuối quý cho 2 bệnh viện thí điểm','Ghi số yêu cầu đúng hạn, mẫu đã nghiệm thu, giờ từng người và ngoại lệ.'],['dmpk','01 hồ sơ bàn giao đầu mối Khe Tre theo mốc 15/03','Đơn vị chốt người, số giờ kiêm nhiệm và ngày nhận việc.']],
 q2:[['tn-a','Biên bản bàn giao của từng bệnh viện nhóm 1','Có ngày hiệu lực, kênh, quyền, kho, người giao và người nhận.'],['tn-b','Biên bản bàn giao của từng bệnh viện nhóm 2','Trưởng nhóm kiêm truyền thông ghi phần việc tại chỗ trong cùng lịch.'],['qc-a','Biên bản nhận quyền kênh và tài khoản thuộc nhóm 1','Đối chiếu quyền và lịch phát với danh sách đơn vị đã bàn giao.'],['qc-b','Biên bản nhận quyền kênh và tài khoản thuộc nhóm 2','Kiểm độc lập quyền và nhật ký sau khi tiếp nhận.'],['dl-1','Bảng đánh giá cuối quý cho 5 bệnh viện và 2 phòng khám','Trưởng phòng đối chiếu với nhật ký từng cơ sở trước khi xem xét bố trí người.']],
 q3:[['tk-nt','Hồ sơ thiết kế thi công biển theo từng điểm đã duyệt','Chuyên viên truyền thông đúng nhóm nhận file, tổ chức thi công theo thẩm quyền.'],['md-ac','Phiếu kiểm kỹ thuật bản dựng dùng bộ mẫu B-7 đã nghiệm thu','Đối chiếu phiên bản, người thử và phạm vi đã bàn giao để tiếp tục duy trì.'],['qlsps','Hồ sơ yêu cầu, ca thử và biên bản nghiệm thu nghiệp vụ sản phẩm số','Phòng Công nghệ và đơn vị kỹ thuật phụ trách nhận yêu cầu theo phân công của hạng mục.'],['bt-b','Nội dung mới cho dịch vụ nhóm 2 theo hạng mục được duyệt','Ghi giờ xây mới riêng để xem xét ngưỡng bổ sung Biên tập.']],
 q4:[['dl-1','01 bảng số liệu tổng kết năm đã đối chiếu','Bàn giao số và nguồn cho Trưởng phòng; mẫu tra mã BC-NAM.'],['qlth-a','01 hồ sơ mục tiêu, ngân sách và kết quả năm nhóm 1','Trưởng phòng nhận, đối chiếu mục tiêu và số đã chốt.'],['qlth-bc','01 hồ sơ mục tiêu, ngân sách và kết quả năm nhóm 2','Trưởng phòng nhận, đối chiếu mục tiêu và số đã chốt.'],['tp','Hồ sơ tổng kết, kế hoạch và phương án nhân sự trình Ban Tổng Giám đốc','Dẫn nguồn theo nhóm, cơ sở, khối lượng đã đo, tháng cao điểm và quyết định cần trình.']]
};
function periodRoleKeys(r,id,site){
 if(model.roles[id].to==='coso')return scopeKeys(r,id,site);
 return roleKeys(r,id,id==='dl-1');
}
function poolReviews(r){
 const list=[];
 for(const id of Object.keys(model.roles)){
   if(id==='dl-2')continue;
   const local=model.roles[id].to==='coso';
   const entries=local?model.sites.filter(s=>r.siteRoles(s).includes(id)).map(s=>s.id):[null];
   for(const site of entries){
     const keys=periodRoleKeys(r,id,site),seats=local?1:model.seats[id];
     const review=TTHStaffing.reviewPosition(r,keys,seats,edits.clinic);
     list.push({id,site,keys,seats,review});
   }
 }
 return list;
}
function capacityBadge(x){
 const v=x.review;
 if(x.id==='qlml')return 'Chờ quyết định phân vùng';
 if(v.annualExcess===null)return 'Chờ số giờ được phân cho Clinic';
 if(v.annualExcess>0)return 'Vượt quỹ bình quân năm';
 if(v.peak.excess>0)return 'Cần hỗ trợ ở tháng cao điểm';
 return 'Việc đã tính nằm trong quỹ giờ';
}
function periodProducts(x){
 const rr=getRun(),keys=new Set(x.keys),periods=x.review.periods.filter(m=>m.excess>0);
 return periods.map(m=>{
   const goods=rr.works.filter(w=>keys.has(w.rid)&&w.hours[m.m-1]>0).sort((a,b)=>b.hours[m.m-1]-a.hours[m.m-1]).slice(0,3)
     .map(w=>btn(w.item.name,'roles',w.id)+' · '+format(w.qty[m.m-1])+' × '+format(sum(w.t))+' phút = '+format(w.hours[m.m-1])+' giờ');
   const docs=rr.docs.map(rec=>({rec,h:sum(rec.monthly[m.m-1].filter(z=>keys.has(z.r)&&z.type==='setup').map(z=>z.h))})).filter(d=>d.h>0).sort((a,b)=>b.h-a.h).slice(0,2)
     .map(d=>btn(d.rec.d.code+' · '+d.rec.d.name,'docs',d.rec.d.id)+' · '+format(d.h)+' giờ');
   return ['Tháng '+m.m,nu(m.excess),nu(m.ongoing),nu(m.setup),[...goods,...docs].join('<br>')];
 });
}
function positionRows(all){
 return all.map(x=>{
   const v=x.review;
   const office=x.site?btn(siteTitle(x.site),'sites',x.site):'Tổng công ty';
   const short=x.id==='dmpk'?'01 đầu mối kiêm nhiệm':String(x.seats);
   const top=v.peak&&v.peak.excess>0?'Tháng '+v.peak.m+' vượt '+format(v.peak.excess)+' giờ':'';
   return [cellRole(x.id)+(x.id==='dl-1'?'<small>Gồm công việc dữ liệu khách hàng kiêm nhiệm.</small>':''),office,short,nu(v.avgHours),e(capacityBadge(x))+(top?'<small>'+e(top)+'</small>':'')];
 });
}
function decisions(r,all){
 const active=all.filter(x=>x.review.annualExcess!==null);
 const yearly=active.filter(x=>x.review.annualExcess>0);
 const peaks=active.filter(x=>x.review.annualExcess===0&&x.review.peak.excess>0);
 const cluster=[...yearly,...peaks];
 const clinic=all.find(x=>x.id==='dmpk');
 const first=yearly.length?'Xác minh khối lượng cả năm của '+yearly.map(x=>name(x.id)+(x.site?' tại '+siteTitle(x.site):'')).join(', ')+'.':'Giữ phương án 22 suất Tổng công ty, 13 suất ở 5 bệnh viện và 1 đầu mối Clinic kiêm nhiệm làm mốc bố trí.';
 const evidence='Số người thực có năm 2027 và lịch trực tại từng cơ sở chờ Phòng Nhân lực và đơn vị xác nhận. Số giờ trong bảng là ước tính theo sản phẩm.';
 const hr=['Chức danh','Địa điểm','Bố trí theo cơ cấu','Giờ việc đã tính/tháng (bình quân)','So với quỹ giờ của cơ cấu'];
 const peaksTable=cluster.length?table(['Vị trí cần xem','Tháng vượt quỹ','Tháng cần hỗ trợ nhiều nhất','Việc có thể quyết'],cluster.map(x=>{
  const m=x.review.peak;const periods=x.review.periods.filter(v=>v.excess>0);
  const action=x.review.annualExcess>0?'Đo lại tải thường xuyên và kiểm khả năng phân công trước khi trình bổ sung người.':m.ongoing===0?'Dàn lại lịch làm tài liệu hoặc bố trí người thử, kiểm đúng chuyên môn.':'Xếp người hỗ trợ việc chuẩn bị hoặc đối soát theo lịch. Giữ người chịu trách nhiệm và thẩm quyền duyệt.';
  return [cellRole(x.id)+(x.site?'<small>'+e(siteTitle(x.site))+'</small>':''),periods.map(t=>'T'+t.m).join(', '),'T'+m.m+' · '+format(m.excess)+' giờ',e(action)];
 }),[2]):'<p>Trong kịch bản này, các vị trí đã có quỹ giờ đều nằm trong quỹ ở cả 12 tháng.</p>';
 return '<h4>Quyết định nhân sự theo kịch bản '+e(cases[u.scenario])+'</h4>'+stack([
 ['Bố trí dài hạn',e(first)+' <b>'+yearly.length+' vị trí/địa điểm có khối lượng đã tính vượt quỹ bình quân năm.</b>'],
 ['Bố trí theo tháng','<b>'+peaks.length+' vị trí/địa điểm chỉ vượt quỹ ở một số tháng.</b> Bảng dưới ghi tháng và số giờ cần thu xếp.'],
 ['Đầu mối Clinic','Khối lượng tham chiếu '+format(clinic.review.avgHours)+' giờ/tháng trong mô hình đủ phạm vi. Chốt số giờ kiêm nhiệm, ngày bàn giao và người thay với đơn vị.']
 ])+'<p class="note">'+e(evidence)+'</p>'+peaksTable+
 (cluster.length?detail('Sản phẩm nào chiếm giờ ở từng tháng vượt quỹ',cluster.map(x=>detail(e(name(x.id))+(x.site?' · '+e(siteTitle(x.site)):''),table(['Tháng','Giờ vượt','Từ vận hành','Từ thiết lập','Đầu ra chiếm nhiều giờ trong tháng'],periodProducts(x),[1,2,3]))).join('')):'')+
 '<h4>Bố trí tại từng bệnh viện và phòng khám</h4><p>Mỗi dòng dưới đây thuộc một địa điểm. Các giờ làm ở Vinh, Hà Tĩnh và Quảng Bình được đối chiếu với người bố trí ở chính bệnh viện đó.</p>'+table(hr,positionRows(all.filter(x=>x.site).sort((a,b)=>model.sites.findIndex(s=>s.id===a.site)-model.sites.findIndex(s=>s.id===b.site))),[2,3])+
 detail('Bố trí từng chức danh ở Tổng công ty',table(hr,positionRows(all.filter(x=>!x.site)),[2,3]),true);
}
function phaseSite(s){return fLabel('Đơn vị', '<select data-set="deliverySite">'+opt(Object.fromEntries(s.map(v=>[v.id,v.name])),u.deliverySite)+'</select>');}
// For every quantity, the system and hospital shares are disjoint and cover the original row.
const splitSeats={
 'bt-ac':{bai:6,dv:4,web:6,kt:9,phat:1,sk:4,cc:1,sua:2,english:2,phaply:1},
 'tk-a':{c1:26,c2:14,c3:3,c4:1,kiem:6,sua:3},
 'md-ac':{ghi:2,am:1,kho:3,sua:1},
 'qc-a':{fb:3,tik:1,khac:4,ads:2,landing:1,suco:1,tin:2,'dia-chi':0}
};
function slotShare(w,slot,qty,month,r){
 if(slot==='all')return qty;
 const z=w.item;
 if(qty==null){
   if(slot==='a'&&typeof z.q==='string'&&z.q.endsWith(':review'))return 0;
   if(slot==='a'&&typeof z.q==='string'&&z.q.endsWith(':script')){const group=z.q.split(':')[0];return sum(r.works.filter(i=>[group+':short',group+':complex',group+':film'].includes(i.item.q)).map(i=>i.qty[month-1]));}
   return null;
 }
 let system;
 if(z.kind==='T')system=u.chiefSeat==='a'?qty:0;
 else if(z.code==='du-gb')system=qty/2;
 else if(typeof z.q==='string'&&z.q.endsWith(':review'))system=0;
 else if(typeof z.q==='string'&&z.q.endsWith(':script')){
   const group=z.q.split(':')[0];
   const direct=r.works.filter(i=>[group+':short',group+':complex',group+':film'].includes(i.item.q));
   system=Math.min(qty,sum(direct.map(i=>i.qty[month-1])));
 }else if(typeof z.q==='string')system=qty;
 else if(Object.hasOwn(splitSeats[z.role],z.code)){
   const cycles=z.period==='w'?r.works.find(i=>i.id===z.role+'/du-gb').qty[month-1]/2:z.period==='2w'?1:z.period==='q'?Number(month%3===0):1;
   const planned=edits.splits?.[z.id]??splitSeats[z.role][z.code];
   system=Math.min(qty,planned*cycles);
 }else system=qty; // Newly activated HQ campaign/stand-in starts with system scope until an item is assigned.
 return slot==='a'?system:qty-system;
}
function slotDoc(d,z,id,slot){
 if(slot==='all'||!splitSeats[id])return true;
 // The master file has system scope; the hospital counterpart tests it when that role is assigned the pilot.
 const hospital=z.stage==='Thử áp dụng'||/bệnh viện|hiện trường/i.test(d.scope);
 return (slot==='b')===hospital;
}
function deliveryRoute(w){
 const z=w.item,r=roleMap[z.role],group=['bt-b','md-b','mdcs-b','qlth-bc'].includes(z.role)?'2':'1';
 if(z.id==='cvt/bv')return ['Trưởng nhóm của từng bệnh viện thuộc phạm vi triển khai xác nhận lịch. Trưởng phòng Marketing nhận tổng hợp từ Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở.','Hằng tuần theo lịch giao việc của bệnh viện.'];
 if(z.id==='cvt-2/tai')return ['Tổ trưởng Tổ Truyền thông và Thương hiệu và Tổ trưởng Tổ Tăng trưởng số nhận kết quả rà tải. Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số báo cáo Trưởng phòng Marketing.','Hằng tuần, một phiếu cho mỗi tổ.'];
 if(z.id==='dl-1/kt')return ['Người quản lý đúng tuyến nhận phiếu kiểm. Trưởng phòng Marketing nhận kết quả đối soát qua báo cáo.','Ghi phiếu theo lịch tuần. Chốt số giờ từ sổ theo dõi vào kỳ báo cáo quý của MTCV.'];
 if(z.id==='dl-1/nam')return ['Trưởng phòng Marketing nhận bảng số liệu để lập và trình báo cáo năm.','Tháng 12, trước khi Trưởng phòng trình báo cáo năm.'];
 if(z.id==='dl-1/tuan')return ['Quản lý thương hiệu và Trưởng phòng Marketing nhận báo cáo BM-2.','Hằng tuần theo lịch báo cáo.'];
 if(z.role.startsWith('qlth-')&&z.code==='hangmuc')return ['Trưởng phòng Marketing duyệt kế hoạch theo phân cấp. Giám đốc cơ sở xác nhận phần chi từ ngân sách cơ sở; cấp tài chính duyệt khoản chi theo thẩm quyền.','Theo lịch hạng mục. Kế hoạch tháng trình chậm nhất ngày 18, duyệt chậm nhất ngày 20 theo MTCV.'];
 if(z.role.startsWith('qlth-')&&z.code==='nam')return ['Trưởng phòng Marketing nhận hồ sơ mục tiêu, ngân sách và kết quả năm của nhóm '+group+'.','Tháng 12, theo hạn chốt báo cáo năm.'];
 if(z.role.startsWith('mdcs-')&&['v2','v3'].includes(z.code))return ['Chuyên viên media nhóm '+group+' tại Tổng công ty kiểm kỹ thuật. Quản lý thương hiệu nhóm '+group+' nghiệm thu mục tiêu. Đơn vị chuyên môn xác nhận y khoa nếu có, cấp được phân quyền duyệt phát hành.','Theo lịch quay và phiếu đặt việc, sau khi có mẫu B-7 hợp lệ.'];
 if(z.role.startsWith('bt-')&&z.code==='loi')return ['Biên tập đúng nhóm chủ trì phần lời/thoại. Chuyên viên media nhóm '+group+' nhận lời đã kiểm để lập phân cảnh. Nội dung y khoa do đơn vị chuyên môn xác nhận.','Theo mốc khóa kịch bản trong phiếu yêu cầu.'];
 if(z.role.startsWith('md-')&&z.code==='kiem')return ['Media cơ sở đúng bệnh viện nhận phiếu sửa hoặc kết quả kiểm kỹ thuật. Quản lý thương hiệu nhóm '+group+' nhận bản đủ điều kiện để nghiệm thu mục tiêu.','Khi cơ sở bàn giao bản dựng, trước bước nghiệm thu và phát hành.'];
 const refs=[...new Set([...(z.jd||[]),...model.crosswalk[z.role].flatMap(([key],i)=>key===z.id?[i+1]:[])])];
 const rows=refs.map(i=>model.jd[z.role][i]).filter(Boolean);
 const terms=[...new Set(rows.map(row=>row[1]).filter(t=>t&&!/^[–—-]$/.test(t)))];
 const destinations=[...new Set(rows.map(row=>row[2]).filter(t=>t&&!/^(?:[–—-]|như trên)/i.test(t)))];
 const norm=t=>String(t).replace(/người quản lý trực tiếp đúng tuyến theo quyết định phân công có hiệu lực/gi,r.bao_cao_cho);
 const receiver=destinations.length===1?norm(destinations[0]):norm(r.phan_dinh_kiem_duyet||r.bao_cao_cho);
 return [receiver,terms.length===1?terms[0]:'Theo kỳ '+periodName(z.period)+' và hạn trên phiếu giao việc. Các mốc theo loại hồ sơ có tại MTCV của vị trí.'];
}
function assignmentCondition(w,site){
 const z=w.item,notes=[];
 if(u.phase==='q1'&&site){
   if(site.group==='clinic')notes.push('Khe Tre nhận việc từ 15/03; chờ số riêng của phòng khám.');
   else{
     const pilot=site.group==='g1'?u.pilot1:u.pilot2;
     notes.push(!pilot?'Chờ chốt bệnh viện thí điểm.':pilot===site.id?'Theo phương án thí điểm đã chọn.':'Đơn vị giữ cách làm hiện hành trong quý I.');
   }
 }
 if(u.phase==='q2'&&site)notes.push('Giao từ ngày ký biên bản tiếp nhận tại đơn vị.');
 const usesTemplate=(z.role.startsWith('mdcs-')&&['v2','v3'].includes(z.code))||(z.role.startsWith('md-')&&z.code==='kiem');
 if(usesTemplate){
   const group=site?site.group:(z.role==='md-ac'?'g1':'g2');
   const rec=getRun().docs.find(r=>r.d.id===(group==='g1'?'B-7~1':'B-7~2'));
   const stageMonths=rec.monthly.flatMap((arr,i)=>arr.some(a=>a.type==='setup')?[i+1]:[]);
   const last=stageMonths.length?' Mốc hoàn tất theo lịch thử: T'+Math.max(...stageMonths)+'.':'';
   notes.push('Chỉ giao quay/dựng hoặc kiểm theo mẫu khi có phiên bản B-7 đúng nhóm đã được nghiệm thu. Trước mốc đó cần bản cũ còn hiệu lực.'+last);
 }
 return notes.length?'<small>'+e(notes.join(' '))+'</small>':'';
}
function roadmapDelivery(){
 const r=getRun(),st=stages[u.phase],rid=u.deliveryRole,local=model.roles[rid].to==='coso';
 const possible=model.sites.filter(s=>r.siteRoles(s).includes(rid));
 if(local&&!possible.some(s=>s.id===u.deliverySite))u.deliverySite=possible[0].id;
 const site=local?siteMap[u.deliverySite]:null;
 const phaseSelect=fLabel('Giai đoạn', '<select data-set="phase">'+opt(Object.fromEntries(Object.entries(stages).map(([k,v])=>[k,v.title])),u.phase)+'</select>');
 const roleSelect=fLabel('Người / chức danh cần giao việc', '<select data-set="deliveryRole">'+opt(Object.fromEntries(db.vi_tri.map(v=>[v.id,v.ten])),rid)+'</select>');
 const division=splitSeats[rid],slot=division?u.deliverySlot:'all';
 const slotSelect=division?fLabel('Phân công trong '+model.seats[rid]+' suất','<select data-set="deliverySlot">'+opt({all:'Cả hai suất',a:'Người phụ trách hệ thống',b:'Người phụ trách bệnh viện'},slot)+'</select>'):'';
 const choices='<div class="control">'+phaseSelect+roleSelect+(local?phaseSite(possible):'')+slotSelect+selCase()+'</div>';
 const phaseTable=table(['Giai đoạn','Phạm vi giao việc','Điều kiện chuyển bước'],Object.entries(stages).map(([k,v])=>[btn(v.title,'stage',k),e(v.scope),e(v.gate)]));
 const heading='<h3>Ai làm việc gì, vào giai đoạn nào?</h3><p>Phương án bố trí 22 suất ở Tổng công ty, 13 suất tại 5 bệnh viện và 1 đầu mối Clinic kiêm nhiệm. Chọn chức danh để xem từng sản phẩm phải giao.</p>'+choices+
   (division?'<p class="fine">Hai người cùng MTCV, phân công cố định theo Mục 2 và Mục 3: một người phụ trách hệ thống, một người phụ trách bệnh viện. Nơi đặt hàng quyết định người nhận từng sản phẩm. Các số phân bổ chưa có phiếu giao là giả định tính thử. Người kiểm độc lập phải khác người lập.</p>':'');
 const gate='<p class="note"><b>'+e(st.title)+'.</b> '+e(st.scope)+'</p>';
 const roleIndex=detail('Danh sách phân công theo đủ 26 chức danh',table(['Chức danh','Suất theo cơ cấu','Phạm vi làm việc'],db.vi_tri.map(v=>[btn(v.ten,'deliveryRole',v.id),v.id==='dmpk'?'1 kiêm nhiệm':v.id==='dl-2'?'Kiêm cùng Đo lường':v.id==='qlml'?'Chờ phân vùng':String(model.seats[v.id]),e(v.phan_dinh_chu_tri_dau_ra||v.muc_dich)]),[1]));
 const keyMilestones=detail('Đầu ra cần chốt để chuyển giai đoạn',table(['Chủ trì phần việc','Đầu ra','Người nhận hoặc điều kiện hoàn thành'],phaseJobs[u.phase].map(([id,job,goal])=>[cellRole(id),e(job),e(goal)]))+'<p>'+e(st.gate)+'</p>',true);
 if(u.phase==='prep'){
   const own=phaseJobs.prep.filter(x=>x[0]===rid);
   return heading+gate+(own.length?table(['Chức danh','Đầu ra chuẩn bị','Bàn giao'],own.map(([id,n,g])=>[e(name(id)),e(n),e(g)])):'<p>Giai đoạn chuẩn bị sử dụng nhân sự hiện có. Chức danh này nhận việc theo quyết định phân công. Sản lượng vận hành ba tháng đầu có ở giai đoạn thí điểm.</p>')+keyMilestones+roleIndex+detail('Toàn bộ lộ trình',phaseTable);
 }
 const monthsHere=st.months;
 const keys=new Set(periodRoleKeys(r,rid,site?.id));
 const works=r.works.filter(w=>keys.has(w.rid));
 const pilots={g1:u.pilot1,g2:u.pilot2},chosen=site?pilots[site.group]:null;
 const inTrial=u.phase==='q1',clinic=rid==='dmpk';
 const pilotInput=group=>fLabel(group==='g1'?'BV thí điểm nhóm 1':'BV thí điểm nhóm 2','<select data-set="'+(group==='g1'?'pilot1':'pilot2')+'">'+opt({'':'Chưa xác nhận',...Object.fromEntries(model.sites.filter(s=>s.group===group).map(s=>[s.id,s.name]))},pilots[group])+'</select>');
 const trialSelection=inTrial?'<div class="control">'+pilotInput('g1')+pilotInput('g2')+'</div><p class="fine">Lựa chọn hai bệnh viện dùng để tính thử lịch giao việc. Danh sách chính thức căn cứ quyết định thí điểm.</p>':'';
 let scope=local?(inTrial?(clinic?'Từ 15/03 chỉ bàn giao đầu mối Khe Tre. Chưa có sản lượng tách riêng Khe Tre cho phần còn lại của tháng.':!chosen?'Địa điểm thí điểm của nhóm chưa xác nhận. Số bên dưới là sản lượng tham chiếu tại bệnh viện này.':chosen===site.id?'Đơn vị được chọn trong kịch bản thí điểm.':'Đơn vị tiếp tục theo phân công hiện hành trong quý I. Số bên dưới dùng đối chiếu khi bàn giao.'):'Sản lượng của riêng '+site.name+'.'):(inTrial?'Khối lượng tham chiếu ở Tổng công ty. Các đầu ra phụ thuộc số bệnh viện và video được tính theo hai đơn vị thí điểm. Các sản lượng cố định toàn nhóm cần đối chiếu phiếu giao trong quý. Vai trò chưa có người nhận phải xác định người kiêm và lịch bàn giao trước khi giao việc.':'Quy cách và sản lượng theo đúng nhóm, đúng người nhận việc.');
 if(u.phase==='q2')scope+=' Sản lượng là mức khi nhận đủ phạm vi; ngày hiệu lực và phần tháng chuyển giao chốt theo biên bản từng đơn vị.';
 function phasedQty(w,m){
   const z=w.item;
   if(inTrial&&clinic)return null;
   if(!inTrial)return w.qty[m-1];
   if(z.role==='cvt'&&z.code==='bv')return w.qty[m-1]*2/5;
   if(typeof z.q!=='string'||!z.q.includes(':'))return w.qty[m-1];
   const [group,type]=z.q.split(':');
   if(!['script','review'].includes(type))return w.qty[m-1];
   if(!pilots[group])return null;
   const siteVol=r.siteInputs[pilots[group]][m-1],all=r.works.find(i=>i.item.q===group+':review');
   return (type==='script'?w.qty[m-1]-all.qty[m-1]:0)+siteVol.v2+siteVol.v3;
 }
 const ready=!(inTrial&&local&&(clinic||!chosen||chosen!==site.id));
 let operationHours=0,pending=0;
 const rows=works.map(w=>{
   const count=monthsHere.map(m=>slotShare(w,slot,phasedQty(w,m),m,r)),incomplete=count.some(v=>v===null);
   const qty=incomplete?null:sum(count),hours=incomplete?null:sum(monthsHere.map((m,i)=>{
     const initial=w.qty[m-1];
     return initial?w.hours[m-1]*count[i]/initial:count[i]*sum(w.t)/60;
   }));
   if(hours!=null)operationHours+=hours;else pending++;
   if(qty===0)return null;
   const [recipient,due]=deliveryRoute(w);
   const quantity=incomplete?'Chờ phạm vi':count.map(v=>format(v)).join(' / ');
   return [btn(w.item.name,'roles',w.id)+assignmentCondition(w,site)+(rid==='dl-1'&&w.item.role==='dl-2'?'<small>Phần dữ liệu kiêm nhiệm</small>':''),quantity,nu(qty),nu(sum(w.t)),nu(hours),e(recipient)+'<small>Hạn: '+e(due)+'</small>'];
 }).filter(Boolean);
 const inScope=z=>keys.has(z.r);
 const splitControls=division?detail('Căn cứ phân sản phẩm giữa hệ thống và bệnh viện',(
   rid==='bt-ac'?fLabel('Suất kiêm Tổ trưởng trong kịch bản','<select data-set="chiefSeat">'+opt({a:'Người phụ trách hệ thống',b:'Người phụ trách bệnh viện'},u.chiefSeat)+'</select>'):'')+
   '<p>Số dưới đây là sản lượng của người phụ trách hệ thống trong một kỳ chuẩn. Phần còn lại thuộc người phụ trách bệnh viện. Thay số theo phiếu của bên đặt hàng. Hai người cùng giữ nghiệp vụ của chức danh.</p><form class="form" data-split-role="'+e(rid)+'">'+
   works.filter(w=>Object.hasOwn(division,w.item.code)).map(w=>fLabel(w.item.name+' / '+periodName(w.item.period),input(w.item.code,edits.splits?.[w.item.id]??division[w.item.code],0,w.item.q))).join('')+apply+'</form>'+
   '<p>Media kiểm bản do bệnh viện nộp tính cho người phụ trách bệnh viện. Phần phân cảnh hoặc kịch bản lời được tách theo nguồn video. Cùng một buổi giao ban, mỗi người ghi thời gian tham dự của mình. Trong hồ sơ tài liệu gốc, phần thử tại bệnh viện chỉ tính cho người được giao thử. Số đo và nhân sự thực có chờ đối chiếu.</p>'):'';
 const stageDocs=r.docs.flatMap(rec=>{
  const matching=monthsHere.flatMap(m=>rec.monthly[m-1].filter(z=>z.type!=='next'&&inScope(z)&&slotDoc(rec.d,z,rid,slot)).map(z=>({...z,m})));
  if(!matching.length)return [];
  const contribution=sum(matching.map(z=>z.h));
  const batches=monthsHere.map(m=>rec.monthly[m-1].filter(z=>z.stage==='Đối chiếu bản gốc'&&z.type==='setup').length);
  const reviews=matching.filter(z=>z.type==='maint').length;
  return [{h:contribution,cells:[btn(rec.d.code+' · '+rec.d.name,'docs',rec.d.id),e(rec.d.scope),e([...new Set(matching.map(z=>'T'+z.m))].join(', ')),e([...new Set(matching.map(z=>z.stage))].join(' · ')),sum(batches)?sum(batches)+' đơn vị trong lịch':reviews?reviews+' lượt rà':'Theo phiên bản',nu(contribution),e(name(rec.d.reviewer))]}];
 });
 const docsHours=sum(stageDocs.map(z=>z.h));
 const caption='Sản lượng T'+monthsHere.join(' / T');
 const advisory='<p class="fine">Định mức là phút của người làm một đơn vị đầu ra. Giờ theo quý gồm thời gian trực tiếp, phối hợp, kiểm, sửa và di chuyển của vị trí. Mỗi người ghi giờ cho công đoạn mình làm. Thời gian chờ duyệt nằm ngoài phép tính.</p>';
 return heading+gate+trialSelection+splitControls+'<h4>'+e(name(rid))+(site?' · '+e(site.name):'')+'</h4><p>'+e(scope)+'</p>'+
 '<p class="receipt"><b>'+(pending&&operationHours===0?'Chờ xác nhận giờ đầu ra vận hành':format(operationHours)+' giờ đầu ra vận hành')+'</b> và <b>'+format(docsHours)+' giờ công việc tài liệu</b> trong quý theo phần đã định lượng.'+(pending?' Còn '+pending+' dòng chờ xác nhận phạm vi.':'')+(!ready?' Số giờ tại cơ sở đang dùng làm tham chiếu, chờ giao cho vai trò mới.':'')+'</p>'+
 (rows.length?table(['Sản phẩm bàn giao',caption,'Tổng sản lượng quý','Phút/đơn vị','Giờ trong quý','Người nhận, kiểm và hạn'],rows,[2,3,4]):'<p>Chưa giao sản phẩm trong giai đoạn đã chọn. Vị trí vùng chỉ nhận việc sau quyết định phân vùng và bàn giao quản lý.</p>')+advisory+
 '<h4>Quy trình, mẫu và báo cáo do vị trí tham gia trong quý</h4>'+(stageDocs.length?table(['Hồ sơ','Phạm vi','Tháng','Phần việc của vị trí','Sản lượng theo lịch','Giờ trong quý','Người kiểm chuẩn'],stageDocs.map(d=>d.cells),[5]):'<p>Chưa phân công hồ sơ tài liệu cho vị trí này trong lịch quý.</p>')+
 keyMilestones+roleIndex+detail('Toàn bộ lộ trình',phaseTable);
}
