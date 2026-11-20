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
 "không quy thành số sản phẩm cá nhân của "+T+"."
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
 "2. "+T+" phân tích nguyên nhân xuyên hai tổ, lập danh sách ưu tiên; "
 "3. Xác định một người chủ trì hành động và xin phê duyệt khi sửa quy trình/hạn mức; "
 "4. Tổ trưởng thực hiện thử nghiệm và theo dõi không làm gián đoạn phê duyệt bắt buộc; "
 "5. Đo lường đối soát kết quả, "+T+" kết luận giữ/sửa/hoàn nguyên; "
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
    "Tỷ lệ cải tiến đạt mục tiêu đã duyệt = hành động đến hạn đạt mục tiêu sau kiểm chứng / tổng hành động cải tiến đến hạn"
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
 "Marketing cơ sở thuộc cả hai nhóm thương hiệu theo cơ cấu 2027; trực tiếp quản lý, "
 "kiểm chuẩn và đánh giá nghiệp vụ các Trưởng nhóm Marketing cơ sở theo một tuyến. "
 "Ban Giám đốc cơ sở quản lý hành chính và xác nhận dữ liệu tại chỗ, không tạo tuyến "
 "chỉ huy nghiệp vụ thứ hai. Mọi thay đổi tuyến quản lý chỉ có hiệu lực khi có quyết định "
 "phân quyền hoặc bàn giao được ban hành; không tự chuyển sang Quản lý mạng lưới theo vùng. "
 "Đầu ra quản trị là bảng tải, "
 "phương án điều phối, báo cáo chất lượng sản xuất và đánh giá theo đúng tuyến có hiệu lực; "
 "không nhận trùng sản lượng bài, thiết kế, video của chuyên viên hoặc giờ điều phối thường lệ của Tổ trưởng."
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

# 1b) Khép kín tuyến điều phối ngoại tuyến và mối quan hệ phòng khám.
# Đây là CƠ CHẾ ĐỀ XUẤT, không tự tạo vị trí, người phụ trách hay quyền mới.
# Người điều phối thường lệ phải được chỉ định từ nhân sự hiện hữu, có hiệu lực.
V["bt-ac"]["bao_cao_cho"]=(
 N+" quản lý trực tiếp nghiệp vụ. Trong vai trò kiêm Tổ trưởng Nội dung và Sáng tạo, "
 "chỉ điều phối người/việc trong phạm vi văn bản phân công (chủ yếu nhóm 1); "
 "không báo cáo cho chính vai trò Tổ trưởng do mình đảm nhiệm; Trưởng phòng xử lý vượt quyền."
)
for role in ("bt-b","tk-b","md-b","tk-nt"):
 v=V[role]
 v["bao_cao_cho"]=(
  N+" quản lý nghiệp vụ thuộc Tổ Nội dung và Sáng tạo. Việc nhận và phân lịch hằng ngày "
  "cho nhóm 2 hoặc thiết kế ngoại tuyến do đầu mối điều phối là nhân sự hiện hữu được "
  "Trưởng phòng chỉ định rõ mã việc, phạm vi, thời hạn và người dự phòng; "
  "không mặc định Tổ trưởng nhóm 1 được điều động chéo nhóm, cũng không để "+N+
  " trực tiếp phân việc thường lệ. Khi thiếu chỉ định có hiệu lực: giữ tại hàng chờ "
  "phân tuyến, Trưởng phòng xác lập đầu mối; không tự phát lệnh thứ hai."
 )
 v["dieu_phoi_theo_phan_cong_2027"]=(
  "Nhận một mã yêu cầu từ cổng chung; kiểm nhóm thương hiệu và tải; "
  "chỉ nhận lịch từ đầu mối được chỉ định có hiệu lực; việc đổi nhóm hoặc đổi người "
  "phải ghi nguồn, người quyết định và thời điểm, không tự cấp quyền."
 )
V["tk-nt"]["muc_dich"]=re.sub(
 r"tuyến điều phối việc của vị trí này thuộc (?:Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở|Chuyên viên trưởng)\.",
 "tuyến quản lý nghiệp vụ thuộc "+N+"; phân lịch thường lệ qua đầu mối được chỉ định có hiệu lực.",
 V["tk-nt"]["muc_dich"]
)
V["dmpk"]["bao_cao_cho"]=(
 "Người phụ trách phòng khám TTH Clinic quản lý công việc chính và hành chính tại chỗ. "
 "Quản lý thương hiệu nhóm 1 xác định mục tiêu; "+N+
 " tiếp nhận và phân tuyến yêu cầu Marketing theo đầu mối TCT; "+T+
 " hướng dẫn và kiểm chuẩn nghiệp vụ truyền thông/kênh số qua cùng mã việc và qua tuyến "
 +N+". Không tạo hai người giao việc hoặc chuyển phòng khám sang nhóm thương hiệu 2."
)
V["dmpk"]["phan_dinh_ban_giao_dau_vao"]=(
 "Đầu mối kiêm nhiệm gửi một hồ sơ thông tin/ảnh đã được phòng khám xác nhận cho đầu mối "
 "Marketing TCT có mã việc; không gửi hai lệnh trùng nhau. Nếu thiếu người nhận hoặc thiếu "
 "quyền phát hành, trả về trạng thái CHỜ PHÂN TUYẾN/CHƯA CÓ ỦY QUYỀN HIỆU LỰC."
)
D["cnnv_dieu_phoi_ngoai_tuyen_2027"]={
 "trang_thai":"Cơ chế đề xuất trong Khung 2027; chỉ kích hoạt phân công cá nhân khi có văn bản có hiệu lực",
 "pham_vi":"Biên tập/Thiết kế/Media nhóm 2 và Thiết kế ngoại tuyến, không bổ sung suất định biên",
 "chu_quan_nghiep_vu":N,
 "xac_lap_dau_moi":"Trưởng phòng Marketing ghi rõ nhân sự hiện hữu, việc/nhóm, thời hạn, người dự phòng và phạm vi điều phối; Tổ trưởng nhóm 1 không mặc nhiên điều phối nhóm 2",
 "thuc_hien":"Người nhận mã việc kiểm căn cứ chỉ định; đầu mối được chỉ định phân lịch và giao chuyên viên; chuyên viên sản xuất và bàn giao chứng cứ",
 "giai_quyet_xung_dot":"Xung đột nhóm, năng lực hay lịch do đầu mối báo "+N+" tổng hợp tải và trình Trưởng phòng quyết định ưu tiên vượt thẩm quyền; không phát sinh hai lệnh",
 "khoa":"Thiếu chỉ định hiệu lực hoặc nhân sự nhận việc: CHỜ PHÂN TUYẾN; không tự lấy "+N+" làm Tổ trưởng thường trực",
 "phan_biet":"Quản lý thương hiệu nghiệm thu mục tiêu; người kiểm độc lập kiểm chuyên môn; quyền phát hành và chi phí là hai quyết định khác nhau."
}
D["cnnv_kiem_soat_luong_va_tham_quyen_2027"]=[
 {"truong_hop":"Yêu cầu nội dung/video cơ sở","mot_dau_moi":"Trưởng nhóm Marketing cơ sở giao nhân viên; "+N+" quản lý tuyến Trưởng nhóm","kiem_chuan":T+" kiểm nghiệp vụ truyền thông theo điểm rủi ro; yêu cầu sửa chuyển qua đầu mối","phe_duyet":"Xác nhận y khoa/pháp lý và người có quyền phát hành, chi phí tách biệt"},
 {"truong_hop":"Việc nhóm 2 và Thiết kế ngoại tuyến","mot_dau_moi":"Đầu mối điều phối hiện hữu được Trưởng phòng chỉ định và ghi mã việc","kiem_chuan":N+" kiểm tải và rủi ro chất lượng, không phân lịch thường lệ","phe_duyet":"Chờ chỉ định hiệu lực thì khóa giao; người làm không tự nghiệm thu"},
 {"truong_hop":"OOH, phát thanh, màn hình cơ sở","mot_dau_moi":"Truyền thông TCT giữ lịch/mẫu; Trưởng nhóm cơ sở giao người vận hành","kiem_chuan":T+" kiểm chuẩn nghiệp vụ; Ban Giám đốc cơ sở xác nhận thực địa","phe_duyet":"Nội dung phát, quyền công bố, hợp đồng và chi phí theo cấp riêng"},
 {"truong_hop":"PR, báo chí, phát ngôn","mot_dau_moi":"Tổ trưởng Truyền thông và Thương hiệu giao Chuyên viên truyền thông","kiem_chuan":T+" giám sát rủi ro; Quản lý thương hiệu xác nhận mục tiêu","phe_duyet":"Người được ủy quyền phát ngôn/phát hành; không cấp mặc nhiên"},
 {"truong_hop":"Quảng cáo, kênh số và dữ liệu","mot_dau_moi":"Tổ trưởng Tăng trưởng số điều phối chuyên viên; Phòng Số hóa phụ trách kỹ thuật hệ thống","kiem_chuan":T+" giám sát chuẩn và tải; chủ dữ liệu xác nhận nguồn","phe_duyet":"Quyền tài khoản, phát hành, chi phí, thay đổi kỹ thuật phải có căn cứ riêng"},
 {"truong_hop":"Kiêm Tổ trưởng đồng thời sản xuất","mot_dau_moi":"Tổ trưởng phân lịch với nhật ký tải riêng, không tự duyệt việc mình làm","kiem_chuan":"Người khác đủ năng lực kiểm độc lập, lưu hai mã nhân sự","phe_duyet":"Nếu chưa có người kiểm hoặc ủy quyền hiệu lực thì khóa nghiệm thu/phát hành"}
]
D["cnnv_tai_hai_chuc_danh_2027"]={
 "trang_thai":"CHƯA ĐỦ GIỜ THỰC ĐO; không kết luận đủ tải hoặc thiếu tải từ định biên mục tiêu",
 "don_vi":"giờ quản trị/tháng, theo mã việc duy nhất; không cộng giờ sản xuất và giờ kiêm Tổ trưởng",
 "cong_thuc":"T = tổng (số lượt kiểm chuẩn hoặc quản trị theo loại việc × phút chuẩn/lượt × tần suất)/60 + giờ họp/báo cáo/đào tạo/ngoại lệ và quản lý tuyến thực đo - giờ trùng đã ghi; so sánh với giờ thực khả dụng đã xác minh",
 "phan_loai_nguon":"(1) Định mức có căn cứ bằng nhật ký chuẩn đã duyệt; (2) giả định kế hoạch chưa xác minh; (3) giờ thực đo bằng mã việc, ngày, người làm và chứng từ",
 "noi_dung":{"chuc_danh":N,"bien_so":"Số tổ và nhóm sản xuất trực thuộc, số Trưởng nhóm cơ sở hai nhóm thực quản lý, số yêu cầu đổi tải, lượt kiểm chuẩn, báo cáo, đào tạo, xung đột và phát sinh","khong_cong":"Giờ Biên tập/Thiết kế/Media, giờ Tổ trưởng kiêm nhiệm, phần vận hành thực địa của cơ sở","kpi":"Tỷ lệ giao đúng tuyến; thời gian giải quyết xung đột; lỗi tái diễn; chất lượng và độ chính xác dự báo tải; kết quả đào tạo"},
 "truyen_thong":{"chuc_danh":T,"bien_so":"Hai tổ TCT, lượt kiểm chuẩn PR/OOH/màn hình/phát thanh/quảng cáo/kênh số, báo cáo liên tổ, đào tạo, rủi ro và cải tiến","khong_cong":"Giờ PR/quảng cáo/sản phẩm số trực tiếp, giờ Tổ trưởng Truyền thông và Tăng trưởng số, công việc cơ sở do Trưởng nhóm giao","kpi":"Lỗi lặp, thời gian chờ duyệt, cải thiện trước–sau, tỷ lệ tuân thủ chuẩn và tỷ lệ khắc phục đúng hạn"},
 "nguong_canh_bao_de_xuat":"Sau khi có nhật ký đủ kỳ và giờ khả dụng được duyệt: tải dự báo từ 80% giờ khả dụng thì cảnh báo; từ 90% xem xét phân bổ lại hoặc giảm vòng kiểm không cần thiết; đây là ngưỡng quản trị tham khảo chưa được ban hành, không phải phê duyệt tăng biên chế",
 "khoa_ket_luan":"Thiếu phút chuẩn/lượt, tần suất và giờ thực đo thì hiển thị CHƯA ĐỦ DỮ LIỆU, không tuyên bố đủ tải."
}

# 1c) Ba tổ không đồng nghĩa ba cấp quản lý. Một chức danh quản lý hai tổ
#     có quyền xử lý xung đột ưu tiên theo phạm vi, nhưng KHÔNG duyệt thay
#     quyết định phát hành/chi phí, không tự làm Tổ trưởng hai tổ.
D["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]={
 "mo_hinh":"Ba tổ nghiệp vụ; hai chức danh quản lý dưới Trưởng phòng Marketing. Tổ Nội dung và Sáng tạo thuộc "+N+
 "; Tổ Truyền thông và Thương hiệu cùng Tổ Tăng trưởng số thuộc "+T+".",
 "phan_biet":"Hai Tổ trưởng Truyền thông và Thương hiệu, Tăng trưởng số điều phối nhân sự, lịch, đầu ra thường ngày trong từng tổ; "+T+
 " quản trị chuẩn chung, tải liên tổ, điểm nghẽn và rủi ro. Không tính sản lượng của chuyên viên thành KPI hay giờ làm của chức danh quản lý.",
 "giao_dien_hang_muc":"Quản lý thương hiệu sở hữu mục tiêu/thông điệp/hạng mục; Biên tập–Thiết kế–Media sản xuất qua tuyến "+N+
 "; Truyền thông và Tăng trưởng số phân phối, vận hành, đo lường qua tuyến "+T+
 ". Một mã hạng mục có các mã nhánh có chủ việc riêng; một đường tiếp nhận, không có hai lệnh đồng thời.",
 "tranh_chap_hai_to":"Hai Tổ trưởng xử lý sai lệch trong lịch đã duyệt; nếu không thống nhất về nguồn lực hoặc ưu tiên liên hai tổ, "+T+
 " đối chiếu mục tiêu được Quản lý thương hiệu nghiệm thu, năng lực tải và rủi ro để chốt phương án trong phạm vi được giao. Thay đổi mục tiêu, chi phí, phát hành hoặc hạn mức phải trình đúng người có quyền.",
 "tranh_chap_lien_tuyen":"Nguồn lực sản xuất/cơ sở thuộc "+N+"; nếu xung đột với hai tổ thuộc "+T+
 ", hai bên đối soát một phiếu xung đột. Không thống nhất hoặc vượt quyền thì Trưởng phòng chốt mức ưu tiên, không cấp thêm tuyến chỉ huy nhân sự.",
 "chuoi_kiem_soat":"Người thực hiện → người kiểm độc lập → xác nhận y khoa/pháp lý khi áp dụng → Quản lý thương hiệu nghiệm thu mục tiêu → quyền phê duyệt phát hành/chi phí theo văn bản riêng. Chức danh quản lý không tự động trở thành cửa duyệt mỗi sản phẩm.",
 "nguon":"Phương án cơ cấu 2027; việc giao nhân sự kiêm nhiệm, sửa quy trình hoặc quyền duyệt chỉ có hiệu lực khi được ban hành theo đúng cấp.",
 "tinh_huong":[
  {"ma":"XT-01","rui_ro":"Hai tổ Truyền thông và Thương hiệu – Tăng trưởng số cùng cần lịch chiến dịch",
   "dau_moi":"Tổ trưởng từng tổ lập lịch và cam kết đầu ra theo một mã hạng mục",
   "quyet_dinh":T+" quyết định điều phối ưu tiên liên hai tổ theo phạm vi quyền; Trưởng phòng xử lý phần vượt quyền",
   "quy_tac_chan":"Thiếu đầu vào đã nghiệm thu, lịch chung hoặc căn cứ đổi hạn thì CHỜ ĐIỀU PHỐI; không phát hành sớm"},
  {"ma":"XT-02","rui_ro":"Quản lý thương hiệu nhóm 2 kiêm Tổ trưởng Truyền thông và Thương hiệu có lợi ích ưu tiên nhóm mình",
   "dau_moi":"Quản lý thương hiệu từng nhóm ghi mục tiêu và thứ tự ưu tiên; Tổ trưởng chỉ xếp lịch cho cả tổ",
   "quyet_dinh":T+" kiểm cân đối tải, giải quyết ưu tiên liên nhóm trong phạm vi được giao; Trưởng phòng chốt thay đổi mục tiêu hoặc ưu tiên cấp phòng",
   "quy_tac_chan":"Không dùng vai trò Tổ trưởng để tự nghiệm thu hoặc tự duyệt hạng mục của mình"},
  {"ma":"XT-03","rui_ro":"Quản lý sản phẩm số kiêm Tổ trưởng Tăng trưởng số tự kiểm, dành tải cho việc mình",
   "dau_moi":"Tổ trưởng Tăng trưởng số lập lịch chung; chuyên viên quảng cáo và Đo lường giữ nhật ký tải riêng",
   "quyet_dinh":T+" giải quyết ưu tiên và kiểm định hiệu suất; Phòng Số hóa thực hiện/kiểm kỹ thuật đúng trách nhiệm",
   "quy_tac_chan":"Người phát triển không tự kiểm độc lập hoặc tự phát hành thay đổi hệ thống; thiếu người kiểm thì CHỜ NGHIỆM THU"},
  {"ma":"XT-04","rui_ro":"Sản phẩm Nội dung – Thiết kế – Media trễ nhưng Truyền thông/quảng cáo đã lên lịch",
   "dau_moi":"Tổ trưởng đầu mối sản xuất đúng nhóm và hai Tổ trưởng tiếp nhận một mã việc, mã nhánh bàn giao rõ",
   "quyet_dinh":N+" xác nhận khả năng sản xuất; "+T+" xác nhận tải hai tổ; Trưởng phòng quyết định khi đổi ưu tiên liên tuyến không thống nhất",
   "quy_tac_chan":"Chưa nghiệm thu sản phẩm/nguồn y khoa/pháp lý thì không được lấy lịch quảng cáo làm quyền phát hành"},
  {"ma":"XT-05","rui_ro":"Nhóm 2 và Thiết kế ngoại tuyến không có người phân lịch thường lệ",
   "dau_moi":"Nhân sự hiện hữu được Trưởng phòng phân công rõ nhóm, việc, thời hạn và người dự phòng",
   "quyet_dinh":N+" quản trị tải và chuyển việc vượt thẩm quyền lên Trưởng phòng; không làm Tổ trưởng mặc định",
   "quy_tac_chan":"Chưa có phân công hiệu lực thì CHỜ PHÂN TUYẾN, không tự chuyển việc sang Tổ trưởng nhóm 1"},
  {"ma":"XT-06","rui_ro":"Cơ sở nhận chỉ đạo kép từ TCT, hoặc bất đồng với Ban Giám đốc cơ sở",
   "dau_moi":"Trưởng nhóm cơ sở giao nhân viên, nhận một mã yêu cầu; Ban Giám đốc cơ sở xác nhận dữ liệu và quản lý hành chính",
   "quyet_dinh":N+" quản lý tuyến Trưởng nhóm; "+T+" gửi kiểm chuẩn truyền thông/số qua tuyến, không ra lệnh nhân sự cơ sở",
   "quy_tac_chan":"Thiếu xác nhận dữ liệu hoặc chỉ định người giao việc hợp lệ thì CHỜ BỔ SUNG/CHỜ PHÂN TUYẾN"},
  {"ma":"XT-07","rui_ro":"Kiểm pháp lý/y khoa, nghiệm thu mục tiêu và duyệt phát hành/chi phí bị nhập làm một",
   "dau_moi":"Người làm ghi nguồn và phiên bản; người kiểm độc lập kiểm chuyên môn; Quản lý thương hiệu nghiệm thu mục tiêu",
   "quyet_dinh":"Người có quyền phát hành và người có quyền chi phí được đối chiếu riêng theo quyết định đang hiệu lực",
   "quy_tac_chan":"CHƯA CÓ ỦY QUYỀN HIỆU LỰC hoặc cùng người tự kiểm thì khóa phát hành/chi, không suy diễn quyền theo chức danh"},
  {"ma":"XT-08","rui_ro":"Khủng hoảng truyền thông, sự cố tài khoản hoặc yêu cầu gấp làm hai tổ bỏ quy trình",
   "dau_moi":"Tổ trưởng đúng tổ ghi nhận sự cố, trạng thái, hành động an toàn thuộc quyền hiện có",
   "quyet_dinh":T+" điều phối khắc phục rủi ro truyền thông/số; "+N+" cân tải sản xuất/cơ sở; Trưởng phòng xử lý vượt quyền",
   "quy_tac_chan":"Không tự phát ngôn, phát hành, chi phí hoặc cấp quyền truy cập để xử lý nhanh khi chưa có căn cứ"},
  {"ma":"XT-09","rui_ro":"Vắng mặt, tuyển thay, chuyển nhóm làm thiếu một chủ trì và sai người kiểm",
   "dau_moi":"Tổ trưởng bàn giao mã việc; người quản lý trực tiếp theo tuyến xác nhận, Phòng Nhân lực đối chiếu hồ sơ",
   "quyet_dinh":"Mỗi thay thế phải có người, phạm vi, thời hạn, tuyến quản lý, người kiểm khác người làm và cấp phê duyệt riêng",
   "quy_tac_chan":"Không có phân công hiệu lực, mã nhân sự hoặc người kiểm độc lập: CHỜ BÀN GIAO/CHỜ NGHIỆM THU"}
 ]
}
# 1c.1) Nhánh xử lý xung đột HAI TỔ do cùng một Chuyên viên trưởng quản lý:
# thuộc QT xung-dot-lich, KHÔNG phát sinh quy trình thứ 61 hoặc cấp duyệt mới.
# Chỉ là quy tắc định tuyến đề xuất; người được ủy quyền thực thi theo văn bản
# hiệu lực. Mã CVT vẫn là khóa kỹ thuật, tên hiển thị dùng đúng hai chức danh.
D["cnnv_nhanh_xung_dot_hai_to_2027"]={
 "quy_trinh_goc":"xung-dot-lich",
 "lien_quan":["yeu-cau-gap","hang-muc","hang-muc-toan-he-thong",
              "quang-cao-tra-phi","phat-thanh-man-hinh","vang-mat",
              "nhan-viec-moi","chuyen-quyen","su-co-tai-khoan"],
 "trang_thai":"NHÁNH ĐIỀU PHỐI ĐỀ XUẤT TRONG QT HIỆN CÓ; chưa thay văn bản phân quyền hoặc ban hành quy trình mới",
 "dieu_kien_kich_hoat":"Tổ Truyền thông và Thương hiệu và Tổ Tăng trưởng số cùng cần thay đổi ưu tiên, lịch hoặc phụ thuộc đầu ra; phải xác định một đầu mối điều phối, phạm vi, người chịu trách nhiệm và căn cứ trước khi thực thi",
 "phai_phan_biet":[
   {"loai":"Cùng một tổ","nguoi_chot":"Tổ trưởng tổ liên quan",
    "pham_vi":"Đổi lịch thường lệ trong thời hạn và nguồn lực đã được phê duyệt"},
   {"loai":"Hai tổ Truyền thông và Thương hiệu – Tăng trưởng số tại Tổng công ty",
    "nguoi_chot":T,
    "pham_vi":"Kiểm tải liên tổ, chọn phương án phối hợp trong phạm vi quản lý hai tổ, không ký duyệt phát hành hay chi phí"},
   {"loai":"Tuyến Nội dung – Sáng tạo/Marketing cơ sở với Truyền thông – Thương hiệu/Tăng trưởng số",
    "nguoi_chot":"Trưởng phòng Marketing nếu "+N+" và "+T+" không thống nhất hoặc yêu cầu vượt quyền",
    "pham_vi":"Không giao lại nhân sự của tuyến kia; hai chức danh cung cấp ý kiến kiểm chuẩn và tải theo phạm vi"},
   {"loai":"Thay mục tiêu, hạn mức, ngân sách, phát hành, phát ngôn, quyền hệ thống",
    "nguoi_chot":"Người có thẩm quyền theo quyết định, ma trận còn hiệu lực",
    "pham_vi":"Không suy diễn quyền chỉ vì giữ chức danh hoặc xử lý khẩn"}
 ],
 "buoc":[
  {"so":1,"ten":"Ghi một phiếu xung đột","chu_tri":"Tổ trưởng nơi tiếp nhận xung đột đầu tiên",
   "dau_vao":"Mã việc, hai lịch tổ, phạm vi nhóm thương hiệu/cơ sở, người làm, hạn và rủi ro",
   "dau_ra":"Một mã phiếu liên kết hai mã nhánh; đánh dấu người tổng hợp duy nhất",
   "chuyen_buoc":"Thiếu dữ liệu hoặc trùng lệnh: CHỜ PHÂN TUYẾN, không tự chuyển việc"},
  {"so":2,"ten":"Đối chiếu tải, phụ thuộc và biện pháp","chu_tri":"Hai Tổ trưởng, một người được xác định làm đầu mối tổng hợp",
   "dau_vao":"Giờ khả dụng thực đo, mốc phát hành đã duyệt, phụ thuộc sản phẩm/trang đích, năng lực dự phòng",
   "dau_ra":"Phương án giữ lịch, thay thứ tự hoặc điều chỉnh đầu vào có căn cứ và nhật ký",
   "chuyen_buoc":"Không tự chuyển quyền nguồn lực ngoài tổ; không dùng giờ quản trị của "+T+" làm giờ tác nghiệp"},
  {"so":3,"ten":"Xác nhận mục tiêu và điều kiện nghiệp vụ","chu_tri":"Quản lý thương hiệu đúng nhóm/hạng mục",
   "dau_vao":"Mục tiêu, thông điệp, phân khúc và thời hạn đã được phê duyệt",
   "dau_ra":"Ý kiến nghiệm thu mục tiêu; trường hợp hai nhóm thì lưu hai phiếu theo mã nhánh",
   "chuyen_buoc":"Không tự nghiệm thu sản phẩm do chính mình thực hiện; không thay kiểm y khoa/pháp lý"},
  {"so":4,"ten":"Chốt phương án đúng tuyến","chu_tri":T+" đối với hai tổ trực thuộc; "+N+" đối với tải sản xuất/cơ sở",
   "dau_vao":"Bảng phương án hai Tổ trưởng, xác nhận mục tiêu và điểm kiểm chuẩn",
   "dau_ra":"Một phương án ưu tiên và người phân việc đúng tổ; khác tuyến hoặc vượt quyền chuyển Trưởng phòng",
   "chuyen_buoc":"Hai chức danh không cùng ra lệnh trực tiếp một nhân sự; Trưởng phòng chỉ quyết trong phạm vi được giao"},
  {"so":5,"ten":"Kiểm quyền quyết định trước thay đổi","chu_tri":"Người có thẩm quyền tương ứng loại quyết định",
   "dau_vao":"Căn cứ phát hành, chi phí, sửa mục tiêu, quyền hệ thống và ủy quyền còn hiệu lực",
   "dau_ra":"Quyết định theo từng quyền hoặc trạng thái CHƯA CÓ ỦY QUYỀN HIỆU LỰC",
   "chuyen_buoc":"Thiếu người kiểm độc lập, xác nhận y khoa/pháp lý hoặc ủy quyền: khóa phát hành/chi; không tự cấp quyền"},
  {"so":6,"ten":"Thông báo một kết quả và hậu kiểm","chu_tri":"Tổ trưởng đầu mối tổng hợp của phiếu xung đột",
   "dau_vao":"Quyết định có hiệu lực, lịch cập nhật, hai mã nhánh, nhật ký người làm/người kiểm",
   "dau_ra":"Một thông báo cho các bên; đối soát thời gian chờ, làm lại và nguyên nhân xung đột",
   "chuyen_buoc":"Giờ chuyên viên, giờ Tổ trưởng kiêm nhiệm và giờ "+T+" được ghi ba loại riêng; không tự cộng trùng"}
 ],
 "quy_tac_ket_thuc":"Chỉ đóng phiếu khi hai tổ đã xác nhận lịch, một người chủ trì mã việc được ghi, quyết định vượt quyền có chứng cứ; không được tự đánh dấu hoàn tất khi chưa có cá nhân và ủy quyền."
}
refs={
 "XT-01":["xung-dot-lich","hang-muc","quang-cao-tra-phi"],
 "XT-02":["xung-dot-lich","hang-muc-toan-he-thong"],
 "XT-03":["xung-dot-lich","website-app","quang-cao-tra-phi"],
 "XT-04":["xung-dot-lich","yeu-cau-gap","hang-muc"],
 "XT-05":["xung-dot-lich","vang-mat","ngoai-luong"],
 "XT-06":["bgd-coso-de-nghi","yeu-cau-le","xung-dot-lich"],
 "XT-07":["hang-muc","mua-sam","quang-cao-tra-phi"],
 "XT-08":["su-co-tai-khoan","danh-gia","yeu-cau-gap"],
 "XT-09":["vang-mat","nghi-viec","nhan-viec-moi"]
}
available={q["id"] for q in D["quy_trinh"]}
for case in D["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]["tinh_huong"]:
    case["quy_trinh_tham_chieu"]=refs[case["ma"]]
    if not set(case["quy_trinh_tham_chieu"])<=available:
        raise RuntimeError("Mã quy trình dẫn chiếu không tồn tại: "+case["ma"])
for q in D["quy_trinh"]:
    if q["id"]=="xung-dot-lich":
        q["nhanh_hai_to_cung_chuyen_vien_truong_2027"]=(
            "Khi xung đột chỉ giữa Tổ Truyền thông và Thương hiệu và Tổ Tăng trưởng số, "
            "người xử lý quản trị hai tổ là "+T+"; mã cvt trong bước gốc chỉ mô tả "
            "trường hợp tải sản xuất/cơ sở, không áp dụng mặc định sang hai tổ này. "
            "Nếu có tuyến Nội dung – Sáng tạo/cơ sở: "+N+" cùng đối chiếu, "
            "vượt quyền/bất đồng chuyển Trưởng phòng. "
            "Không sửa quyền duyệt phát hành hoặc chi phí."
        )
        for i,b in enumerate(q["buoc"],1):
            b["nhanh_hai_to_2027"]={
                "quy_trinh":"xung-dot-lich",
                "loai_xung_dot":"hai_to_tt_tts",
                "nguoi_quan_tri":"cvt-2",
                "pham_vi":"Hai tổ TCT; một mã việc và hai mã nhánh; không cấp quyền duyệt",
                "can_xac_nhan":"Phân loại xung đột và nhân sự theo văn bản có hiệu lực"
            }
            if i==3:
                b["phan_tuyen_chu_tri_theo_pham_vi_2027"]={
                    "hai_to_tct":"cvt-2",
                    "tai_san_xuat_va_marketing_co_so":"cvt",
                    "lien_tuyen_vuot_quyen":"tp",
                    "bat_buoc":"Chọn duy nhất một tuyến theo phạm vi xung đột; khóa nếu chưa rõ"
                }
    elif q["id"] in {"yeu-cau-gap","hang-muc","hang-muc-toan-he-thong",
                     "quang-cao-tra-phi","phat-thanh-man-hinh","vang-mat",
                     "nhan-viec-moi","chuyen-quyen","su-co-tai-khoan"}:
        q["lien_ket_nhanh_xung_dot_hai_to_2027"]=(
            "Nếu cùng cần ưu tiên nguồn lực của hai tổ Truyền thông và Thương hiệu, "
            "Tăng trưởng số: tham chiếu nhánh 6 bước thuộc QT xung-dot-lich; "
            "không tự phát sinh quy trình mới hoặc lệnh giao việc cho Marketing cơ sở."
        )
# 1d) Tên đơn vị Marketing bệnh viện phải gắn với tên cơ sở, không gọi
#     "Tổ Marketing chi nhánh" như tên một đơn vị chính thức.
#     Các tên dưới đây chỉ là nhãn cơ cấu đề án, không tạo thêm suất/đơn vị.
D["cnnv_ten_to_marketing_benh_vien_2027"]={
 "quy_tac":"Tổ Marketing + tên đầy đủ của bệnh viện; chỉ dùng cho bệnh viện có tổ Marketing trong cơ cấu được duyệt. Không dùng cho đầu mối kiêm nhiệm phòng khám, không tự thành lập tổ tại cơ sở dự kiến.",
 "danh_muc_dang_hoat_dong":[
  {"benh_vien":"Bệnh viện Đa khoa TTH Vinh","ten_to":"Tổ Marketing Bệnh viện Đa khoa TTH Vinh","nhom":"nhom_1"},
  {"benh_vien":"Bệnh viện Đa khoa TTH Hà Tĩnh","ten_to":"Tổ Marketing Bệnh viện Đa khoa TTH Hà Tĩnh","nhom":"nhom_1"},
  {"benh_vien":"Bệnh viện Đa khoa TTH Quảng Bình","ten_to":"Tổ Marketing Bệnh viện Đa khoa TTH Quảng Bình","nhom":"nhom_1"},
  {"benh_vien":"Bệnh viện Y học cổ truyền Nguyên Phúc","ten_to":"Tổ Marketing Bệnh viện Y học cổ truyền Nguyên Phúc","nhom":"nhom_2"},
  {"benh_vien":"Bệnh viện Răng hàm mặt và Phẫu thuật tạo hình thẩm mỹ Thái Thượng Hoàng","ten_to":"Tổ Marketing Bệnh viện Răng hàm mặt và Phẫu thuật tạo hình thẩm mỹ Thái Thượng Hoàng","nhom":"nhom_2"}
 ],
 "luu_y":"Tên tổ là nhãn chuẩn hóa theo bệnh viện, không khẳng định đã có quyết định thành lập tổ riêng tại mọi cơ sở. Quyền, định biên, người giữ chức danh phải đối chiếu văn bản nhân sự hiệu lực.",
 "quan_he":"Trưởng nhóm Marketing tại từng bệnh viện nhận một tuyến quản lý Marketing từ "+N+"; Ban Giám đốc bệnh viện phối hợp hai chiều về kế hoạch, nguồn dữ liệu, điều kiện thực địa và quản lý hành chính; "+T+" hướng dẫn nghiệp vụ truyền thông/số qua tuyến, không giao việc trực tiếp cho nhân viên."
}
# Tên đơn vị dùng chung cho JSON, sơ đồ, phụ lục và các trường tìm kiếm.
# Mã chức danh cơ sở (tn-a/tn-b...) là tên CHỨC DANH dùng tại nhiều bệnh viện,
# không ép thay bằng tên một đơn vị cụ thể.
canonical=D["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"]
unit_names={x["ten_to"].casefold():x for x in canonical}
hospital_counts=[3,3,3,2,2]
assert len(canonical)==5 and sum(hospital_counts)==13
D["cnnv_ten_to_marketing_benh_vien_2027"]["tong_so_suat_to_benh_vien"]=13
D["cnnv_ten_to_marketing_benh_vien_2027"]["suat_dau_moi_phong_kham"]=1
D["cnnv_ten_to_marketing_benh_vien_2027"]["tong_suat_marketing_co_so"]=14
D["cnnv_ten_to_marketing_benh_vien_2027"]["phan_biet"]="13 suất thuộc 05 Tổ Marketing bệnh viện; 01 suất đầu mối kiêm nhiệm phòng khám. Đây là suất cơ cấu đề xuất, không đồng nghĩa người thực có hoặc quyết định lập tổ đã có hiệu lực."
for x,n in zip(canonical,hospital_counts):
    x["suat_co_cau_de_xuat"]=n
    x["trang_thai_ten"]="Tên chuẩn hóa theo đề án, hiệu lực thành lập tổ theo văn bản riêng"
actual_units=[x for x in D["don_vi"] if x.get("loai")=="to_marketing_benh_vien"]
assert len(actual_units)==5
for unit in actual_units:
    key=unit["ten"].strip().casefold()
    if key not in unit_names:raise RuntimeError("Tên Tổ Marketing không khớp danh mục: "+unit["ten"])
    standard=unit_names[key]
    unit["ten"]=standard["ten_to"]
    unit["ten_chuan_de_an_2027"]=standard["ten_to"]
    unit["suat_co_cau_de_xuat"]=standard["suat_co_cau_de_xuat"]
    unit["trang_thai_ten"]=standard["trang_thai_ten"]
# 04 hướng dẫn đang dùng từ "Chuyên viên trưởng" chung. Việc kiểm chuẩn
# thuộc đúng tuyến; cấp phê duyệt/ban hành không được suy từ tên chức danh.
for item in D["bo_quy_chuan_da_dong_bo"]:
    code=item["ma"]
    if code=="Content":
        item["kiem"]=N+" kiểm chuẩn hệ thống nội dung; Biên tập khác người soạn kiểm độc lập; bác sĩ xác nhận mệnh đề y khoa."
    elif code=="QC-4":
        item["kiem"]=N+" kiểm chuẩn kỹ thuật sản xuất; Media khác người làm kiểm độc lập; bác sĩ/pháp lý xác nhận khi có yêu cầu."
    elif code=="Xuat-ban-nen-tang":
        item["kiem"]=T+" kiểm chuẩn nghiệp vụ kênh số, Quản lý sản phẩm số kiểm thông số triển khai; người làm không tự kiểm độc lập."
    elif code=="DS-3":
        item["kiem"]=T+" kiểm chuẩn tuân thủ và phiên bản; Quản lý sản phẩm số quản lý danh mục, cần người khác kiểm khi chính mình thực hiện."
    else:raise RuntimeError("Mã quy chuẩn ngoài bốn phạm vi đã đối chiếu: "+code)
    item["phe_duyet"]=(
      "Người có thẩm quyền theo văn bản phân quyền, ủy quyền còn hiệu lực; "
      "không mặc nhiên thuộc Trưởng phòng Marketing hoặc Chuyên viên trưởng. "
      "Chưa có ủy quyền hiệu lực thì CHỜ PHÊ DUYỆT."
    )
    item["trang_thai_2027"]="Ma trận đề xuất trách nhiệm xây dựng và kiểm chuẩn; không phải quyết định ban hành."
for rid in ("mdcs-a","mdcs-b","qhcs"):
    role=V[rid]
    role["bao_cao_cho"]=role["bao_cao_cho"].replace(
      "Tổ trưởng Marketing tại bệnh viện trực tiếp",
      "Trưởng nhóm Marketing cơ sở tại bệnh viện trực tiếp"
    )
for v in D["vi_tri"]:
    if v["id"] in ("tn-a","tn-b","qhcs"):
        v["ten_to_marketing_benh_vien_2027"]="Tên tổ theo danh mục bệnh viện cụ thể; không gọi chung 'Tổ Marketing chi nhánh'."
    if v["id"]=="dmpk":
        v["bao_cao_cho"]=v.get("bao_cao_cho","").replace(
          "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở/2",
          "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở và Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số theo từng phạm vi hướng dẫn nghiệp vụ; không tạo tuyến chỉ huy thứ hai"
        )
# 1e) Danh mục quy trình là hệ thống quản trị, KHÔNG phải việc một người
# soạn tất cả hoặc một cấp quản lý tự ký ban hành. Nguồn phân cấp:
# chức năng nhiệm vụ phòng (4.1), QyĐ.02.MKT/MTVC còn hiệu lực;
# tình trạng của 60 luồng trong đề án không đồng nghĩa 60 văn bản ban hành.
D["cnnv_quan_tri_danh_muc_quy_trinh_2027"]={
 "nguon_phan_cap":"Mục 4.1 và QyĐ.02.MKT/MTVC đang có hiệu lực; phân cấp khác phải có văn bản riêng",
 "trang_thai":"Quy tắc quản trị đề xuất trong Khung Marketing 2027; chưa tự thay thế thủ tục ban hành hiện hành",
 "danh_muc_luong_tham_chieu":[{"ma":q["id"],"ten":q["ten"],
   "trang_thai":"LUỒNG MÔ TẢ TRONG ĐỀ ÁN – CHƯA ĐỐI CHIẾU HIỆU LỰC VĂN BẢN"}
   for q in D["quy_trinh"]],
 "phan_cong":[
  {"vai_tro":"Quản lý thương hiệu theo nhóm","trach_nhiem":
   "Chỉ ra nhu cầu chuẩn hóa mục tiêu, thông điệp, kiến trúc thương hiệu và nghiệm thu hạng mục; đề xuất/sở hữu yêu cầu nghiệp vụ, góp ý dự thảo đúng thương hiệu",
   "khong_lam":"Không tự phê duyệt ban hành tất cả quy trình hoặc thay kiểm pháp lý"},
  {"vai_tro":"Tổ trưởng và Trưởng nhóm Marketing bệnh viện","trach_nhiem":
   "Tập hợp khó khăn, sáng kiến từ chuyên viên và cơ sở; cung cấp luồng thực tế, người làm, thời gian, đầu ra; tổ chức soạn/thử nghiệm theo phân công trong phạm vi mình",
   "khong_lam":"Không tự mở quyền điều động chéo nhóm, thay đổi quy trình có hiệu lực hay cấp quyền phát hành"},
  {"vai_tro":"Chuyên viên chuyên môn và đầu mối kiêm nhiệm","trach_nhiem":
   "Phát hiện công việc chưa có hướng dẫn hoặc quy trình không khả thi; đề xuất có ví dụ/chứng cứ; trực tiếp soạn nội dung kỹ thuật đúng nghiệp vụ khi được giao",
   "khong_lam":"Không tự quyết định chuẩn áp dụng toàn hệ thống hoặc tự kiểm độc lập tài liệu do mình soạn"},
  {"vai_tro":N,"trach_nhiem":
   "Lập, ưu tiên và quản trị danh mục quy trình Nội dung – Sáng tạo, sản xuất và Marketing cơ sở hai nhóm; kiểm chuẩn ranh giới giao việc, chất lượng, tải, biểu mẫu, điểm bàn giao",
   "khong_lam":"Không viết thay chuyên viên, không phân lịch hằng ngày cho nhóm 2/ngoại tuyến khi chưa được phân công, không tự ký ban hành"},
  {"vai_tro":T,"trach_nhiem":
   "Lập, ưu tiên và quản trị danh mục quy trình của Tổ Truyền thông và Thương hiệu và Tổ Tăng trưởng số; kiểm chuẩn PR, thương hiệu, OOH, quảng cáo, kênh số, đo lường và phối hợp hai tổ",
   "khong_lam":"Không tự làm thay chuyên viên, không giao việc trực tiếp Marketing cơ sở, không mặc nhiên phê duyệt phát hành/chi"},
  {"vai_tro":"Trưởng phòng Marketing","trach_nhiem":
   "Hợp nhất một danh mục của phòng, xác định mức ưu tiên, thời hạn, nguồn lực và MỘT đầu mối chủ trì mỗi quy trình liên tổ; chốt kế hoạch nội bộ trong thẩm quyền, trình cấp có quyền khi vượt quyền",
   "khong_lam":"Không được lấy việc chốt kế hoạch hoặc chủ trì xây dựng làm quyền ký ban hành ngoài phân cấp"},
  {"vai_tro":"Phòng Quản lý chất lượng và bộ phận có chức năng liên quan","trach_nhiem":
   "Tham gia chuẩn hóa thể thức, mã hiệu, quản lý phiên bản và kiểm soát hệ thống văn bản trong phạm vi được giao; Phòng Nhân lực đối chiếu MTCV/quyền và nhân sự khi thay đổi",
   "khong_lam":"Không tự nhận mọi quy trình Marketing là quy trình đã ban hành chỉ vì được đưa vào danh mục"},
  {"vai_tro":"Người/cấp có thẩm quyền ban hành","trach_nhiem":
   "Phê duyệt, ký ban hành hoặc cho áp dụng sau khi hồ sơ thẩm định đầy đủ, đúng quyết định phân quyền hiệu lực; quyền chi phí và phát hành sản phẩm được xét riêng",
   "khong_lam":"Không suy ra người ký từ tên vị trí hoặc từ quyền kiểm chuẩn"},
 ],
 "chu_trinh":[
  {"buoc":1,"ten":"Tiếp nhận đề xuất","dau_moi":"Đúng chức danh chuyên môn/Tổ trưởng/Trưởng nhóm cơ sở",
   "dau_ra":"Mã đề xuất, vấn đề, bằng chứng lỗi/thiếu, quy trình liên quan, người gửi"},
  {"buoc":2,"ten":"Đối chiếu quy trình hiện hữu","dau_moi":N+" hoặc "+T+" theo phạm vi",
   "dau_ra":"Phân loại xây mới, sửa, gộp, bãi bỏ; tra 60 luồng mẫu và danh mục văn bản có hiệu lực; không tạo trùng"},
  {"buoc":3,"ten":"Lập danh mục và ưu tiên","dau_moi":N+" hoặc "+T+" theo phạm vi; Trưởng phòng hợp nhất",
   "dau_ra":"Một danh mục cấp phòng với mức rủi ro, người chủ trì duy nhất, hạn và kế hoạch nội bộ được xác nhận đúng quyền"},
  {"buoc":4,"ten":"Soạn dự thảo nghiệp vụ","dau_moi":"Người sở hữu nghiệp vụ/chuyên viên được giao; Tổ trưởng điều phối trong phạm vi",
   "dau_ra":"Sơ đồ bước, đầu vào/đầu ra, kiểm độc lập, biểu mẫu, điểm chặn, ngoại lệ và hồ sơ phiên bản"},
  {"buoc":5,"ten":"Kiểm chuẩn, đối chiếu pháp lý và thử nghiệm","dau_moi":N+" hoặc "+T+" theo phạm vi; liên tổ Trưởng phòng chỉ định một người tổng hợp",
   "dau_ra":"Biên bản kiểm chuẩn, ý kiến Quản lý thương hiệu, y khoa/pháp lý nếu áp dụng, thử nghiệm và xử lý phản biện"},
  {"buoc":6,"ten":"Trình duyệt và ban hành","dau_moi":"Trưởng phòng tổ chức trình; người có thẩm quyền quyết định theo văn bản còn hiệu lực",
   "dau_ra":"Mã văn bản, người ký, ngày hiệu lực, phạm vi áp dụng, phiên bản; thiếu ủy quyền thì CHỜ PHÊ DUYỆT"},
  {"buoc":7,"ten":"Triển khai, đo và rà soát","dau_moi":"Tổ trưởng/Trưởng nhóm triển khai; "+N+" hoặc "+T+" kiểm chuẩn theo phạm vi",
   "dau_ra":"Biên bản phổ biến, nhật ký tuân thủ, KPI, đề xuất phiên bản mới, lịch rà soát"}
 ],
 "truong_danh_muc":[
  "Mã quy trình","Tên quy trình","Nhóm thương hiệu/cơ sở áp dụng",
  "Loại xây mới/sửa/gộp/bãi bỏ","Sự cố hoặc nhu cầu và chứng cứ",
  "Chủ sở hữu nghiệp vụ","Một người chủ trì xây dựng","Người trực tiếp soạn",
  "Người phối hợp và kiểm độc lập","Người kiểm chuẩn theo tuyến",
  "Bộ phận y khoa/pháp lý phải xác nhận nếu áp dụng",
  "Người có quyền ban hành theo căn cứ","Thẩm quyền/ủy quyền hiệu lực",
  "Mức ưu tiên và rủi ro","Hạn hoàn thành và nguồn lực",
  "Biểu mẫu liên quan","Phiên bản và ngày hiệu lực",
  "Trạng thái bản thảo/đang kiểm/chờ duyệt/có hiệu lực/bãi bỏ",
  "Mã thay thế/quan hệ với quy trình khác","Kỳ rà soát và bằng chứng áp dụng"
 ],
 "quy_tac_chong_xung_dot":"Một quy trình liên tổ chỉ có một chủ trì xây dựng do Trưởng phòng chỉ định; hai chức danh quản lý kiểm chuẩn theo phạm vi. Việc thay đổi tải và ưu tiên qua tuyến được giao, không sinh hai lệnh hoặc hai phiếu kiểm cùng nội dung.",
 "dieu_kien_chan":"Thiếu người chủ trì, người kiểm độc lập khi phải kiểm, căn cứ pháp lý/y khoa, văn bản ủy quyền hoặc người ký có thẩm quyền: CHỜ BỔ SUNG/CHỜ PHÊ DUYỆT; không áp dụng bản dự thảo như quy trình hiệu lực.",
 "chu_ky":"Nhận đề xuất liên tục; rà soát danh mục tại giao ban tháng và đánh giá nhu cầu sửa đổi theo quý hoặc khi xảy ra sự cố/đổi pháp luật; đây là chu kỳ kế hoạch đề xuất, chưa phải chỉ đạo đã ban hành.",
 "phan_biet":"60 luồng/407 bước trong Khung 2027 là dữ liệu đề án; số quy trình đã ban hành phải đối chiếu 83 văn bản và quyết định có hiệu lực, không mặc nhiên bằng 60."
}
# Quyền tham gia của 26 mã chức danh: được báo cáo thiếu chuẩn; chủ trì soạn
# chỉ khi có chỉ định. Nhóm chuyên môn là lĩnh vực phát hiện nhu cầu, KHÔNG
# là giấy phép ký ban hành hoặc mở một tuyến giao việc thứ hai.
process_domains={
 "tp":"Danh mục và kế hoạch toàn Phòng Marketing",
 "cvt":"Nội dung – Sáng tạo, Media/Thiết kế và Marketing cơ sở hai nhóm",
 "cvt-2":"Truyền thông – Thương hiệu và Tăng trưởng số hai tổ tại Tổng công ty",
 "qlth-a":"Mục tiêu, định vị, thông điệp và nghiệm thu thương hiệu nhóm 1",
 "qlth-bc":"Mục tiêu, định vị, thông điệp và nghiệm thu thương hiệu nhóm 2; điều phối Tổ Truyền thông và Thương hiệu khi được phân công",
 "cvtt-a":"Báo chí, PR, OOH, phát thanh, màn hình và thông tin nhóm 1",
 "cvtt-bc":"Báo chí, PR, OOH, phát thanh, màn hình và thông tin nhóm 2",
 "bt-ac":"Biên tập, kịch bản, chuẩn nguồn và quy tắc kiểm nội dung nhóm 1; điều phối Tổ Nội dung và Sáng tạo theo phạm vi kiêm nhiệm",
 "bt-b":"Biên tập, kịch bản và chuẩn nguồn nhóm 2",
 "tk-a":"Thiết kế và quy chuẩn ứng dụng nhận diện nhóm 1",
 "tk-b":"Thiết kế và quy chuẩn ứng dụng nhận diện nhóm 2",
 "tk-nt":"File in, OOH và kỹ thuật thiết kế ngoại tuyến",
 "md-ac":"Quay, chụp, hậu kỳ, lưu trữ tư liệu media nhóm 1",
 "md-b":"Quay, chụp, hậu kỳ, lưu trữ tư liệu media nhóm 2",
 "qc-a":"Quảng cáo và vận hành kênh số nhóm 1",
 "qc-b":"Quảng cáo và vận hành kênh số nhóm 2",
 "dl-1":"Đo lường, đối soát, nguồn số liệu và KPI",
 "dl-2":"Dữ liệu khách hàng, thị trường, bảo vệ dữ liệu thuộc phạm vi phụ trách",
 "qlsps":"Nghiệp vụ sản phẩm số, trang đích, bàn giao kỹ thuật và điều phối Tổ Tăng trưởng số khi được phân công",
 "qlml":"Mạng lưới Marketing theo vùng – vị trí dự kiến, không tự có quyền quản lý hoặc xây dựng quy trình",
 "tn-a":"Luồng phối hợp, báo cáo và tác nghiệp Tổ Marketing bệnh viện nhóm 1",
 "tn-b":"Luồng phối hợp, báo cáo và tác nghiệp Tổ Marketing bệnh viện nhóm 2",
 "mdcs-a":"Quay, chụp, dựng tại bệnh viện nhóm 1 và bàn giao Media Tổng công ty",
 "mdcs-b":"Quay, chụp, dựng tại bệnh viện nhóm 2 và bàn giao Media Tổng công ty",
 "qhcs":"Truyền thông, OOH, phát thanh, màn hình, quan hệ đối tác tại bệnh viện",
 "dmpk":"Yêu cầu kiêm nhiệm tại phòng khám, phối hợp theo tuyến Marketing được chỉ định"
}
assert set(process_domains)==set(V)
for v in D["vi_tri"]:
    rid=v["id"]
    v["cnnv_quan_tri_quy_trinh_2027"]={
      "pham_vi_phat_hien_de_xuat":process_domains[rid],
      "quyen_de_xuat":"Ghi nhận khoảng trống và đề xuất sửa/xây/gộp/bãi bỏ kèm ví dụ, chứng cứ trong phạm vi chuyên môn",
      "dieu_kien_chu_tri_soan":"Chỉ khi được giao một mã quy trình, phạm vi và thời hạn; chịu trách nhiệm bản thảo chuyên môn đúng lĩnh vực",
      "kiem_chuan_va_ban_hanh":"Theo hai tuyến quản lý tại mục 4.1; người quản trị kiểm chuẩn không tự mặc nhiên có quyền ký ban hành",
      "hieu_luc":"MTCV 2027 đang đề xuất; nhiệm vụ và quyền nhân sự chính thức theo quyết định còn hiệu lực"
    }
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
      "dieu_phoi_theo_phan_cong":v.get("dieu_phoi_theo_phan_cong_2027",""),
      "quan_tri_danh_muc_quy_trinh":v["cnnv_quan_tri_quy_trinh_2027"],
      "tai_quan_tri_theo_nguon":D["cnnv_tai_hai_chuc_danh_2027"] if v["id"] in ("cvt","cvt-2") else {},
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

# 5) Quyết định có hiệu lực là văn bản gốc, không được sửa câu chữ của
#    quyết định chưa được Phòng Nhân lực/cấp thẩm quyền ban hành bản thay thế.
for doc in D["danh_muc_van_ban"]:
    if doc.get("ma")=="QyĐ.02.MKT" and isinstance(doc.get("dieu_khoan"),list):
        proposal=[
          x.replace("Tổ Truyền thông và Thương hiệu không đặt Tổ trưởng",
            "ĐỀ XUẤT 2027: Tổ Truyền thông và Thương hiệu có Tổ trưởng kiêm nhiệm là Quản lý thương hiệu nhóm 2, chỉ điều phối việc và không có quyền duyệt mặc định")
          for x in doc["dieu_khoan"]
        ]
        if proposal != doc["dieu_khoan"]:
            doc["cnnv_dieu_khoan_de_xuat_2027"]=proposal
        doc["cnnv_van_ban_goc_giu_nguyen_2027"]=True
        doc["cnnv_trang_thai_de_xuat_2027"]="CHƯA BAN HÀNH; không thay đổi quyết định hiện hành hoặc tự kích hoạt quyền kiêm nhiệm"
        doc["cnnv_yeu_cau_dong_bo"]="Phòng Nhân lực và cấp có thẩm quyền đối chiếu CNNV, quyết định có hiệu lực trước khi ban hành bản sửa."
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
    perf_html=""
    if role=="cvt-2":
        sectors=[]
        for item in D["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]["pham_vi"]:
            metrics="".join("<li>"+escape(metric)+"</li>" for metric in item["chi_so"])
            sectors.append(
                '<section style="flex:1 1 280px;min-width:0;max-width:100%;border:1px solid #d7e2ef;'
                'border-radius:8px;padding:10px;box-sizing:border-box;background:#fff">'
                '<strong style="color:#0837A1">'+escape(item["to"])+'</strong>'
                '<ul style="padding-left:20px;margin:7px 0;overflow-wrap:anywhere">'+metrics+'</ul>'
                '<p style="margin:8px 0"><b>Đầu ra cải tiến:</b> '+escape(item["dau_ra_cai_tien"])+'</p>'
                '<p style="margin:8px 0"><b>Nguồn kiểm chứng:</b> '+escape(item["chu_nguon_so_lieu"])+'</p>'
                '</section>'
            )
        perf_html=(
            '<details id="cvt-2-perf-metrics-2027" style="max-width:100%;min-width:0;'
            'box-sizing:border-box;border:1px solid #d7e2ef;border-radius:8px;padding:10px;margin:10px 0;background:#fff">'
            '<summary style="cursor:pointer;color:#0837A1;font-weight:700">Chỉ số và đầu ra cải tiến hiệu suất của hai tổ</summary>'
            '<div style="display:flex;flex-wrap:wrap;gap:10px;margin:12px 0">'+''.join(sectors)+'</div>'
            '<p><b>Điều kiện chốt chỉ tiêu:</b> '+escape(D["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]["dieu_kien"])+'</p>'
            '</details>'
        )
    note=(
      '<div class="cnnv-vt" id="cnnv-vt-'+role+'" '
      'style="background:#f5f9ff;border:1px solid #d3e1f2;border-left:4px solid #0837A1;'
      'border-radius:8px;padding:12px;margin:10px 0;max-width:100%;overflow-wrap:anywhere">'
      '<strong style="display:block;color:#0837A1;margin-bottom:8px">CNNV – chức năng, nhiệm vụ và ranh giới trách nhiệm</strong>'
      '<p><b>Chức năng:</b> '+escape(x["muc_dich"])+'</p>'
      '<p><b>Đầu ra chịu trách nhiệm:</b> '+escape(x["phan_dinh_chu_tri_dau_ra"])+'</p>'
      '<p><b>Bàn giao và phối hợp:</b> '+escape(x["phan_dinh_ban_giao_dau_vao"])+'</p>'
      '<p><b>Thẩm quyền:</b> '+escape(x["phan_dinh_kiem_duyet"])+'</p>'
      '<p><b>Đề xuất và xây dựng quy trình:</b> '+escape(x["cnnv_quan_tri_quy_trinh_2027"]["pham_vi_phat_hien_de_xuat"])+
      '; '+escape(x["cnnv_quan_tri_quy_trinh_2027"]["dieu_kien_chu_tri_soan"])+
      '; '+escape(x["cnnv_quan_tri_quy_trinh_2027"]["kiem_chuan_va_ban_hanh"])+"</p>"
      +('<p><b>Tối ưu hiệu suất hai tổ:</b> '+escape(x["toi_uu_hieu_suat"])+'</p>'
      '<p><b>Chu trình cải tiến và trách nhiệm:</b> '+escape(x["chu_trinh_cai_tien"])+'</p>'
      '<p><b>Ranh giới trách nhiệm và KPI:</b> '+escape(x["ranh_gioi_kpi"])+'</p>'
      if role=="cvt-2" else '')
      +perf_html
      +'<small>Đối chiếu với CNNV phòng tại mục 4.1. Chưa thay văn bản MTCV do Phòng Nhân lực ban hành.</small>'
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

# Mục 4.1 là căn cứ chức năng nhiệm vụ của Phòng, hiển thị danh mục
# quy trình và trách nhiệm, tránh đặt một thủ tục mới bên ngoài cơ cấu.
govern=D["cnnv_quan_tri_danh_muc_quy_trinh_2027"]
if 'id="cnnv-quan-tri-danh-muc-quy-trinh-2027"' not in s:
    mark=re.search(
      r'(<section class="doc-sec sub" data-title="4\.1\. Chức năng, nhiệm vụ, quyền hạn của Phòng Marketing" id="m-4-1">[\s\S]*?</h3>)',
      s
    )
    if not mark:raise RuntimeError("Không tìm thấy mục 4.1 để chèn quản trị danh mục quy trình")
    rows=''.join('<tr><td>'+escape(z["vai_tro"])+'</td><td>'+
                 escape(z["trach_nhiem"])+'</td><td>'+escape(z["khong_lam"])+
                 '</td></tr>' for z in govern["phan_cong"])
    gates=''.join('<tr><td>'+str(z["buoc"])+'</td><td>'+
                  escape(z["ten"])+'</td><td>'+escape(z["dau_moi"])+
                  '</td><td>'+escape(z["dau_ra"])+'</td></tr>'
                  for z in govern["chu_trinh"])
    cols=''.join('<li>'+escape(z)+'</li>' for z in govern["truong_danh_muc"])
    panel=(
      '<details id="cnnv-quan-tri-danh-muc-quy-trinh-2027" '
      'style="max-width:100%;min-width:0;margin:12px 0;padding:12px;'
      'box-sizing:border-box;border:1px solid #d7e2ef;border-radius:8px;overflow-wrap:anywhere">'
      '<summary style="cursor:pointer;font-weight:700;color:#0837A1">'
      'Quản trị danh mục quy trình: đề xuất – soạn thảo – kiểm chuẩn – ban hành</summary>'
      '<p>'+escape(govern["nguon_phan_cap"])+'</p>'
      '<p><b>Nguyên tắc:</b> '+escape(govern["phan_biet"])+'</p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto">'
      '<table class="t" style="min-width:960px;table-layout:auto">'
      '<thead><tr><th>Vị trí/đơn vị</th><th>Trách nhiệm</th><th>Không thuộc quyền mặc định</th></tr></thead>'
      '<tbody>'+rows+'</tbody></table></div>'
      '<p><b>Trình tự quản lý danh mục:</b></p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto">'
      '<table class="t" style="min-width:960px;table-layout:auto">'
      '<thead><tr><th>Bước</th><th>Công việc</th><th>Chủ trì</th><th>Đầu ra</th></tr></thead>'
      '<tbody>'+gates+'</tbody></table></div>'
      '<details style="max-width:100%;min-width:0"><summary style="cursor:pointer">'
      'Các trường bắt buộc của danh mục quy trình</summary><ul style="padding-left:20px">'+cols+'</ul></details>'
      '<p><b>Chống xung đột:</b> '+escape(govern["quy_tac_chong_xung_dot"])+'</p>'
      '<p><b>Điều kiện chặn:</b> '+escape(govern["dieu_kien_chan"])+'</p>'
      '<p><b>Chu kỳ rà soát:</b> '+escape(govern["chu_ky"])+'</p>'
      '<p class="mini">'+escape(govern["trang_thai"])+'</p></details>'
    )
    s=s[:mark.end()]+panel+s[mark.end():]

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
    # Nêu rõ trạng thái đề xuất và các điểm khóa; không biến đề án thành quyết định ủy quyền.
    gate=D["cnnv_dieu_phoi_ngoai_tuyen_2027"]
    load=D["cnnv_tai_hai_chuc_danh_2027"]
    panel+=(
      '<details id="cnnv-dieu-phoi-ngoai-tuyen-2027" style="border:1px solid #d7e2ef;'
      'padding:10px;border-radius:8px;margin:10px 0;max-width:100%;overflow-wrap:anywhere">'
      '<summary style="cursor:pointer;font-weight:700">Điều phối nhóm 2 và Thiết kế ngoại tuyến – điều kiện có hiệu lực</summary>'
      '<p>'+escape(gate["trang_thai"])+'</p>'
      '<p><b>Xác lập đầu mối:</b> '+escape(gate["xac_lap_dau_moi"])+'</p>'
      '<p><b>Quy tắc chặn:</b> '+escape(gate["khoa"])+'</p>'
      '<p><b>Xử lý xung đột:</b> '+escape(gate["giai_quyet_xung_dot"])+'</p>'
      '</details>'
      '<details id="cnnv-tai-hai-chuc-danh-2027" style="border:1px solid #d7e2ef;'
      'padding:10px;border-radius:8px;margin:10px 0;max-width:100%;overflow-wrap:anywhere">'
      '<summary style="cursor:pointer;font-weight:700">Tải và KPI quản trị hai chức danh – chưa kết luận đủ tải</summary>'
      '<p>'+escape(load["trang_thai"])+'</p><p><b>Công thức:</b> '+escape(load["cong_thuc"])+'</p>'
      '<p><b>Phân loại dữ liệu:</b> '+escape(load["phan_loai_nguon"])+'</p>'
      '<p><b>Ngưỡng cảnh báo đề xuất:</b> '+escape(load["nguong_canh_bao_de_xuat"])+'</p>'
      '</details>'
    )
    s=s.replace(anchor,panel+anchor,1)

# Chèn giải thích cơ cấu hai tuyến trong đúng mục 4.3, không thêm màn hình.
# Bảng "Vì sao tách" so sánh mô hình tổ, chưa đủ chứng minh hiệu quả của
# một người quản lý hai tổ: bổ sung cơ chế điều phối và xử lý ngoại lệ.
model=D["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]
if 'id="cnnv-2-chief-3-team-2027"' not in s:
    marker=re.search(
      r'(<section class="doc-sec sub" data-title="4\.3\. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
      r'[\s\S]*?</h3>)',s
    )
    if not marker:raise RuntimeError("Không tìm thấy đúng phần 4.3 để giải thích hai tuyến quản lý")
    rows=''.join(
      '<tr><td>'+escape(z["rui_ro"])+'</td><td>'+escape(z["dau_moi"])+'</td>'
      '<td>'+escape(z["quyet_dinh"])+'</td><td>'+escape(z["quy_tac_chan"])+'</td></tr>'
      for z in model["tinh_huong"]
    )
    note=(
      '<div id="cnnv-2-chief-3-team-2027" style="max-width:100%;min-width:0;'
      'margin:12px 0;padding:12px;border-left:4px solid #0837A1;'
      'background:#f5f8fc;border-radius:6px;box-sizing:border-box;overflow-wrap:anywhere">'
      '<strong style="display:block;color:#0837A1">Ba tổ chuyên môn, hai chức danh quản lý – không phải ba cấp duyệt</strong>'
      '<p>'+escape(model["mo_hinh"])+'</p>'
      '<p><b>Phân công và cải tiến hiệu suất:</b> '+escape(model["phan_biet"])+'</p>'
      '<p><b>Luồng hạng mục:</b> '+escape(model["giao_dien_hang_muc"])+'</p>'
      '<p><b>Giải quyết xung đột hai tổ:</b> '+escape(model["tranh_chap_hai_to"])+'</p>'
      '<p><b>Giải quyết xung đột liên tuyến:</b> '+escape(model["tranh_chap_lien_tuyen"])+'</p>'
      '<p><b>Kiểm, nghiệm thu và duyệt:</b> '+escape(model["chuoi_kiem_soat"])+'</p>'
      '<details style="max-width:100%;min-width:0">'
      '<summary style="font-weight:700;color:#0837A1;cursor:pointer">Ma trận 9 tình huống xung đột và quy tắc chặn</summary>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto;margin-top:10px">'
      '<table class="t" style="min-width:960px;table-layout:auto">'
      '<thead><tr><th>Xung đột</th><th>Đầu mối thường lệ</th><th>Người giải quyết</th><th>Quy tắc chặn</th></tr></thead>'
      '<tbody>'+rows+'</tbody></table></div></details>'
      '<p class="mini">'+escape(model["nguon"])+'</p></div>'
    )
    s=s[:marker.end()]+note+s[marker.end():]

# Nhánh sáu bước của QT xung-dot-lich có trình tự, điều kiện chặn
# và điểm chuyển cấp, không hiển thị như một quy trình thứ 61.
branch=D["cnnv_nhanh_xung_dot_hai_to_2027"]
if 'id="cnnv-six-step-conflict-2027"' not in s:
    marker=re.search(
      r'(<section class="doc-sec sub" data-title="4\.3\. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
      r'[\s\S]*?</h3>)',s)
    if not marker:raise RuntimeError("Không tìm được mục 4.3 để hiển thị nhánh xung đột")
    rows=''.join(
      '<tr><td>'+str(z["so"])+'</td><td>'+escape(z["ten"])+'</td>'
      '<td>'+escape(z["chu_tri"])+'</td><td>'+escape(z["dau_ra"])+'</td>'
      '<td>'+escape(z["chuyen_buoc"])+'</td></tr>'
      for z in branch["buoc"]
    )
    block=(
      '<details id="cnnv-six-step-conflict-2027" style="margin:12px 0;'
      'max-width:100%;min-width:0;overflow-wrap:anywhere;border:1px solid #d7e2ef;'
      'padding:10px;border-radius:8px">'
      '<summary style="cursor:pointer;font-weight:700;color:#0837A1">'
      'Nhánh 6 bước xử lý xung đột hai tổ (thuộc quy trình hiện có)</summary>'
      '<p>'+escape(branch["trang_thai"])+'</p>'
      '<p><b>Điều kiện kích hoạt:</b> '+escape(branch["dieu_kien_kich_hoat"])+'</p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto">'
      '<table class="t" style="min-width:940px;table-layout:auto"><thead>'
      '<tr><th>Bước</th><th>Công việc</th><th>Đầu mối</th><th>Kết quả</th><th>Điều kiện chặn</th></tr>'
      '</thead><tbody>'+rows+'</tbody></table></div>'
      '<p>'+escape(branch["quy_tac_ket_thuc"])+'</p>'
      '<p class="mini">Tuyến xử lý thuộc QT xung-dot-lich; không thêm biên chế, '
      'không thêm cấp duyệt, không thay quyết định hiện hành.</p></details>'
    )
    s=s[:marker.end()]+block+s[marker.end():]

# Tên tổ cơ sở theo từng bệnh viện: chỉ chèn tại phần cơ cấu, không
# sửa dữ liệu lịch sử hay văn bản đã ban hành.
if 'id="cnnv-ten-to-marketing-benh-vien-2027"' not in s:
    marker=re.search(
      r'(<section class="doc-sec sub" data-title="4\.3\. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
      r'[\s\S]*?</h3>)',s
    )
    if not marker:raise RuntimeError("Thiếu mục 4.3 cho bảng tên Tổ Marketing bệnh viện")
    naming=D["cnnv_ten_to_marketing_benh_vien_2027"]
    rows=''.join(
      '<tr><td>'+escape(x["benh_vien"])+'</td><td><strong>'+escape(x["ten_to"])+
      '</strong></td></tr>'
      for x in naming["danh_muc_dang_hoat_dong"]
    )
    box=(
      '<div id="cnnv-ten-to-marketing-benh-vien-2027" style="max-width:100%;'
      'min-width:0;margin:12px 0;overflow-wrap:anywhere">'
      '<h4 style="color:#0837A1">Tên gọi Tổ Marketing tại từng bệnh viện</h4>'
      '<p>'+escape(naming["quy_tac"])+'</p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto">'
      '<table class="t" style="min-width:650px;table-layout:auto">'
      '<thead><tr><th>Bệnh viện</th><th>Tên tổ Marketing theo cơ sở</th></tr></thead>'
      '<tbody>'+rows+'</tbody></table></div>'
      '<p class="mini">'+escape(naming["luu_y"])+'</p>'
      '<p>'+escape(naming["quan_he"])+'</p></div>'
    )
    s=s[:marker.end()]+box+s[marker.end():]

# 6a) Đồng bộ TÊN HIỂN THỊ trực tiếp trong sơ đồ Bộ máy: bảng tên chuẩn
# trước đây chỉ bổ sung phụ lục, trong khi 05 nhãn ô bệnh viện chưa đổi.
# Thay đúng tên đơn vị, giữ nguyên số suất 03/03/03/02/02, mọi nút nhân sự,
# dữ liệu gốc và đầu mối phòng khám (không mặc định lập Tổ phòng khám).
name_catalog=D["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"]
assert len(name_catalog)==5 and sum((3,3,3,2,2))==13
for unit in name_catalog:
    old=unit["benh_vien"]
    new=unit["ten_to"]
    assert new=="Tổ Marketing "+old
    pat=r'(<div class="hosp-h">)'+re.escape(old)+r'(\s*<b>\(\d+\)</b></div>)'
    s,count=re.subn(pat,lambda m:m.group(1)+escape(new)+m.group(2),s,count=1)
    if count!=1:raise RuntimeError("Không tìm thấy tiêu đề ô bệnh viện cần đổi: "+old)
    # Thẻ là nhãn đơn vị, không thay tên chức danh tại các nút bấm.
assert len(re.findall(r'<div class="hosp-h">Tổ Marketing Bệnh viện [^<]+<b>\(\d+\)</b></div>',s))==5
old_group='<strong>Marketing cơ sở và đầu mối phòng khám</strong>'
new_group='<strong>Tổ Marketing tại các bệnh viện và đầu mối phòng khám</strong>'
if s.count(old_group)!=1:raise RuntimeError("Không tìm thấy duy nhất tiêu đề khu vực Marketing cơ sở")
s=s.replace(old_group,new_group,1)
old_summary='<summary>Marketing cơ sở <b>(13)</b>'
new_summary='<summary>Các Tổ Marketing tại bệnh viện <b>(13)</b>'
if s.count(old_summary)!=1:raise RuntimeError("Không tìm thấy duy nhất tiêu đề nhóm 13 suất bệnh viện")
s=s.replace(old_summary,new_summary,1)

# 6a.1) Đối chiếu biểu mẫu các phần 4/8 với sơ đồ, ma trận đơn vị,
# tránh 14 suất bệnh viện trong khi sơ đồ có 13 và 01 đầu mối phòng khám.
s=s.replace(
    "Bộ máy Marketing toàn TTH Group: 36 suất (22 TCT + 14 bệnh viện)",
    "Bộ máy Marketing toàn TTH Group: 36 suất (22 Tổng công ty + 14 cơ sở)"
)
s=s.replace(
    "<span>Tổ Marketing tại 5 bệnh viện</span>",
    "<span>13 suất tại 5 Tổ Marketing bệnh viện và 01 đầu mối phòng khám</span>"
)
note=re.compile(r'(<section class="doc-sec" data-title="8\. Marketing cơ sở" id="m-8">[\s\S]*?)(<p class="acceptance-note"><strong>Các tổ theo đơn vị:</strong>[\s\S]*?</p>)')
def fix_section8(m):
    cnv=D["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"]
    labels=", ".join(escape(v["ten_to"])+" ("+str(v["suat_co_cau_de_xuat"]).zfill(2)+")" for v in cnv)
    return m.group(1)+'<p class="acceptance-note"><strong>Tổ Marketing theo tên bệnh viện:</strong> '+labels+'. <strong>Định biên mục tiêu: 13 suất tại 05 tổ bệnh viện + 01 suất đầu mối kiêm nhiệm phòng khám = 14 suất Marketing cơ sở.</strong> Phòng khám thuộc nhóm 1, không mặc nhiên có Tổ Marketing riêng; tên đơn vị và nhân sự thực tế theo quyết định có hiệu lực.</p>'
s,num_section8=note.subn(fix_section8,s,count=1)
if num_section8!=1:raise RuntimeError("Không thể sửa phần 8 về 13 tổ bệnh viện + 1 phòng khám")
duplicate=N+" Nội dung – Sáng tạo và Marketing cơ sở"
if duplicate in s:s=s.replace(duplicate,N)
if duplicate in s:raise RuntimeError("Còn tên chuyên viên trưởng lặp sau chuẩn hóa")
# 6b) Đồng bộ văn bản sơ đồ HTML tĩnh với dữ liệu MTCV/cơ chế phân việc:
#     thông tin JSON đúng nhưng popup/tóm tắt cũ cũng phải cùng một tuyến.
for rid in ("bt-ac","bt-b","tk-b","md-b","tk-nt","dmpk"):
    label=escape(V[rid]["bao_cao_cho"])
    patt=re.compile(
        r'(<button\b[^>]*\bdata-jd="'+re.escape(rid)+r'"[^>]*>'
        r'(?:(?!</button>)[\s\S])*?<i>Báo cáo cho: </i>)([^<]*)(</span>)'
    )
    s,n=patt.subn(lambda m:m.group(1)+label+m.group(3),s,count=1)
    if n!=1:raise RuntimeError("Không đồng bộ được nhãn Báo cáo cho ở Bộ máy: "+rid)
legacy_load=("≈ 90–96 giờ/tháng có phần mềm (ước tính; gồm ≈ 13 giờ điều phối "
             "người nhóm 2, Chuyên viên thiết kế ngoại tuyến của Tổ Nội dung và Sáng tạo)")
new_load=("Tải quản trị: CHƯA ĐỦ GIỜ THỰC ĐO; không sử dụng ước tính 90–96 "
          "giờ/tháng hoặc 13 giờ điều phối nhóm 2/ngoại tuyến của phương án cũ "
          "để kết luận đủ tải.")
if legacy_load in s:s=s.replace(legacy_load,escape(new_load),1)
else:print("CNNV NOTE: tải ước tính tĩnh ở sơ đồ đã được thay trước đó")
org_title=re.compile(
 r'(<summary>Tổ Nội dung và Sáng tạo \(10\)<small>)([\s\S]*?)(</small></summary>)'
)
summary=("Tổ trưởng kiêm nhiệm chỉ điều phối nhóm 1 trong phạm vi được giao; "
         "nhóm 2 và Thiết kế ngoại tuyến qua đầu mối điều phối có phân công hiệu lực; "
         +N+" quản lý nghiệp vụ, không phân lịch thường lệ.")
s,n=org_title.subn(lambda m:m.group(1)+escape(summary)+m.group(3),s,count=1)
if n!=1:raise RuntimeError("Không tìm được mô tả Tổ Nội dung và Sáng tạo trong sơ đồ")

# 7) Chỉnh riêng sơ đồ Bộ máy: hai chức danh quản lý ở hàng trên,
#    ba tổ ở hàng dưới sử dụng ba cột. Không tái cấu trúc dữ liệu/nhân sự.
# DOM gốc: org-left > col > (col-h, col-b) và
# org-right > (mkt-org-cvt-2, org-right-teams > col + col).
chart_css=r"""
<style id="cnnv-org-three-team-columns-2027">
@media (min-width:1151px){
 #v-org .org-cols{
  display:grid!important;
  grid-template-columns:repeat(6,minmax(0,1fr))!important;
  grid-template-rows:auto auto!important;
  grid-auto-flow:row!important;
  align-items:start!important;
  column-gap:12px!important;
  row-gap:14px!important;
 }
 #v-org .org-cols>.org-left,#v-org .org-cols>.org-right,
 #v-org .org-cols>.org-left>.col{display:contents!important}
 #v-org .org-cols>.org-left>.col>.col-h{
  grid-column:1 / span 3!important;grid-row:1!important;
  min-width:0!important;width:100%!important;
 }
 #v-org .org-cols>.org-right>.mkt-org-cvt-2{
  grid-column:4 / span 3!important;grid-row:1!important;
  min-width:0!important;width:100%!important;
 }
 #v-org .org-cols>.org-left>.col>.col-b{
  grid-column:1 / span 2!important;grid-row:2!important;
  min-width:0!important;width:100%!important;
  align-self:start!important;
 }
 #v-org .org-cols>.org-right>.org-right-teams{
  grid-column:3 / span 4!important;grid-row:2!important;
  display:grid!important;
  grid-template-columns:repeat(2,minmax(0,1fr))!important;
  grid-template-rows:auto!important;
  gap:12px!important;min-width:0!important;width:100%!important;
  align-items:start!important;
 }
 #v-org .org-cols>.org-right>.org-right-teams>.col{
  grid-column:auto!important;grid-row:1!important;
  min-width:0!important;width:100%!important;
 }
}
#v-org .org-cols .col-b,#v-org .org-cols .pos,
#v-org .org-cols .col-h,#v-org .org-cols .org-right-teams{
 box-sizing:border-box!important;min-width:0!important;
 max-width:100%!important;overflow-wrap:anywhere!important;
}
@media(max-width:1150px){
 #v-org .org-cols{grid-template-columns:minmax(0,1fr)!important}
 #v-org .org-cols>.org-left,#v-org .org-cols>.org-right{
  display:flex!important;flex-direction:column!important
 }
 #v-org .org-cols>.org-left>.col{display:block!important}
 #v-org .org-right-teams{
  grid-template-columns:minmax(0,1fr)!important
 }
}
</style>
"""
if 'id="cnnv-org-three-team-columns-2027"' not in s:
    if "</head>" not in s:raise RuntimeError("Không có thẻ head của sơ đồ")
    s=s.replace("</head>",chart_css+"</head>",1)

check=json.loads(re.search(rx,s).group(2))
assert len(check["vi_tri"])==26 and len(check["quy_trinh"])==60 and len(check["danh_muc_van_ban"])==83
assert len(check["cnnv_quan_tri_danh_muc_quy_trinh_2027"]["phan_cong"])==8
assert len(check["cnnv_quan_tri_danh_muc_quy_trinh_2027"]["chu_trinh"])==7
assert len(check["cnnv_quan_tri_danh_muc_quy_trinh_2027"]["truong_danh_muc"])>=18
assert len(check["cnnv_quan_tri_danh_muc_quy_trinh_2027"]["danh_muc_luong_tham_chieu"])==60
assert all("cnnv_quan_tri_quy_trinh_2027" in v and
           v["cnnv_2027"]["quan_tri_danh_muc_quy_trinh"]==v["cnnv_quan_tri_quy_trinh_2027"]
           for v in check["vi_tri"])
assert s.count('id="cnnv-quan-tri-danh-muc-quy-trinh-2027"')==1

assert sum(len(q["buoc"]) for q in check["quy_trinh"])==407
assert all("cnnv_2027" in x for x in check["vi_tri"])
assert all(s.count('id="cnnv-vt-'+role+'"')==1 for role in key_roles)
assert s.count('id="cvt-2-perf-metrics-2027"')==1
assert s.count('id="cnnv-phong-phan-tuyen-2027"')==1
assert s.count('id="cnnv-org-three-team-columns-2027"')==1
assert s.count('id="cnnv-dieu-phoi-ngoai-tuyen-2027"')==1
assert s.count('id="cnnv-tai-hai-chuc-danh-2027"')==1
assert len(check["cnnv_kiem_soat_luong_va_tham_quyen_2027"])==6
assert len(check["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"])==5
assert check["cnnv_ten_to_marketing_benh_vien_2027"]["tong_suat_marketing_co_so"]==14
assert check["cnnv_ten_to_marketing_benh_vien_2027"]["tong_so_suat_to_benh_vien"]==13
assert len([x for x in check["don_vi"] if x.get("loai")=="to_marketing_benh_vien"])==5
assert {x["ten"] for x in check["don_vi"] if x.get("loai")=="to_marketing_benh_vien"}=={x["ten_to"] for x in check["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"]}
assert all("Chuyên viên trưởng" not in x["phe_duyet"].split("Chưa có")[0] or "không mặc nhiên" in x["phe_duyet"] for x in check["bo_quy_chuan_da_dong_bo"])
assert all((N in x["kiem"] or T in x["kiem"]) for x in check["bo_quy_chuan_da_dong_bo"])
assert "22 Tổng công ty + 14 cơ sở" in s
assert "13 suất tại 05 tổ bệnh viện + 01 suất đầu mối kiêm nhiệm phòng khám" in s
assert duplicate not in s

assert all(x["ten_to"]=="Tổ Marketing "+x["benh_vien"] for x in check["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"])
assert s.count('id="cnnv-ten-to-marketing-benh-vien-2027"')==1
assert s.count('<strong>Tổ Marketing tại các bệnh viện và đầu mối phòng khám</strong>')==1
assert s.count('<summary>Các Tổ Marketing tại bệnh viện <b>(13)</b>')==1
assert all(
 s.count('<div class="hosp-h">'+escape(x["ten_to"]))==1
 for x in check["cnnv_ten_to_marketing_benh_vien_2027"]["danh_muc_dang_hoat_dong"]
)
assert len(re.findall(r'<div class="hosp-h">Tổ Marketing Bệnh viện [^<]+<b>\(\d+\)</b></div>',s))==5

assert "/2 hướng dẫn" not in next(x for x in check["vi_tri"] if x["id"]=="dmpk")["bao_cao_cho"]
assert len(check["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]["tinh_huong"])==9
assert len(check["cnnv_nhanh_xung_dot_hai_to_2027"]["buoc"])==6
assert check["cnnv_nhanh_xung_dot_hai_to_2027"]["quy_trinh_goc"]=="xung-dot-lich"
assert len({z["so"] for z in check["cnnv_nhanh_xung_dot_hai_to_2027"]["buoc"]})==6
assert all(all(z.get(k) for k in ("chu_tri","dau_vao","dau_ra","chuyen_buoc")) for z in check["cnnv_nhanh_xung_dot_hai_to_2027"]["buoc"])
assert all(x.get("quy_trinh_tham_chieu") for x in check["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]["tinh_huong"])
assert s.count('id="cnnv-six-step-conflict-2027"')==1
assert next(q for q in check["quy_trinh"] if q["id"]=="xung-dot-lich")["buoc"][2]["phan_tuyen_chu_tri_theo_pham_vi_2027"]["hai_to_tct"]=="cvt-2"
assert len({z["ma"] for z in check["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]["tinh_huong"]})==9
assert all(all(z.get(k) for k in ("rui_ro","dau_moi","quyet_dinh","quy_tac_chan")) for z in check["cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027"]["tinh_huong"])
assert s.count('id="cnnv-2-chief-3-team-2027"')==1
assert all(x.get("cnnv_van_ban_goc_giu_nguyen_2027") for x in check["danh_muc_van_ban"] if x.get("ma")=="QyĐ.02.MKT")
assert "ban hành/hướng dẫn" not in next(x for x in check["vi_tri"] if x["id"]=="cvt-2")["muc_dich"]
assert "trực tiếp quản lý" in next(x for x in check["vi_tri"] if x["id"]=="cvt")["phan_dinh_chu_tri_dau_ra"]
assert "không tự chuyển sang Quản lý mạng lưới theo vùng" in next(x for x in check["vi_tri"] if x["id"]=="cvt")["phan_dinh_chu_tri_dau_ra"]
assert "không tạo tuyến chỉ huy nghiệp vụ thứ hai" in next(x for x in check["vi_tri"] if x["id"]=="cvt")["phan_dinh_chu_tri_dau_ra"]
assert "giảm lãng phí" in next(x for x in check["vi_tri"] if x["id"]=="cvt-2")["muc_dich"]
assert "đánh giá trước–sau" in next(x for x in check["vi_tri"] if x["id"]=="cvt-2")["phan_dinh_chu_tri_dau_ra"]
assert len(check["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]["pham_vi"])==2
assert all(len(z["chi_so"])==4 for z in check["hieu_suat_cvt_truyen_thong_tang_truong_so_2027"]["pham_vi"])

p.write_text(s,"utf-8")
print("PASS CNNV 2027: 26 MTCV, 5 vị trí trọng tâm, 7 mảng chuẩn, 6 điểm luồng, 60 quy trình/407 bước, 83 văn bản")
