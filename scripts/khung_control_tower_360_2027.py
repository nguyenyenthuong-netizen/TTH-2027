#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TTH 2027 - 360-degree evidence and capacity control tower.
A READ-ONLY projection on the existing 26-role ledger. No fabricated output, workload
hours, future assets, revenue, approval or owner. Release gated on live Chrome UI.
"""
import json, re, sys
from pathlib import Path
p=Path(sys.argv[1])/"khung-marketing"/"index.html"
plan_path=Path(sys.argv[1])/"ke-hoach-mkt-2027"/"data.json"
s=p.read_text("utf-8")
marker="tth-control-tower-360-2027"
if marker in s:
    print("PASS CONTROL 360: already present")
    raise SystemExit(0)
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s)
if not m:raise SystemExit("Missing authoritative TTH 2027 model")
D=json.loads(m.group(2))
model=D["dinh_bien_theo_dau_ra_2027"]
plan=json.loads(plan_path.read_text("utf-8"))
year=plan["yearEndCommitments"]
outcomes=year["outcomes"]
metrics=[k for x in outcomes for k in x["kpis"]]
assert len(model["roles"])==26 and sum(model["seats"].values())==36
assert len(outcomes)==7 and len(metrics)==25
assert len(plan["portfolio"]["projects"])==24
assert len(plan["ctdaAddendum"]["programs"])>0
assert model["dedup_scope_audit_2027"]["workflowOutputs"]==568
assert all(x["baseline2026"] is None and x["target2027"] is None for x in metrics)
model["control_360_2027"]={
 "version":marker,
 "sources":["MTCV/CNNV 26 chức danh","Sổ tải W theo công đoạn/kỳ",
            "Sổ tài liệu và CMS chung","Kiểm toán 568 đầu ra",
            "Danh mục chương trình/dự án và KPI cuối năm"],
 "outcomesDraft":len(outcomes),
 "unapprovedResultKpis":sum(k["target2027"] is None or k["baseline2026"] is None for k in metrics),
 "projectsInPlan":len(plan["portfolio"]["projects"]),
 "highlightOutputs":plan["ctdaAddendum"]["counts"]["outputs"],
 "highlightSteps":plan["ctdaAddendum"]["counts"]["steps"],
 "highlightBooking":plan["ctdaAddendum"]["workloadPolicy"]["bookingStatus"],
 "warning":"Sản lượng và phút công đoạn là giả định. Danh mục 132 đầu ra trọng điểm không tự được cộng vào sổ W trước khi có bản đồ giao công đoạn.",
 "normalization":"Một mã việc và một công đoạn làm đúng một lượt. Giờ R/H/K/T/U, tài liệu và CMS đều là một phần của cùng sổ, không cộng lại bảng kiểm toán."
}
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")+s[m.end(2):]
start='<script id="tth-staffing-app">'
a=s.index(start)
b=s.index("</script>",a)
js=s[a+len(start):b]
old="const tabs={suff:'Kết luận định biên',"
new="const tabs={suff:'Kết luận định biên',executive:'Điều hành 360°',"
assert js.count(old)==1
js=js.replace(old,new,1)
old="const panels={roadmap:"
new="const panels={executive:controlTower360,roadmap:"
assert js.count(old)==1
js=js.replace(old,new,1)

insertion=r"""
/* tth-control-tower-360-2027
   Read-only combined management view, never a new ledger of chargeable work. */
function controlTower360(){
 const r=getRun(),a=model.dedup_scope_audit_2027,c=model.control_360_2027,filter=u.towerFilter||'priority';
 const selected=u.period,sc=cases[r.scenario],monthLabel=selected?'tháng '+selected:'cả năm 2027';
 const byKind={R:0,H:0,U:0,K:0,T:0,G:0};
 for(const w of r.works){
  const h=selected?w.hours[selected-1]:sum(w.hours);
  byKind[w.item.kind]=(byKind[w.item.kind]||0)+h;
 }
 const keys=runsKeys(r,'all'),charged=roll(r,keys,selected);
 const difference=Math.abs(sum(Object.values(byKind))-(charged.regular+charged.incident));
 const channels=r.works.filter(w=>['qc-a','qc-b'].includes(w.item.role)&&['fb','tik','khac'].includes(w.item.code));
 const channelHours=sum(channels.map(w=>selected?w.hours[selected-1]:sum(w.hours)/(12)));
 const caps=poolReviews(r);
 const risks=caps.map(x=>{
  const ps=(x.review.periods||[]).filter(v=>!selected||v.m===selected);
  const sorted=[...ps].sort((x,y)=>y.excess-x.excess);
  const worst=sorted[0]||null;
  const unknown=x.review.annualExcess===null;
  const over=ps.some(p=>p.excess>0.000001);
  const overTotal=ps.some(p=>x.review.totalLimit!=null&&p.all>x.review.totalLimit+0.000001);
  return {x,ps,worst,unknown,over,overTotal,priority:unknown?2:overTotal?0:over?1:3};
 });
 const peakRisks=risks.filter(x=>x.over);
 const unknownCaps=risks.filter(x=>x.unknown);
 const ranked=risks.filter(x=>filter==='all'||(filter==='priority'&&(x.over||x.unknown))||(filter==='over'&&x.over)||(filter==='unknown'&&x.unknown))
   .sort((a,b)=>a.priority-b.priority||(b.worst?.excess||0)-(a.worst?.excess||0));
 const status=v=>v.unknown?'CHƯA CÓ QUỸ GIỜ':v.overTotal?'VƯỢT QUỸ GIỜ TỔNG':v.over?'VƯỢT 75% KẾ HOẠCH':'Trong quỹ đã tính; chưa nghiệm thu đủ tải';
 const roleRows=ranked.slice(0,22).map(v=>{
  const item=v.x,peak=v.worst;
  return [
   positionLink(item)+(item.site?'<small>'+e(siteTitle(item.site))+'</small>':'')+
    (item.slot?'<small>'+e(slotLabel(item.slot))+'</small>':''),
   item.seats===0?'Kiêm nhiệm/chưa kích hoạt':nu(item.seats,0),
   peak?'T'+peak.m:'Chờ xác nhận',
   peak?nu(peak.planned,1):'Chưa có quỹ',
   item.x===undefined&&v.unknown?'Chưa chốt':v.unknown?'Chờ quỹ giờ':nu(v.x.review.planLimit,1),
   peak?nu(peak.all,1):'Chờ xác nhận',
   peak?nu(peak.excess,1):'Chưa có số',
   e(status(v))
  ];
 });
 const issueRows=a.openItems.map(x=>[
  e(x.priority),e(x.area),e(x.issue),e(x.gate)
 ]);
 const flow=[
  ['1. Yêu cầu và mục tiêu','Quản lý thương hiệu đúng nhóm xác nhận phạm vi, cơ sở, mục tiêu, mã yêu cầu','Chỉ có một mã yêu cầu gốc'],
  ['2. Kế hoạch và năng lực','Chuyên viên trưởng/Trưởng phòng cân sản lượng, số người, kỳ và quỹ 75%','Không nhận việc vượt khả năng nếu chưa có phương án'],
  ['3. Sản xuất chuyên môn','Biên tập, Thiết kế, Media và cơ sở thực hiện đúng MTCV','Một bản nội dung/sản phẩm gốc, nhiều phiên bản có ghi nguồn'],
  ['4. Kiểm và phê duyệt','Quản lý thương hiệu, chủ dữ liệu y khoa và cấp duyệt đúng phân quyền','Tách làm, kiểm, sửa và quyền ký; không duyệt thay'],
  ['5. Phát hành, vận hành','Người quản lý từng kênh/CMS thực hiện đúng phiên bản và lịch','Không đếm lại công sản xuất nội dung gốc'],
  ['6. Đo lường và cải tiến','Chuyên viên đo lường đối soát, quản lý kết luận, cập nhật định mức','Một số nguồn, không nhân báo cáo theo nền tảng']
 ];
 const outputs=[
  ['Quản trị mục tiêu',c.outcomesDraft+' nhóm kết quả / '+c.unapprovedResultKpis+' chỉ số chưa chốt số nền hoặc mục tiêu',
   'Chưa thể chứng minh hiệu quả doanh thu/chuyển đổi',btn('Xem lộ trình','roadmap')],
  ['Phạm vi CNNV, MTCV',a.mtcvLines+' dòng MTCV; '+a.workflowOutputs+' trách nhiệm theo bước',
   'Cần xác minh phân vai và định mức thực tế',btn('Kiểm toán trách nhiệm','audit')],
  ['Kênh và tài sản',a.channelsUnverified+' ô kênh chưa xác minh',
   'Khóa URL, chủ sở hữu, trạng thái, tần suất và giờ riêng',btn('Quản trị nền tảng','assets')],
  ['CMS Website/App',r.cms.unknown.length+' đầu vào chưa có số đã xác nhận',
   'Chưa được hiểu là 0; không cộng trùng dữ liệu nguồn',btn('Tra khối lượng CMS','cms')],
  ['Hạng mục trọng điểm',c.projectsInPlan+' dự án trong kế hoạch và '+c.highlightOutputs+' đầu ra trong phụ lục trọng điểm',
   'Chưa tự chuyển thành giờ W khi thiếu mã bước/người/định mức',btn('Lộ trình và đầu ra','roadmap')],
  ['Định biên và dự phòng',peakRisks.length+' điểm phân công có tháng vượt; '+unknownCaps.length+' điểm chưa đủ quỹ',
   'Không dùng 25% dự phòng để che tải thường xuyên',btn('Xem kết luận','suff')]
 ];
 const periods=months.filter(m=>!selected||m===selected).map(m=>{
  const v=roll(r,keys,m);
  const split={R:0,H:0,K:0,T:0,U:0,G:0};
  for(const w of r.works)split[w.item.kind]=(split[w.item.kind]||0)+w.hours[m-1];
  return ['T'+m,nu(split.R,1),nu(split.H,1),nu(split.K+split.T,1),nu(v.setup,1),nu(v.maint,1),nu(split.U,1),nu(v.total,1)];
 });
 const controls='<div class="control">'+selCase()+selPeriod()+
  fLabel('Ưu tiên xem','<select data-set="towerFilter">'+opt({
   priority:'Việc cần quyết định trước',over:'Chỉ xem vượt quỹ',unknown:'Chưa xác minh quỹ',all:'Tất cả điểm phân công'
  },filter)+'</select>')+'</div>';
 const notice='<p class="note"><b>Kết luận: chưa đủ căn cứ phê duyệt định biên.</b> '
  +'Dữ liệu là mức sản lượng để tính thử, không phải đầu ra thực đo hoặc số nền 2026. '
  +'Kiểm toán đúng phép cộng không đồng nghĩa đủ việc, đủ thẩm quyền hoặc đạt KPI.</p>';
 const dataCheck=difference<0.001?
  '<p class="fine">Đã đối chiếu các khoản R/H/K/T/U với tổng giờ W kỳ chọn; không cộng thêm một lần từ bảng quản trị. '+e(c.normalization)+'</p>':
  '<p class="note"><b>CẢNH BÁO:</b> tổng giờ phân loại và sổ W chênh '+format(difference,2)+' giờ; chưa sử dụng số này để duyệt định biên.</p>';
 return '<h3>Điều hành Marketing 360° – hiệu quả, công việc và quỹ giờ</h3>'+
  '<p>Một nơi để Ban lãnh đạo xác định <b>cái gì cần quyết định, vị trí nào nghẽn, số nào chưa được xác minh</b>. '
  +'Người vận hành tiếp tục thực hiện theo đúng CNNV/MTCV trong các mục chuyên môn. Các con số luôn lấy từ cùng sổ tải công việc.</p>'+
  notice+controls+
  metrics([[nu(charged.total,0),'Giờ đã lượng hóa '+monthLabel],
   [nu(peakRisks.length,0),'Điểm phân công vượt ở kỳ đã chọn'],
   [nu(unknownCaps.length,0),'Điểm thiếu xác nhận quỹ giờ'],
   [nu(r.cms.unknown.length,0),'Đầu vào CMS chưa xác nhận'],
   [nu(c.unapprovedResultKpis,0),'Chỉ số kết quả chưa có số nền/mục tiêu'],
   [nu(channelHours,1),'Giờ kênh số bình quân/tháng']])+
  '<h4>I. Sáu mặt cần kiểm soát trước khi quyết định</h4>'+
  table(['Phương diện','Đã có trong mô hình','Phần chưa được chứng minh','Mở chi tiết'],outputs)+
  '<h4>II. Tải theo nguồn công việc, không gộp lẫn phát sinh</h4>'+
  table(['Thường xuyên','Trọng điểm/chiến dịch','Quản lý và kiêm nhiệm','Thiết lập/bộ mẫu/CMS','Duy trì tài liệu/CMS','Phát sinh mô phỏng','Tổng giờ đang tính'],[
    [nu(byKind.R,1),nu(byKind.H,1),nu(byKind.K+byKind.T,1),nu(charged.setup,1),nu(charged.maint,1),nu(byKind.U,1),nu(charged.total,1)]
  ],[0,1,2,3,4,5,6])+dataCheck+
  '<h4>III. Điểm nghẽn theo đúng vị trí và đơn vị</h4>'+
  '<p class="fine">Không lấy giờ dư của chức danh này bù cho chức danh khác. Đối với người giữ hai suất hoặc kiêm nhiệm phải đối chiếu phân công, quỹ thực có và lịch hiện diện riêng.</p>'+
  (roleRows.length?table(['Vị trí/đầu mối','Suất','Tháng rủi ro nhất','Giờ kế hoạch','Quỹ 75%/tháng','Tổng gồm sự việc','Giờ vượt','Trạng thái'],roleRows,[1,3,4,5,6]):
  '<p class="note">Không có điểm phân công thuộc bộ lọc này. Không đồng nghĩa hệ thống đã đủ tải khi còn dữ liệu chưa xác nhận.</p>')+
  (ranked.length>22?'<p class="fine">Đang hiện 22/'+format(ranked.length,0)+' điểm phân công ưu tiên; dùng bộ lọc để thu hẹp hoặc mở toàn bộ.</p>':'')+
  detail('IV. Lịch tải 12 tháng và các tháng cao điểm',table(['Tháng','Thường xuyên','Trọng điểm','Quản lý/kiêm nhiệm','Thiết lập','Duy trì','Sự việc','Tổng đã tính'],periods,[1,2,3,4,5,6,7]),false)+
  detail('V. Điều kiện cần đối chiếu đủ trước khi ban hành',table(['Ưu tiên','Phạm vi','Dữ liệu còn thiếu','Căn cứ để khóa'],issueRows),true)+
  detail('VI. Luồng vận hành tối giản – một yêu cầu, sáu bước',table(['Bước','Người/phạm vi','Nguyên tắc tránh trùng'],flow.map(x=>x.map(e))),false)+
  '<p class="fine"><b>Điểm chặn hạng mục trọng điểm:</b> '+e(c.highlightBooking)+'. '+e(c.warning)+
  ' 25% dự phòng được giữ để xử lý phát sinh thực sự; KPI cần số nền, nguồn đo và mục tiêu được phê duyệt trước khi kết luận hiệu quả.</p>';
}
"""
assert js.count("const panels={executive:controlTower360,roadmap:")==1
js=js.replace("const panels={executive:controlTower360,roadmap:",insertion+"\nconst panels={executive:controlTower360,roadmap:",1)
s=s[:a+len(start)]+js+s[b:]
assert s.count(marker)==2
p.write_text(s,"utf-8")
print("PASS CONTROL TOWER 360: 6 decision areas, 26 roles, source-separated workload, staged projects & KPI blockers")
