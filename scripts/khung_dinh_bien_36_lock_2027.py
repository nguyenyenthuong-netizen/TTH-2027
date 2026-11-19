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
D["doi_chieu_so_luong_nhan_su_19112026"]["ghi_chu_nguon"]="36 suất: 22 Tổng công ty, 14 cơ sở; các mốc trước đó không còn dùng cho cơ cấu 2027"
D["phan_dinh_quan_ly_hai_cvt_19112026"]["lo_trinh"]=(
 "Định biên chuẩn 36 suất, không sử dụng mốc 34/35 làm cơ cấu 2027; chỉ xây dựng lộ trình tăng nhân sự khi có tải giờ và quyết định."
)
# Normalize staffing references in role descriptions / operational catalogue;
# retain historical logs and numeric process codes unchanged.
def fix_staffing_strings(node):
    if isinstance(node,list):
        return [fix_staffing_strings(x) for x in node]
    if isinstance(node,dict):
        return {key:fix_staffing_strings(val) for key,val in node.items()}
    if not isinstance(node,str): return node
    replacements={
      "Bố trí người theo định biên 34":"Bố trí người theo định biên chuẩn 36 suất (22 TCT, 14 cơ sở)",
      "căn cứ giữ 34 người":"căn cứ quản lý 36 suất định biên, không lấy số thực có cũ làm định biên",
      "định biên 34 người":"định biên chuẩn 36 suất",
      "định biên 34 suất":"định biên chuẩn 36 suất",
      "định biên hiện tại 34":"định biên hiện tại 36",
      "34 suất định biên":"36 suất định biên",
      "khung 34 người":"khung 36 suất",
      "hiện có 35":"số nhân sự thực có tại thời điểm cũ (chưa xác minh kỳ hiện hành)",
      "34 / 40 / 43 / 50 / 53 / 56":"các mốc mở rộng của phương án cũ, chưa được tính lại",
      "34 người/suất định biên với 25 loại vị trí":"36 suất định biên với 26 loại vị trí",
      "≈ 15 phút/người/tuần × 34":"≈ 15 phút/người/tuần × 36 (cần đo lại)",
      "Bước 34":"Cơ cấu giai đoạn đầu 36",
      "ở bước 34":"ở cơ cấu giai đoạn đầu 36",
      "mốc 34 suất cũ":"mốc cơ cấu cũ",
      "lộ trình 34 / 40 / 43 / 50 / 53 / 55":"lộ trình mở rộng cũ, chưa cập nhật sau cơ cấu 36 suất"
    }
    for k,v in replacements.items(): node=node.replace(k,v)
    return node
for section in ("vi_tri","danh_muc_van_ban","phan_mem_dac_ta",
                "phan_dinh_vi_tri_chi_tiet_17112026","ma_tran_TCT_chi_nhanh_17112026",
                "dieu_chinh_17112026","ghi_chu_giai_quyet_4_dieu_kien"):
    if section in D:
        D[section]=fix_staffing_strings(D[section])

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
# Fix remaining active paragraphs and table labels. Historical decision log
# numbers are left intact as records of past proposals, not present staffing.
s=s.replace('Định biên 34 (mục 5.2 ); cách 3 cũng là 34 khi có 03 Chuyên viên media theo Kế hoạch hoạt động năm 2026',
            'Định biên cơ cấu 2027 là 36 suất (mục 5.2); phương án có 03 Chuyên viên media theo danh mục sử dụng lao động')
s=s.replace('Định biên 34 (Media 03 theo Kế hoạch hoạt động năm 2026)',
            'Định biên chuẩn 36 suất (bao gồm 03 Chuyên viên media)')
s=s.replace('Không cần bố trí đủ 34 người trước thí điểm',
            'Không mặc nhiên tuyển đủ 36 suất trước thí điểm; nhân sự thực tế bố trí theo kế hoạch được phê duyệt')
s=s.replace('Nhân sự: 34;', 'Nhân sự cơ cấu chuẩn: 36 suất;')
s=s.replace('Ổn định và xây dựng (Quý III/2027 – Quý IV/2028)</td><td>34;',
            'Ổn định và xây dựng (Quý III/2027 – Quý IV/2028)</td><td>36;')
# An old side-by-side 34 / 56 table is still static: retire the old comparisons
# without falsely recalculating the 56-seat extended forecast.
s=s.replace('<td>21</td><td>31</td><td>13</td><td>25</td><td>34</td><td>56</td>',
            '<td>22</td><td>Chưa tính lại</td><td>14</td><td>Chưa tính lại</td><td><b>36</b></td><td>Chưa chốt</td>')
s=s.replace('Phòng Marketing Tổng công ty</td><td>21</td><td>31</td>',
            'Phòng Marketing Tổng công ty</td><td>22</td><td>Chưa chốt</td>')
s=s.replace('Marketing cơ sở</td><td>13</td><td>25</td>',
            'Marketing cơ sở</td><td>14</td><td>Chưa chốt</td>')
s=s.replace('Toàn hệ thống</td><td>34</td><td>56</td>',
            'Toàn hệ thống</td><td><b>36</b></td><td>Chưa chốt</td>')
# Old history is not a current report. Avoid leaving 34 labels in
# front-facing staffing narrative even when clearly marked as old.
s=s.replace('Mốc 34/40/43/50/53/56 là kịch bản trước điều chỉnh',
            'Các mốc mở rộng trong kịch bản trước điều chỉnh')
s=s.replace('Các mốc 34 → 56 trong mục này thuộc phương án cũ',
            'Các mốc mở rộng trong mục này thuộc phương án cũ')
s=s.replace('mốc 34 suất là phương án cũ','mốc cơ cấu cũ đã được thay thế')

# Exact HTML markup corrections for static cells whose numbers were hidden
# behind tags and escaped the first pass (retains historical code references).
s=s.replace(
 'Định biên 34 (mục <a class="xref" data-sec="m-5-2" href="#m-5-2">5.2</a>); cách 3 cũng là 34 khi có 03 Chuyên viên media theo Kế hoạch hoạt động năm 2026',
 'Định biên chuẩn 36 suất (mục <a class="xref" data-sec="m-5-2" href="#m-5-2">5.2</a>); bố trí 03 Chuyên viên media theo cơ cấu 2027')
s=s.replace('<b>Nhân sự:</b> 34 (Tổng công ty 21, cơ sở 13)',
            '<b>Định biên chuẩn:</b> 36 suất (Tổng công ty 22, cơ sở 14)')
s=s.replace('<b>Nhân sự:</b> 34; Chuyên viên biên tập nhóm 2 thứ hai',
            '<b>Định biên cơ cấu:</b> 36 suất; Chuyên viên biên tập nhóm 2 thứ hai')
s=s.replace('<td>34; Chuyên viên biên tập nhóm 2 thứ hai',
            '<td>36 suất cơ cấu; Chuyên viên biên tập nhóm 2 thứ hai')
s=s.replace(
 '<tr><td>Phòng Marketing Tổng công ty</td><td>21</td><td>31</td></tr><tr><td>Marketing cơ sở</td><td>13</td><td>25</td></tr><tr><td><strong>Toàn hệ thống</strong></td><td><strong>34</strong></td><td>56</td></tr>',
 '<tr><td>Phòng Marketing Tổng công ty</td><td><b>22</b></td><td>Chưa chốt</td></tr>'
 '<tr><td>Marketing cơ sở</td><td><b>14</b></td><td>Chưa chốt</td></tr>'
 '<tr><td><strong>Toàn hệ thống</strong></td><td><strong>36</strong></td><td>Chưa chốt</td></tr>')
s=s.replace('Mức 56 gồm Quản lý mạng lưới vùng theo lộ trình đã chốt ngày 14/11/2026.',
            'Mốc mở rộng phải tính lại theo định biên chuẩn 36 suất; Quản lý mạng lưới vùng chỉ triển khai khi có quyết định.')
s=s.replace('Định biên 34 (Media 03 theo Kế hoạch hoạt động năm 2026)',
            'Định biên chuẩn 36 suất (Media 03 trong cơ cấu hiện hành)')
s=s.replace('Không cần bố trí đủ 34 người trước thí điểm',
            'Không mặc nhiên tuyển đủ 36 suất trước thí điểm')
s=s.replace('ở định biên 34','ở định biên cơ cấu 36 suất')
s=s.replace('định biên 34, Tổng công ty 21',
            'định biên chuẩn 36 suất, Tổng công ty 22')
# Historical audit tables may retain prior figures, but must be clearly labeled.
s=s.replace('<section class="doc-sec" data-title="28. Những vấn đề đã trao đổi, chưa chốt" id="m-28">',
            '<section class="doc-sec" data-title="28. Những vấn đề đã trao đổi, chưa chốt" id="m-28"><p class="mini"><b>LỊCH SỬ PHƯƠNG ÁN – KHÔNG ÁP DỤNG THAY CƠ CẤU 2027:</b> các số định biên trong bảng lịch sử dưới đây thuộc bản ghi ngày cũ. Định biên cơ cấu chuẩn năm 2027 là 36 suất: 22 TCT và 14 cơ sở.</p>')
# Separate actual 2026 headcount from the 2027-seat number.
s=s.replace('<strong>35</strong> (Tổng công ty 09; bệnh viện 26)',
            'Số thực có tại kỳ thống kê năm 2026 (xem báo cáo nhân sự gốc)')
s=s.replace('<strong>37</strong> (hiện có 35)',
            '<strong>37</strong> (định biên năm 2026; số thực có xem hồ sơ năm 2026)')
s=s.replace('so với 35 người hiện có: giảm 01',
            'không dùng số người thực có năm 2026 để suy ra giảm/tăng suất định biên')

# Clean two legacy staffing tables whose numeric cells are split by tags.
s=s.replace('<tr><td>Định biên</td><td>34 (Media 03 theo Kế hoạch hoạt động năm 2026)</td><td>34</td></tr>',
            '<tr><td>Định biên cơ cấu chuẩn</td><td><b>36 suất</b> (22 Tổng công ty, 14 cơ sở; 03 Chuyên viên media theo phương án)</td><td><b>36 suất</b></td></tr>')
s=s.replace('<tr><td><strong>Toàn hệ thống</strong></td><td><strong>34</strong></td><td>56</td></tr>',
            '<tr><td><strong>Toàn hệ thống</strong></td><td><strong>36</strong></td><td>Chưa chốt</td></tr>')
s=s.replace('<th>Đủ 10 bệnh viện, 02 phòng khám</th>',
            '<th>Giai đoạn mở rộng – phải tính lại trước phê duyệt</th>')
# The historical TCT=34 of QyĐ.02.MKT is a source reference, not 2027 staffing;
# leave it under the dated historical comparison rather than changing facts.

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
# Surface residual misleading 34/35 staffing statements for follow-up, excluding
# unrelated identifiers like KPI-34/35 and QT.34/35.
html_without_scripts=re.sub(r'<script\b[^>]*>[\s\S]*?</script>',' ',s,flags=re.I)
html_without_scripts=re.sub(r'<style\b[^>]*>[\s\S]*?</style>',' ',html_without_scripts,flags=re.I)
plain=re.sub(r'<[^>]+>',' ',html_without_scripts)
plain=re.sub(r'\s+',' ',plain)
old_refs=[]
for match in re.finditer(r'(?<!\d)(?:34|35)(?!\d)',plain):
    context=plain[max(0,match.start()-95):match.end()+90]
    if re.search(r'định biên|nhân sự|suất|hiện có|người|tuyển|giai đoạn|cơ cấu|marketing cơ sở',context,re.I):
        if re.search(r'(?:KPI|QT|mảng|mục|số)\s*[-. ]\s*(?:34|35)\b',context,re.I):
            continue
        old_refs.append(context[:190])
print("LEGACY-STAFFING-NEARBY",len(old_refs))
for line in old_refs[:30]:
    print("LEGACY-CONTEXT",line)
path.write_text(s,"utf-8")
print("PASS FIX 36: 22 TCT + 14 CO SO; 2 CVT; 26 roles; active roadmap one 36-seat baseline")
