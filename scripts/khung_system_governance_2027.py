#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chuẩn hóa MTCV & quy trình liên thông CRM–HIS–Contact Center–Marketing software.
Đây là phụ lục nghiệp vụ DỰ THẢO, không tự tạo quyền duyệt hoặc hiệu lực văn bản.
"""
from pathlib import Path
import json,re,sys
from html import escape
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s)
assert m
d=json.loads(m.group(1))
assert len(d["vi_tri"])==26 and len(d["quy_trinh"])==60
assert all(x.get("chu_tri_chinh") for q in d["quy_trinh"] for x in q["buoc"])
assert "quan_tri_he_thong_lien_thong_2027" not in d
owners=[
("Trưởng phòng Marketing","Chủ yêu cầu nghiệp vụ và ưu tiên Marketing toàn hệ thống; trình ngân sách và thay đổi chính sách theo phân cấp","Không tự duyệt thay Ban Tổng Giám đốc; không thay đơn vị chủ quản dữ liệu khám chữa bệnh"),
("Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số","Giám sát nghiệp vụ tổ Tăng trưởng số, quản trị rủi ro và năng lực thực hiện, kiểm tra độc lập phần việc cấp tổ","Không trực tiếp làm quản trị hệ thống, không thành tuyến quản lý thứ hai của nhân sự cơ sở"),
("Quản lý sản phẩm số","Đầu mối nghiệp vụ Marketing cho website, App, trang đích và tiếp nhận yêu cầu kỹ thuật phần mềm Quản trị Marketing; quản lý danh mục thay đổi, kế hoạch kiểm thử giao diện và chứng cứ nghiệm thu phần Marketing","Không trực tiếp lập trình, cấp quyền hạ tầng, tự phê duyệt phát hành hoặc tự nghiệm thu sản phẩm do mình làm"),
("Chuyên viên dữ liệu khách hàng và thị trường","Chủ nghiệp vụ Marketing của CRM: trường dữ liệu, chất lượng, trùng hồ sơ, phân khúc, đồng ý, yêu cầu kết nối HIS và tiêu chí nghiệm thu dữ liệu","Không là chủ dữ liệu bệnh án/HIS, không tự cấp quyền hay xử lý dữ liệu vượt mục đích được duyệt"),
("Chuyên viên đo lường và đối soát","Chủ đối soát chỉ số nguồn khách, chuyển đổi, chi phí và kết quả giữa nền tảng quảng cáo, CRM và báo cáo Marketing; kiểm độc lập dữ liệu KPI","Không chỉnh sửa dữ liệu HIS, không thay nghiệp vụ CRM hoặc phê duyệt chỉ tiêu KPI"),
("Chuyên viên quảng cáo và kênh số nhóm 1","Quản trị kênh truyền thông và quảng cáo nhóm 1, gắn mã chiến dịch/nguồn khách vào CRM theo chuẩn đã duyệt","Không là quản trị viên CRM, HIS hoặc phần mềm Quản trị Marketing"),
("Chuyên viên quảng cáo và kênh số nhóm 2","Quản trị kênh truyền thông và quảng cáo nhóm 2, gắn mã chiến dịch/nguồn khách theo đúng nhóm thương hiệu","Không là quản trị viên CRM, HIS hoặc phần mềm Quản trị Marketing"),
("Contact Center","Chủ nghiệp vụ tiếp nhận, tư vấn, lịch sử tương tác và kịch bản tư vấn; kiểm soát chất lượng nhân viên theo tiêu chí được duyệt","Không tự đổi nội dung y khoa, cấp quyền dữ liệu bệnh án hay thay bộ phận Marketing duyệt nội dung quảng cáo"),
("Phòng Công nghệ","Chủ triển khai kỹ thuật, tích hợp, tài khoản hệ thống, bảo mật, sao lưu, nhật ký và khôi phục theo phê duyệt","Không tự quyết định mục đích xử lý dữ liệu, thay đổi nghiệp vụ hoặc tự nghiệm thu nghiệp vụ"),
("Nghiệp vụ Y và đơn vị khám chữa bệnh","Chủ xác nhận dữ liệu y tế, mã người bệnh HIS, quyền truy cập thông tin khám chữa bệnh và tính đúng đắn nghiệp vụ y khoa","Không tự phê duyệt chi phí Marketing hay nội dung phát hành thuộc thẩm quyền khác")
]
flows=[
("QT-HT01","Tiếp nhận và thay đổi phần mềm Marketing","Quản lý sản phẩm số","Trưởng phòng Marketing theo phân cấp; chi phí duyệt riêng","Yêu cầu có mã việc, phạm vi, chủ trì, tiêu chí nghiệm thu, tác động quyền và dữ liệu","Tiếp nhận → đánh giá ảnh hưởng 2 phân hệ/4 phần nền → duyệt phạm vi → Phòng Công nghệ triển khai → người khác kiểm thử → nghiệm thu nghiệp vụ → triển khai và theo dõi","Biên bản thay đổi, bản thử, lỗi tồn, lịch sử phiên bản","Chưa duyệt, chưa kiểm thử hoặc người làm trùng người nghiệm thu"),
("QT-HT02","Quản lý tài khoản, quyền và thay đổi nhân sự","Quản lý sản phẩm số (phần mềm Marketing); Chuyên viên dữ liệu khách hàng và thị trường (CRM)","Chủ quản dữ liệu và người có thẩm quyền cấp quyền; Phòng Công nghệ thực thi","Quyết định nhân sự, vai trò, đơn vị, phạm vi dữ liệu, hạn quyền","Đề xuất → xác nhận chủ quản → kiểm xung đột nhiệm vụ → cấp/thu hồi quyền → kiểm độc lập → lưu nhật ký","Danh sách quyền trước/sau, người duyệt, người thực hiện, thời điểm thu hồi","Không tự cấp quyền; không để quyền cũ sau điều chuyển/nghỉ việc"),
("QT-HT03","Liên kết hồ sơ CRM và mã người bệnh HIS","Chuyên viên dữ liệu khách hàng và thị trường (nghiệp vụ CRM)","Nghiệp vụ Y xác nhận mã HIS; Phòng Công nghệ phê duyệt/triển khai kỹ thuật theo phân cấp","Mã CRM, mã người bệnh HIS được hệ thống nguồn xác thực, căn cứ xử lý và quyền truy cập","Xác thực định danh → kiểm trùng → đối chiếu mã nguồn HIS → xác nhận liên kết → đồng bộ trường tối thiểu → ghi lịch sử thay đổi → xử lý sai khớp","Bảng ánh xạ mã có kiểm soát, thời gian đồng bộ, nguồn xác thực, biên bản lỗi","Không tự gộp người bệnh khác nhau; không kéo dữ liệu bệnh án sang CRM ngoài phạm vi được phép"),
("QT-HT04","CRM – Contact Center – nguồn khách","Chuyên viên dữ liệu khách hàng và thị trường; Contact Center chịu trách nhiệm tương tác","Trưởng phòng Marketing và người phụ trách Contact Center theo đúng tuyến","Mã nguồn khách, lịch sử tương tác, trạng thái đồng ý, người nhận xử lý","Tiếp nhận từ kênh → kiểm đồng ý → phân tuyến → Contact Center xử lý → ghi kết quả → phản hồi trạng thái → đối soát","Nhật ký cuộc gọi, trạng thái xử lý, lý do thất bại, chỉ số SLA","Không gửi trùng, không gọi trái phạm vi đồng ý, không đưa thông tin y khoa chưa xác nhận"),
("QT-HT05","Chất lượng tư vấn và chất lượng dữ liệu CRM","Contact Center (chất lượng tư vấn); Chuyên viên dữ liệu khách hàng và thị trường (chất lượng dữ liệu)","Người quản lý từng bộ phận, không tự chấm điểm chính mình","Mẫu chấm chất lượng, quyền nghe/đọc theo vai trò, tỷ lệ sai, khiếu nại","Lấy mẫu → kiểm độc lập → phản hồi → khắc phục → tái kiểm → chốt chỉ số","Phiếu chấm, bằng chứng, mẫu sai, lịch sử khắc phục","Không dùng điểm tự chấm làm kết quả cuối; không khai thác bản ghi ngoài mục đích"),
("QT-HT06","Đối soát số liệu và KPI liên thông","Chuyên viên đo lường và đối soát","Trưởng phòng Marketing duyệt kết quả quản trị theo phân cấp; chủ dữ liệu nguồn xác nhận","Nguồn số liệu quảng cáo, CRM, Contact Center, HIS theo quyền được cấp, phần mềm Marketing","Khóa kỳ → trích xuất có nguồn → đối chiếu chênh lệch → xác nhận chủ dữ liệu → lập báo cáo → lưu vết điều chỉnh","Bảng đối soát theo mã chiến dịch, đơn vị, kỳ, nguồn, công thức và sai lệch","Không tự sửa dữ liệu gốc; không tính thưởng từ KPI chưa được phê duyệt"),
("QT-HT07","Sự cố, sao lưu, phục hồi và thông báo","Phòng Công nghệ chủ kỹ thuật; Quản lý sản phẩm số/Chuyên viên dữ liệu khách hàng và thị trường chủ nghiệp vụ tương ứng","Chủ hệ thống, quản lý nghiệp vụ và người phê duyệt khôi phục theo cấp độ","Mức độ sự cố, ảnh hưởng khách hàng, quyền, dữ liệu, kế hoạch dự phòng","Ghi nhận → phân mức → cô lập rủi ro → duy trì sổ việc tạm → khôi phục → đối soát không mất/nhân đôi → nghiệm thu → đóng sự cố","Biên bản sự cố, nhật ký, kết quả khôi phục và đối soát","Không tắt quy tắc duyệt khi gián đoạn; không khôi phục đè mất dữ liệu mới"),
("QT-HT08","Quản trị danh mục, phiên bản và quy trình dùng chung","Trưởng phòng Marketing chủ danh mục nghiệp vụ; Quản lý sản phẩm số điều phối yêu cầu kỹ thuật","Cấp ban hành quy trình và chủ quản tài liệu theo văn bản hiện hành","Mã tài liệu, bản hiện hành, đối chiếu quy trình cũ, người sở hữu, ngày hiệu lực","Kiểm kê → phân loại giữ/sửa/gộp/bãi bỏ/xây mới → soạn → kiểm độc lập → trình ký → công bố phiên bản → thu hồi bản cũ","Sổ đăng ký quy trình, biên bản đối chiếu, quyết định có hiệu lực, lịch sử phiên bản","Không tự công nhận 60 luồng là quy trình mới; không thay thế quy trình đã ban hành khi chưa có quyết định")
]
assert len(flows)==8
d["quan_tri_he_thong_lien_thong_2027"]={
 "trang_thai":"PHỤ LỤC ĐỀ XUẤT – CHỜ ĐỐI CHIẾU QUY TRÌNH CŨ VÀ PHÊ DUYỆT",
 "phan_loai":{"kenh_so":"Website, mạng xã hội, quảng cáo, trang đích và kênh tiếp cận",
 "crm":"Hệ thống nghiệp vụ quản lý quan hệ khách hàng và dữ liệu tiếp xúc; không phải kênh truyền thông",
 "phan_mem_marketing":"Hệ thống quản trị công việc, quy trình, ngân sách, sản phẩm và KPI; không phải kênh truyền thông",
 "his":"Hệ thống nguồn của dữ liệu khám chữa bệnh; Marketing không là chủ dữ liệu bệnh án"},
 "nguon_du_lieu":"CRM giữ hồ sơ liên hệ và tương tác theo phạm vi được phép; HIS giữ mã người bệnh và dữ liệu khám chữa bệnh; phần mềm Marketing quản trị mã việc, sản phẩm, chi phí, KPI. Liên kết bằng mã tham chiếu, không sao chép dữ liệu bệnh án sang Marketing.",
 "chuyen_tiep":"Vị trí Chuyên viên dữ liệu khách hàng và thị trường chưa có người: Chuyên viên đo lường và đối soát kiêm theo phân công có thời hạn; phần kiểm độc lập và phê duyệt do người khác đảm nhiệm.",
 "chu_the":[{"vi_tri":n,"chu_tri":a,"ranh_gioi":b} for n,a,b in owners],
 "luong_bo_sung":[{"ma_tham_chieu":code,"ten":name,"chu_tri":lead,"quyen_duyet":approve,"dau_vao":inp,"cac_buoc":steps,"dau_ra":out,"quy_tac_chan":gate,"trang_thai":"MÔ TẢ NGHIỆP VỤ ĐỀ XUẤT – CHƯA PHẢI QUY TRÌNH BAN HÀNH"} for code,name,lead,approve,inp,steps,out,gate in flows]
}
role_map={
"qlsps":("Đầu mối thay đổi phần mềm Marketing và phối hợp Phòng Công nghệ; chịu trách nhiệm đặc tả yêu cầu, kiểm thử nghiệp vụ, hồ sơ phiên bản, xử lý sự cố ứng dụng","Không là quản trị viên hạ tầng; không tự nghiệm thu công việc của chính mình; CRM/HIS thuộc chủ nghiệp vụ và chủ dữ liệu tương ứng"),
"dl-2":("Chủ nghiệp vụ CRM phần Marketing: chất lượng hồ sơ, ánh xạ mã CRM–mã người bệnh HIS có xác nhận của Nghiệp vụ Y, phân quyền theo mục đích, quy tắc đồng ý","Không sở hữu dữ liệu bệnh án HIS, không tự ghép hồ sơ khi sai định danh, không tự cấp quyền"),
"dl-1":("Đối soát chỉ số nguồn khách, CRM, Contact Center và báo cáo Marketing theo kỳ, kiểm độc lập KPI và sai lệch","Không thay chủ dữ liệu CRM/HIS; không tự sửa số liệu gốc hoặc chốt KPI chưa phê duyệt"),
"qc-a":("Quản trị kênh số nhóm 1, quảng cáo và mã nguồn khách; bàn giao dữ liệu Lead cho CRM qua luồng đã duyệt","Không quản trị CRM, HIS, phần mềm Marketing hoặc tự cấp quyền dữ liệu"),
"qc-b":("Quản trị kênh số nhóm 2, quảng cáo và mã nguồn khách; bàn giao dữ liệu Lead theo nhóm thương hiệu","Không quản trị CRM, HIS, phần mềm Marketing hoặc tự cấp quyền dữ liệu"),
"cvt-2":("Giám sát tổ Tăng trưởng số, kiểm chất lượng phối hợp phần mềm và CRM theo tuyến nghiệp vụ; phân bổ tải không trùng Tổ trưởng","Không là tuyến quản lý thứ hai của nhân sự cơ sở; không tự duyệt thay Trưởng phòng, Phòng Công nghệ, Nghiệp vụ Y"),
"tp":("Chủ quản yêu cầu Marketing và ưu tiên triển khai CRM/phần mềm Marketing; trình cấp có thẩm quyền quyết định ngân sách và thay đổi lớn","Không thay chủ dữ liệu HIS, quyền duyệt kỹ thuật hoặc quyền phê duyệt tài chính")
}
for x in d["vi_tri"]:
 if x["id"] in role_map:
  a,b=role_map[x["id"]]
  x["bo_sung_quan_tri_he_thong_2027"]={"dau_ra_va_trach_nhiem":a,"ranh_gioi_quyen":b,"can_cu":"Phụ lục quản trị liên thông đề xuất; chờ nghiệm thu và phê duyệt"}
# Cập nhật dòng mô tả đã lỗi thời để không tự khẳng định phần mềm đã đồng bộ.
d["phan_mem_dac_ta"]["ghi_chu"]="Đặc tả tích hợp phần mềm Quản trị Marketing theo Khung 2027; trạng thái triển khai phần mềm thực tế phải đối chiếu phiên bản và biên bản nghiệm thu riêng. Phụ lục quản trị liên thông xác định chủ nghiệp vụ, quyền, đầu vào/đầu ra và kiểm thử; không tự xác nhận phần mềm đã hoàn tất."
s=s[:m.start(1)]+json.dumps(d,ensure_ascii=False,separators=(",",":"))+s[m.end(1):]
assert s.count('<button class="tab"')==12
p.write_text(s,"utf8")
folder=root/"khung-marketing"/"quan-tri-he-thong"
folder.mkdir(parents=True,exist_ok=True)
(folder/"du-lieu.json").write_text(json.dumps(d["quan_tri_he_thong_lien_thong_2027"],ensure_ascii=False,indent=2),"utf8")
def tr(cols):
 return "<tr>"+"".join("<td>"+escape(str(c))+"</td>" for c in cols)+"</tr>"
rs="".join(tr((n,a,b)) for n,a,b in owners)
fs="".join(tr((code,name,lead,approve,inp,steps,out,gate)) for code,name,lead,approve,inp,steps,out,gate in flows)
html=f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Quản trị hệ thống và liên thông – Marketing 2027</title><style>body{{margin:0;background:#f6f8fc;color:#172f50;font:16px/1.55 Arial,sans-serif}}header,main{{padding:18px clamp(12px,3vw,40px)}}header{{background:white;border-top:5px solid #0837A1;border-bottom:2px solid #ED3237}}main{{max-width:1500px;margin:auto}}h1{{font-size:clamp(22px,2.7vw,32px);color:#0837A1}}h2{{font-size:21px}}section{{background:white;border:1px solid #ced9e7;border-radius:10px;margin:16px 0;padding:18px}}.scroll{{overflow-x:auto}}table{{border-collapse:collapse;min-width:1100px;width:100%}}th,td{{border:1px solid #d4deea;padding:10px;vertical-align:top;text-align:left}}th{{background:#e7effe;color:#0837A1}}a{{color:#0837A1}}.status{{font-weight:700;color:#9d2528}}p{{max-width:1150px}}</style></head><body>
<header><a href="../">Khung cơ cấu Marketing 2027</a> · <a href="../nghiem-thu/">Nghiệm thu trước ban hành</a><h1>Quản trị kênh số, CRM, HIS và phần mềm Marketing</h1><p class="status">PHỤ LỤC NGHIỆP VỤ ĐỀ XUẤT – CHƯA PHẢI QUY TRÌNH ĐÃ BAN HÀNH</p></header>
<main><section><h2>Ranh giới hệ thống</h2><p><b>Kênh số:</b> website, mạng xã hội, quảng cáo, trang đích. <b>CRM:</b> quản lý quan hệ khách hàng, hồ sơ liên hệ và tương tác theo quyền. <b>HIS:</b> dữ liệu khám chữa bệnh và mã người bệnh do chủ dữ liệu y tế kiểm soát. <b>Phần mềm Marketing:</b> công việc, quy trình, ngân sách, sản phẩm, báo cáo và KPI.</p><p>Liên thông bằng mã tham chiếu, quyền và lịch sử đồng bộ; không đưa dữ liệu bệnh án sang CRM hoặc phần mềm Marketing ngoài mục đích và phạm vi được phép.</p></section>
<section><h2>Phân định MTCV và trách nhiệm</h2><div class="scroll"><table><thead><tr><th>Vị trí/đơn vị</th><th>Trách nhiệm chủ trì</th><th>Không được tự làm/thay quyền</th></tr></thead><tbody>{rs}</tbody></table></div></section>
<section><h2>8 luồng nghiệp vụ cần đối chiếu quy trình đã ban hành</h2><p>Đây là 8 luồng chi tiết hóa nghiệp vụ, không tự động làm tổng số 60 luồng trong Khung thành 68 quy trình chính thức. Mỗi luồng phải đối chiếu mã và hiệu lực văn bản cũ trước khi đề xuất sửa/gộp/xây mới.</p><div class="scroll"><table><thead><tr><th>Mã tạm</th><th>Tên luồng</th><th>Chủ trì</th><th>Thẩm quyền</th><th>Đầu vào</th><th>Trình tự</th><th>Chứng cứ đầu ra</th><th>Điều kiện chặn</th></tr></thead><tbody>{fs}</tbody></table></div></section>
<section><h2>Điều kiện nghiệm thu</h2><p>Phải có chủ dữ liệu và chủ nghiệp vụ ký xác nhận, danh sách quyền thực tế, bộ trường HIS–CRM được duyệt, ca kiểm thử trùng hồ sơ/sai mã, thử sự cố và khôi phục, số liệu đối soát và văn bản phân cấp có hiệu lực. KPI dự thảo không dùng để tính lương/thưởng.</p><p><a href="du-lieu.json">Tải dữ liệu đối chiếu máy đọc được</a></p></section></main></body></html>"""
(folder/"index.html").write_text(html,"utf8")
# Liên kết trong phần 12 không tạo tab mới, không thay 60 luồng gốc.
needle='<section class="view" data-view="decisions" id="v-decisions">'
assert s.count(needle)==1
link='<p style="padding:12px 16px;border:1px solid #b7c8df;border-left:4px solid #0837A1;border-radius:8px;background:#fff;font-size:15px"><b>Quản trị hệ thống liên thông:</b> <a href="quan-tri-he-thong/">xem phân định MTCV, CRM–HIS–Contact Center và 8 luồng phần mềm Marketing</a> (đề xuất, chờ đối chiếu và phê duyệt).</p>'
assert 'href="quan-tri-he-thong/"' not in s
s=s.replace(needle,needle+link,1)
p.write_text(s,"utf8")
print("PASS: 26 MTCV; 60 existing flows preserved; 8 detailed subflows; software status corrected; 12 tabs")
