#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""26-role workload/standard-time audit, generated from live TTH 2027 framework.
No fabricated quantities, timings, headcount or formal approvals.
568 workflow-output records are leads for product-type consolidation, NOT 568 product standards.
"""
from pathlib import Path
from collections import Counter, defaultdict
from html import escape
import csv
import json
import re
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
source=root/"khung-marketing"/"index.html"
html=source.read_text(encoding="utf-8")
match=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',html)
assert match, "Khong thay CSDL khung"
D=json.loads(match.group(1))
roles=D["vi_tri"]
flows=D["quy_trinh"]
assert len(roles)==26 and len(flows)==60,(len(roles),len(flows))
assert len({r["id"] for r in roles})==26
role_by_id={r["id"]:r for r in roles}

records=[]
for flow in flows:
    for step_index,step in enumerate(flow["buoc"],1):
        actors=step.get("thuc_hien",[])
        contracts=step.get("doi_soat_tung_dau_ra_2027",[])
        assert len(actors)==len(contracts),(flow.get("id"),step_index,len(actors),len(contracts))
        for actor,contract in zip(actors,contracts):
            rid=str(actor).split("|",1)[0].strip()
            records.append({
                "id":contract["ma_dau_ra"],
                "flow":flow.get("ten",flow.get("id","")),
                "step":step_index,
                "actor":rid,
                "role":role_by_id.get(rid,{}).get("ten","CHƯA GẮN VÀO 26 MÃ VỊ TRÍ"),
                "deliverable":str(contract.get("dien_giai","")),
                "responsible":str(contract.get("chu_tri_01","")),
                "line":str(contract.get("tuyen_quan_ly_01","")),
                "approval":str(contract.get("quyen_duyet_cuoi_01","")),
                "accounting":str(contract.get("cach_hach_toan_tai_01","")),
            })
assert len(records)==568 and len({r["id"] for r in records})==568
per_role=defaultdict(list)
for rec in records:per_role[rec["actor"]].append(rec)
assigned=sum(len(per_role[r["id"]]) for r in roles)
unmapped=len(records)-assigned
folder=root/"khung-marketing"/"dinh-muc-26-vi-tri"
folder.mkdir(parents=True,exist_ok=True)

# SUMMARY: all 26 kinds of job position, not necessarily 26 currently staffed posts.
summary_headers=[
 "Mã vị trí","Tên vị trí","Giờ kế hoạch trong nguồn (chỉ tham khảo)",
 "Phạm vi sản phẩm/đầu ra theo MTCV","Số bản ghi đầu ra gắn mã vị trí trong 568 bản ghi",
 "Danh mục loại sản phẩm chuẩn đã được phê duyệt","Số lượng sản phẩm / kỳ",
 "Định mức phút / sản phẩm theo độ phức tạp","Giờ thực đo / kỳ",
 "Giờ di chuyển / phối hợp / kiểm tra / sửa","Giờ làm việc hữu ích / người / kỳ",
 "Số suất đề xuất cho vị trí","Định biên theo tải đã tính","Trạng thái kiểm chứng","Người xác nhận"
]
summary_rows=[]
for role in roles:
    summary_rows.append([
        role["id"],role["ten"],role.get("gio_ke_hoach",""),
        role.get("phan_dinh_chu_tri_dau_ra",""),len(per_role[role["id"]]),
        "CHƯA CHỐT","","","","","","","","CHƯA ĐỦ DỮ LIỆU",""
    ])
with (folder/"tong-hop-26-vi-tri.csv").open("w",newline="",encoding="utf-8-sig") as file:
    wr=csv.writer(file)
    wr.writerow(summary_headers)
    wr.writerows(summary_rows)

# WORKING LOG: do not equate an individual workflow step with a normalized product.
detail_headers=[
 "Mã đầu ra trong quy trình","Tên quy trình","Bước","Mã vai trò ghi thực hiện",
 "Tên vị trí (nếu ánh xạ được)","Đầu ra ở bước nghiệp vụ",
 "Chủ trì/tuyến quản lý theo dự thảo","Cửa phê duyệt","Nguyên tắc tính giờ",
 "Mã loại sản phẩm sau khi chuẩn hóa","Đơn vị tính sản phẩm",
 "Độ phức tạp","Sản lượng yêu cầu / tháng","Phút chuẩn / đơn vị",
 "Giờ trực tiếp thực hiện","Giờ phối hợp/kiểm/duyệt/sửa",
 "Giờ di chuyển/ngoại lệ","Giờ thực đo có chứng từ",
 "Ngày/kỳ xác minh","Người xác nhận","Trạng thái"
]
detail_rows=[]
for rec in records:
    detail_rows.append([
        rec["id"],rec["flow"],rec["step"],rec["actor"],rec["role"],
        rec["deliverable"],rec["responsible"]+" | "+rec["line"],
        rec["approval"],rec["accounting"],
        "","","","","","","","","","","","CHƯA ĐỊNH MỨC"
    ])
with (folder/"doi-soat-568-dau-ra-de-do-gio.csv").open("w",newline="",encoding="utf-8-sig") as file:
    wr=csv.writer(file)
    wr.writerow(detail_headers)
    wr.writerows(detail_rows)

# Browser-based review. Data fields intentionally remain blank until measured and signed.
def e(value):return escape(str(value or ""),quote=True)
def txtshort(value,length=170):
    value=str(value or "")
    return e(value[:length]+("…" if len(value)>length else ""))
rows=[]
for idx,role in enumerate(roles,1):
    rid=role["id"]
    count=len(per_role[rid])
    rows.append(
        '<tr><td class="numeric">'+str(idx)+'</td><td><a href="#vt-'+e(rid)+'"><strong>'+
        e(role["ten"])+'</strong></a><small>'+e(rid)+'</small></td><td>'+
        e(role.get("gio_ke_hoach","Chưa định lượng"))+'</td><td>'+
        txtshort(role.get("phan_dinh_chu_tri_dau_ra","Chưa mô tả"))+'</td><td class="numeric">'+
        str(count)+'</td><td><span class="pending">CHƯA ĐỦ DỮ LIỆU</span></td></tr>'
    )
sections=[]
for role in roles:
    rid=role["id"]
    items=per_role[rid]
    itemrows="".join(
        "<tr><td>"+e(t["id"])+"</td><td>"+e(t["flow"])+"</td><td>"+
        e(t["deliverable"])+"</td><td>"+e(t["approval"])+
        "</td><td>Chưa phân loại sản phẩm</td><td>Chưa có</td><td>Chưa có</td></tr>"
        for t in items
    )
    if not itemrows:
        itemrows='<tr><td colspan="7">Chưa ánh xạ được bản ghi đầu ra trực tiếp với mã vị trí này. Phải kiểm tra thực tế và hồ sơ phân công.</td></tr>'
    sections.append(
        '<details id="vt-'+e(rid)+'"><summary>'+e(role["ten"])+' <span>('+
        str(len(items))+' bản ghi đầu ra gắn mã)</span></summary>'
        '<p><b>Giờ kế hoạch đã nêu trong hồ sơ:</b> '+e(role.get("gio_ke_hoach") or "Chưa có")+'</p>'
        '<p><b>Trách nhiệm đầu ra theo MTCV:</b> '+e(role.get("phan_dinh_chu_tri_dau_ra") or "Chưa có")+'</p>'
        '<p class="small">Danh mục bên dưới là đầu ra ở bước quy trình, KHÔNG phải sản lượng định mức. Phải nhóm thành sản phẩm chuẩn trước khi ấn định số lượng và phút/đơn vị.</p>'
        '<div class="scroll"><table><thead><tr><th>Mã đầu ra</th><th>Quy trình</th><th>Nội dung đầu ra</th><th>Cửa duyệt</th>'
        '<th>Loại sản phẩm chuẩn</th><th>Sản lượng</th><th>Phút chuẩn</th></tr></thead><tbody>'+
        itemrows+'</tbody></table></div></details>'
    )
css=r"""*{box-sizing:border-box}body{margin:0;color:#20304a;background:#f4f7fc;font:15px/1.55 Arial,"Segoe UI",sans-serif}
header{background:#fff;border-top:6px solid #0837A1;border-bottom:2px solid #ED3237;padding:21px max(16px,3vw)}
main{max-width:1530px;margin:auto;padding:18px max(13px,2vw) 50px}
h1,h2{color:#0837A1}h1{font-size:clamp(24px,2.6vw,33px);margin:9px 0}
h2{font-size:20px}a{color:#0837A1}article,section{background:#fff;border:1px solid #d4dfec;border-radius:9px;padding:18px;margin:13px 0}
.head{display:flex;gap:9px;flex-wrap:wrap}.head a{display:inline-block;border:1px solid #a6bee1;border-radius:7px;padding:10px;text-decoration:none;font-weight:700}
.warn{border-left:4px solid #ED3237;padding:11px 14px;background:#fff8f8;font-weight:600}
.scroller,.scroll{overflow-x:auto;width:100%}table{border-collapse:collapse;width:100%;min-width:950px;font-size:13px}
td,th{padding:9px 11px;border:1px solid #d5dfeb;vertical-align:top;text-align:left}th{background:#edf3ff;white-space:nowrap;color:#0837A1}
.numeric{text-align:center}small,.small{font-size:12px;color:#607089;display:block}
.pending{font-size:11px;color:#9a3d14;background:#fff0df;padding:3px 5px;border-radius:5px;font-weight:700;white-space:nowrap}
details{border:1px solid #d5dfeb;border-radius:8px;margin:11px 0;padding:12px}summary{cursor:pointer;font-weight:700;color:#0837A1;font-size:16px}
summary span{color:#64718a;font-weight:400}details p{margin:9px 0}
footer{text-align:center;color:#617187;font-size:12px;padding:0 18px 28px}
@media(max-width:760px){table{min-width:850px}td,th{font-size:12px}h1{font-size:22px}section{padding:13px}}
@media print{body{background:white;font:14pt "Times New Roman",serif}h1,h2{color:#111}section,article{break-inside:avoid}table{font-size:10pt}}
"""
page="""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Định mức sản phẩm và giờ công – 26 vị trí Marketing TTH 2027</title>
<style>"""+css+"""</style></head><body><header><a href="../">← Về Khung cơ cấu Marketing 2027</a>
<h1>Đối soát sản phẩm đầu ra và định mức thời gian – 26 loại vị trí</h1>
<p>Hồ sơ chuẩn bị tính định biên theo từng vị trí. Phạm vi: 26 loại vị trí trong khung, 60 luồng, 568 bản ghi đầu ra.</p></header><main>
<section><h2>Trạng thái và điều kiện tính định biên</h2>
<p class="warn">CHƯA ĐỦ ĐIỀU KIỆN KẾT LUẬN ĐỊNH BIÊN TỪNG VỊ TRÍ: chưa chốt sản lượng theo sản phẩm chuẩn, phút/giờ chuẩn, giờ thực đo, phân loại mức độ và số giờ khả dụng xác minh. Giờ kế hoạch của hồ sơ cũ chỉ mang tính tham khảo.</p>
<p>26 là số <b>loại vị trí</b>, không phải 26 nhân sự; gồm cả vị trí theo điều kiện mở rộng và kiêm nhiệm. 568 là <b>bản ghi đầu ra theo bước quy trình</b>, không đồng nghĩa 568 loại sản phẩm phải giao.</p>
<p><b>Cách tính sau khi đủ dữ liệu:</b> Giờ cần = tổng theo sản phẩm (sản lượng × phút chuẩn / 60) + giờ quản trị, phối hợp, kiểm duyệt, sửa, di chuyển và ngoại lệ không trùng lặp. Số suất = giờ cần / giờ làm việc hữu ích thực tế/người/kỳ; kiểm tra biến động kỳ, người kiêm nhiệm và mức dự phòng trước khi làm tròn.</p>
<div class="head"><a href="tong-hop-26-vi-tri.csv" download>Tải bảng tổng hợp 26 vị trí (CSV)</a>
<a href="doi-soat-568-dau-ra-de-do-gio.csv" download>Tải bảng 568 đầu ra để phân loại và đo giờ (CSV)</a>
<a href="../chi-so-dinh-bien/">Mở báo cáo đối soát định biên</a></div></section>
<section><h2>Ma trận tổng hợp 26 vị trí</h2>
<p>Chọn chức danh để xem phạm vi công việc và các bản ghi đầu ra theo vai trò. Chỗ chưa có số liệu phải để trống khi xuất bảng, không tự dùng các ước tính cũ để kết luận.</p>
<div class="scroller"><table><thead><tr><th>STT</th><th>Vị trí</th><th>Giờ kế hoạch nguồn</th><th>Trách nhiệm sản phẩm</th><th>Bản ghi gắn mã</th><th>Kết quả tính tải</th></tr></thead><tbody>"""+''.join(rows)+"""</tbody></table></div></section>
<section><h2>Đầu ra theo từng chức danh</h2>"""+''.join(sections)+"""</section>
<section><h2>Bước cần chốt để bảo vệ định biên trước Ban Tổng Giám đốc</h2>
<ol><li>Trưởng phòng, hai Chuyên viên trưởng và Tổ trưởng thống nhất <b>mã sản phẩm</b>, mức độ phức tạp, người chịu trách nhiệm và tiêu chuẩn nghiệm thu cho từng chức danh.</li>
<li>Từng vị trí/cơ sở ghi <b>sản lượng dự kiến theo tháng, quý và năm</b>, phân biệt thường xuyên, trọng điểm, phát sinh và việc theo đợt.</li>
<li>Đo giờ trực tiếp, sửa, đợi duyệt, điều phối và di chuyển bằng <b>một mã việc – một người – một loại giờ</b>; loại trừ trùng lặp với giờ quản trị cấp trên.</li>
<li>Phòng Nhân lực đối soát <b>giờ khả dụng/người</b>, chế độ làm việc, kiêm nhiệm, ngày nghỉ và lộ trình nhân sự; Marketing lập phép tính theo từng vị trí/cơ sở.</li>
<li>Trưởng phòng tổng hợp, các đầu mối xác nhận và trình Ban Tổng Giám đốc trước khi kết luận định biên 36 suất theo năng suất.</li></ol>
<p class="small">Đây là tài liệu và bảng thu thập dữ liệu phục vụ xác minh. Chưa phải mẫu đã phê duyệt hoặc kết quả phân bổ biên chế được ban hành.</p></section>
</main><footer>TTH GROUP • Marketing 2027 • Trang đối soát công việc, thời gian và đầu ra</footer></body></html>"""
(folder/"index.html").write_text(page,"utf-8")

# Link directly to GitHub-hosted appendix: current Vercel project redirects only some paths.
link='<div id="tth-role-time-standard-link" style="margin:12px 0;padding:13px 15px;border-left:4px solid #ED3237;background:#F3F7FC;border-radius:8px"><strong>Định mức sản phẩm và thời gian theo TOÀN BỘ 26 loại vị trí:</strong> <a style="font-weight:800;color:#0837A1" href="https://nguyenyenthuong-netizen.github.io/TTH-2027/khung-marketing/dinh-muc-26-vi-tri/" target="_blank" rel="noopener">Mở bảng chi tiết và tải 02 phụ lục CSV</a>. <b>Trạng thái:</b> có giờ kế hoạch và đầu ra nguồn; chưa đủ sản lượng, phút chuẩn và giờ thực đo để xác nhận từng suất định biên.</div>'
if 'id="tth-role-time-standard-link"' not in html:
    at='<section class="view" data-view="staffing" id="v-staffing">'
    assert at in html,"Không thấy phần Định biên của khung"
    html=html.replace(at,at+link,1)
    source.write_text(html,encoding="utf-8")
# Verification.
with (folder/"tong-hop-26-vi-tri.csv").open(encoding="utf-8-sig",newline="") as file:
    assert len(list(csv.reader(file)))==27
with (folder/"doi-soat-568-dau-ra-de-do-gio.csv").open(encoding="utf-8-sig",newline="") as file:
    assert len(list(csv.reader(file)))==569
assert len(sections)==26 and len(rows)==26
print("PASS ROLE LOAD STANDARD AUDIT: roles=26, outputs=568, assigned="+str(assigned)+", other="+str(unmapped)+", all estimates clearly unverified")
