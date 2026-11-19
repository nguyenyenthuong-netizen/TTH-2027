#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm thử tình huống NGHIỆP VỤ giả lập dựa trên đúng 568 đầu ra của đề án.

Đây không phải giao dịch thật đã thực hiện trên hệ thống nội bộ; không tạo
quyết định phân quyền mới và không coi chứng từ giả lập là có hiệu lực.
"""
import json,sys,re
from pathlib import Path
from html import escape
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s);assert m
D=json.loads(m.group(2))
Q={q["id"]:q for q in D["quy_trinh"]}
REG={v["id"] for v in D["vi_tri"]}

def eval_case(c):
 q=Q[c["flow"]]
 b=q["buoc"][c["step"]-1]
 assert len(b["doi_soat_tung_dau_ra_2027"])==len(b["thuc_hien"])
 record=b["doi_soat_tung_dau_ra_2027"][c["actor"]-1]
 owner_map=record["ma_chu_tri_theo_nhom"]
 issues=[]
 if len(owner_map)==2:
    if c.get("group") not in ("nhom_1","nhom_2"):
        issues.append("Chưa chốt nhóm thương hiệu")
        owner=None
    else:owner=owner_map[c["group"]]
 else:owner=owner_map["co_dinh"]
 if owner is not None and c.get("owner_role",owner)!=owner:
    issues.append("Người được giao không thuộc đúng vai trò đầu ra")
 if not c.get("person_id"):
    issues.append("Chưa xác định người chịu trách nhiệm chính")
 if c.get("checker_id")==c.get("person_id") and c.get("need_independent_check",False):
    issues.append("Một người vừa làm vừa tự kiểm")
 if b.get("can_nguoi_xac_nhan_chuyen_mon") and not c.get("medical_verified",False):
    issues.append("Chưa xác nhận chuyên môn y tế")
 if b.get("can_duyet_phat_hanh") and not c.get("signed_approval",False):
    issues.append("Thiếu người có thẩm quyền duyệt phát hành")
 if c.get("spending",False) and not c.get("budget_approved",False):
    issues.append("Thiếu duyệt chi phí đúng hạn mức")
 if c.get("privacy_required",False) and not c.get("valid_consent",False):
    issues.append("Chưa có căn cứ dùng hình ảnh/thông tin người bệnh")
 if c.get("delegation_required",False) and not c.get("valid_delegation",False):
    issues.append("Chưa có ủy quyền thay người còn hiệu lực")
 if c.get("evidence_required",False) and not c.get("evidence_valid",False):
    issues.append("Thiếu bằng chứng nghiệm thu hoặc ảnh/số đo")
 if c.get("public_statement",False) and not c.get("spokesperson_approved",False):
    issues.append("Thiếu phê duyệt của người phát ngôn hợp lệ")
 if c.get("double_booked_hours",False):
    issues.append("Một đoạn giờ đã được tính vào hai đầu ra hoặc hai người")
 return {"ten":c["name"],"luong":q["ten"],"vi_tri_chu_tri_kiem":owner,
         "ma_dau_ra":record["ma_dau_ra"],"ket_qua":"CHẶN" if issues else "ĐỦ ĐIỀU KIỆN BÀN GIAO",
         "ly_do":"; ".join(issues) if issues else "Đúng một chủ trì, đúng tuyến, đủ cửa kiểm tương ứng",
         "expected":c["expected"]}

cases=[
 {"name":"Video Hạng mục nhóm 1 – bản dựng có xác nhận y tế","flow":"hang-muc","step":6,"actor":3,"person_id":"TEST_MEDIA_N1","checker_id":"TEST_MEDIA2_N1","medical_verified":True,"expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
 {"name":"Người dựng video tự kiểm bản dựng của mình","flow":"hang-muc","step":6,"actor":3,"person_id":"TEST_MEDIA_N1","checker_id":"TEST_MEDIA_N1","need_independent_check":True,"medical_verified":True,"expected":"CHẶN"},
 {"name":"Nghiệm thu sản phẩm y tế nhưng thiếu xác nhận chuyên môn","flow":"hang-muc","step":7,"actor":1,"person_id":"TEST_BRAND","medical_verified":False,"signed_approval":True,"expected":"CHẶN"},
 {"name":"Nội dung đã kiểm nhưng thiếu quyền phát hành","flow":"hang-muc","step":7,"actor":1,"person_id":"TEST_BRAND","medical_verified":True,"signed_approval":False,"expected":"CHẶN"},
 {"name":"Hạng mục đã đủ kiểm và ủy quyền GIẢ LẬP","flow":"hang-muc","step":7,"actor":1,"person_id":"TEST_BRAND","medical_verified":True,"signed_approval":True,"expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
 {"name":"Ký chi ngoài hạn mức nhưng chưa có cấp duyệt","flow":"hang-muc","step":3,"actor":1,"person_id":"TEST_TP","spending":True,"budget_approved":False,"expected":"CHẶN"},
 {"name":"Contact Center chủ nghiệp vụ kịch bản tư vấn","flow":"crm","step":6,"actor":1,"person_id":"TEST_CC","expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
 {"name":"Bệnh viện chuyên khoa hai người: Trưởng nhóm vận hành phát thanh","flow":"phat-thanh-man-hinh","step":5,"actor":1,"person_id":"TEST_TN2","expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
 {"name":"Hình ảnh người bệnh chưa có đồng ý","flow":"noi-dung-nguoi-benh","step":4,"actor":1,"group":"nhom_2","person_id":"TEST_QC_N2","privacy_required":True,"valid_consent":False,"expected":"CHẶN"},
 {"name":"Gỡ hình theo yêu cầu rút đồng ý","flow":"noi-dung-nguoi-benh","step":6,"actor":1,"group":"nhom_2","person_id":"TEST_QC_N2","expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
 {"name":"Trang đích toàn hệ thống chưa chọn nhóm","flow":"hang-muc-toan-he-thong","step":10,"actor":1,"person_id":"TEST_QC","expected":"CHẶN"},
 {"name":"Trang đích nhóm 2 đã xác định vị trí","flow":"hang-muc-toan-he-thong","step":10,"actor":1,"group":"nhom_2","owner_role":"qc-b","person_id":"TEST_QC_B","expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
 {"name":"Chuyển quyền khi vắng nhưng không có quyết định","flow":"vang-mat","step":3,"actor":1,"person_id":"TEST_CVT","signed_approval":True,"delegation_required":True,"valid_delegation":False,"expected":"CHẶN"},
 {"name":"Biển bảng hỏng: thiếu ảnh hiện trạng và số đo","flow":"bien-bang-hong","step":1,"actor":1,"person_id":"TEST_QHCS","evidence_required":True,"evidence_valid":False,"expected":"CHẶN"},
 {"name":"Giao kiểm biển bảng cho Media cơ sở","flow":"bien-bang-hong","step":1,"actor":1,"owner_role":"mdcs-a","person_id":"TEST_MEDIA_COSO","expected":"CHẶN"},
 {"name":"Khủng hoảng: tự phát ngôn khi chưa được ủy quyền","flow":"danh-gia","step":5,"actor":2,"person_id":"TEST_CVTT","public_statement":True,"spokesperson_approved":False,"expected":"CHẶN"},
 {"name":"Trùng giờ sản xuất và quản lý trong báo cáo","flow":"hang-muc","step":11,"actor":1,"person_id":"TEST_DO_LUONG","double_booked_hours":True,"expected":"CHẶN"},
 {"name":"Đối soát nguồn khách tách khỏi nghiệm thu Hạng mục","flow":"hang-muc","step":11,"actor":1,"person_id":"TEST_DO_LUONG","expected":"ĐỦ ĐIỀU KIỆN BÀN GIAO"},
]
output=[eval_case(c) for c in cases]
errors=[x for x in output if x["ket_qua"]!=x["expected"]]
assert not errors,"Tình huống không đúng: "+repr(errors)
assert len(output)==18
assert sum(x["ket_qua"]=="CHẶN" for x in output)>=9

D["kiem_thu_tinh_huong_2027"]={
 "loai":"Kiểm thử giả lập theo cấu trúc nghiệp vụ – không phải bản ghi thực tế hay phê duyệt có hiệu lực",
 "tong_tinh_huong":len(output),
 "ket_qua":output,
 "chu_y":"Mọi dữ liệu nhân sự dùng mã TEST_ để không lẫn với người thật; 'đủ điều kiện' chỉ là kết quả logic giả lập."
}
m=rx.search(s)
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]
# Hiển thị gọn trong đúng mục 4.3, không thêm menu hoặc kéo dài mặc định.
mark='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
assert mark in s
idx=s.index(mark)
end_heading=s.index("</h3>",idx)+5
body=(
 '<details id="tth-scenario-tests-2027" style="margin:12px 0;max-width:100%;'
 'padding:11px;border:1px solid #d3e1f1;border-radius:8px;background:#fff">'
 '<summary style="cursor:pointer;font-weight:700;color:#0837A1">Kiểm thử 18 tình huống thực tiễn'
 ' (giả lập nghiệp vụ: đạt/chặn đúng điều kiện)</summary>'
 '<p>Không sử dụng dữ liệu người bệnh hay nhân viên thật. '
 'Mã TEST_ là định danh giả lập; mọi phân quyền thật phải căn cứ văn bản còn hiệu lực.</p>'
 '<div style="max-width:100%;overflow-x:auto"><table class="t" style="min-width:760px">'
 '<thead><tr><th>Tình huống</th><th>Đầu ra</th><th>Kết quả</th><th>Căn cứ kiểm</th></tr></thead>'
 '<tbody>'+''.join(
    '<tr><td>'+escape(x["ten"])+'</td><td>'+escape(x["ma_dau_ra"])+'</td>'
    '<td>'+escape(x["ket_qua"])+'</td><td>'+escape(x["ly_do"])+'</td></tr>'
    for x in output
 )+'</tbody></table></div></details>'
)
if 'id="tth-scenario-tests-2027"' not in s:s=s[:end_heading]+body+s[end_heading:]
audit=json.loads(rx.search(s).group(2))
assert audit["kiem_thu_tinh_huong_2027"]["tong_tinh_huong"]==18
assert s.count('id="tth-scenario-tests-2027"')==1
p.write_text(s,"utf-8")

out=Path("artifacts/khung-e2e")
out.mkdir(parents=True,exist_ok=True)
(out/"kiem_thu_18_tinh_huong.json").write_text(json.dumps(output,ensure_ascii=False,indent=2),"utf-8")
print("PASS 18 BUSINESS SCENARIOS:",sum(x["ket_qua"]=="CHẶN" for x in output),
      "correct blocks;",sum(x["ket_qua"]!="CHẶN" for x in output),"valid mock handoffs.")
