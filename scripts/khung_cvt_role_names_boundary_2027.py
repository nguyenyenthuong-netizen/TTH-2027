#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chốt tên đầy đủ hai chức danh và chống giao việc trùng với chuyên viên/tổ trưởng.

Chạy sau toàn bộ bước dựng nguồn và CSS; KHÔNG đổi mã kỹ thuật cvt/cvt-2,
không tự cấp quyền phát hành, tài chính hoặc duyệt nhân sự.
"""
from pathlib import Path
from html import escape
import json,re,sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
html=p.read_text("utf-8")
m=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',html)
if m is None: raise ValueError("Mất cơ sở dữ liệu nhúng")
D=json.loads(m.group(2))
R={r["id"]:r for r in D["vi_tri"]}
NOI_DUNG=R["cvt"]["ten"]
TRUYEN_THONG=R["cvt-2"]["ten"]
assert NOI_DUNG=="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
assert TRUYEN_THONG=="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
assert len(R)==26 and len(D["quy_trinh"])==60 and len(D["danh_muc_van_ban"])==83

# Chỉ thay câu chữ hiển thị. Không thay các mã định danh, tên trường, khóa liên kết.
def fix_label(s):
    if not isinstance(s,str):return s
    replaces=[
      (r'\bChuyên viên trưởng\s+thứ\s+hai\b', TRUYEN_THONG),
      (r'\bChuyên viên trưởng\s+thứ\s+nhất\b', NOI_DUNG),
      (r'\bChuyên viên trưởng\s+(?:số\s*)?2\b', TRUYEN_THONG),
      (r'\bChuyên viên trưởng\s+(?:số\s*)?1\b', NOI_DUNG),
      (r'\bCVT\s*[-.]?\s*2\b',TRUYEN_THONG),
      (r'\bCVT\s*[-.]?\s*1\b',NOI_DUNG),
      (r'\bChuyên viên trưởng Nội dung\s*[–-]\s*Cơ sở\b',NOI_DUNG),
      (r'\bCVT Nội dung\s*[–-]\s*Cơ sở\b',NOI_DUNG),
      (r'\bCVT Truyền thông\s*[–-]\s*Số\b',TRUYEN_THONG),
      (r'\bChuyên viên trưởng Truyền thông\s*[–-]\s*Số\b',TRUYEN_THONG),
      (r'\bCVT Nội dung\s*[–-]\s*Sáng tạo\b',NOI_DUNG),
    ]
    for pat,new in replaces:
        flags=0 if pat.startswith(r'\bCVT') else re.I
        s=re.sub(pat,lambda _m:new,s,flags=flags)
    return s

# Chỉ tác động chuỗi văn bản, KHÔNG thay các khóa "CVT1"/"CVT2" trong dữ liệu
# nguồn đã dùng làm liên kết; hiển thị toàn bộ bằng tên vị trí đầy đủ.
def walk(node):
    if isinstance(node,str):
        if node in ("cvt","cvt-2","cvt2"):return node
        if node.startswith(("cvt|","cvt-2|")):return node
        return fix_label(node)
    if isinstance(node,list):return [walk(x) for x in node]
    if isinstance(node,dict):return {k:walk(v) for k,v in node.items()}
    return node
D=walk(D)

# Ánh xạ tên người quản lý trong trường diễn giải, không đánh số chức danh.
legacy=D.get("phan_dinh_quan_ly_hai_cvt_19112026",{}).get("tuyen",{})
if "CVT1" in legacy and "CVT2" in legacy:
    D["phan_dinh_quan_ly_hai_cvt_19112026"]["tuyen_hien_thi"]=[
        {"ten_chuc_danh":NOI_DUNG,"pham_vi":legacy["CVT1"]},
        {"ten_chuc_danh":TRUYEN_THONG,"pham_vi":legacy["CVT2"]},
    ]
D["ranh_gioi_khong_trung_viec_2027"]={
 "ten_chuc_danh":[NOI_DUNG,TRUYEN_THONG],
 "quan_ly_va_thuc_hien":"Chuyên viên trưởng chịu trách nhiệm quản lý mục tiêu, chuẩn, tải việc và kiểm soát theo tuyến; Tổ trưởng điều phối việc hằng ngày; chuyên viên trực tiếp tạo ra sản phẩm. Không nhân đôi đầu ra hoặc điểm KPI.",
 "dau_ra_quan_ly_noi_dung":"Kế hoạch tải và điều phối nguồn lực sản xuất, bộ tiêu chuẩn Biên tập–Thiết kế–Media, biên bản xử lý xung đột và báo cáo Marketing cơ sở; không mặc định viết bài, thiết kế, quay dựng thay thành viên.",
 "dau_ra_quan_ly_truyen_thong":"Bộ chuẩn PR, OOH, phát thanh, màn hình, quảng cáo, kênh số; báo cáo rủi ro, chất lượng thực thi và hiệu quả hai tổ thuộc Tổng công ty; không mặc định sản xuất nội dung, vận hành quảng cáo hoặc tác nghiệp truyền thông thay chuyên viên.",
 "nguoi_giao_viec_co_so":"Trưởng nhóm Marketing cơ sở giao nhiệm vụ trực tiếp cho người tại bệnh viện. "+NOI_DUNG+" quản lý tuyến, duyệt điều phối trong phạm vi được giao; "+TRUYEN_THONG+" gửi yêu cầu nghiệp vụ qua đúng tuyến, không tạo lệnh thứ hai.",
 "khong_trung_voi_quan_ly_thuong_hieu":"Quản lý thương hiệu giữ mục tiêu, thông điệp và nghiệm thu hạng mục thương hiệu. Cả hai Chuyên viên trưởng không tự động thay quyền nghiệm thu của Quản lý thương hiệu.",
 "khong_trung_voi_chuyen_vien_truyen_thong":"Chuyên viên truyền thông triển khai PR, báo chí, đối tác, OOH, phát thanh/màn hình và hồ sơ hiện trường theo phân công; Chuyên viên trưởng quản lý chuẩn, rủi ro và chất lượng, không mặc định thay người thực hiện.",
 "khong_trung_voi_chuyen_vien_tang_truong_so":"Chuyên viên quảng cáo/kênh số trực tiếp vận hành, tối ưu và báo cáo chiến dịch; Chuyên viên trưởng kiểm soát tiêu chuẩn, tải và rủi ro, không ghi cùng một sản phẩm thành hai đầu ra.",
 "phan_quyen":"Phân biệt người làm, kiểm biên tập/kỹ thuật, xác nhận y khoa/pháp lý, nghiệm thu mục tiêu thương hiệu, duyệt phát hành và duyệt chi; không có quyền duyệt chỉ vì chức danh quản lý.",
 "xung_dot":"Có một đầu mối giao việc cho mỗi nhân sự; bất đồng giữa hai tuyến hoặc thay đổi ngân sách, mục tiêu, thẩm quyền phải trình Trưởng phòng/cấp được ủy quyền bằng văn bản.",
}

# Nguồn JSON được gắn lại trước khi sửa chữ hiển thị, bảo toàn script nhúng.
html=html[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+html[m.end(2):]
# Bỏ các cách gọi đánh số ở văn bản HTML tĩnh mà không chạm dữ liệu JS/CSS/attributes.
blocks=re.split(r'(<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>)',html,flags=re.I)
for i in range(0,len(blocks),2):
    items=re.split(r'(<[^>]+>)',blocks[i])
    for j in range(0,len(items),2):
        items[j]=fix_label(items[j])
    blocks[i]="".join(items)
html="".join(blocks)

# Dùng bảng ranh giới ngay trong phần đã có, không thêm menu/đường dẫn mới.
marker='<section id="tth-cvt-deep-audit-1911"'
if marker not in html: raise ValueError("Thiếu mục đối chiếu trách nhiệm chức danh")
if 'id="tth-cvt-cross-role-boundaries-2027"' not in html:
    cases=[
      ("Quản lý chuyên môn", "Quản lý chuẩn Nội dung–Sáng tạo, tải sản xuất và Trưởng nhóm Marketing cơ sở cả hai nhóm", "Quản lý chuẩn Truyền thông–Thương hiệu, Tăng trưởng số và hai tổ tại Tổng công ty", "Tổ trưởng giao việc từng ngày; người làm chịu trách nhiệm sản phẩm"),
      ("Biên tập, Thiết kế, Media", "Điều phối năng lực, quy chuẩn kỹ thuật và xử lý xung đột lịch sản xuất", "Chỉ kiểm chuẩn nghiệp vụ thông điệp/kênh khi liên quan", "Biên tập, Thiết kế, Media trực tiếp tạo/sửa/kiểm sản phẩm trong phạm vi được giao"),
      ("PR, OOH, phát thanh, màn hình", "Bố trí năng lực sản xuất/điều phối Marketing cơ sở khi có đầu việc", "Kiểm chuẩn nghiệp vụ, rủi ro, tuân thủ và kết quả hai tổ", "Chuyên viên truyền thông thực hiện, tổ chức hiện trường, quản lý hồ sơ và báo cáo"),
      ("Quảng cáo, kênh số", "Phối hợp cung ứng nội dung, thiết kế, media theo yêu cầu đã ghi nhận", "Quản lý tiêu chuẩn vận hành, tiến độ, chất lượng và rủi ro", "Chuyên viên quảng cáo/kênh số thiết lập, tối ưu, đăng và báo cáo theo quyền"),
      ("Marketing tại bệnh viện", "Quản lý trực tiếp Trưởng nhóm, điều phối tải và chốt một lịch công việc", "Hướng dẫn nghiệp vụ thông qua tuyến quản lý, không giao lệnh trực tiếp nhân viên cơ sở", "Trưởng nhóm cơ sở giao việc, kiểm hiện trường; Ban Giám đốc cơ sở quản lý hành chính theo phân cấp"),
      ("Thông điệp và phê duyệt", "Kiểm chuẩn đầu ra sản xuất; không thay nghiệm thu thương hiệu", "Kiểm chuẩn truyền thông/kênh; không tự duyệt phát hành", "Quản lý thương hiệu nghiệm thu mục tiêu/thông điệp; cấp có thẩm quyền duyệt y khoa, pháp lý, phát hành và chi phí riêng"),
    ]
    cells="".join("<tr>"+"".join("<td>"+escape(c)+"</td>" for c in row)+"</tr>" for row in cases)
    section=('<div id="tth-cvt-cross-role-boundaries-2027" style="margin:13px 0 0">'
      '<h4 style="color:#0837A1;margin:0 0 7px;font-size:17px">Ranh giới trách nhiệm với các tổ và vị trí liên quan</h4>'
      '<p style="margin:0 0 9px">Chuyên viên trưởng chịu trách nhiệm quản lý theo tuyến; Tổ trưởng phân công tác nghiệp; chuyên viên tạo sản phẩm. Một đầu ra chỉ có một người chịu trách nhiệm chính, không nhận trùng KPI.</p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto"><table class="t wide" style="min-width:1080px;width:100%;table-layout:auto">'
      '<thead><tr><th>Đầu việc</th><th>'+escape(NOI_DUNG)+'</th><th>'+escape(TRUYEN_THONG)+'</th><th>Người trực tiếp thực hiện và cấp có thẩm quyền</th></tr></thead>'
      '<tbody>'+cells+'</tbody></table></div></div>')
    # Place immediately after heading of the existing review section, not nested inside another card/table.
    start=html.index(marker)
    offset=html.index('</p>',start)+4
    html=html[:offset]+section+html[offset:]

# Tự động từ chối nếu còn tên đánh số trong vùng chữ hiển thị hoặc CSDL dạng văn bản.
all_names=json.dumps(D,ensure_ascii=False)
# ID kỹ thuật còn được phép tồn tại: mã, khóa JSON, nhóm thương hiệu.
view=re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>',' ',html,flags=re.I)
view=re.sub(r'<[^>]+>',' ',view)
bad=re.search(r'Chuyên viên trưởng\s+(?:thứ\s+(?:nhất|hai)|(?:số\s*)?[12]\b)|\bCVT\s*[12]\b|Chuyên viên trưởng Nội dung\s*[–-]\s*Cơ sở\b',view,re.I)
if bad:raise ValueError("Còn cách gọi chức danh sai trong phần hiển thị: "+bad.group(0))
assert html.count('id="tth-cvt-cross-role-boundaries-2027"')==1
assert len(D["vi_tri"])==26 and len(D["quy_trinh"])==60
p.write_text(html,"utf-8")
print("ROLE-NAMES-BOUNDARY PASS: two exact job titles, distinct managers, 26 positions / 60 processes / 83 documents, no numbered job titles visible")
