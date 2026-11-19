#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chuẩn hóa CNNV 2027: chức năng, nhiệm vụ, đầu ra, quyền hạn, quan hệ, KPI, tải.
Không coi nhiệm vụ quản lý là quyền phát hành/chi; không cộng trùng tải Tổ trưởng.
Chạy cuối pipeline sau chuẩn hóa tên chức danh và phân quyền hai tuyến.
"""
import json,re,sys
from pathlib import Path
from html import escape

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
rx=r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)'
m=re.search(rx,s)
if not m:raise RuntimeError("Không tìm thấy dữ liệu khung")
D=json.loads(m.group(2))
V={x["id"]:x for x in D["vi_tri"]}
assert len(V)==26 and len(D["quy_trinh"])==60 and len(D["danh_muc_van_ban"])==83
assert sum(len(q["buoc"]) for q in D["quy_trinh"])==407
N=V["cvt"]["ten"]
T=V["cvt-2"]["ten"]
assert N=="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
assert T=="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"

# 1) Sửa MTCV gốc ở các chức danh trọng tâm: CNNV, không nhập nhằng quyền duyệt.
c2=V["cvt-2"]
c2["muc_dich"]=(
 "Chịu trách nhiệm quản trị nghiệp vụ và chất lượng vận hành của Tổ Truyền thông và Thương hiệu, "
 "Tổ Tăng trưởng số tại Tổng công ty; kiểm soát sự thống nhất của chuẩn PR, thương hiệu, OOH, "
 "phát thanh, màn hình, quảng cáo và kênh số tại các cơ sở cả hai nhóm. "
 "Chủ trì xây dựng, quản lý phiên bản, hướng dẫn áp dụng và trình cấp có thẩm quyền "
 "phê duyệt, ban hành quy chuẩn; tổ chức kiểm tra theo rủi ro và khắc phục lỗi tái diễn. "
 "Không giao việc trực tiếp hoặc đánh giá hành chính Trưởng nhóm Marketing bệnh viện."
)
c2["viec_chung"]=(
 "Quản trị danh mục quy chuẩn nghiệp vụ trong phạm vi hai tổ; theo dõi chất lượng và tiến độ tổng hợp, "
 "đánh giá năng lực Tổ trưởng, xử lý điểm nghẽn hoặc xung đột vượt phạm vi một tổ, quản lý rủi ro "
 "PR/OOH/kênh số; tổng hợp kết quả liên tổ. Tổ trưởng kiêm nhiệm phân công và nhắc tiến độ hằng ngày; "
 "chuyên viên tổ chức thực hiện. Với cơ sở, chuyển yêu cầu phát sinh ảnh hưởng tải việc qua "
 +N+"; không lập lệnh giao việc thứ hai."
)
c2["phan_dinh_chu_tri_dau_ra"]=(
 "Chủ trì hồ sơ quy chuẩn/phiên bản thuộc hai tổ; báo cáo chất lượng vận hành hai tổ, danh mục lỗi "
 "và biện pháp khắc phục, báo cáo phối hợp liên tổ, đánh giá năng lực và rủi ro nghiệp vụ, "
 "chỉ số tuân thủ tại cơ sở. Không nhận các đầu ra bài viết, quảng cáo, PR hay kết quả Hạng mục "
 "là sản phẩm cá nhân; không kiểm duyệt từng sản phẩm thông thường nếu đã có tuyến kiểm đúng chuẩn."
)
c2["phan_dinh_ban_giao_dau_vao"]=(
 "Nhận báo cáo tải và chất lượng từ Tổ trưởng hai tổ; nhận phản hồi của Quản lý thương hiệu "
 "và vấn đề nghiệp vụ tại cơ sở theo phiếu; chuyển yêu cầu cần sản xuất hoặc điều chỉnh "
 "nhân sự cơ sở qua "+N+"; chuyển vướng mắc ngân sách, thương hiệu, quyền phát hành "
 "vượt phân cấp cho Trưởng phòng/cấp được ủy quyền."
)
c2["phan_dinh_kiem_duyet"]=(
 "Kiểm chuẩn nghiệp vụ theo mẫu và theo mức độ rủi ro; có trách nhiệm ghi nhận, cảnh báo "
 "và yêu cầu khắc phục điểm không phù hợp. Không tự phát sinh quyền ký ban hành quy chuẩn, "
 "phát ngôn, phê duyệt nội dung y khoa, phát hành, ngân sách, nhân sự hay cấp quyền quản trị cao nhất."
)
# Bổ sung trách nhiệm chủ động nâng hiệu suất, không chỉ giám sát và xử lý lỗi.
c2["muc_dich"] += (
 " Đồng thời chịu trách nhiệm thiết kế và dẫn dắt cơ chế nâng hiệu suất, giảm lãng phí "
 "thời gian, hạn chế tái làm và cải tiến quy trình phối hợp giữa hai tổ theo dữ liệu; "
 "không lấy số lượng báo cáo hoặc số lần kiểm tra làm thước đo hiệu quả cải tiến."
)
c2["viec_chung"] += (
 " Định kỳ phân tích dữ liệu mã việc, thời gian xử lý chủ động/chờ duyệt, tỷ lệ đúng hạn, "
 "tỷ lệ sửa lại, chất lượng bàn giao và năng lực tải của từng tổ; truy nguyên điểm nghẽn, "
 "xác định nguyên nhân và chủ trì phương án cải tiến liên tổ theo một người phụ trách, "
 "mốc kiểm chứng, thời hạn và chỉ số trước–sau. Thử nghiệm thay đổi trong phạm vi quyền "
 "đã giao; sửa hoặc ban hành quy trình chính thức phải trình đúng cấp có thẩm quyền. "
 "Không duyệt lặp từng sản phẩm và không nhận việc phân lịch hàng ngày của hai Tổ trưởng."
)
c2["phan_dinh_chu_tri_dau_ra"] += (
 " Ngoài ra chủ trì bảng điều hành hiệu suất và tải của hai tổ (số liệu đối soát theo nguồn), "
 "danh mục điểm nghẽn kèm nguyên nhân gốc, phương án cải tiến đã phân công và biên bản "
 "đánh giá trước–sau; hồ sơ phiên bản quy trình và bằng chứng hướng dẫn triển khai. "
 "Đánh giá kết quả cải tiến theo thời gian xử lý, chất lượng, tuân thủ và hiệu suất nguồn lực; "
 "không quy thành số sản phẩm của Chuyên viên trưởng."
)
c2["phan_dinh_ban_giao_dau_vao"] += (
 " Hai Tổ trưởng cung cấp dữ liệu mã việc và nhật ký tải đã phân loại giờ, lịch, vòng sửa, "
 "sự cố và chất lượng nghiệm thu; Chuyên viên Đo lường và đối soát xác nhận số liệu nguồn "
 "độc lập. Sau khi phân tích, giao Tổ trưởng đúng tổ triển khai hành động cải tiến, "
 "theo dõi kết quả và nhận báo cáo đối chiếu; việc ảnh hưởng tải sản xuất/cơ sở chuyển "
 "qua đúng tuyến "+N+"."
)
c2["phan_dinh_kiem_duyet"] += (
 " Được yêu cầu dữ liệu, báo cáo nguyên nhân, khắc phục sai lệch theo chuẩn đang có hiệu lực, "
 "và đề xuất thử nghiệm cải tiến trong phạm vi được giao. Không tự thay đổi quy chế, "
 "cơ cấu nhân sự, phê duyệt chỉ tiêu, ngân sách hoặc quyền phát hành."
)
c2["toi_uu_hieu_suat"] = (
 "Trách nhiệm quản trị: xác lập đường cơ sở theo từng loại công việc, xác định năng lực xử lý "
 "và giới hạn tải; phát hiện thời gian chờ, bàn giao vòng vo, sửa đi sửa lại, lỗi tuân thủ "
 "và phối hợp trễ; lựa chọn ưu tiên cải tiến theo ảnh hưởng tới chất lượng, tốc độ và nguồn lực. "
 "Mỗi cải tiến phải có mã, một chủ trì, dữ liệu trước–sau, tiêu chí nghiệm thu và quyết định "
 "chuẩn hóa hoặc hoàn nguyên."
)
c2["chu_trinh_cai_tien"] = (
 "1. Tổ trưởng ghi nhận mã việc, thời gian thực làm/chờ, số vòng chỉnh sửa và chứng từ; "
 "2. Chuyên viên trưởng phân tích nguyên nhân xuyên hai tổ, lập danh sách ưu tiên; "
 "3. Xác định một người chủ trì hành động và xin phê duyệt khi sửa quy trình/hạn mức; "
 "4. Tổ trưởng thực hiện thử nghiệm và theo dõi không làm gián đoạn phê duyệt bắt buộc; "
 "5. Đo lường đối soát kết quả, Chuyên viên trưởng kết luận giữ/sửa/hoàn nguyên; "
 "6. Trình cấp có quyền ban hành phiên bản chuẩn, hướng dẫn và kiểm tra lỗi tái diễn."
)
c2["ranh_gioi_kpi"] = (
 "Tổ trưởng chịu giao việc, tiến độ và chất lượng tác nghiệp trong tổ; chuyên viên chịu sản phẩm "
 "và vận hành kênh; Quản lý thương hiệu chịu mục tiêu/hạng mục; Chuyên viên Đo lường và đối soát "
 "chịu nguồn số liệu độc lập. Vị trí này chịu trách nhiệm cải thiện cơ chế liên tổ và kết quả "
 "kiểm chứng, không cộng sản lượng/giờ của cấp dưới, không tự phê duyệt nội dung hay chi phí."
)
D["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]={
 "chuc_danh":T,
 "muc_dich":"Tối ưu hiệu suất và tính thông suốt của Tổ Truyền thông và Thương hiệu và Tổ Tăng trưởng số",
 "pham_vi":[
  {"to":"Tổ Truyền thông và Thương hiệu",
   "chi_so":[
    "Tỷ lệ bàn giao đúng hạn = đầu ra đúng hạn / đầu ra đến hạn có chứng từ",
    "Tỷ lệ nghiệm thu vòng đầu = đầu ra đạt ngay lần kiểm đầu / đầu ra đã kiểm",
    "Thời gian xử lý trung vị theo loại việc; tách giờ thực làm và chờ xác nhận",
    "Tỷ lệ lỗi nhận diện/PR/OOH/phát thanh/màn hình tái diễn = lỗi tái diễn / tổng lỗi ghi nhận"
   ],
   "dau_ra_cai_tien":"Bản đồ điểm nghẽn yêu cầu–kiểm–duyệt–triển khai; giải pháp giảm vòng sửa, giảm chờ và tăng tuân thủ",
   "chu_nguon_so_lieu":"Tổ trưởng ghi nhận; người kiểm và nhật ký hiện trường xác thực, Đo lường đối soát khi có dữ liệu hệ thống"},
  {"to":"Tổ Tăng trưởng số",
   "chi_so":[
    "Tỷ lệ thiết lập chiến dịch/trang đích đúng lịch = số nhiệm vụ đúng hạn / tổng nhiệm vụ đến hạn",
    "Tỷ lệ sai cấu hình/phân quyền/nguồn đo = nhiệm vụ phát sinh lỗi / nhiệm vụ đã nghiệm thu",
    "Thời gian từ nhận đủ đầu vào đến kích hoạt hợp lệ, tách thời gian chờ phê duyệt",
    "Tỷ lệ hoàn tất hành động tối ưu được đo trước–sau và xác minh bởi dữ liệu độc lập"
   ],
   "dau_ra_cai_tien":"Chuẩn hóa checklist trước phát hành, điểm bàn giao CRM/kênh/trang đích, giảm lỗi thiết lập và thời gian xử lý",
   "chu_nguon_so_lieu":"Tổ trưởng, chuyên viên kênh số và hồ sơ nền tảng; Đo lường đối soát số liệu nguồn"}
 ],
 "ky_kiem_soat":"Theo dõi theo mã việc; rà soát điểm nghẽn thường xuyên và đánh giá kết quả cải tiến theo kỳ quản trị được phê duyệt",
 "quy_trinh":"Ghi nhận dữ liệu → phân tích điểm nghẽn → giao một chủ trì cải tiến → thử nghiệm có kiểm soát → đối soát trước–sau → chuẩn hóa phiên bản hoặc hoàn nguyên",
 "dieu_kien":"Mục tiêu/ngưỡng KPI cần chốt sau khi có đường cơ sở thực đo, phân loại độ phức tạp và quyết định có hiệu lực; không tự áp chỉ tiêu hoặc lấy dữ liệu quảng cáo chưa đối soát",
 "hieu_luc":"Nội dung thiết kế CNNV trong đề án, không tự thay quyết định phân quyền hoặc văn bản nhân sự"
}
c1=V["cvt"]
c1["phan_dinh_chu_tri_dau_ra"]=(
 "Quản trị năng lực và chất lượng khối Nội dung – Sáng tạo; trực tiếp quản lý dọc các Trưởng nhóm "
 "Marketing bệnh viện của hai nhóm thương hiệu; chốt tải, mức ưu tiên và một lịch giao việc của "
 "Marketing cơ sở. Đầu ra quản trị là bảng tải, phương án điều phối, báo cáo chất lượng sản xuất "
 "và đánh giá Trưởng nhóm theo chứng cứ; không nhận trùng sản lượng bài, thiết kế, video của chuyên viên "
 "hoặc giờ điều phối thường lệ của Tổ trưởng."
)
c1["phan_dinh_ban_giao_dau_vao"]=(
 "Nhận yêu cầu sản xuất đúng luồng từ Quản lý thương hiệu và hai tổ chuyên môn; "
 "xác nhận tải/ưu tiên cơ sở khi "+T+" đề xuất thay đổi nghiệp vụ; "
 "Tổ trưởng Nội dung và Sáng tạo nhận và phân lịch sản xuất trong phần phạm vi đã giao. "
 "Vấn đề vượt tuyến, quyền và ngân sách chuyển Trưởng phòng/cấp được ủy quyền."
)

# Tổ trưởng kiêm nhiệm: giữ trách nhiệm thực hiện chuyên môn và tách rõ giờ điều phối.
for role in ("qlth-bc","qlsps"):
    v=V[role]
    current=v["viec_chung"]
    extra=(" Trong vai trò Tổ trưởng kiêm nhiệm: nhận và kiểm tính đầy đủ yêu cầu, phân việc theo "
           "lịch và năng lực, theo dõi hạn, xử lý ngoại lệ trong tổ, bàn giao chứng cứ vận hành cho "
           +T+". Không tự kiểm/duyệt độc lập sản phẩm do chính mình thực hiện hoặc thay quyết định "
           "về ngân sách, phát hành, dữ liệu chuyên môn. Giờ Tổ trưởng ghi riêng, không cộng vào "
           "giờ quản trị của "+T+".")
    if extra not in current:v["viec_chung"]=current+extra
V["qlth-bc"]["phan_dinh_ban_giao_dau_vao"]=(
 "Quản lý thương hiệu nhóm 2: nhận mục tiêu, nguồn, kế hoạch; nghiệm thu đúng phần nhóm 2. "
 "Vai trò Tổ trưởng Tổ Truyền thông và Thương hiệu: nhận danh sách việc đủ điều kiện, "
 "giao việc trong tổ, theo dõi hạn và chuyển xung đột vượt cấp đến "+T+". "
 "Hai vai trò sử dụng một nhật ký, phân giờ và KPI riêng."
)
V["qlsps"]["phan_dinh_ban_giao_dau_vao"]=(
 "Quản lý sản phẩm số giữ đầu mối nghiệp vụ website/App/trang đích với Phòng Số hóa; "
 "vai trò Tổ trưởng Tổ Tăng trưởng số phân lịch, phân việc chuyên viên quảng cáo, đo lường và số; "
 "đối soát tải, bàn giao rủi ro vượt cấp cho "+T+". "
 "Không tự duyệt thay đổi công nghệ, phát hành hoặc chi phí ngoài thẩm quyền."
)
V["bt-ac"]["phan_dinh_ban_giao_dau_vao"]=(
 "Trong phạm vi Biên tập nhóm 1: nhận yêu cầu theo nhóm và giao nội dung đã kiểm cho Thiết kế/Media. "
 "Khi được chỉ định kiêm Tổ trưởng Nội dung và Sáng tạo, chỉ điều phối thường lệ trong phạm vi "
 "văn bản giao nhiệm vụ; phần nhân sự nhóm 2 và thiết kế ngoại tuyến phải có đầu mối điều phối "
 "được chỉ định rõ, không tự coi "+N+" là Tổ trưởng thường trực và không tự cho phép "
 "xử lý chéo nội dung của hai nhóm."
)

# 2) Tạo cùng một mẫu CNNV cho 26 mã chức danh, trích từ các trường MTCV đang có,
#    nhưng không suy diễn thêm một quyền phê duyệt chưa được giao.
for v in D["vi_tri"]:
    v["cnnv_2027"]={
      "chuc_nang":v.get("muc_dich",""),
      "nhiem_vu_trong_tam":v.get("phan_dinh_chu_tri_dau_ra",""),
      "dau_vao_va_ban_giao":v.get("phan_dinh_ban_giao_dau_vao",""),
      "ranh_gioi_khong_lam_thay":v.get("phan_dinh_khong_thuoc_trach_nhiem",""),
      "quyen_han_va_kiem_soat":v.get("phan_dinh_kiem_duyet",""),
      "quan_he_bao_cao":v.get("bao_cao_cho",""),
      "tai_cong_viec":v.get("gio_ke_hoach",""),
      "toi_uu_hieu_suat":v.get("toi_uu_hieu_suat",""),
      "chu_trinh_cai_tien":v.get("chu_trinh_cai_tien",""),
      "ranh_gioi_kpi":v.get("ranh_gioi_kpi",""),
      "nguon":"Mô tả vị trí trong Khung cơ cấu Marketing 2027; phê duyệt chính thức theo QyĐ.02.MKT/Phòng Nhân lực",
      "trang_thai":"Nội dung chuẩn hóa trong đề án; không thay văn bản nhân sự/phân quyền đang có hiệu lực"
    }

# 3) Ma trận CNNV nghiệp vụ: quản lý chuẩn ≠ soạn kỹ thuật ≠ thực hiện ≠ phê duyệt.
D["cnnv_kiem_soat_nghiep_vu_2027"]=[
 {"mang":"PR, báo chí, phát ngôn, dư luận","chu_tri_quan_tri":T,
  "soan_va_thuc_hien":"Chuyên viên truyền thông đúng nhóm; Tổ trưởng Truyền thông và Thương hiệu điều phối",
  "kiem_tra":"Kiểm theo rủi ro; Quản lý thương hiệu xác nhận đúng mục tiêu/thông điệp",
  "phe_duyet":"Người có thẩm quyền phát ngôn, phát hành và chi phí theo quy chế"},
 {"mang":"OOH, biển bảng, phát thanh, màn hình nội viện","chu_tri_quan_tri":T,
  "soan_va_thuc_hien":"Chuyên viên truyền thông TCT phụ trách lịch/đề bài; Thiết kế, Media làm file; Marketing cơ sở vận hành và nghiệm thu hiện trường",
  "kiem_tra":"Đúng chuẩn nhận diện, kỹ thuật và nội dung; cơ sở xác nhận hiện trạng",
  "phe_duyet":"Theo quy trình OOH/âm thanh/màn hình và loại nội dung; không duyệt mặc nhiên bởi Chuyên viên trưởng"},
 {"mang":"Quảng cáo trả phí, kênh số, chính sách nền tảng","chu_tri_quan_tri":T,
  "soan_va_thuc_hien":"Chuyên viên quảng cáo/kênh số lập và tối ưu; Quản lý sản phẩm số giữ chuẩn kênh, Tổ trưởng Tăng trưởng số điều phối",
  "kiem_tra":"Đầu vào được nghiệm thu; chính sách nền tảng, quyền, nguồn dữ liệu và pháp lý được kiểm theo điểm chặn",
  "phe_duyet":"Quản lý thương hiệu nghiệm thu mục tiêu; pháp lý, phát hành và chi phí theo quyền riêng"},
 {"mang":"Sản phẩm số, website/App và trang đích","chu_tri_quan_tri":T,
  "soan_va_thuc_hien":"Quản lý sản phẩm số chủ nghiệp vụ; Phòng Số hóa thực hiện kỹ thuật; Biên tập/Thiết kế/Kênh số cung cấp đầu ra",
  "kiem_tra":"Quản lý sản phẩm số nghiệm thu nghiệp vụ; đơn vị chủ dữ liệu xác nhận nguồn",
  "phe_duyet":"Thay đổi lớn, quyền công bố và chi phí theo phân cấp; không gán cho Chuyên viên trưởng theo chức danh"},
 {"mang":"Đo lường, đối soát và dữ liệu khách hàng","chu_tri_quan_tri":T,
  "soan_va_thuc_hien":"Chuyên viên đo lường và đối soát; Chuyên viên dữ liệu khách hàng và thị trường theo nguồn, giai đoạn định biên",
  "kiem_tra":"Kiểm nguồn, đối soát độc lập, quyền truy cập và bảo vệ dữ liệu",
  "phe_duyet":"Người chủ dữ liệu, cấp duyệt báo cáo/chi theo phân cấp; không sửa dữ liệu gốc để đạt KPI"},
 {"mang":"Nội dung – Biên tập – Thiết kế – Media","chu_tri_quan_tri":N,
  "soan_va_thuc_hien":"Biên tập, Thiết kế, Media đúng nhóm; Tổ trưởng Nội dung và Sáng tạo điều phối theo phạm vi được chỉ định",
  "kiem_tra":"Biên tập/kỹ thuật độc lập; xác nhận y khoa và pháp lý đúng tầng",
  "phe_duyet":"Quản lý thương hiệu nghiệm thu mục tiêu; người có quyền duyệt phát hành, chi phí riêng"},
 {"mang":"Marketing cơ sở, kế hoạch và tải nguồn lực","chu_tri_quan_tri":N,
  "soan_va_thuc_hien":"Trưởng nhóm cơ sở giao việc; chuyên viên tại cơ sở thực hiện",
  "kiem_tra":"Ban Giám đốc cơ sở xác nhận thông tin/điều kiện thực địa; kiểm chuyên môn Truyền thông – Thương hiệu – Số qua đúng tuyến",
  "phe_duyet":"Người có thẩm quyền y khoa, phát hành và ngân sách theo phân cấp"}
]

# 4) Điểm bàn giao 1 đầu mối, không thêm bước duyệt mới cho việc thường lệ.
D["cnnv_luong_lien_to_2027"]=[
 {"buoc":"01. Tiếp nhận và xác định yêu cầu","chu_tri":"Quản lý thương hiệu hoặc Trưởng nhóm Marketing cơ sở theo loại việc",
  "dau_ra":"Một mã việc, mục tiêu, dữ liệu gốc, hạn, phân loại rủi ro, nguồn chi"},
 {"buoc":"02. Xác định tải và tuyến giao việc","chu_tri":"Tổ trưởng đúng tổ; "+N+" nếu đổi tải sản xuất/cơ sở",
  "dau_ra":"Một chủ việc và một lịch phân công; "+T+" chỉ phối hợp khi ảnh hưởng hai tổ hoặc chuẩn kênh"},
 {"buoc":"03. Tác nghiệp","chu_tri":"Chuyên viên đúng chuyên môn, đúng nhóm và theo phân quyền",
  "dau_ra":"Sản phẩm hoặc tác vụ có nhật ký, nguồn và người thực hiện"},
 {"buoc":"04. Kiểm và nghiệm thu","chu_tri":"Người kiểm chuyên môn độc lập; Quản lý thương hiệu nghiệm thu mục tiêu",
  "dau_ra":"Phiếu kiểm, xác nhận y khoa/pháp lý nếu áp dụng, bằng chứng nghiệm thu"},
 {"buoc":"05. Phê duyệt và phát hành","chu_tri":"Cấp được phân quyền phát hành/chi phí theo loại việc",
  "dau_ra":"Lịch sử duyệt, quyền, phiên bản và chứng cứ phát hành"},
 {"buoc":"06. Đo lường, khắc phục và đánh giá","chu_tri":"Tổ trưởng theo dõi đầu ra; hai chức danh Chuyên viên trưởng phân tích kết quả quản trị đúng tuyến",
  "dau_ra":"KPI cá nhân/tổ/quản lý không ghi trùng, hồ sơ lỗi và hành động khắc phục"}
]

# 5) Những quy tắc CNNV sai thời cơ cấu: sửa mô tả nguồn đề án chờ phê duyệt,
#    không sửa sự thật của quyết định nhân sự đã có hiệu lực.
for doc in D["danh_muc_van_ban"]:
    if doc.get("ma")=="QyĐ.02.MKT" and isinstance(doc.get("dieu_khoan"),list):
        doc["dieu_khoan"]=[
          x.replace("Tổ Truyền thông và Thương hiệu không đặt Tổ trưởng",
            "Tổ Truyền thông và Thương hiệu có Tổ trưởng kiêm nhiệm là Quản lý thương hiệu nhóm 2, chỉ điều phối việc và không có quyền duyệt mặc định")
          for x in doc["dieu_khoan"]
        ]
        doc["cnnv_yeu_cau_dong_bo"]="Cần Phòng Nhân lực/Phòng Quản lý chất lượng đối chiếu CNNV và quyết định có hiệu lực trước khi ban hành bản sửa."
D["cnnv_nguyen_tac_2027"]={
 "khong_phat_sinh_quyen":"Chức năng quản lý, kiểm soát và duyệt là ba loại quyền khác nhau. Chưa có ủy quyền hiệu lực thì không có quyền thay.",
 "to_truong_noi_dung":"Phải chốt đầu mối điều phối thường lệ cho nhóm 2 và Thiết kế ngoại tuyến bằng phân công cụ thể. Không tự động nâng quyền chéo nhóm của Tổ trưởng nhóm 1 hoặc giao thường trực lên Chuyên viên trưởng.",
 "ba_tang_tai":"Giờ người trực tiếp thực hiện, giờ kiêm Tổ trưởng và giờ quản trị Chuyên viên trưởng tách riêng; không cộng trùng.",
 "kpi":"Đầu ra sản phẩm tính cho người thực hiện; năng lực điều phối và tiến độ cho Tổ trưởng; chuẩn/hiệu quả/rủi ro liên tổ cho Chuyên viên trưởng; kết quả Hạng mục cho Quản lý thương hiệu.",
 "dieu_kien":"Đề xuất trong Khung 2027; việc sửa chức năng, nhân sự, thẩm quyền chính thức cần văn bản có hiệu lực."
}

s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]

# 6) Đưa CNNV vào ngay các MTCV cần phân định, không tạo màn hình/menu mới.
key_roles=["cvt","cvt-2","qlth-bc","qlsps","bt-ac"]
for role in key_roles:
    x=V[role]
    note=(
      '<div class="cnnv-vt" id="cnnv-vt-'+role+'" '
      'style="background:#f5f9ff;border:1px solid #d3e1f2;border-left:4px solid #0837A1;'
      'border-radius:8px;padding:12px;margin:10px 0;max-width:100%;overflow-wrap:anywhere">'
      '<strong style="display:block;color:#0837A1;margin-bottom:8px">CNNV – chức năng, nhiệm vụ và ranh giới trách nhiệm</strong>'
      '<p><b>Chức năng:</b> '+escape(x["muc_dich"])+'</p>'
      '<p><b>Đầu ra chịu trách nhiệm:</b> '+escape(x["phan_dinh_chu_tri_dau_ra"])+'</p>'
      '<p><b>Bàn giao và phối hợp:</b> '+escape(x["phan_dinh_ban_giao_dau_vao"])+'</p>'
      '<p><b>Thẩm quyền:</b> '+escape(x["phan_dinh_kiem_duyet"])+'</p>'
      +('<p><b>Tối ưu hiệu suất hai tổ:</b> '+escape(x["toi_uu_hieu_suat"])+'</p>'
      '<p><b>Chu trình cải tiến và trách nhiệm:</b> '+escape(x["chu_trinh_cai_tien"])+'</p>'
      '<p><b>Ranh giới trách nhiệm và KPI:</b> '+escape(x["ranh_gioi_kpi"])+'</p>'
      if role=="cvt-2" else '')
      '<small>Đối chiếu với CNNV phòng tại mục 4.1. Chưa thay văn bản MTCV do Phòng Nhân lực ban hành.</small>'
      '</div>'
    )
    pat=r'(<article\b[^>]*\bid="jd-'+re.escape(role)+r'"[^>]*>[\s\S]*?<div class="jd-body">)'
    matched=re.search(pat,s)
    if not matched:raise RuntimeError("Thiếu mục MTCV "+role)
    if 'id="cnnv-vt-'+role+'"' not in s:
        s=s[:matched.end()]+note+s[matched.end():]

# Giữ mục 4.3 đúng cơ cấu 2027; tránh số 13h cũ bị hiểu như tải quản lý đã phê duyệt.
old="Chuyên viên trưởng dành khoảng 13 giờ/tháng cho phần nhóm 2 và việc chung"
if old in s:
    s=s.replace(old,"phần điều phối nhóm 2 và việc chung của "+N+" chưa đủ giờ thực đo, không sử dụng số 13 giờ/tháng của phương án cũ để kết luận tải của cơ cấu mới",1)
else:
    print("CNNV NOTE: mục 4.3 có thể đã được hiệu chỉnh ở bước trước")

# Chèn bảng quy chuẩn vào đúng mục chức năng nhiệm vụ Phòng, không mở thêm menu.
anchor='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
if anchor not in s:raise RuntimeError("Không tìm được vị trí chương 4.3")
if 'id="cnnv-phong-phan-tuyen-2027"' not in s:
    rows=''.join(
      '<tr><td>'+escape(x["mang"])+'</td><td>'+escape(x["chu_tri_quan_tri"])+
      '</td><td>'+escape(x["soan_va_thuc_hien"])+'</td><td>'+
      escape(x["phe_duyet"])+'</td></tr>'
      for x in D["cnnv_kiem_soat_nghiep_vu_2027"]
    )
    panel=(
      '<div id="cnnv-phong-phan-tuyen-2027" style="margin:15px 0 18px">'
      '<h4 style="color:#0837A1;margin:5px 0 7px">Phân cấp CNNV và quản lý quy chuẩn theo tuyến</h4>'
      '<p class="mini">Bảng này phân biệt người chịu trách nhiệm quản trị quy chuẩn với người soạn, '
      'người thực hiện và cấp có thẩm quyền. Việc thông thường không mặc nhiên tăng thêm vòng duyệt.</p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto">'
      '<table class="t" style="min-width:920px;table-layout:auto">'
      '<thead><tr><th>Mảng chức năng</th><th>Quản trị quy chuẩn</th><th>Soạn và thực hiện</th><th>Phê duyệt</th></tr></thead>'
      '<tbody>'+rows+'</tbody></table></div>'
      '<p class="mini">Cơ cấu CNNV trong đề án; thẩm quyền ban hành và nhân sự kiêm nhiệm phải đối chiếu văn bản có hiệu lực.</p>'
      '</div>'
    )
    s=s.replace(anchor,panel+anchor,1)

check=json.loads(re.search(rx,s).group(2))
assert len(check["vi_tri"])==26 and len(check["quy_trinh"])==60 and len(check["danh_muc_van_ban"])==83
assert sum(len(q["buoc"]) for q in check["quy_trinh"])==407
assert all("cnnv_2027" in x for x in check["vi_tri"])
assert all(s.count('id="cnnv-vt-'+role+'"')==1 for role in key_roles)
assert s.count('id="cnnv-phong-phan-tuyen-2027"')==1
assert "ban hành/hướng dẫn" not in next(x for x in check["vi_tri"] if x["id"]=="cvt-2")["muc_dich"]
assert "giảm lãng phí" in next(x for x in check["vi_tri"] if x["id"]=="cvt-2")["muc_dich"]
assert "đánh giá trước–sau" in next(x for x in check["vi_tri"] if x["id"]=="cvt-2")["phan_dinh_chu_tri_dau_ra"]
assert len(check["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]["pham_vi"])==2
assert all(len(z["chi_so"])==4 for z in check["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]["pham_vi"])

p.write_text(s,"utf-8")
print("PASS CNNV 2027: 26 MTCV, 5 vị trí trọng tâm, 7 mảng chuẩn, 6 điểm luồng, 60 quy trình/407 bước, 83 văn bản")
