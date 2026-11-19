#!/usr/bin/env python3
"""Khóa duy nhất 36 suất (22 TCT, 14 cơ sở) là định biên hiện hành của phương án TTH 2027.

Không coi thực có 35 năm 2026, mô hình 34 trước điều chỉnh hoặc 56 trong
kịch bản mở rộng cũ là định biên cơ cấu 2027. Không đổi mã QT.34, QT.35,
KPI-34, KPI-35 hay số thứ tự biểu mẫu/quy trình.
"""
from pathlib import Path
from html import escape
import json,re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
path=root/"khung-marketing"/"index.html"
s=path.read_text("utf-8")
j=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',s)
if j is None: raise ValueError("Missing canonical CSDL")
D=json.loads(j.group(2))
CUR=D["phan_dinh_quan_ly_hai_cvt_19112026"]["dinh_bien"]
assert (CUR["tong"],CUR["tct"],CUR["benh_vien"],CUR["cvt"])==(36,22,14,2)
assert len(D["vi_tri"])==26 and len(D["quy_trinh"])==60

# The old roadmap cannot be corrected by adding two seats to every future step:
# replace active table with the only proven 36-seat baseline. Git history
# retains old proposal; it is not displayed as active staffing.
old_steps=D["lo_trinh_dinh_bien"]["buoc"]
assert old_steps[0]["tong"]==34
D["lo_trinh_dinh_bien"].update({
    "can_cu":"ĐỊNH BIÊN CƠ CẤU MARKETING 2027: 36 suất = 22 Tổng công ty + 14 cơ sở. Đây là phương án cơ cấu được xác định để trình phê duyệt nhân sự; không đồng nghĩa số người đã nhận việc. Định mức và nhu cầu tuyển thực tế phải đối soát theo tải, số người kiêm nhiệm và quyết định có hiệu lực. Phương án mở rộng trước đây chưa được tính lại sau khi bổ sung Chuyên viên trưởng thứ hai.",
    "buoc":[{
       "buoc":"Cơ cấu giai đoạn đầu 2027 – chuẩn 36 suất",
       "them":"Bao gồm 02 Chuyên viên trưởng và 03 tổ chuyên môn; không cộng suất kiêm nhiệm hai lần",
       "tct":22,"co_so":14,"tong":36
    }],
    "doc_ket_qua":[
       "36 suất là cơ cấu hiện hành của phương án 2027: 22 Tổng công ty, 14 cơ sở.",
       "Các mốc tăng nhân sự theo mở cơ sở chưa được phê duyệt thành lộ trình mới. Tính lại sau khi đo giờ công; không dùng mốc trước điều chỉnh như tổng định biên hiện tại.",
       "Không dùng số thực có của năm 2026 để thay tổng định biên 2027; thực có, tuyển mới và suất cơ cấu là ba chỉ số khác nhau.",
       "Quản lý mạng lưới vùng chỉ kích hoạt theo quyết định phân vùng và giao quản lý có hiệu lực."
    ],
    "trang_thai_sau_co_cau_2_cvt_1911":"CHUẨN 36 SUẤT 2027, 22 TCT + 14 CƠ SỞ; LỘ TRÌNH MỞ RỘNG CHƯA TÍNH LẠI."
})
D["doi_chieu_so_luong_nhan_su_19112026"]={
  "dinh_bien_chuan":36,
  "tong_cong_ty":22,
  "co_so":14,
  "chuyen_vien_truong":2,
  "to_chuyen_mon":3,
  "tinh_trang":"Phương án cơ cấu chốt 36 suất; nhân sự thực có là dữ liệu nhân sự tại kỳ chốt, chưa được xác minh tại thời điểm chạy",
  "canh_bao":"Không chấp nhận tổng định biên giai đoạn đầu khác 36 trên biểu đồ, báo cáo, văn bản, trang mô tả, quy trình hoặc slide."
}
# Specific current-baseline data in statements whose meaning is 2027 rather than
# a cross-reference (QT.34 etc).
for key in ("phan_mem_dac_ta","ghi_chu_kiem_soat_mot_luot"):
    if key not in D: continue
D["bo_quy_chuan_da_dong_bo"]["dinh_bien_hien_hanh_1911"]="36 suất: 22 Tổng công ty, 14 cơ sở; các mốc trước đó không còn dùng cho cơ cấu 2027"
D["phan_dinh_quan_ly_hai_cvt_19112026"]["lo_trinh"]=(
 "Định biên chuẩn 36 suất, không sử dụng mốc 34/35 làm cơ cấu 2027; chỉ xây dựng lộ trình tăng nhân sự khi có tải giờ và quyết định."
)
# Previous scenario notes may be retained in document history, but not as the
# active staffing baseline; correct the relevant old active prose.
replacements=[
 ('hiện có 35','số nhân sự thực có năm 2026 (cần đối chiếu hồ sơ nhân sự)'),
 ('37 (hiện có 35)','37 (số thực có của năm 2026 phải đối chiếu)'),
 ('so với 35 người hiện có: giảm 01','không lấy số thực có năm 2026 làm tổng định biên 2027'),
 ('so với 35 người hiện có: giảm 01','không dùng số thực có năm 2026 làm định biên 2027'),
 ('giảm 03 người, 8%','giảm 01 suất so với định biên 37 trước đây (khoảng 2,7%)'),
 ('giảm 03 người, 8%;','giảm 01 suất so với định biên 37 trước đây (khoảng 2,7%);'),
 ('Định biên Marketing toàn hệ thống 37 (Tổng công ty 10; bệnh viện 27), hiện có 35',
  'Định biên theo nguồn năm 2026: 37 (Tổng công ty 10; bệnh viện 27); số thực có tại thời điểm đó cần đối chiếu'),
 ('Định biên 34 (mục 5.2 )','Định biên 36 theo phương án cơ cấu 2027 (mục 5.2 )'),
 ('Toàn hệ thống 34','Toàn hệ thống 36'),
 ('34 (Tổng công ty 21, cơ sở 13)','36 (Tổng công ty 22, cơ sở 14)'),
 ('Nhân sự: 34 (Tổng công ty 21, cơ sở 13)','Nhân sự theo cơ cấu 2027: 36 (Tổng công ty 22, cơ sở 14)'),
 ('Nhân sự: 34;','Nhân sự cơ cấu 2027: 36;'),
 ('Tổng công ty 21, cơ sở 13: 34','Tổng công ty 22, cơ sở 14: 36'),
 ('34 suất định biên','36 suất định biên'),
 ('không tính vào 34 suất','không tính vào 36 suất'),
 ('Định biên mục tiêu trình phê duyệt: 34 người theo phương án đề xuất',
  'Định biên cơ cấu 2027: 36 suất (22 TCT, 14 cơ sở) theo phương án đề xuất'),
 ('định biên 34 người','định biên 36 suất'),
 ('định biên 34;','định biên 36;'),
 ('định biên 34,','định biên 36,'),
 ('ở định biên 34','ở cơ cấu 36 suất'),
 ('ở bước 34','ở cơ cấu 36 suất'),
 ('khung 34 người','khung 36 suất'),
 ('căn cứ giữ 34 người','căn cứ theo dõi 36 suất định biên'),
 ('25 loại vị trí','26 loại vị trí'),
 ('ma trận 25 vị trí','ma trận 26 vị trí')
]
for a,b in replacements: s=s.replace(a,b)
# Phrases in 2026 reference docs should not be re-characterized as an
# official approved 2027 number. Add context instead of substituting digits.
historical=[
  ('QyĐ.02.MKT phiên bản 3.0 ghi Tổng công ty 34, toàn hệ thống 62;',
   'QyĐ.02.MKT phiên bản 3.0 là tài liệu tham chiếu lịch sử (số liệu cũ, không phải cơ cấu 2027);'),
  ('định biên Tổng công ty 34 trong văn bản không còn là số mới nhất',
   'định biên trong văn bản cũ đã được thay thế bằng phương án 36 suất toàn hệ thống'),
  ('04 Chuyên viên thiết kế, định biên 33 (nay 34 với 03 Chuyên viên media theo Kế hoạch hoạt động năm 2026',
   '04 Chuyên viên thiết kế theo nguồn năm 2026 (mô hình 2027 xác định định biên chuẩn 36 suất, gồm 03 Chuyên viên media theo phương án'),
]
for a,b in historical: s=s.replace(a,b)
# Archive-style chart has already been replaced by previous consistency script.
# Keep only 36 current in the front-facing staffing area, not a legacy 34-row table.
s=re.sub(r'<details><summary style="cursor:pointer;color:#0837A1;font-weight:700">Xem lộ trình tham chiếu cũ \(không áp dụng để bố trí người\)</summary>[\s\S]*?</details>',
 '<p><b>Lộ trình mở rộng:</b> chưa tính lại theo cơ cấu 36 suất; cần dữ liệu khối lượng, định mức và quyết định phê duyệt trước khi xác định từng mốc.</p>',s,count=1)
# Remove outdated static roadmap trend claims that would compete with 36.
s=re.sub(r'Lộ trình theo cơ sở và định biên mục tiêu: 34 → 40 → 43 → 50 → 53 → 56 người\.',
         'Lộ trình mở rộng theo cơ cấu 36 suất đang được đối soát tải việc, chưa chốt các mốc mới.',s)
s=re.sub(r'Điều kiện triển khai lộ trình: sáu mốc tổng định biên mục tiêu 34 / 40 / 43 / 50 / 53 / 56[^<]{0,330}',
         'Điều kiện triển khai lộ trình: định biên giai đoạn đầu 36 suất; mốc mở rộng cần tính lại từ dữ liệu giờ thực đo và quyết định có hiệu lực. ',s)
s=s.replace('34 → 40 → 43 → 50 → 53 → 56','36 (mốc hiện hành); tăng thêm chờ phê duyệt')
s=s.replace('Toàn hệ thống</th></tr></thead><tbody><tr><td>Hiện tại</td><td>21</td><td>31</td><td>13</td><td>25</td><td>34</td>',
            'Toàn hệ thống</th></tr></thead><tbody><tr><td>Hiện tại</td><td>22</td><td>Chưa tính lại</td><td>14</td><td>Chưa tính lại</td><td>36</td>')
# Must not recast old 34-person workload estimate as measured 36-person workload.
s=s.replace('Chưa có phần mềm: khoảng 100 giờ/tháng ở 34 người', 
            'Chưa có phần mềm: giờ bổ sung ở cơ cấu 36 suất cần đo lại (ước tính cũ 100 giờ/tháng không được coi là định mức mới)')
s=s.replace('34 người (≈ 0,7 người)','cơ cấu cũ (≈ 0,7 suất dự toán)')
s=s.replace('≈ 15 phút/người/tuần × 34','≈ 15 phút/người/tuần × 36 (cần đo lại)')
s=s.replace('≈ 100 giờ/tháng ở 34 người','giờ chưa có phần mềm ở cơ cấu 36 suất cần đo lại')
# Direct HTML descriptions of 2027 initial structure
s=s.replace('Marketing cơ sở 14; toàn hệ thống 34', 'Marketing cơ sở 14; toàn hệ thống 36')
s=s.replace('<div class="stat"><b>56</b><span>khi đủ 10 bệnh viện, 02 phòng khám (gồm Quản lý mạng lưới vùng)</span></div>',
            '<div class="stat"><b>36</b><span>suất cơ cấu hiện hành; lộ trình mở rộng chưa tính lại</span></div>')
s=s.replace('Định biên 34 (Media 03 theo Kế hoạch hoạt động năm 2026)',
            'Định biên hiện tại 36 suất (Media 03 theo phương án sử dụng lao động)')
# Output JSON from corrected data after all visible replacements.
j2=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',s)
if j2 is None: raise ValueError("Lost CSDL after replacements")
s=s[:j2.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[j2.end(2):]
check=json.loads(re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s).group(1))
assert len(check["lo_trinh_dinh_bien"]["buoc"])==1
assert check["lo_trinh_dinh_bien"]["buoc"][0]["tong"]==36
assert check["lo_trinh_dinh_bien"]["buoc"][0]["tct"]==22
assert check["lo_trinh_dinh_bien"]["buoc"][0]["co_so"]==14
assert check["phan_dinh_quan_ly_hai_cvt_19112026"]["dinh_bien"]["tong"]==36
# Audit only active current staffing assertions; historical source refs QT.34 etc are different numerals.
active_markers=[
 r'định biên (?:hiện tại|hiện hành|giai đoạn đầu|cơ cấu 2027)\s*(?:là|:)?\s*(?:34|35)\b',
 r'(?:34|35)\s*(?:người|suất)\s*(?:thuộc )?định biên (?:hiện tại|hiện hành|2027)',
 r'nhân sự (?:giai đoạn đầu|hiện tại):\s*(?:34|35)\b',
]
for pattern in active_markers:
    if re.search(pattern,s,re.IGNORECASE):
        raise ValueError("Legacy 34/35 still active: "+pattern)
path.write_text(s,"utf-8")
print("PASS FIX 36: 22 TCT + 14 CO SO; 2 CVT; 26 roles; active roadmap one 36-seat baseline")
