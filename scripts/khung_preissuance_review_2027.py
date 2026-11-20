#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nghiệm thu trước ban hành: kiểm tra kỹ thuật & điều kiện pháp lý riêng biệt.
Không tự ký, cấp mã hay biến quy trình mẫu trong đề án thành văn bản có hiệu lực.
"""
from pathlib import Path
from html import escape
import re,sys,json,datetime
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
idx=root/"khung-marketing"/"index.html"
s=idx.read_text("utf-8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s)
assert m,"Thiếu cơ sở dữ liệu Marketing"
d=json.loads(m.group(1))
assert len(d["quy_trinh"])==60
assert len(d["danh_muc_van_ban"])==83
assert len(d["vi_tri"])==26
assert s.count('<button class="tab"')==12
assert s.count('class="lead tth-truong-nhom"')==5
assert '<span class="state">Đang trống</span>' not in s
cross=d["doi_chieu_quy_trinh_cu_2027"]
assert cross["tong_luong"]==60 and len(cross["danh_sach"])==60
assert cross["co_van_ban_co_the_lien_quan"]+cross["chua_tim_thay_trong_danh_muc"]==60
assert all("CHƯA" in x["trang_thai"] for x in d["danh_muc_van_ban"])
post=[
 ("01","Cơ cấu TCT/cơ sở, sơ đồ 12 phần","Kiểm thử trực tuyến đạt","Chờ Ban TGĐ phê duyệt chính thức"),
 ("02","Chức năng nhiệm vụ 26 vị trí, 2 Chuyên viên trưởng","Đã mô tả trong đề án","Chờ từng ngành dọc/Phòng Nhân lực xác nhận tuyến và thẩm quyền"),
 ("03","Định biên dự kiến và nhân sự thực vị","Có phương án, chưa có hồ sơ ký đủ","Chờ bảng thực vị và lộ trình nhân lực được xác nhận"),
 ("04","60 luồng / 83 mục danh mục quản trị","Đã lập đối chiếu sơ bộ","52 ứng viên/08 chưa thấy; toàn văn cũ, mã, hiệu lực phải kiểm"),
 ("05","Quyền giao việc, kiểm chuẩn, duyệt phát hành, duyệt chi","Đã mô hình hóa logic","Chờ ma trận thẩm quyền có hiệu lực và người ký đúng cấp"),
 ("06","09 chỉ số trọng tâm 2026/2027 theo TB 156","Chưa có bản số liệu đã ký xác nhận","Bổ sung số thực hiện đến 31/10/2026 và chỉ tiêu 2027"),
 ("07","Mẫu biểu Kế hoạch năm 2027","Có phương án triển khai","Chờ thống nhất mẫu chính thức với Phòng TCKH"),
 ("08","Chuyển tiếp, đào tạo, kiểm thử vận hành thực tế","Có quy tắc mô phỏng/kiểm thử","Chờ biên bản chạy thử và giao quyền theo ngày hiệu lực"),
 ("09","Vercel và GitHub Pages","Đã đồng bộ và đối soát byte tại thời điểm kiểm tra","Không thay thế nghiệm thu nghiệp vụ"),
 ("10","Biên bản ký nghiệm thu / quyết định ban hành","Chưa có chữ ký và số quyết định","Chưa đủ điều kiện công nhận hiệu lực văn bản")
]
data={"status":"HO_SO_TRINH_KIEM_TRA_CHUA_BAN_HANH",
 "verified_at":"2026-11-20",
 "scope":{"views":12,"roles":26,"flows":60,"documents":83,"matched_candidate":cross["co_van_ban_co_the_lien_quan"],"not_found":cross["chua_tim_thay_trong_danh_muc"]},
 "outstanding":[{"id":i,"dimension":t,"technical_evidence":a,"issuance_gate":b} for i,t,a,b in post],
 "sign_off":{"marketing":False,"human_resources":False,"quality":False,"finance":False,"technology":False,"executive":False},
 "principle":"Nghiệm thu kỹ thuật không thay thế xác nhận quản trị hoặc quyết định ban hành. 60 luồng là đề án, không phải 60 quy trình mới có hiệu lực."}
out=root/"khung-marketing"/"nghiem-thu"
out.mkdir(parents=True,exist_ok=True)
(out/"ket-qua.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),"utf-8")
rows="".join(f"<tr><td>{i}</td><td>{escape(t)}</td><td>{escape(a)}</td><td>{escape(b)}</td></tr>" for i,t,a,b in post)
page="""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nghiệm thu trước ban hành – Khung Marketing 2027</title>
<style>body{font:16px/1.6 Arial,sans-serif;color:#23334d;margin:0;background:#f5f7fb}header,main{padding:20px clamp(14px,3vw,45px)}header{background:#fff;border-top:6px solid #0837A1;border-bottom:2px solid #ED3237}h1{color:#0837A1;font-size:clamp(21px,2.5vw,31px)}h2{font-size:21px}a{color:#0837A1}main{max-width:1470px;margin:auto}section{background:#fff;border:1px solid #c5d3e3;border-radius:10px;padding:16px;margin:14px 0}table{width:100%;border-collapse:collapse;min-width:950px}th,td{border:1px solid #cdd8e4;padding:10px;text-align:left;vertical-align:top}th{background:#e8f0ff;color:#0837A1}th:first-child{width:50px}.scroll{overflow:auto}.lead{font-size:17px;font-weight:700}footer{font-size:13px;padding:20px}</style></head><body>
<header><a href="../">Về Khung cơ cấu Marketing 2027</a><h1>Hồ sơ rà soát và nghiệm thu trước ban hành</h1>
<p>Đối chiếu yêu cầu Thông báo số 156/TB-TTH ngày 14/11/2026. Bản kiểm soát ngày 20/11/2026.</p></header><main>
<section><h2>Kết quả hiện tại</h2><p class="lead">Đạt về cấu trúc và kiểm thử kỹ thuật theo phạm vi đã chạy. CHƯA ĐỦ ĐIỀU KIỆN xác nhận ban hành đồng loạt 60 quy trình và 23 văn bản tham chiếu.</p>
<p>Đối chiếu sơ bộ 60/60 luồng: <b>__RELATED__</b> luồng có văn bản có thể liên quan theo tên/phạm vi và <b>__NOTFOUND__</b> luồng chưa tìm thấy trong Phụ lục 03. Chưa có kết luận hiệu lực hoặc phương án sửa/giữ/gộp/bãi bỏ/xây mới.</p>
<p><a href="../doi-chieu-quy-trinh/">Mở phụ lục đối chiếu 60 luồng</a></p></section>
<section><h2>Ma trận điều kiện chốt trước trình ký</h2><div class="scroll"><table><thead><tr><th>TT</th><th>Đầu việc</th><th>Bằng chứng hiện có</th><th>Điều kiện trước ban hành</th></tr></thead><tbody>__ROWS__</tbody></table></div></section>
<section><h2>Phân tầng ban hành</h2><p><b>Tầng A – Cơ cấu:</b> Quyết định cơ cấu, chức năng, định biên, ma trận thẩm quyền và điều khoản chuyển tiếp. Chỉ ký sau khi các đầu mối xác nhận nội dung và số liệu.</p>
<p><b>Tầng B – Quy trình:</b> Từng quy trình được kiểm toàn văn, xác định kế thừa/điều chỉnh/hợp nhất/bãi bỏ/xây mới, cấp mã và ký theo đúng thẩm quyền. Không thay thế văn bản đang hiệu lực bằng sơ đồ luồng dự kiến.</p>
<p>Các chữ ký, số quyết định và thời điểm hiệu lực phải được ghi nhận từ văn bản thực tế; chưa ký thì không được tự đánh dấu “đã ban hành”.</p></section>
</main><footer><a href="../">Khung cơ cấu 2027</a> · <a href="ket-qua.json">Dữ liệu nghiệm thu</a></footer></body></html>"""
page=page.replace("__ROWS__",rows).replace("__RELATED__",str(cross["co_van_ban_co_the_lien_quan"])).replace("__NOTFOUND__",str(cross["chua_tim_thay_trong_danh_muc"]))
(out/"index.html").write_text(page,"utf-8")
# Cập nhật liên kết trong Phần 12, không thêm tab và không thay nội dung quy trình.
view='<section class="view" data-view="decisions" id="v-decisions">'
assert s.count(view)==1
link='<p style="padding:12px 16px;border:1px solid #b7c8df;border-left:4px solid #0837A1;border-radius:8px;background:#fff;font-size:15px"><b>Nghiệm thu trước ban hành:</b> <a href="nghiem-thu/">xem ma trận điều kiện chốt và hồ sơ cần ký xác nhận</a>. Nghiệm thu kỹ thuật không đồng nghĩa có hiệu lực văn bản.</p>'
assert 'href="nghiem-thu/"' not in s
s=s.replace(view,view+link,1)
idx.write_text(s,"utf-8")
assert idx.stat().st_size>3_000_000
print("PASS pre-issuance matrix: 10 checks, no unsigned status asserted, 12 tabs intact, 60 flows, 83 documents")
