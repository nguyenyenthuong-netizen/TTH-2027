#!/usr/bin/env python3
"""Doi soat dinh bien, KPI, dau ra va quyen quy trinh tu chinh CSDL khung.
Khong tu suy dien dinh muc/nguoi duyet khi du lieu chua duoc phe duyet.
"""
from pathlib import Path
from collections import Counter
from html import escape
import json
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
path = root / "khung-marketing" / "index.html"
s = path.read_text("utf-8")
m = re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>', s)
if not m:
    raise RuntimeError("Khong tim thay CSDL nguon khung co cau")
d = json.loads(m.group(1))
roles = d["vi_tri"]
ids = {r["id"] for r in roles}
kpis = d.get("kpi_vi_tri", {})
docs = d.get("danh_muc_van_ban", [])
flows = d.get("quy_trinh", [])
steps = [step for q in flows for step in q.get("buoc", [])]
lead_step = Counter(step.get("chu_tri_chinh", "").split("|")[0].strip() for step in steps)
lead_doc = Counter(doc.get("chu_tri", "").split("|")[0].strip() for doc in docs)
flows_by_role = {role_id: [] for role_id in ids}
for flow in flows:
    involved = set()
    for step in flow.get("buoc", []):
        involved.add(str(step.get("chu_tri_chinh", "")).split("|")[0].strip())
        involved.update(str(x).split("|")[0].strip() for x in step.get("thuc_hien", []))
        involved.update(str(x).split("|")[0].strip() for x in step.get("phoi_hop", []))
    for role_id in ids.intersection(involved):
        flows_by_role[role_id].append(flow.get("ten", flow.get("id", "?")))
missing = [r for r in roles if r["id"] not in kpis]
draft = [r for r in roles if r["id"] in kpis and "chưa" in kpis[r["id"]].get("trang_thai_phe_duyet", "").lower()]
approved_note = [r for r in roles if r["id"] in kpis and "đã chốt" in kpis[r["id"]].get("trang_thai_phe_duyet", "").lower()]
has_owner = sum(bool(x.get("chu_tri_chinh")) for x in steps)
current = d.get("phan_dinh_quan_ly_hai_cvt_19112026", {}).get("dinh_bien", {})
roadmap = d.get("lo_trinh_dinh_bien", {}).get("buoc", [])
initial = roadmap[0] if roadmap else {}
current_total = current.get("tong")
initial_total = initial.get("tong")
reconcile = current_total != initial_total

def status_for(r):
    k = kpis.get(r["id"])
    if not k:
        return "Chưa có bảng KPI", "bad"
    st = k.get("trang_thai_phe_duyet", "Chưa xác định phê duyệt")
    if "chưa" in st.lower() or "dự thảo" in st.lower():
        return "Dự thảo, chưa phê duyệt", "warn"
    return "Ghi nhận đã chốt, cần đối chiếu quyết định", "ok"

def pill(label, kind):
    return '<span class="tag ' + kind + '">' + escape(label) + '</span>'

rows = []
for r in roles:
    role_id = r["id"]
    label, kind = status_for(r)
    hours = r.get("gio_ke_hoach") or "Chưa có định lượng trong hồ sơ vị trí"
    output = r.get("phan_dinh_chu_tri_dau_ra") or "Chưa tách đầu ra"
    kpi_n = len(kpis.get(role_id, {}).get("ca_nhan", [])) + len(kpis.get(role_id, {}).get("chung", []))
    involved = flows_by_role[role_id]
    involved_html = "<details><summary>" + str(len(involved)) + " quy trình có ghi tham gia</summary>" + "<ul>" + "".join("<li>" + escape(n) + "</li>" for n in involved) + "</ul></details>" if involved else "Chưa ánh xạ chính xác mã vị trí"
    rows.append(
        "<tr><td><b>" + escape(r.get("ten", role_id)) + "</b><small>" + escape(role_id) + "</small></td>"
        "<td>" + escape(hours) + "</td>"
        "<td>" + pill(label, kind) + "<small>" + str(kpi_n) + " chỉ số trong bảng</small></td>"
        "<td class=num>" + str(lead_step[role_id]) + "</td>"
        "<td class=num>" + str(lead_doc[role_id]) + "</td>"
        "<td>" + involved_html + "</td>"
        "<td>" + escape(output) + "</td></tr>"
    )

alerts = [
    ("Định biên tại mốc đầu", "Chưa thống nhất" if reconcile else "Đã khớp",
     "Sơ đồ hiện tại: " + str(current_total) + " (" + str(current.get("tct")) + " TCT + " + str(current.get("benh_vien")) + " cơ sở); lộ trình tại mốc hiện tại: " + str(initial_total) + " (" + str(initial.get("tct")) + " TCT + " + str(initial.get("co_so")) + " cơ sở). Không tự cộng 2 người vào tất cả mốc."),
    ("KPI theo loại vị trí", str(len(kpis)) + "/" + str(len(roles)),
     "Chưa có: " + ", ".join(x["ten"] for x in missing) + "."),
    ("Trạng thái chỉ tiêu", str(len(draft)) + " bảng chưa phê duyệt",
     str(len(approved_note)) + " bảng có ghi 'đã chốt' cần đối chiếu văn bản chấp thuận; không suy đoán đã áp dụng thưởng."),
    ("Quy trình vận hành", str(len(flows)) + " quy trình / " + str(len(steps)) + " bước",
     str(has_owner) + " bước có trường chủ trì; dữ liệu vẫn có mã chức năng dùng chung, chưa chắc đã ánh xạ tới nhân sự duy nhất."),
    ("Văn bản cần quản lý", str(len(docs)) + " văn bản",
     str(lead_doc["cvt"]) + " văn bản ghi Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở chủ trì xây dựng; " + str(lead_doc["cvt-2"]) + " ghi Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số. Cần tách người chủ trì xây dựng và người chịu trách nhiệm chuyên môn."),
    ("Quản lý nghiệp vụ hai Chuyên viên trưởng", "Cần đồng bộ",
     "Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số chưa được gắn bước chủ trì trong quy trình mẫu; không suy từ đó rằng vị trí này không có trách nhiệm chuyên môn."),
    ("Định lượng giờ công Media cơ sở", "Chưa có đủ dữ liệu",
     "Ngưỡng kế hoạch không đồng nghĩa giờ đã sử dụng hoặc giờ còn dư; phải đối soát nhật ký đầu việc của từng cơ sở."),
    ("Quy trình phải nắm theo vị trí", "Chưa có ma trận nghiệm thu riêng",
     "Quy trình có ghi tham gia không thay thế danh mục bắt buộc phải nắm, cấp độ hiểu/thực hiện, kiểm tra định kỳ và chứng cứ đào tạo."),
    ("Đầu ra & tiêu chuẩn", "Cần chốt theo sản phẩm",
     "Mô tả phạm vi và KPI tỷ trọng chưa thay thế định mức đầu ra theo sản phẩm, độ phức tạp, số lượng, thời gian chuẩn và tiêu chí nghiệm thu.")
]
alert_html = "".join(
    '<div class="audit-card"><strong>' + escape(name) + '</strong><b>' + escape(state) +
    '</b><p>' + escape(note) + '</p></div>' for name, state, note in alerts
)
rows_html = "\n".join(rows)

output_fields = [
    "Mã vị trí, nhóm thương hiệu, cơ sở và người quản lý trực tiếp",
    "Danh mục sản phẩm đầu ra có mã; mức độ phức tạp và đơn vị tính",
    "Nhu cầu theo kỳ và sản lượng giao; tách việc thường xuyên, phát sinh, trọng điểm",
    "Giờ chuẩn cho mỗi loại sản phẩm; giờ thực tế; di chuyển, sửa, chờ duyệt",
    "Năng lực hữu ích theo người, kiêm nhiệm, ca trực, nghỉ phép và dự phòng",
    "Định biên theo từng người/nhóm/cơ sở và kịch bản mở cơ sở",
    "Người yêu cầu, người chủ trì, người phối hợp, người kiểm chuyên môn",
    "Người xác nhận y khoa, nghiệm thu mục tiêu, duyệt phát hành, duyệt chi phí",
    "Chỉ tiêu sản lượng, SLA thời gian xử lý, tỷ lệ đúng hạn, tồn việc và quá hạn",
    "Tỷ lệ đạt ngay lần đầu, số vòng sửa, tỷ lệ lỗi tuân thủ",
    "Kết quả kinh doanh/tiếp cận theo vai trò; không quy công trùng",
    "Ngân sách, chi phí đơn vị sản phẩm, chi phí trên khách hợp lệ",
    "Công thức KPI, trọng số, chỉ tiêu mục tiêu, ngưỡng đạt và chống gian lận",
    "Nguồn dữ liệu, mã chứng cứ, kỳ chốt, người đối soát và người duyệt",
    "Quy trình/văn bản phải nắm, chủ trì xây dựng, kiểm chuẩn, thực hiện; hiệu lực",
    "Người thay thế và điều kiện ủy quyền, bàn giao, thu hồi quyền",
    "Ma trận quy trình bắt buộc phải nắm: tên quy trình, cấp độ, đánh giá và cập nhật",
    "Quy tắc chặn thiếu chứng cứ, vượt quyền, xung đột nhóm hoặc vượt tải",
    "Điều kiện xem xét bổ sung nhân sự, thời điểm đo và cấp phê duyệt"
]
field_html = "".join("<li>" + escape(q) + "</li>" for q in output_fields)

style = """
:root{--blue:#0837A1;--red:#ED3237;--ink:#172B4D;--line:#d8e4f1;--soft:#f3f7fc}
*{box-sizing:border-box}body{margin:0;color:var(--ink);background:var(--soft);font:15px/1.5 Arial,"Segoe UI",sans-serif}
header{padding:22px min(4vw,42px);background:#fff;border-top:6px solid var(--blue);border-bottom:4px solid var(--red)}
header h1{margin:5px 0;color:var(--blue);font-size:clamp(21px,3vw,30px)}header p{margin:3px 0}
header a{color:var(--blue);font-weight:700}
main{padding:15px min(4vw,42px) 50px;max-width:1800px;margin:auto}
section{background:white;border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:16px 0}
h2{font-size:20px;color:var(--blue);margin:0 0 12px}h3{font-size:16px;color:#17406e}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px}
.audit-card{padding:12px;border:1px solid var(--line);border-left:4px solid var(--red);border-radius:10px;background:#fff}
.audit-card strong,.audit-card b{display:block}.audit-card b{color:#ad2b2f}.audit-card p{margin:5px 0 0;font-size:13px}
.table-wrap{overflow-x:auto;width:100%;border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;min-width:1100px}th,td{padding:10px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);font-size:13.5px}
th{background:#eaf1ff;color:#123a80;position:sticky;top:0}td small{display:block;color:#62748a;margin-top:4px}
.num{text-align:center;font-weight:700;white-space:nowrap}.tag{display:inline-block;border-radius:6px;padding:2px 7px;font-weight:700;font-size:12px}
.tag.bad{color:#9c2525;background:#fee8e9}.tag.warn{color:#8f6114;background:#fff3d5}.tag.ok{color:#175b46;background:#eaf8f1}
ul{columns:2;column-gap:30px;padding-left:22px}li{break-inside:avoid;margin-bottom:8px}
.note{font-size:13px;color:#4e6179}
input{width:100%;padding:12px;border:1px solid #a8c1e3;border-radius:8px;margin:0 0 12px;font-size:15px}
@media(max-width:750px){ul{columns:1}section{padding:14px}td,th{font-size:13px}}
"""
html_page = """<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Đối chiếu định biên – Đầu ra – Quy trình | TTH 2027</title><style>""" + style + """</style></head><body>
<header><a href="../">Về Khung cơ cấu Marketing 2027</a><h1>Đối chiếu định biên, sản lượng, KPI và quy trình</h1>
<p>Dữ liệu tự tổng hợp từ nguồn khung cơ cấu hiện hành; là bảng kiểm tính đầy đủ, không phải quyết định định biên hay phê duyệt KPI.</p></header><main>
<section><h2>Các điểm phải đối soát trước khi chốt</h2><div class="cards">""" + alert_html + """</div></section>
<section><h2>Bảng đối chiếu 26 loại vị trí</h2><p class="note">Bước chủ trì = lần xuất hiện của mã vị trí đúng trong trường chủ trì của 407 bước. Văn bản chủ trì = trách nhiệm soạn/quản lý văn bản, không phải toàn bộ trách nhiệm nghiệp vụ. Cột đầu ra là mô tả, chưa phải cam kết sản lượng.</p>
<input id="find" type="search" aria-label="Tìm kiếm vị trí" placeholder="Tìm vị trí, KPI, giờ, đầu ra..."><div class="table-wrap">
<table id="matrix"><thead><tr><th>Vị trí</th><th>Giờ kế hoạch nguồn</th><th>KPI</th><th>Chủ trì bước</th><th>Chủ trì văn bản</th><th>Quy trình đang ghi tham gia</th><th>Đầu ra thuộc phạm vi</th></tr></thead><tbody>""" + rows_html + """</tbody></table></div></section>
<section><h2>19 trường dữ liệu bắt buộc để nghiệm thu định biên và đầu ra</h2><ol>""" + field_html + """</ol></section>
<section><h2>Nguyên tắc chốt</h2><p><b>Không suy từ số suất cơ cấu ra số người phải tuyển.</b> Sản lượng theo định mức chỉ được phê duyệt khi có số giờ thực đo, tiêu chuẩn chất lượng, tỷ lệ việc trọng điểm/phát sinh và năng lực thực tế theo người. Không cộng trùng giờ kiêm nhiệm, không giao hai tuyến quản lý và không lấy chỉ tiêu dự thảo để tính thưởng.</p>
<p class="note">Bảng được tạo lại cùng quy trình xuất bản để thay đổi khi nguồn khung thay đổi; mọi điều chỉnh mốc 34/36/56 phải được đối soát trên cùng một cơ sở tính.</p></section>
</main><script>document.getElementById('find').addEventListener('input',function(){const q=this.value.toLocaleLowerCase('vi');document.querySelectorAll('#matrix tbody tr').forEach(tr=>tr.hidden=!tr.textContent.toLocaleLowerCase('vi').includes(q))})</script>
</body></html>"""
folder = root / "khung-marketing" / "chi-so-dinh-bien"
folder.mkdir(parents=True, exist_ok=True)
(folder / "index.html").write_text(html_page, "utf-8")
if "id=\"tth-dinh-bien-audit-link\"" not in s:
    mark = '<section class="view" data-view="staffing" id="v-staffing">'
    if mark not in s:
        raise RuntimeError("Khong tim thay phan dinh bien de lien ket bang doi chieu")
    insert = ('<div id="tth-dinh-bien-audit-link" style="margin:12px 0;padding:12px 15px;'
              'border-left:4px solid #ED3237;background:#F3F7FC;border-radius:8px">'
              '<strong>Đối soát cơ sở tính định biên và giao chỉ tiêu:</strong> '
              '<a style="font-weight:800;color:#0837A1" href="chi-so-dinh-bien/">'
              'Mở bảng đối chiếu 26 vị trí, KPI, đầu ra, quy trình và tình trạng dữ liệu</a>. '
              'Các mốc 34/36 và KPI chưa duyệt cần thống nhất trước khi ban hành.</div>')
    before = s.index(mark) + len(mark)
    s = s[:before] + insert + s[before:]
    path.write_text(s, "utf-8")
print("MARKETING-QUANT-AUDIT",len(roles),"positions",len(kpis),"KPI sets",
      len(docs),"documents",len(flows),"flows",len(steps),"steps",
      "headcount-conflict",reconcile,"missing-KPI",len(missing),"draft-KPI",len(draft))
