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

# SCENARIO: hospital staffing and output-based estimates; separate proposed planning case from observed volumes.
# Values below are assumptions to be replaced with branch-specific plans and time logs.
SCENARIOS=json.loads(r'''{"general":{"tn-a":[["Tiếp nhận và phân tuyến yêu cầu khoa/phòng",24,0.5],["Tin hoạt động Facebook bệnh viện (biên soạn ngắn/đăng đúng quyền)",12,1.25],["Đối soát thông tin trước phát hành",4,1],["Kế hoạch Marketing cơ sở tháng",1,6],["Giao ban, điều phối lịch và tải",4,2.5],["Điều phối hiện trường sự kiện (khác phần tổ chức của Truyền thông)",3,5],["Thu thập xác nhận chuyên môn và chứng từ",16,0.75],["Báo cáo và đối soát số liệu kỳ",5,1.5]],"mdcs-a":[["V1 – clip tin nhanh tại cơ sở",6,1.5],["V2 – video theo mẫu đã duyệt, bao gồm dựng tại cơ sở",6,5],["V3 – phỏng vấn/câu chuyện theo mẫu, không gồm hậu kỳ vượt mẫu",2,10],["Bộ ảnh/ảnh hiện trường được bàn giao",12,2.5],["Ghi hình sự kiện theo lịch (không tính lại phần dựng)",3,5],["Biên mục, lưu kho và đối chiếu quyền sử dụng tư liệu",18,0.5],["Di chuyển ghi hình theo lệnh điều phối",8,1.5],["Hiệu chỉnh bản dựng theo lượt phản hồi hợp lệ",6,1]],"qhcs":[["Tổ chức hiện trường sự kiện, phối hợp chương trình",3,8],["Vận hành phát thanh và màn hình nội viện theo lịch",4,2.5],["Kiểm tra hiện trạng biển bảng và hồ sơ ảnh",4,2],["Phối hợp bác sĩ/khoa phòng và xác minh nội dung",16,1],["Hoạt động cộng đồng/điểm chạm theo kế hoạch",4,5],["Hồ sơ nghiệm thu, biên bản tại hiện trường",4,2],["Báo cáo nghiệp vụ và bàn giao",5,1.5]]},"specialty":{"tn-b":[["Tiếp nhận yêu cầu khoa/phòng và phân tuyến",16,0.5],["Tin ngắn Facebook bệnh viện theo phân quyền",10,1.25],["Điều phối sự kiện và hoạt động cơ sở",2,8],["Vận hành phát thanh/màn hình nội viện theo lịch",4,2.5],["Kiểm tra hiện trạng biển bảng và ảnh nghiệm thu",4,2],["Kế hoạch Marketing cơ sở tháng",1,6],["Giao ban và điều phối lịch, nhân sự",4,2.5],["Xác minh dữ kiện và phối hợp chuyên môn",12,0.75],["Báo cáo tuần, tháng và đối soát",5,1.5]],"mdcs-b":[["V1 – clip tin nhanh tại cơ sở",4,1.5],["V2 – video theo mẫu B-7 do Media cơ sở dựng",6,5],["V3 – phỏng vấn/câu chuyện trong mẫu B-7",2,10],["Bộ ảnh/chùm ảnh hiện trường",10,2.5],["Ghi hình hoạt động, sự kiện theo lịch",2,5],["Biên mục và lưu kho tư liệu hợp lệ",14,0.5],["Di chuyển ghi hình theo phân công",6,1.5],["Hiệu chỉnh bản dựng sau kiểm kỹ thuật",6,1]]},"clinic":{"dmpk":[["Tổng hợp nhu cầu truyền thông của hai phòng khám",8,0.5],["Gửi ảnh có chứng cứ nguồn và quyền sử dụng",8,0.75],["Cập nhật thông tin cơ sở đã được xác nhận",8,0.5],["Tập hợp tài liệu, giấy đồng ý và hồ sơ chuyển tuyến",4,1],["Phối hợp lịch với Marketing Tổng công ty",4,1],["Hỗ trợ một hoạt động tại phòng khám",1,3]]}}''')
SITES=[
 ("Bệnh viện Đa khoa TTH Vinh","general",3),
 ("Bệnh viện Đa khoa TTH Hà Tĩnh","general",3),
 ("Bệnh viện Đa khoa TTH Quảng Bình","general",3),
 ("Bệnh viện Y học cổ truyền Nguyên Phúc","specialty",2),
 ("Bệnh viện Răng hàm mặt và Phẫu thuật tạo hình thẩm mỹ Thái Thượng Hoàng","specialty",2),
 ("Đầu mối kiêm nhiệm chung TTH Clinic (Khe Tre và A Lưới)","clinic",1),
]
PLAN_HOURS_PER_PERSON=142.0 # Planning capacity referenced in existing framework section 6.
model_rows=[]
site_aggregates=[]
role_aggregates={}
for site,category,people in SITES:
    site_hours=0
    site_people=0
    for role_id,items in SCENARIOS[category].items():
        assert role_id in role_by_id
        site_people+=1
        role_hours=0
        for name,qty,hours_per_unit in items:
            qty=float(qty)
            hours_per_unit=float(hours_per_unit)
            assert qty>0 and hours_per_unit>0
            h=round(qty*hours_per_unit,2)
            role_hours+=h
            site_hours+=h
            model_rows.append([site,category,people,role_id,role_by_id[role_id]["ten"],
                               name,qty,hours_per_unit,h,
                               "GIẢ ĐỊNH THAM CHIẾU – CHƯA XÁC NHẬN",
                               "Kế hoạch nguồn chưa cung cấp sản lượng thực tế theo cơ sở; cơ sở phải điều chỉnh và ký xác nhận"])
        role_aggregates[(site,role_id)]=round(role_hours,2)
    assert site_people==people,(site,site_people,people)
    site_aggregates.append((site,category,people,round(site_hours,2),
                            round(people*PLAN_HOURS_PER_PERSON,2)))
assert len(site_aggregates)==6
assert sum(z[2] for z in site_aggregates)==14 # 13 hospital positions + one clinic concurrent duty.
assert abs(role_aggregates[("Bệnh viện Đa khoa TTH Vinh","tn-a")]-81.5)<0.01
assert abs(role_aggregates[("Bệnh viện Đa khoa TTH Vinh","mdcs-a")]-131)<0.01
assert abs(role_aggregates[("Bệnh viện Đa khoa TTH Vinh","qhcs")]-93.5)<0.01
assert abs(role_aggregates[("Bệnh viện Y học cổ truyền Nguyên Phúc","tn-b")]-87)<0.01
assert abs(role_aggregates[("Bệnh viện Y học cổ truyền Nguyên Phúc","mdcs-b")]-113)<0.01
assert abs(role_aggregates[("Đầu mối kiêm nhiệm chung TTH Clinic (Khe Tre và A Lưới)","dmpk")]-25)<0.01
model_headers=["Cơ sở","Loại cơ sở theo mô hình","Số vị trí trong phương án",
 "Mã vị trí","Tên vị trí","Loại sản phẩm/công việc",
 "Sản lượng dự kiến/tháng – GIẢ ĐỊNH","Giờ chuẩn/đơn vị – GIẢ ĐỊNH",
 "Giờ nhu cầu/tháng – KỊCH BẢN","Trạng thái dữ liệu","Điều kiện sử dụng"]
with (folder/"kich-ban-san-luong-5-benh-vien-va-clinic.csv").open("w",encoding="utf-8-sig",newline="") as fh:
    writer=csv.writer(fh)
    writer.writerow(model_headers)
    writer.writerows(model_rows)

# This is a workload sensitivity scenario, not a validated business-demand forecast.
def fmt_num(val):
    return str(int(val)) if float(val).is_integer() else ("%0.2f"%val).rstrip("0").rstrip(".")
summary_html=[]
for site,category,people,hours,capacity in site_aggregates:
    if category=="clinic":
        cap="-"
        ratio="Kiêm nhiệm, không quy đổi 01 suất toàn thời gian từ 25 giờ mẫu"
    else:
        cap=fmt_num(capacity)
        ratio=fmt_num(round(hours/capacity*100,1))+"% nhu cầu giả định / giờ kế hoạch"
    summary_html.append(
        "<tr><td>"+e(site)+"</td><td class='n'>"+str(people)+
        "</td><td class='n'>"+fmt_num(hours)+"</td><td class='n'>"+cap+
        "</td><td>"+e(ratio)+"</td><td>CHƯA XÁC MINH SẢN LƯỢNG</td></tr>"
    )
detail_html=[]
for site,category,people,hours,capacity in site_aggregates:
    local=[r for r in model_rows if r[0]==site]
    trs="".join("<tr><td>"+e(r[4])+"</td><td>"+e(r[5])+"</td><td class='n'>"+
        fmt_num(r[6])+"</td><td class='n'>"+fmt_num(r[7])+
        "</td><td class='n'>"+fmt_num(r[8])+"</td></tr>" for r in local)
    subsummary="".join(
        "<li>"+e(role_by_id[k]["ten"])+": <b>"+fmt_num(v)+" giờ/tháng</b></li>"
        for (branch,k),v in role_aggregates.items() if branch==site
    )
    detail_html.append("<details><summary>"+e(site)+" – "+fmt_num(hours)+
        " giờ/tháng theo kịch bản</summary><ul>"+subsummary+"</ul><div class='scroll'>"+
        "<table><thead><tr><th>Vị trí</th><th>Sản phẩm/việc</th><th>Số lượng/tháng</th>"+
        "<th>Giờ/đơn vị</th><th>Tổng giờ/tháng</th></tr></thead><tbody>"+trs+
        "</tbody></table></div></details>")
scenario_css="""*{box-sizing:border-box}body{margin:0;font:15px/1.5 Arial,sans-serif;background:#f4f7fc;color:#172a45}
header{background:#fff;border-top:6px solid #0837A1;border-bottom:2px solid #ED3237;padding:20px clamp(16px,4vw,50px)}
h1,h2{color:#0837A1}h1{font-size:clamp(23px,3vw,34px)}h2{font-size:20px}
a{color:#0837A1}main{max-width:1510px;margin:auto;padding:20px clamp(12px,3vw,38px)}
section{border:1px solid #d5e0ec;border-radius:9px;padding:17px;background:white;margin:14px 0}
.note{padding:12px;border-left:4px solid #ED3237;background:#fff7f7;font-weight:600}
.small{color:#52627d;font-size:13px}.scroll{overflow-x:auto;width:100%}table{border-collapse:collapse;width:100%;min-width:900px;font-size:13px}
th,td{padding:9px 11px;border:1px solid #d7e0ec;vertical-align:top;text-align:left}th{color:#0837A1;background:#ecf3ff}
.n{text-align:right;white-space:nowrap}details{padding:13px;border:1px solid #d7e0ec;border-radius:8px;margin:11px 0}
summary{cursor:pointer;color:#0837A1;font-weight:700}ul{padding-left:22px}
@media print{body{background:white;font:14pt "Times New Roman",serif}section,details{break-inside:avoid}table{font-size:10pt}}
"""
scenario_page="""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kịch bản sản lượng, giờ công Marketing cơ sở – 2027</title><style>"""+scenario_css+"""</style></head><body>
<header><a href="../">← Phụ lục 26 vị trí</a><h1>Kịch bản sản lượng và giờ công Marketing cơ sở</h1>
<p>5 bệnh viện (03 đơn vị 3 vị trí và 02 đơn vị 2 vị trí), 01 đầu mối chung kiêm nhiệm TTH Clinic.</p></header><main>
<section><h2>Tổng hợp tính theo số lượng × định mức thời gian</h2>
<p class="note">Đây là <b>KỊCH BẢN ĐỀ XUẤT ĐỂ THỬ TÍNH</b>. Sản lượng, giờ/đơn vị và nhu cầu theo địa điểm được khởi tạo bằng giả định, <b>CHƯA LẤY TỪ NHẬT KÝ SẢN XUẤT CỦA TỪNG BỆNH VIỆN</b>. Không dùng như KPI đã duyệt hoặc bằng chứng định biên 14 suất.</p>
<p>Ngưỡng giờ kế hoạch tham chiếu từ Mục 6: 142 giờ/người/tháng. Số 252/394 giờ trong bảng khung cũ là khả năng phân bổ sau việc cố định theo tính toán nguồn, không phải giờ thực tế còn dư; không cộng thêm một khoản 32 giờ nếu công việc cố định đã nằm trong sản lượng.</p>
<p><a href="../kich-ban-san-luong-5-benh-vien-va-clinic.csv" download>Tải bảng sản lượng – định mức – giờ từng vị trí, từng bệnh viện (CSV)</a>.</p>
<div class="scroll"><table><thead><tr><th>Cơ sở</th><th>Số vị trí</th><th>Giờ nhu cầu kịch bản/tháng</th><th>Giờ kế hoạch</th><th>Đối chiếu</th><th>Trạng thái</th></tr></thead><tbody>"""+
"".join(summary_html)+"""</tbody></table></div></section>
<section><h2>Từng sản phẩm, từng vị trí</h2><p class="small">Các số ban đầu chỉ dùng kiểm tra tính hợp lý. Bệnh viện phải xác nhận nhu cầu thực tế theo kênh, chiến dịch, lượng yêu cầu từ khoa phòng và tính mùa vụ. Không giao thêm sản phẩm chỉ vì còn giờ kế hoạch.</p>"""+
"".join(detail_html)+"""</section>
<section><h2>Điều kiện chốt thành định biên</h2>
<ol><li>Trưởng nhóm và Ban Giám đốc cơ sở xác nhận sản lượng thực tế/sản lượng kế hoạch được giao theo từng sản phẩm và kênh.</li>
<li>Chuyên viên trưởng đúng tuyến đối chiếu giờ trực tiếp và thời gian sửa/kiểm, tách giờ thực địa khỏi giờ hậu kỳ Tổng công ty.</li>
<li>Đối soát giờ thực đo trong kỳ thí điểm và giờ người làm thực tế; tách phần ủy quyền, kiêm nhiệm và dự phòng.</li>
<li>Marketing Tổng công ty cùng Phòng Nhân lực chốt phương pháp và giờ khả dụng theo chế độ lao động; trình cấp có thẩm quyền phê duyệt.</li>
</ol></section></main></body></html>"""
branch_folder=folder/"co-so"
branch_folder.mkdir(parents=True,exist_ok=True)
(branch_folder/"index.html").write_text(scenario_page,encoding="utf-8")
# Make the scenario visible both from appendix and section 5 of the framework.
appendix_index=folder/"index.html"
appendix_html=appendix_index.read_text(encoding="utf-8")
if 'id="tth-branch-production-scenario"' not in appendix_html:
    insert=('<section id="tth-branch-production-scenario"><h2>Ví dụ đã tính sản lượng × giờ công cho Marketing cơ sở</h2>'
            '<p>03 bệnh viện đa khoa: mỗi cơ sở 3 vị trí; 02 bệnh viện chuyên khoa: mỗi cơ sở 2 vị trí; TTH Clinic: đầu mối kiêm nhiệm chung. Các con số đang là <b>kịch bản tham chiếu chưa xác nhận</b>, không phải KPI chính thức.</p>'
            '<p><a href="co-so/">Xem sản lượng từng sản phẩm, từng vị trí tại 5 bệnh viện và TTH Clinic</a> · '
            '<a href="kich-ban-san-luong-5-benh-vien-va-clinic.csv" download>Tải bảng CSV</a></p></section>')
    appendix_html=appendix_html.replace("</main>",insert+"</main>",1)
    appendix_index.write_text(appendix_html,encoding="utf-8")
live=source.read_text(encoding="utf-8")
old='<td>Marketing cơ sở</td><td>02–03/bệnh viện</td><td>02 người còn 252 giờ, 03 người còn 394 giờ sau việc cố định</td><td>Định hướng của Tổng Giám đốc ngày 21/10/2026</td><td>Cần sản lượng</td>'
new='<td>Marketing cơ sở</td><td>02–03/bệnh viện</td><td>02 người 284 giờ; 03 người 426 giờ kế hoạch. Các số 252/394 giờ là năng lực sau việc cố định theo tính toán cũ, không phải giờ dư thực đo.</td><td>Kịch bản khởi tạo từ danh mục đầu ra; phải chốt sản lượng theo kế hoạch từng cơ sở và nhật ký thực tế</td><td><a href="https://nguyenyenthuong-netizen.github.io/TTH-2027/khung-marketing/dinh-muc-26-vi-tri/co-so/" target="_blank" rel="noopener">Xem kịch bản định lượng: 02 vị trí ≈ 200 giờ/tháng; 03 vị trí ≈ 306 giờ/tháng (chưa xác nhận)</a></td>'
assert old in live,"Không tìm được dòng cần sản lượng của Marketing cơ sở trong mục 6"
live=live.replace(old,new,1)
if 'id="tth-role-time-standard-link"' in live and "Kịch bản sản lượng Marketing cơ sở" not in live:
    live=live.replace('id="tth-role-time-standard-link"', 'id="tth-role-time-standard-link"',1)
    hook='<section class="view" data-view="staffing" id="v-staffing">'
    banner='<p style="margin:8px 14px;padding:12px;background:#eaf1ff;border-left:4px solid #0837A1"><strong>Kịch bản sản lượng Marketing cơ sở:</strong> <a href="https://nguyenyenthuong-netizen.github.io/TTH-2027/khung-marketing/dinh-muc-26-vi-tri/co-so/" target="_blank" rel="noopener">Mở bảng tính thử theo từng bệnh viện (02/03 vị trí) và đầu mối TTH Clinic</a>; chưa đủ nhật ký để xác nhận định biên.</p>'
    assert hook in live
    live=live.replace(hook,hook+banner,1)
source.write_text(live,encoding="utf-8")
print("PASS BRANCH SCENARIO: 5 hospitals + 1 shared clinic, total positions=14, scenario rows="+str(len(model_rows)))
for z in site_aggregates:print("CASE",z)
