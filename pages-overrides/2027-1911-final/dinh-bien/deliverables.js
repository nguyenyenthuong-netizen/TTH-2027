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
function seatMonths(r,id,slot){
 const rows=r.monthly([id]).map(row=>Object.fromEntries(Object.keys(row).map(k=>[k,0])));
 const segmentKeys=['direct','coord','check','fix','travel'];
 for(const w of r.works.filter(item=>item.rid===id)){
   w.qty.forEach((qty,i)=>{
     if(!qty)return;
     const selected=slotShare(w,slot,qty,i+1,r);
     const factor=selected/qty,parts=w.segments[i];
     const hours=w.hours[i]*factor;
     rows[i][w.item.kind==='U'?'incident':'regular']+=hours;
     if(w.item.kind==='T')rows[i].lead+=hours;
     segmentKeys.forEach((key,j)=>rows[i][key]+=parts[j]*factor);
   });
 }
 for(const rec of r.docs){
   rec.monthly.forEach((records,i)=>{
     records.filter(item=>item.r===id&&slotDoc(rec.d,item,id,slot)).forEach(item=>rows[i][item.type]+=item.h);
   });
 }
 return rows;
}
function poolReviews(r){
 const list=[];
 for(const id of Object.keys(model.roles)){
   if(id==='dl-2')continue;
   const local=model.roles[id].to==='coso';
   if(splitSeats[id]){
     for(const slot of ['a','b']){
       const monthly=seatMonths(r,id,slot),personRun={...r,monthly:()=>monthly};
       list.push({id,site:null,keys:[id],seats:1,slot,review:TTHStaffing.reviewPosition(personRun,[id],1,null)});
     }
     continue;
   }
   const entries=local?model.sites.filter(s=>r.siteRoles(s).includes(id)).map(s=>s.id):[null];
   for(const site of entries){
     const keys=periodRoleKeys(r,id,site),seats=local?1:model.seats[id];
     const review=TTHStaffing.reviewPosition(r,keys,seats,edits.clinic);
     list.push({id,site,keys,seats,review});
   }
 }
 return list;
}
function slotLabel(slot){return slot==='a'?'phụ trách hệ thống':'phụ trách bệnh viện';}
function positionLink(item){
 if(item.slot)return btn(name(item.id)+' · '+slotLabel(item.slot),'deliveryRole',item.id+'/'+item.slot);
 return cellRole(item.id);
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
   const goods=rr.works.filter(w=>keys.has(w.rid)&&w.hours[m.m-1]>0).map(w=>{
     const total=w.qty[m.m-1],qty=x.slot?slotShare(w,x.slot,total,m.m,rr):total;
     return {w,qty,h:total?w.hours[m.m-1]*qty/total:0};
   }).filter(item=>item.h>0).sort((a,b)=>b.h-a.h).map(({w,qty,h})=>
     (x.slot?btn(w.item.name,'deliveryRole',x.id+'/'+x.slot):btn(w.item.name,'roles',w.id))+' · '+format(qty)+' × '+format(sum(w.t))+' phút = '+format(h)+' giờ');
   const docs=rr.docs.map(rec=>({rec,h:sum(rec.monthly[m.m-1].filter(z=>keys.has(z.r)&&z.type==='setup'&&(!x.slot||slotDoc(rec.d,z,x.id,x.slot))).map(z=>z.h))}))
     .filter(item=>item.h>0).sort((a,b)=>b.h-a.h)
     .map(item=>btn(item.rec.d.code+' · '+item.rec.d.name,'docs',item.rec.d.id)+' · '+format(item.h)+' giờ');
   return ['Tháng '+m.m,nu(m.excess),nu(m.ongoing),nu(m.setup),[...goods,...docs].join('<br>')];
 });
}
function positionRows(all){
 return all.map(x=>{
   const v=x.review;
   const office=x.site?btn(siteTitle(x.site),'sites',x.site):'Tổng công ty';
   const short=x.id==='dmpk'?'01 đầu mối kiêm nhiệm':String(x.seats);
   const top=[v.annualExcess>0?'Năm vượt '+format(v.annualExcess)+' giờ':'',v.peak&&v.peak.excess>0?'Tháng '+v.peak.m+' vượt '+format(v.peak.excess)+' giờ':''].filter(Boolean).join(' · ');
   return [positionLink(x)+(x.id==='dl-1'?'<small>Gồm công việc dữ liệu khách hàng kiêm nhiệm.</small>':''),office,short,nu(v.avgHours),e(capacityBadge(x))+(top?'<small>'+e(top)+'</small>':'')];
 });
}
function decisions(r,all){
 const active=all.filter(x=>x.review.annualExcess!==null);
 const yearly=active.filter(x=>x.review.annualExcess>0);
 const peaks=active.filter(x=>x.review.annualExcess===0&&x.review.peak.excess>0);
 const cluster=[...yearly,...peaks];
 const clinic=all.find(x=>x.id==='dmpk');
 const first=yearly.length?'Xác minh khối lượng cả năm của '+yearly.map(x=>name(x.id)+(x.slot?' · '+slotLabel(x.slot):'')+(x.site?' tại '+siteTitle(x.site):'')+' (vượt '+format(x.review.annualExcess)+' giờ/năm)').join(', ')+'.':'Giữ phương án 22 suất Tổng công ty, 13 suất ở 5 bệnh viện và 1 đầu mối Clinic kiêm nhiệm làm mốc bố trí.';
 const evidence='Số người thực có năm 2027 và lịch trực tại từng cơ sở chờ Phòng Nhân lực và đơn vị xác nhận. Số giờ trong bảng là ước tính theo sản phẩm.';
 const hr=['Chức danh','Địa điểm','Bố trí theo cơ cấu','Giờ việc đã tính/tháng (bình quân)','So với quỹ giờ của cơ cấu'];
 const peaksTable=cluster.length?table(['Người hoặc vị trí cần xem','Tháng vượt quỹ','Tháng cần hỗ trợ nhiều nhất','Việc có thể quyết'],cluster.map(x=>{
  const m=x.review.peak;const periods=x.review.periods.filter(v=>v.excess>0);
  const action=x.review.annualExcess>0?'Năm vượt '+format(x.review.annualExcess)+' giờ kế hoạch. Đo lại tải và kiểm khả năng phân công trước khi trình bổ sung người.':m.ongoing===0?'Dàn lại lịch làm tài liệu hoặc bố trí người thử, kiểm đúng chuyên môn.':'Xếp người hỗ trợ việc chuẩn bị hoặc đối soát theo lịch. Giữ người chịu trách nhiệm và thẩm quyền duyệt.';
  return [positionLink(x)+(x.site?'<small>'+e(siteTitle(x.site))+'</small>':''),periods.map(t=>'T'+t.m).join(', '),'T'+m.m+' · '+format(m.excess)+' giờ',e(action)];
 }),[2]):'<p>Trong kịch bản này, các vị trí đã có quỹ giờ đều nằm trong quỹ ở cả 12 tháng.</p>';
 return '<h4>Quyết định nhân sự theo kịch bản '+e(cases[u.scenario])+'</h4>'+stack([
 ['Bố trí dài hạn',e(first)+' <b>'+yearly.length+' người hoặc vị trí có khối lượng đã tính vượt quỹ bình quân năm.</b>'],
 ['Bố trí theo tháng','<b>'+peaks.length+' người hoặc vị trí chỉ vượt quỹ ở một số tháng.</b> Bảng dưới ghi tháng và số giờ cần thu xếp.'],
 ['Đầu mối Clinic','Khối lượng tham chiếu '+format(clinic.review.avgHours)+' giờ/tháng trong mô hình đủ phạm vi. Chốt số giờ kiêm nhiệm, ngày bàn giao và người thay với đơn vị.']
 ])+'<p class="note">'+e(evidence)+'</p>'+peaksTable+
 (cluster.length?detail('Xem toàn bộ đầu ra trong các tháng vượt quỹ',cluster.map(x=>detail(e(name(x.id))+(x.slot?' · '+e(slotLabel(x.slot)):'')+(x.site?' · '+e(siteTitle(x.site)):''),table(['Tháng','Giờ vượt','Từ vận hành','Từ thiết lập','Đầu ra và công việc tài liệu trong tháng'],periodProducts(x),[1,2,3]))).join('')):'')+
 '<h4>Bố trí tại từng bệnh viện và phòng khám</h4><p>Ở Tổng công ty, các chức danh có hai người được đối chiếu riêng theo phần việc hệ thống và bệnh viện. Điều chỉnh sản lượng phân công trong Lộ trình và đầu ra sẽ cập nhật bảng này. Mỗi dòng dưới đây thuộc một địa điểm. Các giờ làm ở Vinh, Hà Tĩnh và Quảng Bình được đối chiếu với người bố trí ở chính bệnh viện đó.</p>'+table(hr,positionRows(all.filter(x=>x.site).sort((a,b)=>model.sites.findIndex(s=>s.id===a.site)-model.sites.findIndex(s=>s.id===b.site))),[2,3])+
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
 const z=w.item,role=z.role,code=z.code;
 const group=['qlth-bc','cvtt-bc','bt-b','tk-b','md-b','qc-b','tn-b','mdcs-b'].includes(role)?'2':'1';
 const brand='Quản lý thương hiệu nhóm '+group;
 const editorial='Chuyên viên biên tập nhóm '+group;
 const media='Chuyên viên media Tổng công ty nhóm '+group;
 const channels='Chuyên viên quảng cáo và kênh số nhóm '+group;
 const comm='Chuyên viên truyền thông nhóm '+group;
 const creativeLead='Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở';
 const digitalLead='Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số';
 const branchLead='Trưởng nhóm Marketing cơ sở tại bệnh viện';
 const approval='Người có thẩm quyền duyệt phát hành theo phân cấp.';
 let receiver='';
 if(code==='du-gb')receiver='Trưởng phòng Marketing chủ trì giao ban. Vị trí tham dự và nhận kết luận theo lịch phòng.';
 else if(code==='ban-giao')receiver='Người được giao tiếp nhận phần việc và quản lý trực tiếp theo tuyến nhận phiếu bàn giao.';
 else if(code.startsWith('tt-')){
   const lead=role==='bt-ac'?creativeLead:digitalLead;
   receiver=code==='tt-tailieu'?lead+' nhận bảng theo dõi của tổ.':'Các thành viên của tổ nhận phân công hoặc nhắc hạn. '+lead+' nhận nội dung vượt khả năng điều phối.';
 }else{
   const routes={
    tp:{
     'kh-nam':'Ban Tổng Giám đốc nhận kế hoạch và dự toán năm để xem xét theo thẩm quyền.',
     ky:'Người trình kế hoạch hoặc chủ hạng mục nhận ý kiến duyệt theo phạm vi được giao.',
     trinh:'Ban Tổng Giám đốc hoặc cấp có thẩm quyền nhận tờ trình theo loại hồ sơ.',
     'giao-ban':'Các vị trí được giao việc trong phòng nhận kết luận và thời hạn thực hiện.',
     'gb-tct':'Ban Tổng Giám đốc nhận báo cáo tại giao ban; các đầu mối liên quan nhận chỉ đạo được chuyển về.',
     'gb-tgd':'Tổng Giám đốc nhận báo cáo tiến độ và chỉ đạo tại giao ban.',
     nganh:'Các đầu mối Marketing ngành dọc nhận kết luận, công việc và hạn thực hiện.',
     'bc-thang':'Ban Tổng Giám đốc nhận báo cáo tháng; Chuyên viên đo lường và đối soát cung cấp số liệu.',
     kpi:'Nhân sự được đánh giá và Phòng Nhân lực nhận kết quả theo thẩm quyền.',
     'bc-nam':'Ban Tổng Giám đốc nhận báo cáo tổng kết năm.',
     'uy-quyen':'Người phụ trách hồ sơ hoặc quyền liên quan nhận kết quả kiểm tra; việc vượt thẩm quyền chuyển Ban Tổng Giám đốc.'
    },
    cvt:{
     'tai-nd':'Tổ trưởng Tổ Nội dung và Sáng tạo nhận lịch cân tải; Trưởng phòng Marketing xử lý nội dung vượt thẩm quyền.',
     bv:'Trưởng nhóm của từng bệnh viện thuộc phạm vi triển khai xác nhận lịch. Trưởng phòng Marketing nhận tổng hợp từ '+creativeLead+'.',
     mau:'Tổ trưởng Tổ Nội dung và Sáng tạo nhận kết quả kiểm và phân công khắc phục; Trưởng phòng Marketing nhận báo cáo.',
     gt:'Trưởng nhóm cơ sở và đầu mối sản xuất liên quan nhận phân công ưu tiên. Trưởng phòng Marketing quyết định nội dung vượt thẩm quyền.',
     'huan-luyen':'Tổ trưởng và người tham gia huấn luyện nhận kết quả đánh giá; Phòng Nhân lực nhận hồ sơ nhân sự theo phân công.',
     baocao:'Trưởng phòng Marketing nhận báo cáo sai lệch tải và phương án điều chỉnh.',
     suco:'Đầu mối nhận việc thay và Trưởng nhóm liên quan nhận biên bản; Trưởng phòng Marketing xử lý nội dung vượt thẩm quyền.'
    },
    'cvt-2':{
     tai:'Tổ trưởng Tổ Truyền thông và Thương hiệu và Tổ trưởng Tổ Tăng trưởng số nhận kết quả rà tải. '+digitalLead+' báo cáo Trưởng phòng Marketing.',
     ooh:'Tổ trưởng Tổ Truyền thông và Thương hiệu và chuyên viên phụ trách nhận kết quả kiểm để khắc phục.',
     kenh:'Tổ trưởng Tổ Tăng trưởng số và chuyên viên phụ trách nhận kết quả kiểm để khắc phục.',
     chuyen:creativeLead+' nhận yêu cầu làm thay đổi lịch hoặc nhân sự cơ sở và chuyển theo tuyến Trưởng nhóm.',
     'dao-tao':'Tổ trưởng tổ liên quan và người tham gia nhận nội dung, kết quả huấn luyện.',
     baocao:'Trưởng phòng Marketing nhận báo cáo hiệu suất và phương án cải tiến hai tổ.',
     'canh-bao':'Tổ trưởng tổ liên quan và người phụ trách đầu ra nhận cảnh báo; Trưởng phòng Marketing xử lý nội dung vượt thẩm quyền.'
    },
    brand:{
     'ke-hoach':'Trưởng phòng Marketing nhận và duyệt kế hoạch theo phân cấp; Giám đốc cơ sở xác nhận chi thuộc ngân sách cơ sở.',
     hangmuc:'Trưởng phòng Marketing duyệt kế hoạch theo phân cấp. Giám đốc cơ sở xác nhận phần chi từ ngân sách cơ sở; cấp tài chính duyệt khoản chi theo thẩm quyền.',
     yeucau:'Đầu mối điều phối sản xuất được giao nhận phiếu đủ thông tin và phân việc đúng nhóm thương hiệu.',
     nghiemthu:'Đầu mối bàn giao sản phẩm và người phụ trách phát hành nhận kết quả nghiệm thu mục tiêu của '+brand+'.',
     'tien-do':'Trưởng phòng Marketing nhận báo cáo tiến độ; đầu mối liên quan nhận phần việc theo mã hạng mục.',
     hopdong:'Kế toán và cấp duyệt theo phân cấp nhận hồ sơ chi, hợp đồng và chứng từ đã đối soát.',
     tongket:'Trưởng phòng Marketing nhận báo cáo kết thúc hạng mục; Chuyên viên đo lường và đối soát cung cấp kết quả đối chiếu.',
     nam:'Trưởng phòng Marketing nhận hồ sơ mục tiêu, ngân sách và kết quả năm của nhóm '+group+'.',
     dn:'Đơn vị hoặc đối tác theo hồ sơ yêu cầu nhận bộ thông tin dịch vụ đã được xác nhận và duyệt theo thẩm quyền.',
     doitac:'Đơn vị hoặc đối tác liên quan và Trưởng phòng Marketing nhận nội dung thống nhất trong phạm vi hạng mục.'
    },
    comm:{
     bao:'Trưởng phòng Marketing hoặc cấp có thẩm quyền duyệt phát ngôn. '+brand+' nghiệm thu mục tiêu trước khi gửi cơ quan báo chí.',
     ooh:brand+' nhận hồ sơ, nghiệm thu theo hạng mục; Chuyên viên thiết kế ngoại tuyến nhận yêu cầu file thi công.',
     danhgia:'Trưởng phòng Marketing và chuyên viên phụ trách nhận cảnh báo để xử lý đánh giá nhạy cảm theo phân cấp.',
     sukien:brand+' và đơn vị tổ chức nhận hồ sơ phối hợp báo chí, đối tác hoặc sự kiện.',
     lich:branchLead+' hoặc đầu mối truyền thông cơ sở nhận lịch phát đã duyệt; '+brand+' nghiệm thu mục tiêu.',
     ct:'Trưởng phòng Marketing duyệt mẫu theo phân cấp; Ban Giám đốc cơ sở duyệt áp dụng tại địa phương.',
     suco:'Trưởng phòng Marketing nhận hồ sơ sự cố và quyết định phát ngôn theo thẩm quyền; '+digitalLead+' kiểm chuẩn nghiệp vụ.',
     kol:brand+' nhận hồ sơ hợp tác và nghiệm thu mục tiêu; cấp có thẩm quyền duyệt cam kết.',
     'mo-ooh':brand+' nhận hồ sơ truyền thông ngoại tuyến khai trương và nghiệm thu theo hạng mục.'
    },
    editorial:{
     bai:brand+' nhận bản thảo để nghiệm thu mục tiêu; bác sĩ xác nhận nội dung y khoa, người khác kiểm độc lập. '+approval,
     dv:brand+' nhận bài dịch vụ để nghiệm thu; đơn vị chuyên môn xác nhận nội dung và thông tin dịch vụ. '+approval,
     loi:media+' nhận kịch bản lời đã kiểm để lập phân cảnh. '+brand+' nghiệm thu mục tiêu; đơn vị chuyên môn xác nhận y khoa.',
     web:'Quản lý sản phẩm số nhận nội dung để cập nhật website hoặc App; bác sĩ xác nhận lại thông tin chuyên môn.',
     kt:'Người soạn nhận phiếu kiểm độc lập để sửa; '+brand+' nhận kết quả nghiệm thu theo hạng mục.',
     phat:media+' nhận lời phát thanh đã kiểm để sản xuất file âm thanh; '+brand+' nghiệm thu nội dung.',
     sk:brand+' nhận tin sau sự kiện hoặc bài nội bộ để nghiệm thu. '+approval,
     cc:'Contact Center nhận thông tin dịch vụ đã được '+brand+' nghiệm thu và cấp có thẩm quyền duyệt theo phân cấp.',
     sua:'Người yêu cầu sửa và người kiểm độc lập nhận bản cập nhật; '+brand+' nghiệm thu theo hạng mục.',
     english:'Quản lý sản phẩm số hoặc Contact Center nhận bản tiếng Anh theo mục đích sử dụng; bác sĩ xác nhận nội dung y khoa.',
     phaply:'Bộ phận pháp chế nhận chứng cứ Marketing để hoàn thiện hồ sơ theo thẩm quyền.',
     'mo-bai-gt':brand+' nhận bài giới thiệu cơ sở mới để nghiệm thu; đơn vị chuyên môn xác nhận thông tin dịch vụ.',
     'mo-mc':'Đầu mối tổ chức khai trương nhận kịch bản MC đã kiểm; '+brand+' nghiệm thu mục tiêu.',
     'mo-bai-kt':brand+' nhận bài truyền thông khai trương để nghiệm thu. '+approval
    },
    design:{
     c1:brand+' hoặc người yêu cầu nhận bản đúng quy cách; người kiểm độc lập kiểm trước phát hành.',
     c2:brand+' hoặc người yêu cầu nhận file thiết kế để nghiệm thu; người khác kiểm nhận diện.',
     c3:brand+' hoặc người yêu cầu nhận bộ file nguồn và file xuất; người khác kiểm nhận diện.',
     c4:brand+' nghiệm thu hình ảnh chủ đạo; cấp có thẩm quyền duyệt nhận diện theo phân cấp.',
     kiem:'Người làm thiết kế nhận phiếu kiểm nhận diện độc lập và xử lý sai lệch.',
     sua:'Người yêu cầu nhận phiên bản đã sửa; người khác kiểm lại trước phát hành.',
     'mo-anpham':brand+' và đầu mối tổ chức khai trương nhận ấn phẩm theo danh mục đã giao.'
    },
    'tk-nt':{
     banve:'Chuyên viên truyền thông đúng nhóm nhận file kỹ thuật để triển khai biển sau khi cấp có thẩm quyền duyệt.',
     kiem:'Người làm file in nhận phiếu kiểm độc lập để xử lý thông số.',
     trangtri:'Chuyên viên truyền thông đúng nhóm nhận file triển khai trang trí theo địa điểm.',
     thu:'Chuyên viên truyền thông và đơn vị phụ trách địa điểm nhận biên bản khảo sát hoặc so mẫu in.'
    },
    media:{
     pc:'Media cơ sở hoặc ê-kíp sản xuất đúng nhóm nhận bảng phân cảnh và danh sách cảnh quay.',
     kiem:'Media cơ sở đúng bệnh viện nhận phiếu sửa hoặc kết quả kiểm kỹ thuật. '+brand+' nhận bản đủ điều kiện để nghiệm thu mục tiêu.',
     v3t:brand+' nhận bản V3 vượt mẫu để nghiệm thu mục tiêu; người khác kiểm kỹ thuật. '+approval,
     v4:brand+' nhận bản V4 chiến dịch để nghiệm thu mục tiêu; người khác kiểm kỹ thuật. '+approval,
     ghi:'Ê-kíp dựng đúng nhóm nhận tư liệu quay chuyên sâu kèm quyền sử dụng và mã hạng mục.',
     am:comm+' và đầu mối phát thanh cơ sở nhận file âm thanh đã kiểm mức âm.',
     kho:'Người quản lý kho tư liệu và đầu mối sử dụng đúng nhóm nhận lô tư liệu kèm quyền sử dụng.',
     sua:'Người yêu cầu và người kiểm kỹ thuật độc lập nhận phiên bản đã sửa; '+brand+' nghiệm thu mục tiêu.',
     v2t:brand+' nhận video sản xuất tại Tổng công ty để nghiệm thu mục tiêu; người khác kiểm kỹ thuật. '+approval,
     'mo-quay':'Ê-kíp dựng đúng nhóm nhận tư liệu quay khai trương theo mã hạng mục.',
     'mo-dung':brand+' nhận video khai trương để nghiệm thu mục tiêu; người khác kiểm kỹ thuật. '+approval
    },
    channels:{
     fb:brand+' nhận lịch và kết quả kênh để nghiệm thu; Chuyên viên đo lường và đối soát nhận số liệu.',
     tik:brand+' nhận lịch và kết quả kênh để nghiệm thu; Chuyên viên đo lường và đối soát nhận số liệu.',
     khac:brand+' nhận lịch và kết quả kênh để nghiệm thu; Chuyên viên đo lường và đối soát nhận số liệu.',
     ads:brand+' nghiệm thu mục tiêu chiến dịch; Chuyên viên đo lường và đối soát nhận số liệu. Chi phí do cấp có thẩm quyền duyệt.',
     landing:'Quản lý sản phẩm số nhận trang đích để nghiệm thu; Chuyên viên đo lường và đối soát kiểm mã nguồn và form.',
     suco:'Tổ trưởng Tổ Tăng trưởng số nhận hồ sơ sự cố; Trưởng phòng Marketing quyết định nội dung vượt quyền.',
     tin:'Contact Center hoặc nhóm khách đủ điều kiện nhận tin theo kênh được duyệt; Chuyên viên dữ liệu kiểm danh sách và điều kiện sử dụng.',
     'dia-chi':brand+' nhận kết quả cập nhật; đơn vị sở hữu địa điểm xác nhận thông tin gốc.',
     'mo-ads':brand+' nhận kết quả chiến dịch khai trương; cấp có thẩm quyền duyệt chi theo phân cấp.'
    },
    'dl-1':{
     tuan:'Quản lý thương hiệu và Trưởng phòng Marketing nhận báo cáo BM-2.',
     chot:'Trưởng phòng Marketing nhận và duyệt bản chốt kỳ theo phân cấp; số được đối soát độc lập.',
     bc:'Quản lý thương hiệu nhận bộ số và thuyết minh để lập báo cáo tháng.',
     hm:'Quản lý thương hiệu phụ trách hạng mục và Trưởng phòng Marketing nhận kết quả đối soát.',
     kt:'Tổ trưởng Tổ Tăng trưởng số nhận phiếu theo tuyến; Trưởng phòng Marketing nhận số tổng hợp qua báo cáo.',
     kpi:'Trưởng phòng Marketing nhận bảng điểm và thực hiện đánh giá theo phân cấp.',
     nam:'Trưởng phòng Marketing nhận bảng số liệu để lập và trình báo cáo năm.',
     'phan-tich':'Người yêu cầu thuộc Ban Tổng Giám đốc nhận bảng phân tích qua tuyến và mã việc đã giao.'
    },
    'dl-2':{
     ds:'Chuyên viên quảng cáo và kênh số đúng nhóm nhận danh sách đủ điều kiện cho đợt gửi. Bộ phận phụ trách dữ liệu và pháp chế kiểm điều kiện sử dụng.',
     chatluong:'Trưởng phòng Marketing nhận báo cáo chất lượng CRM; đầu mối dữ liệu liên quan nhận lỗi để xử lý.',
     'thi-truong':'Quản lý thương hiệu và Trưởng phòng Marketing nhận báo cáo khảo sát, dữ liệu và phân tích.',
     sai:'Quản lý sản phẩm số nhận phiếu để tổng hợp; Phòng Công nghệ xử lý kỹ thuật, Trưởng phòng Marketing nhận báo cáo theo phân cấp.',
     'anh-khach':'Trưởng phòng Marketing nhận báo cáo quyền sử dụng hình ảnh; Trưởng nhóm cơ sở và Kênh số xử lý chứng từ hoặc gỡ khi cần.'
    },
    qlsps:{
     yeucau:'Phòng Số hóa hoặc Phòng Công nghệ theo hệ thống nhận yêu cầu nghiệp vụ và tiêu chí nghiệm thu.',
     uat:'Đơn vị kỹ thuật phụ trách thay đổi nhận biên bản kiểm thử và bằng chứng lỗi hoặc đạt.',
     seo:'Chuyên viên biên tập đúng nhóm nhận yêu cầu cập nhật nội dung; Quản lý thương hiệu đúng nhóm nhận kết quả.',
     kenh:'Tổ trưởng và chuyên viên phụ trách kênh nhận phiếu xử lý; '+digitalLead+' kiểm chuẩn nghiệp vụ theo phân công.',
     suco:'Phòng Công nghệ hoặc đơn vị kỹ thuật phụ trách nhận lỗi; '+digitalLead+' nhận báo cáo nghiệp vụ.',
     'ben-thu-ba':'Quản lý thương hiệu nhóm 2 nhận biên bản rà vận hành website của đơn vị tương ứng.'
    },
    qlml:{
     vung:creativeLead+' nhận kết quả đánh giá Trưởng nhóm khi có quyết định bàn giao tuyến vùng.',
     baocao:creativeLead+' nhận báo cáo vùng theo danh sách cơ sở được bàn giao.'
    },
    branch:{
     nhucau:brand+' và đầu mối được phân tuyến tại Tổng công ty nhận phiếu đủ thông tin.',
     tin:'Ban Giám đốc cơ sở xác nhận nội dung tại chỗ; đầu mối phát hành nhận tin theo phân cấp.',
     'ke-hoach':brand+' nhận kế hoạch tháng của bệnh viện; Ban Giám đốc cơ sở xác nhận nhu cầu tại chỗ.',
     hop:'Nhân sự Marketing tại bệnh viện nhận lịch và kết luận giao ban của Trưởng nhóm.',
     thaydoi:brand+', '+channels+' và '+editorial+' nhận thông tin đã được cơ sở xác nhận theo phạm vi.',
     sk:'Nhân sự tại hiện trường nhận phân công sự kiện; Ban Giám đốc cơ sở xác nhận phần tại chỗ.',
     chot:creativeLead+' nhận báo cáo tuần và số liệu từ Trưởng nhóm cơ sở.',
     'danh-gia':creativeLead+' nhận phiếu nhận xét nhân sự do Trưởng nhóm quản lý.',
     'nt-le':'Đầu mối Tổng công ty đã giao yêu cầu nhận biên bản điều kiện tại cơ sở; '+brand+' nghiệm thu mục tiêu hạng mục.'
    },
    onsite:{
     haucan:branchLead+' và đơn vị tổ chức nhận hồ sơ hiện trường; Ban Giám đốc cơ sở duyệt phần thuộc thẩm quyền.',
     congdong:branchLead+' và đơn vị chủ trì hoạt động nhận biên bản; Ban Giám đốc cơ sở duyệt phần tại chỗ.',
     bien:comm+' và Chuyên viên thiết kế ngoại tuyến nhận phiếu hiện trạng biển kèm ảnh.',
     'baocao-bien':comm+' và Chuyên viên thiết kế ngoại tuyến nhận báo cáo tháng kèm ảnh; Trưởng nhóm cơ sở theo dõi việc xử lý.',
     'bao-hong':branchLead+' và đầu mối phụ trách sửa chữa tại bệnh viện nhận thông tin trong ngày; '+comm+' nhận để theo dõi theo tuyến.',
     phat:comm+' nhận xác nhận lịch phát và ảnh màn hình; cơ sở xác nhận tình trạng thực tế.',
     dongy:'Chuyên viên dữ liệu khách hàng và thị trường nhận trạng thái đồng ý theo quyền; '+branchLead+' kiểm đủ chứng từ trước bàn giao.',
     bandi:comm+' và đầu mối Tổng công ty theo mã việc nhận biên bản, ảnh và kết quả hiện trường.',
     dilai:branchLead+' nhận thông tin hoàn thành chuyến đi theo lệnh đã giao.',
     hop:branchLead+' chủ trì giao ban tại cơ sở và giao lịch cho nhân sự Marketing.'
    },
    localmedia:{
     v1:branchLead+' nhận clip tin nhanh và tư liệu để chuyển theo tuyến. '+approval,
     v2:media+' kiểm kỹ thuật bản dựng; '+brand+' nghiệm thu mục tiêu. Đơn vị chuyên môn xác nhận y khoa khi có. '+approval,
     v3:media+' kiểm kỹ thuật bản dựng; '+brand+' nghiệm thu mục tiêu. Đơn vị chuyên môn xác nhận y khoa khi có. '+approval,
     anh:'Người yêu cầu theo mã việc và '+branchLead+' nhận bộ ảnh hiện trường kèm quyền sử dụng.',
     sukien:'Ê-kíp sản xuất đúng nhóm và '+branchLead+' nhận tư liệu sự kiện theo mã việc.',
     kho:'Người quản lý kho tư liệu và '+branchLead+' nhận lô tư liệu kèm chứng từ quyền sử dụng.',
     sua:media+' nhận bản dựng đã sửa để kiểm kỹ thuật; '+brand+' nghiệm thu mục tiêu.',
     di:branchLead+' nhận xác nhận chuyến đi ghi hình theo lệnh.',
     hop:branchLead+' chủ trì giao ban tại cơ sở và giao lịch cho nhân sự Marketing.'
    },
    dmpk:{
     yc:creativeLead+' tiếp nhận và phân tuyến một mã việc cho Tổng công ty; '+brand+' xác định mục tiêu.',
     anh:'Đầu mối Marketing Tổng công ty theo mã việc nhận ảnh đã được phòng khám xác nhận; '+channels+' đăng theo phân quyền.',
     capnhat:'Đầu mối Marketing Tổng công ty và '+channels+' nhận thông tin đã được phòng khám xác nhận.',
     quyen:'Đầu mối Marketing Tổng công ty và Chuyên viên dữ liệu nhận chứng từ theo quyền truy cập.',
     sukien:'Người phụ trách phòng khám và đầu mối Marketing theo mã việc nhận xác nhận hỗ trợ hiện trường.',
     di:'Người phụ trách phòng khám và đầu mối Marketing theo mã việc nhận kết quả bàn giao.',
     phoi:creativeLead+' tiếp nhận lịch và phân tuyến nhu cầu Marketing của phòng khám.'
    }
   };
   let family=role;
   if(role.startsWith('qlth-'))family='brand';
   else if(role.startsWith('cvtt-'))family='comm';
   else if(role.startsWith('bt-'))family='editorial';
   else if(role==='tk-a'||role==='tk-b')family='design';
   else if(role.startsWith('mdcs-'))family='localmedia';
   else if(role.startsWith('md-'))family='media';
   else if(role.startsWith('qc-'))family='channels';
   else if(role.startsWith('tn-'))family=['haucan','congdong','bien','phat','dongy','bandi','dilai'].includes(code)?'onsite':'branch';
   else if(role==='qhcs')family='onsite';
   receiver=routes[family]?.[code]||'Người nhận đầu ra cụ thể chờ xác nhận theo phiếu giao việc và tuyến quản lý của vị trí.';
 }
 const special={
   'cvt/bv':'Hằng tuần theo lịch giao việc của từng bệnh viện.',
   'cvt-2/tai':'Hằng tuần, một phiếu cho mỗi tổ.',
   'dl-1/kt':'Ghi phiếu theo lịch tuần. Chốt số giờ từ sổ theo dõi vào kỳ báo cáo quý của MTCV.',
   'dl-1/nam':'Tháng 12, trước khi Trưởng phòng trình báo cáo năm.',
   'dl-1/tuan':'Hằng tuần theo lịch báo cáo.',
   'qhcs/bien':'Hằng tuần theo lịch kiểm tại bệnh viện.',
   'qhcs/baocao-bien':'Hằng tháng sau khi tổng hợp các lượt kiểm.',
   'qhcs/bao-hong':'Báo trong ngày khi phát hiện hư hỏng.',
   'tn-b/bien':'Hằng tháng theo lịch kiểm hiện trạng của bệnh viện.',
   'tp/kpi':'Trong 05 ngày làm việc đầu quý sau. Tháng 1 chốt quý IV/2026 khi có hồ sơ bàn giao.',
   'dl-1/kpi':'Trong 05 ngày làm việc đầu quý sau. Tháng 1 chốt quý IV/2026 khi có hồ sơ bàn giao.'
 };
 const due=special[z.id]||'Theo kỳ '+periodName(z.period)+'; hạn cụ thể theo MTCV và phiếu giao việc.';
 return [receiver,due];
}
function actualRoleScope(rid,site){
 const v=roleMap[rid],g=v.nhom_thuong_hieu;
 if(rid==='qlml')return 'Vị trí dự kiến; chỉ nhận phạm vi và tải của các cơ sở khi có quyết định phân vùng và bàn giao.';
 if(site?.group==='clinic')return 'Một đầu mối kiêm nhiệm chung cho TTH Clinic Khe Tre và A Lưới theo phương án trong Khung. Chưa có giờ được phân và sản lượng tách riêng từng phòng khám.';
 if(site)return 'Công việc và lượng tại '+site.name+'; điều phối, xác nhận và nghiệm thu theo tuyến của cơ sở và Tổng công ty.';
 const hospitals=group=>model.sites.filter(s=>s.group===group).map(s=>s.name).join('; ');
 if(g==='N1')return 'Nhóm 1: TTH Group, TTH Healthcare, TTH Hospital và TTH Clinic theo phần việc được giao. Ba bệnh viện trong mô hình: '+hospitals('g1')+'. Clinic dùng một đầu mối chung, chưa tách lượng theo phòng khám.';
 if(g==='N2')return 'Nhóm 2: '+hospitals('g2')+'; Winmed, Tuệ Đức Thiện và các đơn vị khác thuộc nhóm theo phạm vi giao việc. Phần lớn sản lượng chưa được tách riêng cho từng công ty.';
 return 'Phạm vi chung hai nhóm theo MTCV và từng mã việc: '+hospitals('g1')+'; '+hospitals('g2')+'; TTH Clinic và các đơn vị khác khi được giao. Lượng từng đơn vị ngoài năm bệnh viện chưa có đầy đủ căn cứ.';
}
function roleMandate(rid,site){
 const v=roleMap[rid],c=v.cnnv_2027||{};
 const rows=[['Phạm vi trong hệ thống',actualRoleScope(rid,site)],['Chức năng',c.chuc_nang||v.muc_dich],['Nhiệm vụ trọng tâm',c.nhiem_vu_trong_tam||v.phan_dinh_chu_tri_dau_ra],['Đầu ra chủ trì',v.phan_dinh_chu_tri_dau_ra],['Đầu vào và bàn giao',c.dau_vao_va_ban_giao||v.phan_dinh_ban_giao_dau_vao],['Tuyến quản lý',c.quan_he_bao_cao||v.bao_cao_cho],['Giới hạn và thẩm quyền',c.ranh_gioi_khong_lam_thay],['Kiểm và duyệt',c.quyen_han_va_kiem_soat||v.phan_dinh_kiem_duyet]];
 let html='<h4>Chức năng, nhiệm vụ và phạm vi của '+e(v.ten)+'</h4>'+stack(rows.filter(x=>x[1]).map(([a,b])=>[a,e(plain(b))]));
 if(rid==='dl-1'){
  const d=roleMap['dl-2'],x=d.cnnv_2027||{};
  html+='<p class="note"><b>Phần kiêm nhiệm trong cùng quỹ giờ:</b> '+e(d.ten)+'. Xem riêng chức danh này trong danh sách để đối chiếu toàn bộ nhiệm vụ.</p>'+stack([['Chức năng kiêm nhiệm',e(x.chuc_nang)],['Nhiệm vụ kiêm nhiệm',e(x.nhiem_vu_trong_tam)],['Giới hạn và bàn giao',e(x.ranh_gioi_khong_lam_thay)+'<br>'+e(x.dau_vao_va_ban_giao)]]);
 }
 return html+'<p class="fine">Nội dung trích từ CNNV và MTCV trong Khung 2027; phân công chính thức theo quyết định và hồ sơ nhân sự có hiệu lực.</p>';
}
function sourceMtcv(rid){
 let out=detail('Toàn bộ '+(model.jd[rid].length-1)+' dòng đầu ra, kỳ hạn và nơi nhận trong MTCV gốc',origOutputs(rid));
 if(rid==='dl-1')out+=detail('MTCV gốc của Chuyên viên dữ liệu khách hàng và thị trường đang kiêm nhiệm',origOutputs('dl-2'));
 return out;
}
function workBasis(w,inTrial,pilots){
 const z=w.item;
 if(inTrial&&z.id==='cvt/bv')return 'Hai Trưởng nhóm của hai bệnh viện thí điểm theo lộ trình; sau thí điểm đối chiếu số bệnh viện đã bàn giao.';
 if(inTrial&&typeof z.q==='string'&&/:(review|script)$/.test(z.q)){
  const group=z.q.split(':')[0],id=pilots[group];
  return (id?'Tính phần V2/V3 của '+siteTitle(id)+' theo kịch bản thí điểm. ':'Chờ xác nhận bệnh viện thí điểm của nhóm để tính phần V2/V3. ')+volumeReason(w);
 }
 return volumeReason(w);
}
function assignmentCondition(w,site){
 const z=w.item,notes=[];
 if(z.id==='tp/kpi'||z.id==='dl-1/kpi')notes.push('Các mốc T1, T4, T7 và T10 là chốt kết quả quý trước. Mốc T1 chỉ thực hiện khi có hồ sơ được bàn giao.');
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
 const heading='<h3>Đầu ra theo từng vị trí và lộ trình</h3><p>Phương án gồm 22 suất ở Tổng công ty, 13 suất tại 5 bệnh viện và 1 đầu mối Clinic kiêm nhiệm. Chọn chức danh, giai đoạn và đơn vị để đọc chức năng, sản phẩm, số lượng tính thử, người nhận và thời hạn.</p>'+choices+
   (division?'<p class="fine">Hai người cùng MTCV, phân công cố định theo Mục 2 và Mục 3: một người phụ trách hệ thống, một người phụ trách bệnh viện. Nơi đặt hàng quyết định người nhận từng sản phẩm. Các số phân bổ chưa có phiếu giao là giả định tính thử. Người kiểm độc lập phải khác người lập.</p>':'');
 const gate='<p class="note"><b>'+e(st.title)+'.</b> '+e(st.scope)+'</p>';
 const roleIndex=detail('Xem đủ 26 chức danh và một số đầu ra chính',table(['Chức danh','Suất theo cơ cấu','Phần việc chủ trì trong MTCV','Ví dụ sản phẩm để mở chi tiết'],db.vi_tri.map(v=>[btn(v.ten,'deliveryRole',v.id),v.id==='dmpk'?'1 kiêm nhiệm':v.id==='dl-2'?'Kiêm cùng Đo lường':v.id==='qlml'?'Chờ phân vùng':String(model.seats[v.id]),e(v.phan_dinh_chu_tri_dau_ra||v.muc_dich),e(model.work.filter(w=>w.role===v.id&&w.kind!=='T'&&w.code!=='du-gb').slice(0,3).map(w=>w.name).join(' · '))]),[1])+'<p>Chọn tên chức danh để xem toàn bộ đầu ra và phần tài liệu trong kỳ.</p>');
 const keyMilestones=detail('Đầu ra cần chốt để chuyển giai đoạn',table(['Chủ trì phần việc','Đầu ra','Người nhận hoặc điều kiện hoàn thành'],phaseJobs[u.phase].map(([id,job,goal])=>[cellRole(id),e(job),e(goal)]))+'<p>'+e(st.gate)+'</p>',true);
 if(u.phase==='prep'){
   const own=phaseJobs.prep.filter(x=>x[0]===rid);
   return heading+roleIndex+gate+roleMandate(rid,site)+(own.length?table(['Chức danh','Đầu ra chuẩn bị','Bàn giao'],own.map(([id,n,g])=>[e(name(id)),e(n),e(g)])):'<p>Giai đoạn chuẩn bị sử dụng nhân sự hiện có. Chức danh này nhận việc theo quyết định phân công. Sản lượng vận hành ba tháng đầu có ở giai đoạn thí điểm.</p>')+sourceMtcv(rid)+keyMilestones+detail('Toàn bộ lộ trình',phaseTable);
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
 let operationHours=0,pending=0;const conditional=[];
 const rows=works.map(w=>{
   const count=monthsHere.map(m=>slotShare(w,slot,phasedQty(w,m),m,r)),incomplete=count.some(v=>v===null);
   const qty=incomplete?null:sum(count),hours=incomplete?null:sum(monthsHere.map((m,i)=>{
     const initial=w.qty[m-1];
     return initial?w.hours[m-1]*count[i]/initial:count[i]*sum(w.t)/60;
   }));
   if(hours!=null)operationHours+=hours;else pending++;
   const [recipient,due]=deliveryRoute(w);
   const product=btn(w.item.name,'roles',w.id)+(rid==='dl-1'&&w.item.role==='dl-2'?'<small>Phần dữ liệu kiêm nhiệm</small>':'')+'<small><b>Quy cách:</b> '+e(w.item.note)+'<br><b>Căn cứ trong Khung:</b> '+e(w.item.ref)+'</small>'+assignmentCondition(w,site);
   if(qty===0){
     const when=w.item.kind==='G'?'Chờ quyết định phân vùng':w.item.period.startsWith('y')?'Thực hiện vào '+periodName(w.item.period):slot!=='all'?'Chưa phân cho người đang chọn trong kịch bản':w.item.kind==='U'?'Khi phát sinh; chưa có số lần để tính giờ':'Chưa có số lượng trong kỳ hoặc theo điều kiện giao việc';
     conditional.push([product,e(when),e(recipient)+'<small>Hạn: '+e(due)+'</small>']);return null;
   }
   const quantity=incomplete?'Chờ xác nhận phạm vi':count.map((v,i)=>'T'+monthsHere[i]+': '+format(v)).join(' / ');
   const measure='<b>'+e(quantity)+'</b><small>Tổng quý: '+format(qty)+' · '+format(sum(w.t))+' phút/đầu ra · '+format(hours)+' giờ</small><small><b>Cách xác định lượng:</b> '+e(workBasis(w,inTrial,pilots))+'</small>';
   return [product,measure,e(recipient)+'<small>Hạn: '+e(due)+'</small>'];
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
 const advisory='<p class="fine">Định mức là phút của người làm một đơn vị đầu ra. Giờ theo quý gồm thời gian trực tiếp, phối hợp, kiểm, sửa và di chuyển của vị trí. Mỗi người ghi giờ cho công đoạn mình làm. Thời gian chờ duyệt nằm ngoài phép tính.</p>';
 return heading+roleIndex+gate+trialSelection+roleMandate(rid,site)+splitControls+'<h4>Sản phẩm của '+e(name(rid))+(site?' · '+e(site.name):'')+'</h4><p>'+e(scope)+'</p><p class="note"><b>Số lượng và thời gian là kịch bản tính thử.</b> Cần đối chiếu kế hoạch từng đơn vị, nhật ký thực hiện, nhân sự thực có và thời điểm bàn giao trước khi giao chỉ tiêu hoặc quyết định số người. Nhịp thực hiện, quy cách và phạm vi được ghi trên từng dòng.</p>'+
 '<p class="receipt"><b>'+(pending&&operationHours===0?'Chờ xác nhận giờ đầu ra vận hành':format(operationHours)+' giờ đầu ra vận hành')+'</b> và <b>'+format(docsHours)+' giờ công việc tài liệu</b> trong quý theo phần đã định lượng.'+(pending?' Còn '+pending+' dòng chờ xác nhận phạm vi.':'')+(!ready?' Số giờ tại cơ sở đang dùng làm tham chiếu, chờ giao cho vai trò mới.':'')+'</p>'+
 (rows.length?table(['Sản phẩm và quy cách bàn giao','Sản lượng, thời gian và căn cứ tính thử','Người nhận, kiểm và hạn'],rows):'<p>Chưa có sản phẩm được định lượng trong giai đoạn đã chọn.</p>')+advisory+
 (conditional.length?'<h4>Đầu ra theo phát sinh, điều kiện hoặc đến kỳ khác</h4><p>Các việc này vẫn thuộc phạm vi vị trí; số 0 trong kỳ không có nghĩa là bỏ nhiệm vụ.</p>'+table(['Sản phẩm và quy cách','Điều kiện thực hiện','Người nhận, kiểm và hạn'],conditional):'')+
 '<h4>Quy trình, mẫu và báo cáo do vị trí tham gia trong quý</h4>'+(stageDocs.length?table(['Hồ sơ','Phạm vi','Tháng','Phần việc của vị trí','Sản lượng theo lịch','Giờ trong quý','Người kiểm chuẩn'],stageDocs.map(d=>d.cells),[5]):'<p>Chưa phân công hồ sơ tài liệu cho vị trí này trong lịch quý.</p>')+
 sourceMtcv(rid)+keyMilestones+detail('Toàn bộ lộ trình',phaseTable);
}
