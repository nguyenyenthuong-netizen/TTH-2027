#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit semantic consistency across all 12 parts of TTH Marketing 2027.
Produces an evidence-oriented report; never changes staffing volumes/targets.
"""
from __future__ import annotations
import html as H
import json, re, sys
from pathlib import Path

root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
page=root/"khung-marketing"/"index.html"
s=page.read_text(encoding="utf-8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s)
assert m,"Cannot audit: source CSDL missing"
d=json.loads(m.group(1))
embed=re.search(r'<iframe id="tth-mkt-2027-workframe"[^>]*srcdoc="([^"]+)"',s,re.S)
assert embed,"Cannot audit: annual plan iframe missing"
inside=H.unescape(embed.group(1))
j=re.search(r'<script type="application/json" id="tth-plan-2027-data">([\s\S]*?)</script>',inside)
assert j,"Cannot audit: embedded plan JSON missing"
p=json.loads(j.group(1))
model=d["dinh_bien_theo_dau_ra_2027"]
portfolio=p["portfolio"]
addon=p["ctdaAddendum"]
outcomes=p["yearEndCommitments"]
scope=model["dedup_scope_audit_2027"]
views=re.findall(r'<section class="view" data-view="([^"]+)" id="([^"]+)">',s)
assert len(views)==12,len(views)
assert len(d["vi_tri"])==26 and len(d["quy_trinh"])==60
assert len(model["work"])==273 and len(model["docs"])==171
assert len(portfolio["programs"])==6 and len(portfolio["projects"])==24 and len(portfolio["tasks"])==288
assert len(outcomes["outcomes"])==7 and len(outcomes["monthlyGates"])==84
assert len(addon["outputs"])==132 and len(addon["operations"])==660

idx_base={x["id"]:x["ten"] for x in d["kpi"]}
idx_plan={x["id"]:x["name"] for x in portfolio["kpis"]}
collisions=[dict(id=k,base=idx_base[k],plan=idx_plan[k]) for k in sorted(set(idx_base)&set(idx_plan)) if idx_base[k]!=idx_plan[k]]
crosswalk=portfolio.get("kpiCodeCrosswalk",[])
assert len(crosswalk)==len(idx_plan)==23, "KPI plan crosswalk incomplete"
assert {x["canonicalCode"] for x in crosswalk}==set(idx_plan), "KPI canonical code mismatch"
assert len({x["sourceCode"] for x in crosswalk})==23, "Duplicate source KPI code"
assert all(x.get("equivalentStrategicKpiId") is None for x in crosswalk), "Unverified strategy mapping must remain blank"
zero_seat=[]
for key,headcount in model["seats"].items():
    if headcount!=0:continue
    work=[w for w in model["work"] if w["role"]==key and
          isinstance(w["q"],(int,float)) and w["q"]>0 and sum(w["t"])>0 and w.get("kind")!="G"]
    if work:zero_seat.append(dict(role=key,roleName=model["roles"][key]["name"],activeWork=len(work),sampleCodes=[w["id"] for w in work[:5]]))
unlinked=[x["taskId"] for x in portfolio["tasks"] if not x.get("workloadLedgerId")]
unapproved=[x["projectId"] for x in portfolio["projects"] if x.get("budgetVND") is None or x.get("targetValue") is None]
unknown_stage=[x["stageId"] for x in portfolio["stageRegister"] if x.get("plannedHours") is None]
no_hours=[x["id"] for x in p["monthlyActions"] if x.get("hours") is None]
src_goals={x["id"]:x["ten"] for x in d["muc_tieu_chien_luoc"]}
titles=json.dumps(outcomes["outcomes"],ensure_ascii=False).lower()
gap=["MT5 – thương hiệu nhà tuyển dụng, gắn kết nội bộ",
     "MT3 – khách hiện hữu, tái sử dụng dịch vụ, NPS/CSAT",
     "MT4 – kết quả đối tác và tác động cộng đồng độc lập"]
assert not collisions, "Distinct KPI namespaces must have zero collisions"
assert len(unlinked)==288 and zero_seat
assert scope["candidateOverlapGroups"]>=25
assert scope["mtcvNeedsVerification"]>=476

issues=[
("Ngăn nghiệm thu","01 – Tổng quan / 11 – Phần mềm","Đã tách mã KPI; còn thiếu đối chiếu ý nghĩa",f"{len(crosswalk)} chỉ số kế hoạch có mã riêng KH27-KPI; không còn đụng mã chiến lược. Tuy nhiên chưa được xác nhận tương đương chỉ số gốc.","Duyệt ánh xạ KPI theo định nghĩa, công thức, chủ dữ liệu, số nền, phạm vi và thẩm quyền; không ghép theo số thứ tự.","CSDL KPI 42 và sổ đối chiếu 23 mã kế hoạch"),
("Ngăn ban hành","05 – Định biên / 03 – MTCV","Vị trí không có suất nhưng có giờ kế hoạch","; ".join(f"{x['role']}: {x['activeWork']} đầu việc W có số lượng >0" for x in zero_seat),"Xác nhận ai kiêm nhiệm, tên người và phân bổ giờ vào một quỹ thực tế; không tạo suất mới tự động.","SEATS + W"),
("Ngăn ban hành","05 – Định biên / 11 – Phần mềm","Chưa nối tải hạng mục trọng điểm",f"{len(unlinked)}/288 công việc trọng điểm thiếu workloadLedgerId; {len(addon['operations'])}/660 công đoạn phụ lục thiếu giờ chuẩn hoặc chưa cho phép cộng tải.","Đối chiếu công đoạn với W hiện có; bổ sung giờ cho phần tăng thực chất; chặn tính trùng.","Portfolio và CTDA Addendum"),
("Ngăn ban hành","05 – Định biên / 09 – Lộ trình","Số giờ Clinic kiêm nhiệm chưa chốt","36 suất cơ cấu gồm 1 đầu mối Clinic kiêm nhiệm; gio_phan_bo_clinic hiện để trống.","Tách số vị trí và FTE, xác nhận lịch/giờ người thực hiện tại Khe Tre – A Lưới.","Dữ liệu nhân sự và Mục 05"),
("Thiếu căn cứ","03 – MTCV / 04 – Phân công / 07 – Phối hợp", "Khối lượng MTCV còn phải xác minh",f"{scope['mtcvNeedsVerification']}/496 dòng MTCV cần xác minh; {scope['candidateOverlapGroups']} nhóm nghi giao thoa; {scope['workflowUnverifiedFlagged']}/568 bản ghi bước chưa đủ bằng chứng.","Khóa mã sản phẩm, công đoạn, một chủ trì, một quản lý, phê duyệt và giờ từng người.","Kiểm toán dedup 2027"),
("Thiếu căn cứ","05 – Định biên / 11 – Phần mềm","Giờ cho kế hoạch tháng và giai đoạn còn thiếu",f"{len(no_hours)}/{len(p['monthlyActions'])} dòng kế hoạch tháng không có hours; {len(unknown_stage)}/{len(portfolio['stageRegister'])} giai đoạn chưa có plannedHours.","Định mức phút chuẩn, sản lượng theo độ khó, giờ kiểm/duyệt/di chuyển và thực tế từng tháng.","MonthlyActions và StageRegister"),
("Thiếu căn cứ","01 – Tổng quan / 08 – Vận hành / 11 – Phần mềm","Kết quả năm chưa phủ đầy đủ mục tiêu chiến lược","Có 06 mục tiêu chiến lược, 08 đích quản trị, 07 kết quả năm và 25 chỉ số đề xuất; các nhánh MT3, MT4, MT5 chưa nối đủ kết quả đích.","Đối chiếu 06 mục tiêu/09 chỉ số chỉ đạo với mọi mục tiêu năm và KPI; bổ sung kết quả vòng đời, đối tác, tuyển dụng khi có căn cứ.","Kết quả 2027 và CSDL chiến lược"),
("Thiếu căn cứ","02 – Bộ máy / 04 – Phân công","Một số người chủ kết quả lệch phạm vi nhóm","Mục tiêu T05 giao qlth-a nhưng gồm dự án P11 của nhóm 2; P09 phụ trách kênh hai nhóm nhưng chủ dự án là qc-a.","Chốt một chủ cấp hệ thống và phân nhánh trách nhiệm theo nhóm 1/2; giữ tuyến một quản lý.","Portfolio T05, P09, P11"),
("Đối chiếu lịch sử","09 – Lộ trình / 05 – Định biên","Mốc định biên mở rộng cũ và phương án hiện hành song song","CSDL lịch sử có mốc 34/40/43/50/53/56; hiện hành 36 (22 TCT + 13 BV + 01 Clinic kiêm nhiệm).","Gắn nhãn lịch sử trong mọi bảng, không dùng 56 làm đầu ra mô hình mới nếu chưa tính lại.","Lo_trinh_dinh_bien, phương án 2 CVT"),
("Thiếu căn cứ","10 – Lương thưởng / 12 – Văn bản","Không thể dùng KPI/giờ mô phỏng làm căn cứ chi, thưởng","23 KPI dự án chưa có số nền và đích; 24 dự án chưa khóa ngân sách; 83 văn bản kiểm kê và 60 quy trình chưa mặc nhiên là văn bản đã duyệt.","Giữ trạng thái dự thảo; xác nhận phân cấp, danh mục hiệu lực, sổ quyết định và nguồn dữ liệu.","Hồ sơ kế hoạch, sổ văn bản")
]
counts=dict(views=len(views),roles=len(d["vi_tri"]),seats=sum(model["seats"].values()),workRows=len(model["work"]),documents=len(model["docs"]),mtcvLines=scope["mtcvLines"],mtcvNeedsVerification=scope["mtcvNeedsVerification"],workflowOutputs=scope["workflowOutputs"],workflowUnverified=scope["workflowUnverifiedFlagged"],candidateOverlaps=scope["candidateOverlapGroups"],kpiBase=len(idx_base),kpiPlan=len(idx_plan),kpiCollisions=len(collisions),kpiCrosswalk=len(crosswalk),outcomes=len(outcomes["outcomes"]),outcomeIndicators=sum(len(x["kpis"]) for x in outcomes["outcomes"]),monthlyOutcomeGates=len(outcomes["monthlyGates"]),monthlyPlanRows=len(p["monthlyActions"]),monthlyPlanWithoutHours=len(no_hours),projects=len(portfolio["projects"]),projectTasksWithoutLedger=len(unlinked),stagesWithoutHours=len(unknown_stage),newAddendumOutputCount=len(addon["outputs"]),newAddendumStepsWithoutStandard=sum(x.get("standardHours") is None for x in addon["operations"]),clinicFTEUnknown=d.get("doi_chieu_so_luong_nhan_su_19112026",{}).get("co_so_chi_tiet",{}).get("gio_phan_bo_clinic") is None)
sections=[
("01. Tổng quan","Thiếu kết nối","06 mục tiêu, 08 đích quản trị và 07 kết quả năm chưa có ma trận ánh xạ; MT3, MT4, MT5 chưa phủ đủ."),
("02. Bộ máy","Cơ cấu thống nhất, chứng từ thiếu","22 TCT + 13 bệnh viện + 01 Clinic kiêm nhiệm = 36 vị trí, nhưng không phải 36 FTE xác nhận."),
("03. Mô tả công việc","Cần xác minh","26 chức danh, 496 dòng MTCV; nhiều liên kết sang công đoạn chỉ là tham chiếu."),
("04. Phân công, KPI","Còn điểm chặn","Nhiều vai trò tổng quát cần chọn người, tuyến duyệt, quyền kiểm; chủ mục tiêu một số hạng mục chéo nhóm."),
("05. Định biên","Chưa đủ căn cứ","W tính được tải giả định nhưng còn dòng thiếu mã giờ, 0 suất có W và gián đoạn theo tháng."),
("06. Quan hệ 4 bên","Cơ bản thống nhất","Hai CVT tách quản lý trực tiếp/kiểm chuyên môn; Clinic cần xác nhận quyết định và giờ kiêm nhiệm."),
("07. Phối hợp","Chưa đóng toàn bộ","25 nhóm nguy cơ giao thoa; quy tắc chặn có nhưng chưa có đủ chứng từ áp dụng."),
("08. Luồng vận hành","Cấu trúc đủ, chưa nghiệm thu","60 quy trình – 407 bước – 568 bản ghi; kiểm thử thực tế chưa thể suy từ việc đủ mã."),
("09. Lộ trình","Cần làm rõ lịch sử","Phương án 36 và mốc mở rộng cũ 34→56 tồn tại đồng thời, phải tách bản cũ và tính lại mốc tương lai."),
("10. Lương, thưởng","Chờ phê duyệt","Không được kết toán KPI mới hoặc giờ mô phỏng khi chưa có quy định và chỉ tiêu hiệu lực."),
("11. Phần mềm","Đã tách không gian mã; còn đối chiếu nghiệp vụ","42 KPI chiến lược và 23 KPI kế hoạch không còn trùng mã kỹ thuật; 23 KPI vẫn chưa xác nhận tương đương và 25 KPI kết quả cần đối chiếu."),
("12. Quyết định, văn bản","Chưa ban hành","Tình trạng hồ sơ và thẩm quyền chưa đủ để coi toàn khung là quy chế có hiệu lực.")
]
report=dict(asOf="2026-11-21",status="CHUA_DU_DIEU_KIEN_NGHIEM_THU",source="Trang Khung Marketing 2027 được xây từ CSDL và dữ liệu kế hoạch trong cùng GitHub Pages",counts=counts,issues=[dict(severity=a,scope=b,title=c,detail=e,fix=f,evidence=g) for a,b,c,e,f,g in issues],sections=[dict(section=a,status=b,reason=c) for a,b,c in sections],kpiCollisions=collisions,kpiNamespaceCrosswalk=crosswalk,zeroSeatWork=zero_seat,strategicGaps=gap,interpretation="Các cảnh báo thiếu căn cứ không đồng nghĩa lỗi đã xảy ra trong thực tế. Không thay đổi người, KPI, giờ, ngân sách nếu chưa có dữ liệu và quyết định.")
dst=root/"khung-marketing"/"kiem-toan-toan-khung-2027";dst.mkdir(parents=True,exist_ok=True)
(dst/"bao-cao.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
E=H.escape
rows="".join(f"<tr><td>{E(a)}</td><td><strong>{E(b)}</strong></td><td>{E(c)}</td></tr>" for a,b,c in sections)
details="".join(f"<details><summary><span>{E(a)}</span> · {E(c)}</summary><p><b>Phạm vi:</b> {E(b)}</p><p>{E(e)}</p><p><b>Điều kiện xử lý:</b> {E(f)}</p><p class='source'>{E(g)}</p></details>" for a,b,c,e,f,g in issues)
cells="".join(f'<div class="metric"><b>{value}</b><span>{E(label)}</span></div>' for value,label in [(counts["roles"],"Chức danh"),(counts["seats"],"Suất cơ cấu, gồm kiêm nhiệm"),(counts["kpiCollisions"],"Mã KPI còn trùng"),(counts["candidateOverlaps"],"Nhóm nguy cơ giao thoa"),(counts["projectTasksWithoutLedger"],"Việc trọng điểm thiếu mã giờ"),(counts["monthlyPlanWithoutHours"],"Dòng tháng thiếu giờ")])
pagehtml=f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kiểm toán mâu thuẫn – Khung Marketing TTH 2027</title>
<style>:root{{--blue:#0837A1;--red:#ED3237}}*{{box-sizing:border-box}}body{{font:17px/1.62 Arial,sans-serif;color:#17304d;background:#f4f7fc;margin:0}}header{{background:var(--blue);color:#fff;padding:28px max(22px,calc((100% - 1260px)/2));border-bottom:4px solid var(--red)}}h1{{font-size:30px;line-height:1.3;margin:4px 0 10px}}main{{max-width:1300px;margin:auto;padding:25px}}h2{{font-size:23px;color:var(--blue);margin:24px 0 13px}}.note{{background:#fff;border:1px solid #d5e1f1;border-left:4px solid var(--red);padding:17px 19px;border-radius:7px}}.metrics{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}}.metric{{background:white;border:1px solid #d6e2f0;border-radius:9px;padding:17px}}.metric b{{display:block;font-size:28px;color:var(--blue)}}.metric span{{font-size:15px}}.scroll{{overflow:auto;border:1px solid #d9e2ef;border-radius:9px;max-height:720px}}table{{min-width:1000px;border-collapse:collapse;width:100%;background:#fff}}td,th{{padding:13px 15px;text-align:left;border-bottom:1px solid #e6ebf3;vertical-align:top;font-size:16px}}th{{background:#eaf0fa;position:sticky;top:0}}details{{background:white;margin:10px 0;border:1px solid #d9e3f2;border-radius:9px;padding:14px 18px}}summary{{cursor:pointer;font-size:18px;font-weight:700;color:var(--blue)}}details p{{margin:9px 0}}.source{{color:#576c85;font-size:14px}}a{{color:var(--blue)}}@media(max-width:800px){{.metrics{{grid-template-columns:repeat(2,minmax(0,1fr))}}main{{padding:14px}}}}@media(max-width:520px){{.metrics{{grid-template-columns:1fr}}}} </style></head><body><header><div>TTH GROUP · MARKETING 2027 · KIỂM TOÁN NỘI BỘ</div><h1>Rà soát mâu thuẫn Khung cơ cấu và Mục 05 – Định biên</h1><p>Kết quả từ dữ liệu dựng trang · 21/11/2026 · Chưa đủ điều kiện nghiệm thu</p></header><main><p class="note"><strong>Kết luận:</strong> 12 phần và 26 chức danh có cấu trúc; đã tách mã KPI kỹ thuật nhưng chưa đối chiếu tương đương về nghiệp vụ; tải trọng điểm chưa ánh xạ, thiếu định mức, giờ Clinic và các điều kiện cần kiểm chứng. Không dùng tổng số dòng hoặc số suất cơ cấu làm bằng chứng định biên đã đủ tải.</p><div class="metrics">{cells}</div><h2>Đối soát cả 12 phần</h2><div class="scroll"><table><thead><tr><th>Phần</th><th>Trạng thái</th><th>Căn cứ rà soát</th></tr></thead><tbody>{rows}</tbody></table></div><h2>Điểm chưa thống nhất và điều kiện khóa</h2>{details}<p><a href="bao-cao.json">Dữ liệu kiểm toán JSON</a> · <a href="../../ke-hoach-mkt-2027/doi-chieu-ma-kpi.csv">Sổ 23 mã KPI cần duyệt</a> · <a href="../../ke-hoach-mkt-2027/doi-chieu-tai-288-cong-viec-trong-diem.csv">Sổ đối soát tải 288 việc</a> · <a href="../#dinh-bien-2027">Quay lại Mục 05</a></p><p class="source">Bản kiểm toán không sửa định mức, ngân sách, quyết định nhân sự, hiệu lực quy trình hoặc KPI. Chỉ có xác nhận nghiệp vụ và số liệu nguồn mới được dùng để đóng từng vấn đề.</p></main></body></html>'''
(dst/"index.html").write_text(pagehtml,encoding="utf-8")
entry='<section class="view" data-view="staffing" id="v-staffing">'
assert s.count(entry)==1 and 'kiem-toan-toan-khung-2027/' not in s
link='<p style="margin:12px 18px;padding:14px 18px;background:#f4f7fd;border:1px solid #b5cbea;border-left:4px solid #ED3237;border-radius:9px;font-size:16px;line-height:1.55"><strong>Kiểm toán mâu thuẫn toàn khung:</strong> <a href="kiem-toan-toan-khung-2027/">Mở bảng đối soát 12 phần, Mục 05, 23 mã KPI đã tách và các điều kiện chặn nghiệm thu</a>. Đây là cảnh báo dữ liệu dự thảo, không phải kết quả kiểm soát công việc đã hoàn tất.</p>'
s=s.replace(entry,entry+link,1)
page.write_text(s,encoding="utf-8")
print("PASS AUDIT REPORT:", len(sections),"sections,",len(issues),"open issue groups,",len(collisions),"KPI collisions,",len(zero_seat),"zero-seat workloads,",len(unlinked),"unlinked project tasks.")
