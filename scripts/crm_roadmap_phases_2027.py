#!/usr/bin/env python3
"""CRM presentation final: 2 phases grounded in the Bizfly supplier conversation;
append the exact six-service internal input slide; preserve all six older slides.
Only modifies assembled CRM, not the Marketing organizational framework.
"""
from pathlib import Path
import sys,re
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
p=root/"crm-da-kenh"/"index.html"
s=p.read_text("utf-8")
if "id=\"s7\"" in s:raise SystemExit("CRM_FINAL: s7 already exists; refuse duplicates")
road_re=re.compile(r'(<div class="roadmap">)(.*?)(</div>\s*<div class="decisionGrid">)',re.S|re.I)
m=road_re.search(s)
if not m:raise SystemExit("CRM_FINAL: original roadmap not found")
old=m.group(2)
if len(re.findall(r'<div class="phase">',old))!=3:raise SystemExit("CRM_FINAL: expected source with three phase cards")
for marker in ("GIAI ĐOẠN 1","GIAI ĐOẠN 2","GIAI ĐOẠN 3","CRM lõi","Đa kênh","HIS"):
 if marker not in old:raise SystemExit("CRM_FINAL: missing source term "+marker)
new_roadmap='''<div class="phase">
<div class="phase-index">01</div><div class="eyebrow">GIAI ĐOẠN 1</div>
<b>CRM + Call Center + HIS</b>
<small><strong>CRM đa kênh:</strong> hợp nhất Chat (Fanpage, Zalo, TikTok theo khả năng kết nối được xác nhận), Call, nguồn Ads, Web/App; quản lý hồ sơ liên hệ, lịch sử tương tác, ticket và người phụ trách.<br/>
<strong>Call Center:</strong> kết nối 1900/hotline, tiếp nhận và lưu vết cuộc gọi, chuyển đúng tuyến xử lý.<br/>
<strong>HIS:</strong> liên thông lịch khám và trạng thái nghiệp vụ theo phân quyền; chatbot ở bước đầu trả lời theo kịch bản đã duyệt.</small>
</div>
<div class="phase">
<div class="phase-index">02</div><div class="eyebrow">GIAI ĐOẠN 2</div>
<b>AI</b>
<small><strong>01.</strong> AI tạo ticket hỗ trợ từ cuộc gọi.<br/>
<strong>02.</strong> AI Call tự động gọi ra theo nghiệp vụ và điều kiện liên hệ được phép.<br/>
<strong>03.</strong> AI Chat trả lời, tư vấn theo ngữ cảnh từ dữ liệu được duyệt; kết nối HIS trong phạm vi được cấp quyền.<br/>
<strong>04.</strong> AI tự động tạo ticket hỗ trợ từ Chat.</small>
</div>'''
s=s[:m.start(2)]+new_roadmap+s[m.end(2):]
old_sub="Đi từ nền tảng dữ liệu đến liên thông HIS và tự động hóa; không đầu tư dàn trải."
new_sub="Hai giai đoạn: xây nền tảng CRM đa kênh, Call Center, HIS trước; ứng dụng AI khi đạt điều kiện nghiệm thu."
if s.count(old_sub)!=1:raise SystemExit("CRM_FINAL: original subtitle not found uniquely")
s=s.replace(old_sub,new_sub,1)
# Keep original six screens; append a genuinely selectable seventh screen.
slide7='''<section class="slide" id="s7">
<div class="slideHeader"><div><div class="stepnum">07 / THÔNG TIN NỘI BỘ CẦN THỐNG NHẤT</div>
<h1>Chốt đầu vào triển khai.<br/><em>Không để thiếu căn cứ báo giá.</em></h1>
<p>Danh mục dữ liệu cần nội bộ xác nhận theo bảng nhà cung cấp; chưa có số lượng thì giữ trạng thái chờ chốt, không tự ước tính.</p></div>
<div class="sidetag">DANH MỤC CẦN CHỐT · 06 DỊCH VỤ</div></div>
<div class="crm-internal-wrap">
<table class="crm-internal-table" aria-label="Sáu dịch vụ Bizfly và thông tin cần nội bộ chốt">
<thead><tr><th scope="col">STT</th><th scope="col">Tên dịch vụ</th><th scope="col">Thông tin cần nội bộ chốt</th></tr></thead>
<tbody>
<tr><td data-label="STT">01</td><th scope="row" data-label="Dịch vụ">Bizfly CRM</th><td data-label="Thông tin cần chốt">Số data lưu trữ; số nhân sự sử dụng.</td></tr>
<tr><td data-label="STT">02</td><th scope="row" data-label="Dịch vụ">Bizfly Chat</th><td data-label="Thông tin cần chốt">Số kênh kết nối (tài khoản Zalo OA/Zalo cá nhân, Fanpage…); số data lưu trữ. Đối chiếu thêm khả năng kết nối TikTok theo xác nhận của nhà cung cấp.</td></tr>
<tr><td data-label="STT">03</td><th scope="row" data-label="Dịch vụ">Bizfly Call Center</th><td data-label="Thông tin cần chốt">Số đầu số hotline kết nối; số máy lẻ (nhân sự cần gọi điện).</td></tr>
<tr><td data-label="STT">04</td><th scope="row" data-label="Dịch vụ">Bizfly Ticket</th><td data-label="Thông tin cần chốt">Số lượng ticket: không giới hạn; dung lượng: không giới hạn (xác nhận điều kiện gói dịch vụ).</td></tr>
<tr><td data-label="STT">05</td><th scope="row" data-label="Dịch vụ">Bizfly Email MKT</th><td data-label="Thông tin cần chốt">Số lượt gửi email theo kỳ 6 tháng hoặc 12 tháng.</td></tr>
<tr><td data-label="STT">06</td><th scope="row" data-label="Dịch vụ">ZBS/SMS</th><td data-label="Thông tin cần chốt">Số lượng brandname cần sử dụng.</td></tr>
</tbody></table>
<div class="crm-internal-note"><strong>Những quyết định nghiệp vụ cần thống nhất:</strong>
Phạm vi dữ liệu HIS được phép liên thông; quyền tạo và bàn giao ticket; điều kiện nghiệm thu từng dịch vụ;
AI tạo ticket từ cuộc gọi có được thí điểm ở Giai đoạn 1 hay không; cơ chế kiểm soát AI Call và AI Chat.
<em>Chưa chốt số lượng, báo giá hoặc thời điểm triển khai AI trong bảng này.</em></div>
</div></section>'''
insert=re.compile(r'(</section>\s*)(<div class="bottomNav">)',re.I)
m=insert.search(s)
if not m:raise SystemExit("CRM_FINAL: bottom navigation anchor absent")
s=s[:m.start()]+m.group(1)+slide7+"\n"+m.group(2)+s[m.end():]
# Add the seventh menu item before the existing sidebar JS creates buttons.
old_names="'Lộ trình & quyết định'];"
new_names="'Lộ trình & quyết định','Thông tin nội bộ cần chốt'];"
if s.count(old_names)!=1:raise SystemExit("CRM_FINAL: nav labels source mismatch")
s=s.replace(old_names,new_names,1)
controls={
"active=Math.max(0,Math.min(5,i))":"active=Math.max(0,Math.min(slides.length-1,i))",
"active===5":"active===slides.length-1",
"document.getElementById('pageCount').textContent='0'+(active+1)+' / 06'":"document.getElementById('pageCount').textContent=String(active+1).padStart(2,'0')+' / '+String(slides.length).padStart(2,'0')",
'id="pageCount">01 / 06':'id="pageCount">01 / 07',
"6 màn quyết định":"7 màn quyết định",
'<div class="hero-scroll">01 <span>—</span> 06</div>':'<div class="hero-scroll">01 <span>—</span> 07</div>'
}
for before,after in controls.items():
 if s.count(before)!=1:raise SystemExit(f"CRM_FINAL: navigation token not unique: {before} count={s.count(before)}")
 s=s.replace(before,after,1)
styles='''<style id="tth-crm-final-two-phases-and-internal-2027">
.roadmap{display:grid!important;grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:16px!important}
.roadmap .phase{min-width:0!important;max-width:none!important;overflow-y:auto!important}
.roadmap .phase>b{font-size:clamp(21px,1.7vw,28px)!important;line-height:1.2!important}
.roadmap .phase>small{font-size:clamp(13px,.98vw,16px)!important;line-height:1.47!important;display:block!important;overflow-wrap:anywhere}
.roadmap .phase>small strong{font-weight:800;color:#0d3679}
#s7{overflow-y:auto!important;scrollbar-width:thin}
#s7 .crm-internal-wrap{display:flex;flex-direction:column;gap:14px;margin:12px 0 0;min-width:0}
#s7 .crm-internal-table{width:100%;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid #C9D9F0;border-radius:13px;overflow:hidden}
#s7 .crm-internal-table th,#s7 .crm-internal-table td{padding:11px 14px;border-bottom:1px solid #E0E8F4;text-align:left;vertical-align:middle;font-size:clamp(13px,.95vw,16px);line-height:1.35;color:#193B70}
#s7 .crm-internal-table thead th{background:#0837A1;color:#fff;font-weight:800}
#s7 .crm-internal-table tbody tr:last-child th,#s7 .crm-internal-table tbody tr:last-child td{border-bottom:0}
#s7 .crm-internal-table tbody tr:nth-child(even){background:#F4F7FD}
#s7 .crm-internal-table tbody th{font-weight:800;color:#123F8B;white-space:normal}
#s7 .crm-internal-table th:first-child,#s7 .crm-internal-table td:first-child{width:65px;text-align:center}
#s7 .crm-internal-table thead th:nth-child(2){width:205px}
#s7 .crm-internal-note{padding:12px 15px;border-radius:12px;border-left:4px solid #ED3237;background:#EDF3FE;font-size:clamp(12px,.91vw,14px);line-height:1.43;color:#243F67}
#s7 .crm-internal-note strong{color:#0837A1}#s7 .crm-internal-note em{display:block;font-style:normal;margin-top:5px;color:#61728B}
@media(max-width:760px){
 .roadmap{grid-template-columns:minmax(0,1fr)!important}
 #s7 .crm-internal-table,#s7 .crm-internal-table tbody{display:block}
 #s7 .crm-internal-table thead{display:none}
 #s7 .crm-internal-table tr{display:grid;grid-template-columns:32px minmax(0,1fr);padding:9px 11px;gap:4px 10px;border-bottom:1px solid #DCE6F4}
 #s7 .crm-internal-table td,#s7 .crm-internal-table th{border:0!important;padding:3px 0!important;font-size:13px!important}
 #s7 .crm-internal-table td:first-child{grid-column:1;grid-row:1;width:auto!important;text-align:left}
 #s7 .crm-internal-table th{grid-column:2;grid-row:1}
 #s7 .crm-internal-table td:last-child{grid-column:1/span 2;grid-row:2}
 #s7 .crm-internal-note{font-size:12.5px}
}
</style>'''
if s.count('</head>')!=1:raise SystemExit("CRM_FINAL: invalid document head")
s=s.replace('</head>',styles+'</head>',1)
if len(re.findall(r'<section class="slide(?: active)?" id="s[1-7]">',s))!=7:
 raise SystemExit("CRM_FINAL: slide count not 7")
if len(re.findall(r'<div class="phase">',new_roadmap))!=2:raise SystemExit("CRM_FINAL: phase count changed")
p.write_text(s,"utf-8")
print("CRM_FINAL_OK 02 stages: CRM + Call Center + HIS (includes omnichannel), AI; 07 slides; original six Bizfly input rows; buttons dynamic.",len(s))
