#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bảng đối chiếu nguồn gốc 60 luồng 2027 với PHỤ LỤC 03 (5.QTQĐ.pdf).
CHỈ đối chiếu tên/phạm vi. Chưa đọc đủ văn bản gốc, chưa xác nhận hiệu lực,
không được tự suy kết luận là xây mới, sửa đổi hay thay thế văn bản cũ.
"""
from pathlib import Path
from html import escape
import json, re, sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
INDEX = ROOT / "khung-marketing" / "index.html"
html = INDEX.read_text("utf-8")
match = re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>', html)
if not match:
    raise RuntimeError("Không tìm thấy CSDL khung")
data = json.loads(match.group(1))
flows = data["quy_trinh"]
assert len(flows) == 60
assert len({q["id"] for q in flows}) == 60

# Giữ nguyên cách ghi của nguồn PDF; không 'sửa' mã trùng và ngày có nghi vấn.
# Trường: (STT trong PDF, Tên trong PDF, Mã, Ngày ghi ở PDF, Phạm vi).
OLD = [
 (1, "Quy định chức năng nhiệm vụ phòng MKT", "QyĐ.02.MKT", "24/01/2025", "Toàn hệ thống"),
 (4, "Quy trình quản lý thông tin website", "QT.07.MKT.TCT", "04/06/2024", "Toàn hệ thống"),
 (5, "Quy trình thiết kế phòng MKT", "QT.06.MKT.TCT", "06/10/2023", "P.MKT"),
 (6, "Quy trình triển khai chạy quảng cáo", "QT05.MKT.TCT", "07/10/2023", "P.MKT"),
 (7, "Quy định nhằm hạn chế rủi ro trang thông tin điện tử, mạng xã hội", "QyĐ.03.MKT.TCT", "28/06/2023", "P.MKT"),
 (8, "Quy trình thu thập dữ liệu dự án", "QT.08.MKT.TCT", "03/07/2024", "P.MKT"),
 (9, "Quy định quản lý sử dụng hình ảnh, nội dung truyền thông của công ty", "QĐ.MKT.01", "31/10/2022", "Toàn hệ thống"),
 (10, "Quy định trực Fanpage", "QyĐ.04.MKT.TCT", "25/06/2024", "Toàn hệ thống"),
 (11, "Quy trình đăng bài lên mạng xã hội", "QT.04.TCT.MKT", "10/02/2023", "Toàn hệ thống"),
 (12, "Quy định trang trí noel, trang trí tết", "QĐ.01.MKT", "12/12/2022", "Toàn hệ thống"),
 (13, "Quy định xây dựng video đăng mạng xã hội", "QyĐ.03.MKT.TCT", "10/06/2023", "Toàn hệ thống"),
 (14, "Quy định chức năng nhiệm vụ phòng MKT", "QyĐ.02.MKT", "24/01/2025", "Toàn hệ thống"),
 (15, "Quy định quản lý hệ thống truyền thông nội viện, bảng biển ngoại viện", "QyĐ.32.MKT", "06/05/2025", "Toàn hệ thống"),
 (16, "Quy định phát triển nội dung giữa phòng MKT TCT và MKT CN", "QyD.03.MKT", "02/06/2025", "Toàn hệ thống"),
 (17, "Quy định phối hợp làm việc bộ phận Media giữa Phòng Marketing TCT và Marketing các chi nhánh", "QyĐ.04.MKT", "19/03/2025", "Toàn hệ thống"),
 (18, "Quy trình tổ chức chương trình, sự kiện", "QT.49.MKT", "6/7/2025", "Toàn hệ thống"),
 (19, "Quy định quản lý dữ liệu ảnh trong quá trình xây dựng bệnh viện", "QyĐ.06.MKT", "22/07/2025", "Toàn hệ thống"),
 (20, "Quy trình về rà soát, cập nhật thông tin, hình ảnh của đơn vị trên website", "QyĐ.02.MKT", "1/7/2025", "Toàn hệ thống"),
 (21, "Quy định về quản lý và vận hành kênh truyền thông online", "QyĐ.05.MKT", "7/15/2025", "Toàn hệ thống"),
 (22, "Quy trình phê duyệt và đăng bài lên Fanpage", "QT.09.MKT", "28/10/2025", "Toàn hệ thống"),
 (23, "Quy trình chụp ảnh và đăng bài truyền thông", "QT.10.MKT", "30/10/2025", "Toàn hệ thống"),
 (24, "Quy trình bảo vệ Fanpage", "QT.11.MKT", "17/12/2025", "Toàn hệ thống"),
 (25, "Quy trình thực hiện chạy quảng cáo Online", "QT.12.MKT", "15/12/2025", "Toàn hệ thống"),
]
assert len(OLD) == 23
OLD_BY_ROW = {x[0]: x for x in OLD}
# Chỉ là ứng viên theo tên và phạm vi của PHỤ LỤC 03, KHÔNG phải đã xác nhận tương ứng.
CANDIDATES = {
 "hang-muc":[18], "yeu-cau-le":[16,17], "tin-trong-ngay":[11,22,23],
 "danh-gia":[7,9,21,24], "co-so-moi":[1,15,16],
 "hang-muc-toan-he-thong":[16,18], "bo-nhan-dien":[5,9,15],
 "hoi-nghi-khoa-hoc":[18], "bien-bang-hong":[15], "website-app":[4,20],
 "tuyen-duoi-tai-tro":[18], "nghi-viec":[24], "phap-luat":[7,21],
 "cong-ty-trong-tap-doan":[16], "kol":[9,18], "su-kien-co-so":[18],
 "tuyen-dung":[11,22], "chuyen-quyen":[21,24], "le-tet":[12,15],
 "chuong-trinh-he-thong":[18], "mao-danh":[7,21,24],
 "ra-soat-noi-dung-y-khoa":[4,20], "phat-thanh-man-hinh":[15],
 "xung-dot-lich":[16,17], "yeu-cau-gap":[16],
 "mua-truyen-thong":[15], "bao-chi-bac-si":[9],
 "noi-bo-phong-ban":[16,18], "ho-tro-lien-co-so":[17],
 "truyen-thong-cheo":[16], "dinh-chinh":[9,11,22],
 "su-co-tai-khoan":[21,24], "btgd-giao-viec":[1],
 "bgd-coso-de-nghi":[1,16], "doi-tac":[18],
 "doi-ten-chuyen-nhom":[5,9], "thanh-tra-kiem-tra":[7,21],
 "tam-ngung-doi-gio":[4,20,21], "phat-truc-tiep":[13,21,22],
 "noi-dung-nguoi-benh":[9,13,23], "he-thong-gian-doan":[4,21],
 "nghien-cuu-thi-truong":[8], "kham-suc-khoe-doanh-nghiep":[18],
 "khao-sat-hai-long":[8], "nguoi-benh-nuoc-ngoai":[4,11],
 "dich-benh-thien-tai":[21], "quang-cao-san-pham":[7,21,25],
 "lich-dang-thang":[10,11,21,22], "quang-cao-tra-phi":[6,25],
 "bao-cao-giao-ban":[1], "nhan-viec-moi":[1,24],
 "dieu-chinh-ke-hoach":[16]
}
assert set(CANDIDATES).issubset({q["id"] for q in flows})
assert all(n in OLD_BY_ROW for nums in CANDIDATES.values() for n in nums)
# Không mặc định một quy định tổng quát đồng nghĩa một luồng đã có quy trình tương ứng.
records = []
for i,q in enumerate(flows,1):
    candidates = [OLD_BY_ROW[n] for n in CANDIDATES.get(q["id"], [])]
    records.append({
      "stt":i,"ma_2027":q["id"],"ten_2027":q["ten"],
      "ung_vien_cu":[{"stt_phu_luc":x[0],"ten":x[1],"ma":x[2],"ngay":x[3],"pham_vi":x[4]} for x in candidates],
      "tinh_trang_tim_kiem":("Có văn bản liên quan theo tên/phạm vi" if candidates else "Chưa tìm thấy trong Phụ lục 03"),
      "tinh_trang_hieu_luc":"Chưa kiểm tra văn bản gốc và quyết định thay thế",
      "ket_luan_xu_ly":"Chờ đối chiếu hồ sơ gốc: giữ nguyên / sửa / gộp / bãi bỏ / xây mới",
      "can_lam":"Thu thập bản gốc, kiểm tra điều khoản, mã & phiên bản, hiệu lực, trách nhiệm theo cơ cấu 2027"
    })
assert len(records)==60
count_related=sum(bool(x["ung_vien_cu"]) for x in records)
count_no=60-count_related

def e(x):return escape(str(x),quote=True)
def display_old(arr):
    if not arr:return '<span class="warn">Chưa tìm thấy mục tương ứng trong danh mục đã có</span>'
    return "<ul class=\"old-docs\">"+"".join(
      "<li><b>"+e(x["ten"])+"</b><small>STT "+str(x["stt_phu_luc"])+
      " · Mã ghi trong danh mục: "+e(x["ma"])+" · Ngày: "+e(x["ngay"])+
      " · "+e(x["pham_vi"])+"</small></li>" for x in arr)+"</ul>"

headers=["STT","Luồng vận hành 2027","Văn bản cũ có thể liên quan (theo Phụ lục 03)","Nhận định sơ bộ","Hiệu lực văn bản cũ","Hướng xử lý sau đối chiếu","Bằng chứng cần bổ sung"]
rows=[]
for r in records:
    rows.append("<tr data-kind=\""+("related" if r["ung_vien_cu"] else "notfound")+"\">"
      +"<td>"+str(r["stt"])+"</td>"
      +"<td><b>"+e(r["ten_2027"])+"</b><small>Mã luồng: "+e(r["ma_2027"])+"</small></td>"
      +"<td>"+display_old(r["ung_vien_cu"])+"</td>"
      +"<td>"+e(r["tinh_trang_tim_kiem"])+"</td>"
      +"<td>"+e(r["tinh_trang_hieu_luc"])+"</td>"
      +"<td>"+e(r["ket_luan_xu_ly"])+"</td>"
      +"<td>"+e(r["can_lam"])+"</td></tr>")
table="<table class=\"process-compare-table\"><thead><tr>"+"".join("<th>"+e(x)+"</th>" for x in headers)+"</tr></thead><tbody>"+"".join(rows)+"</tbody></table>"
note=(
 "<p><b>Nguyên tắc:</b> 60 luồng 2027 chưa mặc nhiên là 60 quy trình mới. "
 "Ứng viên cũ được ghép theo tên và phạm vi <b>chưa có đối chiếu nội dung toàn văn</b>; "
 "chưa có kết luận giữ nguyên, sửa đổi, hợp nhất, bãi bỏ hoặc xây mới.</p>"
 "<p><b>Nguồn cũ:</b> Phụ lục 03 – Danh mục quy trình áp dụng Phòng Marketing (tệp 5.QTQĐ.pdf, 1 trang; "
 "mục 1 và 4–25, thiếu số 2–3). Cần yêu cầu bộ văn bản đầy đủ và hồ sơ hiệu lực.</p>"
 "<p><b>Cảnh báo chất lượng nguồn:</b> Mục 1 và 14 trùng; QyĐ.02.MKT xuất hiện với tên khác tại mục 20; "
 "QyĐ.03.MKT.TCT xuất hiện tại mục 7 và 13 cho hai nội dung khác nhau; "
 "ngày mục 21 được ghi “7/15/2025” không đúng cách ghi ngày thông thường. "
 "Giữ nguyên theo danh mục nguồn, chờ xác minh với đơn vị quản lý văn bản.</p>"
)
css="""
.tth-process-compare{margin:20px 0;padding:16px;border:1px solid #c9d9e9;border-left:5px solid #0837A1;border-radius:12px;background:#fff;color:#172B4D}
.tth-process-compare h3{font-size:20px;color:#0837A1;margin:0 0 8px}
.tth-process-compare p{font-size:14px;line-height:1.55;margin:8px 0}
.tth-process-compare a{color:#0837A1;font-weight:800;text-decoration:underline}
.tth-process-compare summary{cursor:pointer;font-weight:700;padding:10px 4px}
.tth-process-compare .compare-wrap{overflow-x:auto;max-width:100%}
.process-compare-table{border-collapse:collapse;min-width:1320px;width:100%;background:#fff;font-size:13px}
.process-compare-table th,.process-compare-table td{border:1px solid #d7e1ed;padding:10px 9px;text-align:left;vertical-align:top}
.process-compare-table th{position:sticky;top:0;background:#e9f1ff;color:#09347f}
.process-compare-table td:first-child{font-weight:800;text-align:center}
.process-compare-table small{display:block;margin-top:6px;font-size:12px;color:#4d6078}
.process-compare-table .old-docs{list-style:none;margin:0;padding:0}
.process-compare-table .old-docs li{margin:0 0 9px}
.process-compare-table .warn{color:#8b5a12;font-weight:700}
"""
mainPanel=(
 '<div id="tth-process-compare-2027" class="tth-process-compare">'
 '<h3>Đối chiếu 60 luồng vận hành 2027 với quy trình, quy định cũ</h3>'
 '<p>Đã đưa vào bảng <b>60/60 luồng</b>. Có <b>'+str(count_related)+'</b> luồng tìm thấy văn bản có thể liên quan '
 'theo tên/phạm vi; <b>'+str(count_no)+'</b> chưa tìm thấy trong Phụ lục 03. Đây <b>không phải kết luận hiệu lực</b>.</p>'
 '<p><a href="doi-chieu-quy-trinh/">Mở bảng đối chiếu đầy đủ, có tìm kiếm và lọc (60 dòng)</a></p>'
 '<details><summary>Xem trực tiếp bảng 60 dòng trong Khung cơ cấu</summary>'
 +note+'<div class="compare-wrap">'+table+'</div></details></div>'
)
if 'id="tth-process-compare-2027"' in html:
    raise RuntimeError("Bảng đối chiếu đã được chèn từ trước")
marker='<div id="ops-root"></div>'
if html.count(marker)!=1:
    raise RuntimeError("Không tìm thấy điểm chèn Phần 08")
html=html.replace(marker,mainPanel+marker,1)
# Giữ 12 tab không đổi, thêm liên kết ở Phần 12 để người trình duyệt tìm được phụ lục.
dec='<section class="view" data-view="decisions" id="v-decisions">'
if html.count(dec)!=1: raise RuntimeError("Không tìm thấy phần 12")
html=html.replace(dec,dec+
 '<div class="tth-process-compare"><b>Đối chiếu quy trình cũ và cơ cấu 2027:</b> '
 '<a href="doi-chieu-quy-trinh/">Mở phụ lục 60 luồng, mã và ngày văn bản liên quan, trạng thái hiệu lực</a>. '
 'Chưa có kết luận thay thế/ban hành mới khi chưa kiểm tra văn bản gốc.</div>',1)
if "</head>" not in html:raise RuntimeError("HTML thiếu head")
html=html.replace("</head>","<style>"+css+"</style></head>",1)
INDEX.write_text(html,"utf-8")
out=ROOT/"khung-marketing"/"doi-chieu-quy-trinh"
out.mkdir(parents=True,exist_ok=True)
standalone='''<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Đối chiếu 60 luồng 2027 với quy trình cũ | TTH Group</title>
<style>:root{--blue:#0837A1;--red:#ED3237;--ink:#172B4D;--line:#d7e1ed}*{box-sizing:border-box}
body{margin:0;background:#f3f6fb;font:15px/1.55 "Segoe UI",Arial,sans-serif;color:var(--ink)}
header{background:#fff;border-top:6px solid var(--blue);border-bottom:3px solid var(--red);padding:18px 4vw}
header h1{font-size:clamp(22px,3vw,31px);margin:8px 0;color:var(--blue)}
header a{color:var(--blue);font-weight:700}
main{max-width:1900px;margin:auto;padding:20px 4vw 65px}
section{background:white;border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:15px}
section h2{font-size:20px;color:var(--blue);margin:0 0 8px}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}
.controls input,.controls select{font:inherit;padding:11px 12px;border:1px solid #a7c2df;border-radius:8px;background:#fff;min-width:220px}
.controls input{flex:1}
.counter{font-weight:700;color:var(--blue)}
.table-scroll{overflow:auto;max-height:78vh;border:1px solid var(--line)}
'''+css+'''</style></head><body>
<header><a href="../">Về Khung cơ cấu Marketing 2027</a><h1>Phụ lục đối chiếu quy trình cũ – luồng 2027</h1>
<p>Ma trận làm việc để xác minh văn bản hiện hành; không phải quyết định ban hành, sửa đổi hoặc bãi bỏ.</p></header>
<main><section><h2>Phạm vi và trạng thái đối chiếu</h2>
<p><b>60</b> luồng năm 2027; <b>'''+str(count_related)+'''</b> có văn bản có thể liên quan theo danh mục cũ; <b>'''+str(count_no)+'''</b> chưa tìm thấy trong tài liệu nguồn này. Cả hai nhóm đều phải kiểm tra toàn văn và hiệu lực.</p>
'''+note+'''</section><section><h2>Bảng chi tiết theo từng luồng</h2>
<div class="controls"><input id="search" type="search" placeholder="Tìm tên luồng, mã quy trình cũ, nội dung...">
<select id="kind" aria-label="Lọc tình trạng"><option value="all">Tất cả 60 luồng</option>
<option value="related">Có văn bản có thể liên quan</option><option value="notfound">Chưa tìm thấy trong Phụ lục 03</option></select></div>
<p class="counter" id="count"></p><div class="table-scroll">'''+table+'''</div></section></main>
<script>
const rows=[...document.querySelectorAll(".process-compare-table tbody tr")];
const s=document.getElementById("search"), k=document.getElementById("kind"), c=document.getElementById("count");
function apply(){let n=0,needle=s.value.trim().toLocaleLowerCase("vi");
for(const r of rows){let show=(k.value==="all"||r.dataset.kind===k.value)&&r.textContent.toLocaleLowerCase("vi").includes(needle);r.hidden=!show;if(show)n++}
c.textContent="Đang hiển thị "+n+" / "+rows.length+" luồng";}
s.addEventListener("input",apply);k.addEventListener("change",apply);apply();
</script></body></html>'''
(out/"index.html").write_text(standalone,"utf-8")
(out/"doi-chieu-60-luong.json").write_text(json.dumps({
 "nguon":"5.QTQĐ.pdf – Phụ lục 03 Danh mục quy trình áp dụng Phòng Marketing",
 "nguyen_tac":"Chưa đối chiếu toàn văn hoặc hiệu lực. Ứng viên theo tên/phạm vi, không tự xác nhận mới hoặc thay thế.",
 "danh_muc_van_ban_cu":[{"stt":x[0],"ten":x[1],"ma":x[2],"ngay_ghi_nguon":x[3],"pham_vi":x[4]} for x in OLD],
 "doi_chieu":records
},ensure_ascii=False,indent=2),"utf-8")
# Kiểm thử tĩnh: không phát sinh tab thứ 13, 60 dòng, 23 mục nguồn, link có thật.
assert html.count('<button class="tab"')==12
assert len(re.findall(r'<tr data-kind="(?:related|notfound)">',standalone))==60
assert standalone.count("QyĐ.02.MKT")>=3
print("PASS: 60 luồng; "+str(count_related)+" có ứng viên; "+str(count_no)+" chưa thấy trong danh mục; 23 văn bản ghi nguồn; 12 tab được giữ nguyên")
