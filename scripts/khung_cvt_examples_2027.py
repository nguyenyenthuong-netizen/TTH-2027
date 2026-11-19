#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thêm ví dụ vận hành của hai tuyến chuyên viên quản lý; không tự cấp quyền duyệt."""
from pathlib import Path
from html import escape
import json,re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s)
assert m,"Thiếu CSDL nhúng"
D=json.loads(m.group(2))
Q={q["id"]:q for q in D["quy_trinh"]}
V={v["id"]:v for v in D["vi_tri"]}
assert len(Q)==60 and len(V)==26
N=V["cvt"]["ten"]
T=V["cvt-2"]["ten"]
assert N=="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
assert T=="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
# (Mã, Luồng, Tình huống, Chủ việc/đầu ra, CVT Nội dung, CVT Truyền thông,
#  Người kiểm và bàn giao, Quyền phê duyệt, Giờ/KPI)
cases=[
("VD01","tin-trong-ngay","Tin V1 về hoạt động bệnh viện","Trưởng nhóm cơ sở giao người viết/quay, ghi một mã tin; người thực hiện bàn giao bản tin và tư liệu.","Quản lý tải Trưởng nhóm cơ sở; chỉ điều phối khi đổi ưu tiên hoặc thiếu nguồn lực.","Kiểm chuẩn nghiệp vụ kênh khi có rủi ro hoặc sai mẫu, không mặc nhiên kiểm từng tin.","Biên tập đúng nhóm kiểm nội dung; cơ sở xác nhận sự kiện; kiểm y khoa nếu có tuyên bố y tế.","Người có quyền phát hành trên kênh được phân cấp duyệt; người đăng chỉ thực hiện sau duyệt.","Giờ viết/quay/dựng thuộc người làm; giờ giao việc Tổ trưởng/Trưởng nhóm; hai CVT chỉ ghi giờ xử lý ngoại lệ."),
("VD02","tin-trong-ngay","Video V2 theo mẫu tại cơ sở","Trưởng nhóm cơ sở giao Media cơ sở quay, dựng hoàn chỉnh theo mẫu được giao.","Giải quyết thiếu máy, thiếu người hoặc xung đột lịch; không nhận sản lượng video làm KPI cá nhân.","Kiểm tuân thủ mẫu video/kênh nếu phát sinh lỗi hệ thống, không dựng thay Media.","Biên tập kiểm lời; người kiểm kỹ thuật độc lập kiểm file và tỷ lệ màn hình.","Phát hành theo quyền kênh có hiệu lực, không do hai CVT mặc nhiên duyệt.","Giờ quay/dựng ghi cho Media cơ sở; giờ kiểm ghi người kiểm; điều phối chỉ tính phút thực tế."),
("VD03","hang-muc","Video V3 phỏng vấn, câu chuyện người bệnh","Đầu mối nội dung lập lời và phân cảnh; Media cơ sở quay; Media TCT xử lý hậu kỳ phức tạp khi được giao.","Chốt tải sản xuất TCT–cơ sở theo một lịch, xác định rõ một người nhận bản dựng cuối.","Kiểm chuẩn truyền thông, quyền sử dụng hình ảnh và rủi ro phát hành nếu hồ sơ yêu cầu.","Biên tập độc lập kiểm câu chữ; chuyên môn y tế xác nhận nội dung y khoa; chứng từ đồng ý hình ảnh.","Quản lý thương hiệu nghiệm thu mục tiêu; người có thẩm quyền duyệt phát hành và chi phí riêng.","Mỗi người ghi giờ theo tác vụ thực; không cộng toàn bộ giờ hậu kỳ cho cả Media cơ sở và TCT."),
("VD04","hang-muc","Phim V4 chiến dịch toàn hệ thống","Quản lý thương hiệu chịu kết quả hạng mục; tổ sản xuất phân vai kịch bản lời, thiết kế, quay và hậu kỳ.","Điều phối nguồn lực sản xuất giữa các nhóm và cơ sở, giải quyết quá tải đúng tuyến.","Điều phối hai tổ Truyền thông–Thương hiệu và Tăng trưởng số về kế hoạch truyền thông và phân phối.","Biên tập, thiết kế, Media kiểm độc lập theo chuyên môn; y khoa/pháp lý kiểm khi áp dụng.","Cấp có thẩm quyền phê duyệt phát hành, hợp đồng và ngân sách theo từng cửa; không gộp làm một.","Giờ từng chuyên viên theo công đoạn; Tổ trưởng ghi giờ phân lịch; CVT ghi giờ quản trị thật, không nhân đôi."),
("VD05","bgd-coso-de-nghi","Ban Giám đốc cơ sở yêu cầu thay thông điệp","Trưởng nhóm cơ sở tiếp nhận yêu cầu và ghi nguồn, hạn; Quản lý thương hiệu quản lý mục tiêu.","Nhận phần thay đổi tải và lịch nhân sự cơ sở; không tự duyệt thông điệp thương hiệu.","Kiểm chuẩn cách triển khai truyền thông và kênh, gửi góp ý qua tuyến, không ra lệnh thứ hai cho cơ sở.","Quản lý thương hiệu xác nhận mục tiêu/thông điệp; biên tập kiểm bản thay đổi.","Trưởng phòng xử lý bất đồng liên tuyến; quyền phát hành/chi phí vẫn theo phân cấp.","Ghi một mã yêu cầu đổi; giờ chỉnh sửa thuộc người sửa, giờ phối hợp chỉ cho người thực hiện."),
("VD06","xung-dot-lich","Hai tổ và cơ sở trùng lịch chiến dịch","Tổ trưởng/Trưởng nhóm nộp bảng tải và mức ưu tiên từng đầu ra.","Điều phối năng lực sản xuất và cơ sở; đưa một phương án khả thi.","Xác nhận tải và thứ tự ưu tiên trong hai tổ chuyên môn phụ trách.","Chuyên viên chịu trách nhiệm sản phẩm không bị thay đổi ngầm; ghi nhận quyết định điều phối.","Trưởng phòng xử lý xung đột liên tuyến; không dùng quyền phê duyệt phát hành để quyết định nhân sự.","Giờ xử lý xung đột ghi một lần cho người làm; không cộng lại giờ sản xuất theo kế hoạch."),
("VD07","yeu-cau-gap","Yêu cầu gấp thay nội dung quảng cáo","Người yêu cầu lập phiếu gấp với lý do, hạn, mẫu nguồn, chi phí dự kiến.","Nếu cần viết/thiết kế/quay hoặc nhân sự cơ sở, xác nhận tải và tuyến sản xuất.","Đánh giá rủi ro chính sách quảng cáo và tải hai tổ; phân loại ưu tiên trong phạm vi quản trị.","Biên tập kiểm lời; pháp lý/y khoa xác nhận phần bắt buộc; Quản lý thương hiệu nghiệm thu mục tiêu.","Người có quyền duyệt phát hành và ngân sách quyết định riêng; gấp không được bỏ cửa chặn.","Chỉ ghi giờ thực làm và kiểm gấp, có mã phiếu; phần chờ duyệt không tính thành sản phẩm mới."),
("VD08","quang-cao-tra-phi","Quảng cáo có giá và chương trình dịch vụ","Quản lý thương hiệu xác định mục tiêu; chuyên viên quảng cáo thiết lập; Biên tập và Thiết kế làm ấn phẩm.","Bố trí tải sản xuất ảnh/lời; không tự xác nhận giá hoặc duyệt y khoa.","Kiểm chuẩn kênh, thiết lập nguồn đo, xử lý sai chính sách và xung đột liên tổ.","Đơn vị sở hữu dịch vụ xác nhận giá, điều kiện và y khoa; Biên tập kiểm nội dung; đo lường đối soát nguồn.","Phê duyệt quảng cáo y tế, phát hành và ngân sách đúng người có quyền; cấm chạy khi thiếu xác nhận.","Giờ thiết lập và tối ưu của Quảng cáo, giờ sản xuất của chuyên viên khác tách biệt; CVT chỉ ghi giờ ngoại lệ."),
("VD09","phat-thanh-man-hinh","Màn hình và phát thanh nội viện","Truyền thông đúng nhóm lập lịch và hồ sơ phát; Trưởng nhóm cơ sở phân người vận hành hiện trường.","Quản lý tải nhân sự cơ sở, giải quyết thay ca qua đúng Trưởng nhóm.","Chủ trì chuẩn phát thanh/màn hình và kiểm sự tuân thủ; không trực tiếp vận hành thay cơ sở.","Biên tập kiểm lời, đơn vị y tế xác nhận phần chuyên môn; cơ sở lưu nhật ký phát và ảnh kiểm tra.","Phê duyệt nội dung phát theo người được ủy quyền; sửa lịch không thay quyền duyệt nội dung.","Giờ viết, dựng, lập lịch, kiểm hiện trường phân theo từng người; không gộp mọi giờ cho Truyền thông."),
("VD10","bien-bang-hong","Biển bảng OOH hỏng, sai nhận diện","Truyền thông cơ sở chụp ảnh, đo kích thước, mở phiếu sự cố; bộ phận phụ trách triển khai sửa.","Quản lý nguồn lực cơ sở nếu cần người/giờ hỗ trợ, không nhận công tác kiểm biển bảng làm việc thường lệ.","Kiểm chuẩn nhận diện và yêu cầu khắc phục lỗi lặp; phối hợp Truyền thông TCT đúng nhóm.","Thiết kế kiểm file thi công; cơ sở đối chiếu ảnh trước/sau, biên bản hiện trường.","Duyệt sửa chữa/chi phí theo hạn mức và đơn vị chủ tài sản, không mặc nhiên thuộc CVT.","Giờ kiểm hiện trường thuộc người đi kiểm; giờ thiết kế thuộc Thiết kế; CVT ghi thời gian xử lý ngoại lệ."),
("VD11","danh-gia","Phản ánh tiêu cực, nguy cơ khủng hoảng","Chuyên viên truyền thông lập hồ sơ sự việc, xác minh dữ kiện từ cơ sở và đề xuất phương án.","Điều phối nguồn lực thu thập tại cơ sở khi được yêu cầu; không phát ngôn.","Đánh giá rủi ro truyền thông, đề xuất quy trình phản hồi và kiểm chuẩn kênh.","Ban Giám đốc cơ sở xác nhận dữ kiện; pháp lý/y khoa kiểm phạm vi; Quản lý thương hiệu kiểm thông điệp.","Chỉ người phát ngôn hoặc người có ủy quyền hợp lệ phê duyệt phát ngôn; Trưởng phòng điều phối liên tuyến.","Giờ xử lý của người thực hiện ghi theo phiếu khủng hoảng; CVT không tính số bài/clip thành KPI cá nhân."),
("VD12","vang-mat","Nhân sự nghỉ, phải thay người quản lý kênh","Tổ trưởng/Trưởng nhóm lập bàn giao công việc, danh mục file, quyền và hạn.","Quản lý lịch sản xuất/cơ sở và bàn giao kho tư liệu theo tuyến.","Xác nhận tải hai tổ, kiểm kê quyền kênh/quảng cáo, không tự cấp hoặc thu hồi quyền quản trị.","Người thay chỉ nhận tác vụ trong phạm vi văn bản ủy quyền; quản trị viên kiểm nhật ký quyền.","Nhân lực duyệt nghỉ theo quy chế; người quản trị được phân quyền cấp/thu hồi quyền, không phải hai CVT mặc định.","Giờ bàn giao và giờ thực hiện thay ghi riêng; không tính một sản phẩm cho cả người nghỉ và người thay."),
("VD13","crm","Kịch bản Contact Center cho dịch vụ mới","Contact Center là đầu mối nghiệp vụ tư vấn; Biên tập hỗ trợ biên soạn ngôn ngữ khi được giao.","Điều phối tải Biên tập nếu phát sinh yêu cầu sản xuất nội dung; không nhận nghiệp vụ tư vấn.","Kiểm tính nhất quán thông điệp đa kênh khi có liên hệ quảng cáo/kênh số; không sở hữu kịch bản nghiệp vụ.","Đơn vị chuyên môn y tế xác nhận chỉ dẫn dịch vụ; Contact Center nghiệm thu khả năng tư vấn.","Người có thẩm quyền nghiệp vụ phê duyệt kịch bản; phát hành kênh và chi phí là các quyền khác.","Giờ soạn lời Biên tập khác giờ xây dựng nghiệp vụ Contact Center; quản lý chỉ tính phần thực làm."),
("VD14","he-thong-gian-doan","Hệ thống Marketing gián đoạn, phải nhập bù","Quản lý sản phẩm số tiếp nhận sự cố; từng người lập nhật ký tác nghiệp tạm.","Kiểm kho tư liệu và tải sản xuất/cơ sở, thống nhất một sổ tạm đúng tuyến.","Kiểm lịch phát, quảng cáo và hai tổ; báo rủi ro chậm tiến độ.","Chuyên viên đo lường và đối soát kiểm nhập bù độc lập; đơn vị công nghệ xác nhận khôi phục.","Không tự cấp quyền duyệt thay khi phần mềm lỗi; giữ chứng từ phê duyệt ngoài hệ thống hợp lệ.","Giờ nhập bù ghi đúng người thực hiện; thời gian gián đoạn không tự sinh sản lượng trùng."),
]
assert len(cases)==14 and len({x[0] for x in cases})==14
assert all(x[1] in Q for x in cases)
D["vi_du_van_hanh_hai_chuyen_vien_truong_2027"]=[
dict(zip(["ma","ma_quy_trinh","tinh_huong","chu_viec","cvt_noi_dung","cvt_truyen_thong","kiem_tra","phe_duyet","hach_toan"],x))
for x in cases]
D["vi_du_van_hanh_hai_chuyen_vien_truong_2027_nguyen_tac"]={
"loai":"Ví dụ mô phỏng phân vai theo đề án, không phải hồ sơ đã xảy ra",
"nguoi_chiu_trach_nhiem":"Một người được chỉ định trên từng mã đầu ra thực tế, không lấy chức danh làm thay mã nhân sự",
"tuyen_quan_ly":"Chỉ một tuyến quản lý trực tiếp; ý kiến chuyên môn liên tuyến không tạo quản lý kép",
"phe_duyet":"Chỉ người có quyền theo ma trận còn hiệu lực; kiểm tra, nghiệm thu, phê duyệt phát hành và chi phí là bốn cửa riêng",
"tai":"Giờ chuyên viên, giờ Tổ trưởng/Trưởng nhóm và giờ quản trị của hai chức danh thực đo tách nhau; không tính trùng sản lượng"}
m=rx.search(s)
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]
marker='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
assert s.count(marker)==1
assert 'id="tth-cvt-worked-examples-2027"' not in s
idx=s.index(marker)
at=s.index("</h3>",idx)+5
labels=[
("chu_viec","Chủ việc và đầu ra"),
("cvt_noi_dung",N),
("cvt_truyen_thong",T),
("kiem_tra","Kiểm tra chuyên môn và bàn giao"),
("phe_duyet","Phê duyệt có hiệu lực"),
("hach_toan","Hạch toán giờ và KPI")
]
style='<style id="tth-cvt-examples-style-2027">#tth-cvt-worked-examples-2027{max-width:100%;min-width:0;overflow-wrap:anywhere}#tth-cvt-worked-examples-2027 .cvt-case{border:1px solid #d7e2f0;border-radius:8px;background:#fff;margin:10px 0;max-width:100%;box-sizing:border-box}#tth-cvt-worked-examples-2027 .cvt-case>summary{cursor:pointer;padding:12px 14px;color:#0837A1;font-weight:700;line-height:1.5}#tth-cvt-worked-examples-2027 .cvt-case-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:0 12px 12px}#tth-cvt-worked-examples-2027 .cvt-case-cell{min-width:0;border:1px solid #e4eaf3;border-radius:6px;padding:10px;overflow-wrap:anywhere}#tth-cvt-worked-examples-2027 .cvt-case-cell strong{display:block;color:#0837A1;font-size:.94em;margin-bottom:4px}@media(max-width:760px){#tth-cvt-worked-examples-2027 .cvt-case-grid{grid-template-columns:minmax(0,1fr)}#tth-cvt-worked-examples-2027 .cvt-case>summary{padding:12px}}</style>'
body=[style,'<div id="tth-cvt-worked-examples-2027" style="max-width:100%;min-width:0;box-sizing:border-box;margin:16px 0 22px">']
body.append('<h4 style="margin:10px 0;color:#0837A1">14 tình huống đối chiếu hai tuyến quản lý chuyên môn</h4>')
body.append('<p><strong>Nguyên tắc:</strong> một mã việc, một người chủ trì thực tế, một tuyến quản lý, một người quyết định cuối theo từng loại phê duyệt, một lần ghi giờ. '+escape(N)+' và '+escape(T)+' quản trị đúng phạm vi; không tự mặc định quyền viết bài, dựng video, phát hành, duyệt y khoa hoặc chi phí. Đây là mô phỏng để đối chiếu, không thay quyết định giao quyền.</p>')
for x in D["vi_du_van_hanh_hai_chuyen_vien_truong_2027"]:
 code=x["ma"];qid=x["ma_quy_trinh"]
 body.append('<details class="cvt-case"'+(' open' if code=="VD01" else '')+'><summary>'+escape(code+' – '+x["tinh_huong"])+'</summary><div class="cvt-case-grid">')
 for key,label in labels:
  body.append('<div class="cvt-case-cell"><strong>'+escape(label)+'</strong><div>'+escape(x[key])+'</div></div>')
 body.append('</div><p style="padding:0 12px 12px;margin:0"><a href="#vh-qt-'+escape(qid)+'" style="color:#0837A1;text-decoration:underline">Xem quy trình liên quan</a></p></details>')
body.append('<p>Để đưa vào vận hành, từng mã việc còn phải gắn nhân sự, phân công, chứng từ, quyền có hiệu lực và giờ thực đo. Thiếu điều kiện bắt buộc thì khóa bàn giao hoặc phát hành.</p></div>')
s=s[:at]+''.join(body)+s[at:]
assert s.count('id="tth-cvt-worked-examples-2027"')==1
assert s.count('class="cvt-case"')==14
assert s.count('class="cvt-case-cell"')==14*6
assert s.count('Xem quy trình liên quan')==14
assert '<table class="t" style="min-width:1180px' not in s
p.write_text(s,"utf-8")
print("PASS: 14 responsive examples, 14 links, explicit 2 CVTs, approvals and workload accounting")
