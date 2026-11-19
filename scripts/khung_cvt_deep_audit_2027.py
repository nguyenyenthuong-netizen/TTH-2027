#!/usr/bin/env python3
"""Deep CVT 1/2 role & workflow consistency, built from canonical embedded khung data.

Non-approval rule: owning a SOP, checking professional standards and publishing
approval are separate. This patch never grants a new publishing or spending right.
Idempotent on a newly assembled (or repeatedly audited) site.
"""
from pathlib import Path
from collections import Counter
from html import escape
import json, re, sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
path=root/"khung-marketing"/"index.html"
src=path.read_text("utf-8")
mm=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',src)
if not mm: raise ValueError("CSDL khung missing")
d=json.loads(mm.group(2))
p={x["id"]:x for x in d["vi_tri"]}
for k in ("cvt","cvt-2"):
    if k not in p: raise ValueError("Missing CVT: "+k)
if len(d["vi_tri"])!=26 or len(d["quy_trinh"])!=60:
    raise ValueError("Baseline changed: inspect before CVT corrections")

first=p["cvt"]["ten"]
second=p["cvt-2"]["ten"]

# SOP drafting / revision stewardship; not a grant of executive power.
# All below are existing proposed documents, not signed policies.
cvt2_doc_ids={
 "QT.11": "Quy chuẩn nhận diện và nghiệm thu thương hiệu; sản xuất mẫu và vật phẩm thuộc CVT Nội dung – Cơ sở",
 "QT.20": "Chuẩn truyền thông KOL/KOC; quản lý thương hiệu nghiệm thu mục tiêu, pháp chế và người duyệt giữ thẩm quyền riêng",
 "QT.22": "Quy tắc truyền thông tuyển dụng, thông điệp và kênh; phòng Nhân lực sở hữu nội dung tuyển dụng",
 "QT.27": "Kiểm chuẩn phản ứng truyền thông mạo danh; khủng hoảng liên nhóm vẫn do Trưởng phòng chủ trì",
 "QT.29": "Chuẩn phát thanh, màn hình nội viện; lịch và sản phẩm phải qua các cấp duyệt theo ma trận",
 "QT.33": "Chuẩn quan hệ báo chí, truyền hình, truyền thanh và hợp đồng truyền thông; duyệt chi theo ma trận tài chính",
 "QT.34": "Chuẩn quan hệ báo chí và phỏng vấn bác sĩ; chuyên môn y khoa do người được giao xác nhận",
 "QT.39": "Chuẩn vận hành, rủi ro và khắc phục quyền truy cập kênh số; cấp/thu hồi quyền theo ma trận có hiệu lực",
 "QT.43": "Chuẩn hợp tác truyền thông, đồng thương hiệu; chữ ký hợp đồng và chi phí theo phân cấp",
 "QT.47": "Chuẩn phát trực tiếp và quản trị kênh; Biên tập/Media chịu đầu ra sản xuất, không mặc nhiên CVT2 duyệt phát hành",
 "QT.57": "Chuẩn quảng cáo trả phí, kênh số, giám sát và tối ưu; nội dung, nghiệm thu Hạng mục và chi phí độc lập",
 "QyĐ.05.MKT": "Chuẩn quản lý kênh, tài khoản và gửi tin; cấp phát quyền phải đúng danh sách người có thẩm quyền",
 "QCPN-MKT": "Chuẩn phát ngôn, quan hệ công chúng; quyền phát ngôn chính thức vẫn theo quy chế",
 "QT.05.MKT.TCT": "Chuẩn nghiệp vụ lập kế hoạch quảng cáo; ngân sách, phát hành và chi phí duyệt riêng",
 "QT-PT-HT": "Chuẩn phát thanh nội viện; xác nhận nội dung và cấp phát hành theo ma trận"
}
shared_docs={
 "QT.12":"CVT2 kiểm chuẩn báo chí, kênh và truyền thông sự kiện; CVT1 quản lý sản xuất và nguồn lực",
 "QT.16":"CVT2 kiểm chuẩn truyền thông, tài trợ ngoại viện; CVT1 điều phối Marketing cơ sở",
 "QT.23":"CVT2 kiểm chuẩn quản trị kênh/quảng cáo; CVT1 quản lý kho sản phẩm, nhân sự và bàn giao",
 "QT.35":"CVT2 kiểm chuẩn truyền thông nội bộ; CVT1 điều phối sản xuất và yêu cầu trong phòng",
 "QT.38":"CVT2 xử lý rủi ro truyền thông/kênh; CVT1 kiểm nguồn bản sản xuất và hồ sơ sửa",
 "QT.48":"CVT2 kiểm chuẩn thông điệp và rủi ro công bố; CVT1 kiểm nguồn tư liệu và phối hợp biên tập",
 "QT.55":"CVT2 kiểm chuẩn kênh quảng cáo; CVT1 phối hợp nội dung, xác nhận y tế/pháp chế thuộc tuyến độc lập",
 "QT.56":"CVT2 chuẩn chất lượng kênh/lịch đăng; CVT1 giữ tải sản xuất và chất lượng biên tập",
 "QyĐ.03.MKT":"CVT2 tham gia phần kênh, OOH, phát ngôn; CVT1 tham gia sản phẩm sản xuất và nguồn lực",
 "MT-TQ":"CVT2 đối chiếu quyền kiểm chuyên môn, CVT1 đối chiếu quyền điều phối; người ban hành thẩm quyền giữ nguyên"
}
for v in d["danh_muc_van_ban"]:
    code=v["ma"]
    if code in cvt2_doc_ids:
        if v["chu_tri"] not in ("cvt","cvt-2"):
            raise ValueError("Unexpected SOP lead "+code+" "+v["chu_tri"])
        v["chu_tri"]="cvt-2"
        v["trach_nhiem_nghiep_vu"]=cvt2_doc_ids[code]
        v["trang_thai_phan_cong_1911"]="Phương án phân vai xây dựng/quản lý văn bản; chưa thay quyết định phê duyệt, ban hành."
    elif code in shared_docs:
        v["phoi_hop_chuyen_mon_1911"]=shared_docs[code]
        v["trang_thai_phan_cong_1911"]="Phối hợp chuyên môn theo hai tuyến, không đồng chủ duyệt phát hành."
d["cvt_phan_cong_van_ban_1911"]={
    "nguyen_tac":"Chủ trì xây dựng/quản lý SOP không đồng nghĩa chủ trì mọi nghiệp vụ của quy trình, quyền kiểm duyệt sản phẩm, quyền phát hành, quyền tài chính, cấp quyền công nghệ hoặc quyền quản lý nhân viên.",
    "nguon":"Danh mục 83 văn bản nội bộ trong cơ sở dữ liệu khung; phương án cần cấp có thẩm quyền phê duyệt.",
    "cvt_2_chu_tri_xay_dung":sorted(cvt2_doc_ids),
    "phoi_hop_ca_hai":sorted(shared_docs)
}

# Correct ambiguous ownership in role descriptions, without inventing approvals.
p["tp"]["phan_dinh_ban_giao_dau_vao"]=(
    "Nhận báo cáo theo lĩnh vực từ "+first+" và "+second+
    "; nhận kết quả Hạng mục từ Quản lý thương hiệu, số liệu từ vị trí đo lường và đối soát; ký/duyệt theo ma trận thẩm quyền."
)
for role_id,field,old,new in [
    ("md-ac","viec_chung","(Chuyên viên trưởng giữ, Trưởng phòng duyệt","("+first+" chịu trách nhiệm chuẩn sản xuất; Trưởng phòng duyệt"),
    ("md-b","muc_dich","(quyền: Chuyên viên trưởng)","(quyền kho tư liệu theo ma trận; "+first+" kiểm soát nghiệp vụ sản xuất)"),
    ("qc-a","phan_dinh_kiem_duyet","Chuyên viên trưởng quản quyền theo ma trận",
     "Người được phân quyền cấp/thu hồi quyền theo ma trận; "+second+" kiểm chuẩn kênh số, không tự sinh quyền phát hành"),
    ("qlml","phan_dinh_kiem_duyet","Chuyên viên trưởng phê duyệt phân công theo văn bản/phạm vi",
     first+" quản lý tuyến trực tiếp cho đến khi quyết định phân vùng có hiệu lực; Trưởng phòng/cấp có thẩm quyền phê duyệt việc chuyển tuyến"),
]:
    oldval=p[role_id].get(field,"")
    if old in oldval:
        p[role_id][field]=oldval.replace(old,new)
    else:
        raise ValueError("Role text changed, manual review: "+role_id+"."+field)
# Make measurable outputs for both Chiefs explicit but do not fabricate throughput.
for role_id in ("cvt","cvt-2"):
    r=p[role_id]
    r["bo_chi_so_quan_tri_can_xac_nhan"]={
        "dinh_bien":"Tách giờ quản lý, đào tạo, kiểm chuẩn và hỗ trợ đột xuất; đo thực tế theo tháng, không tính trùng tổ trưởng",
        "dau_ra":"Số hồ sơ điều phối/quy chuẩn/kiểm tra/đào tạo và số vụ xử lý theo mã công việc, không đặt quota khi thiếu nhu cầu thực",
        "chat_luong":"Đúng hạn; đủ hồ sơ; tỷ lệ đạt ngay vòng đầu; tỷ lệ lỗi tái diễn",
        "hieu_qua":"Tồn việc, tỷ lệ quá tải theo nhân sự, số xung đột tuyến, thời gian xử lý xung đột; không nhận KPI sản xuất của vị trí khác",
        "phap_ly":"Kiểm y khoa, kiểm pháp lý, nghiệm thu mục tiêu, duyệt phát hành và duyệt chi phí phải là các căn cứ độc lập",
        "trang_thai":"Chỉ số quản trị cần đo thí điểm, KPI hai chức danh chưa phê duyệt"
    }
# Resolve an outright outdated claim that the Chief is the team leader in routine schedule.
for x in d.get("lich_van_hanh",[]):
    y=x.get("phu_trach","")
    old="Tổ trưởng của tổ (Tổ Truyền thông và Thương hiệu: Chuyên viên trưởng)"
    if old in y:
        x["phu_trach"]=y.replace(old,"Tổ trưởng được giao của từng tổ; "+second+" quản lý chuyên môn hai tổ, không tự kiêm Tổ trưởng")
# Process participation: only specialist inspection on a relevant step, never final approval.
technical={
    "bo-nhan-dien":(2,"Kiểm chuẩn thương hiệu, không thay người kiểm kỹ thuật file"),
    "mao-danh":(1,"Kiểm chuẩn xử lý mạo danh, phát ngôn và đối ứng kênh"),
    "phat-thanh-man-hinh":(2,"Kiểm chuẩn kế hoạch phát, màn hình, phát thanh nội viện"),
    "mua-truyen-thong":(2,"Kiểm chuẩn kênh và điều kiện chuyên môn nhà cung cấp truyền thông"),
    "bao-chi-bac-si":(1,"Hướng dẫn nghiệp vụ báo chí/phỏng vấn, không duyệt thay y khoa"),
    "su-co-tai-khoan":(2,"Kiểm chuẩn an toàn kênh số và ghi nhận rủi ro"),
    "doi-tac":(2,"Kiểm chuẩn truyền thông đối tác, đồng thương hiệu"),
    "phat-truc-tiep":(2,"Kiểm chuẩn trực tiếp, phát hành theo ma trận quyền"),
    "quang-cao-tra-phi":(2,"Kiểm chuẩn nghiệp vụ quảng cáo và kênh số"),
    "quang-cao-san-pham":(2,"Kiểm chuẩn kênh quảng cáo, không thay kiểm pháp lý/y khoa"),
    "chuyen-quyen":(2,"Kiểm chuẩn quyền quản trị kênh; người cấp quyền theo ma trận có hiệu lực"),
    "lich-dang-thang":(2,"Kiểm chuẩn vận hành kênh số và lịch đăng; không thay nghiệm thu Hạng mục"),
    "dinh-chinh":(2,"Kiểm chuẩn xử lý truyền thông sau phát hành"),
    "su-kien-co-so":(2,"Kiểm chuẩn truyền thông sự kiện, không thay điều phối nhân sự cơ sở"),
    "thanh-tra-kiem-tra":(3,"Đối soát hồ sơ hoạt động kênh, hợp đồng truyền thông"),
    "phap-luat":(3,"Kiểm chuẩn chính sách nền tảng quảng cáo/kênh số, không thay Pháp chế"),
    "nghien-cuu-thi-truong":(2,"Kiểm chuẩn phương pháp truyền thông/đo lường, không cấp quyền duyệt chi"),
    "noi-bo-phong-ban":(2,"Kiểm chuẩn thông điệp truyền thông nội bộ"),
    "tuyen-dung":(2,"Kiểm chuẩn truyền thông tuyển dụng, không thay Phòng Nhân lực"),
    "doi-ten-chuyen-nhom":(5,"Kiểm chuẩn tên kênh/nhận diện, cấp/thu hồi quyền theo ma trận"),
    "ra-soat-noi-dung-y-khoa":(3,"Kiểm chuẩn truyền thông/kênh, không thay xác nhận y khoa"),
    "mua-sam":(3,"Đối soát chuyên môn khi mua dịch vụ Truyền thông/Thương hiệu/Tăng trưởng số")
}
flows={q["id"]:q for q in d["quy_trinh"]}
for fid,(step_no,meaning) in technical.items():
    if fid not in flows: raise ValueError("Missing flow "+fid)
    q=flows[fid]
    if not (1<=step_no<=len(q["buoc"])): raise ValueError("Step mismatch "+fid)
    step=q["buoc"][step_no-1]
    together=step.setdefault("phoi_hop",[])
    if not any(str(x).split("|")[0]=="cvt-2" for x in together):
        together.append("cvt-2|"+meaning)
    step["kiem_chuan_nghiep_vu_1911"]=meaning+"; không tạo thêm cửa duyệt phát hành hoặc tăng tải cơ sở khi chưa có thẩm quyền."
# Explicit professional hand-off in the internal audio/screen schedule.
step=flows["phat-thanh-man-hinh"]["buoc"][1]
step["phoi_hop"]=[
    ("cvt-2|kiểm chuẩn kế hoạch phát; không tự duyệt phát hành" if x=="cvt|duyệt kế hoạch phát" else x)
    for x in step.get("phoi_hop",[])
]
# Production scheduling conflict: neither Chief alone can decide cross-domain neutral staff.
q=flows["xung-dot-lich"]
old="Chưa thống nhất: Chuyên viên trưởng quyết định phần điều phối nguồn lực trong khối mình quản lý."
replacement=( "Chưa thống nhất: "+first+" quyết định điều phối nguồn lực sản xuất trong phạm vi được giao; "
              +second+" xác nhận năng lực và chuẩn chuyên môn của hai tổ phụ trách. "
              "Tranh chấp nguồn lực trung lập ngoài tuyến một Chuyên viên trưởng, ngân sách hoặc ưu tiên hai nhóm "
              "phải chuyển Trưởng phòng quyết định, lưu phiếu điều chỉnh lịch.")
for x in q["buoc"]:
    if old in x.get("noi_dung",""): x["noi_dung"]=x["noi_dung"].replace(old,replacement)
# Distinguish two lines in onboarding / handover rather than always route to CVT1.
onboarding=flows["nhan-viec-moi"]
for b in onboarding["buoc"]:
    if str(b.get("chu_tri_chinh","")).split("|")[0]=="cvt":
        b["chu_tri_theo_tuyen_1911"]={
            "noi_dung_va_co_so":"cvt",
            "truyen_thong_thuong_hieu_tang_truong_so":"cvt-2",
            "ghi_chu":"Đơn vị được tuyển thuộc tuyến quản lý nào thì người quản lý tuyến đó chủ trì; quyền cấp phát phần mềm theo ma trận hiện hành. Trưởng phòng xử lý liên tuyến."
        }
        b["noi_dung"]=b.get("noi_dung","") + (
            " [ĐỐI CHIẾU TUYẾN 19/11: nhân sự Tổ Nội dung và Sáng tạo/Marketing cơ sở: "+
            first+"; nhân sự Tổ Truyền thông và Thương hiệu/Tổ Tăng trưởng số: "+
            second+"; không mặc nhiên cấp quyền duyệt sản phẩm hay chi phí.]"
        )
        if not any(str(x).split("|")[0]=="cvt-2" for x in b.setdefault("phoi_hop",[])):
            b["phoi_hop"].append("cvt-2|chỉ phần nhân sự thuộc hai tổ trực tiếp phụ trách")
# Correct team-scope ambiguities in staffing and section texts at data level.
m=d.get("quan_ly_mang_luoi_vung",{})
s0=m.get("nguyen_tac","")
if "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở2 người" in s0:
    m["nguyen_tac"]=s0.replace("Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở2 người",
         "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở tối đa 12 người")
q=p["qlml"]
q["gio_ke_hoach"]=q["gio_ke_hoach"].replace("Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở2",
    "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở tối đa 12")
# Create inspection-ready learning / coordination scope, not pretend 60 SOPs are approved.
d["ma_tran_cvt_nam_quy_trinh_1911"]={
    "trang_thai":"Danh mục phải nắm trong phương án; hoàn thành khi có tài liệu ban hành, đào tạo, kiểm tra năng lực và nhật ký cập nhật.",
    "cvt":{
        "chuyen_sau":["QT.1","QT.2","QT.3","QT.7","QT.8","QT.9","QT.11","QT.17","QT.23","QT.30","QT.31","QT.36","QT.42","QT.44","QT.58","QT.59"],
        "phoi_hop":["QT.20","QT.27","QT.29","QT.33","QT.34","QT.38","QT.39","QT.43","QT.47","QT.56","QT.57"]},
    "cvt-2":{
        "chuyen_sau":["QT.11","QT.20","QT.22","QT.27","QT.29","QT.33","QT.34","QT.39","QT.43","QT.47","QT.56","QT.57"],
        "phoi_hop":["QT.1","QT.2","QT.3","QT.7","QT.9","QT.23","QT.30","QT.36","QT.42","QT.44","QT.58","QT.59"]},
    "chung":["QT.6","QT.15","QT.18","QT.25","QT.32","QT.40","QT.41","QT.45","QT.48","QT.49","QT.54","QT.60"],
    "truong_chung_nhan":["ma_tai_lieu","phien_ban_hieu_luc","cap_do_nam","ngay_dao_tao",
                        "nguoi_kiem_tra","hinh_thuc_kiem_tra","ket_qua","ngay_kiem_tra_lai"],
    "muc_do":"Chuyên sâu: tự xây, hướng dẫn, kiểm soát trong phạm vi. Phối hợp: hiểu đầu vào, đầu ra và chuyển tuyến. Chung: nhận diện rủi ro, nắm điều kiện chặn, tìm đúng chủ trì.",
    "canh_bao":"Dòng dữ liệu chủ trì bước trong 60 quy trình chưa được tách triệt để theo tuyến; khi triển khai phải chọn người thực hiện theo mô tả công việc và ma trận thẩm quyền đã ban hành."
}
for id in ("cvt","cvt-2"):
    a=d["ma_tran_cvt_nam_quy_trinh_1911"][id]
    allcodes=a["chuyen_sau"]+a["phoi_hop"]+d["ma_tran_cvt_nam_quy_trinh_1911"]["chung"]
    unknown=[c for c in allcodes if c not in {x["ma"] for x in d["danh_muc_van_ban"]}]
    if unknown: raise ValueError("Invalid mandatory procedure codes: "+",".join(unknown))

# Render quick-to-verify visual summary in actual Position Description tab.
docs=d["danh_muc_van_ban"]
def documents(role_id):
    selected=[x for x in docs if x.get("chu_tri")==role_id]
    li="".join("<li><b>"+escape(x["ma"])+"</b> – "+escape(x["ten"])+"</li>" for x in selected)
    return "<details><summary>"+str(len(selected))+" văn bản ghi đầu mối soạn/quản lý</summary><ol>"+li+"</ol></details>"
def learn(role_id):
    L=d["ma_tran_cvt_nam_quy_trinh_1911"][role_id]
    return '<p><b>Nắm chuyên sâu:</b> '+escape(", ".join(L["chuyen_sau"]))+'</p><p><b>Nắm phối hợp:</b> '+escape(", ".join(L["phoi_hop"]))+'</p>'
summary_html='<section id="tth-cvt-deep-audit-1911" style="border:1px solid #d4e3f1;border-left:5px solid #ED3237;background:#fff;border-radius:12px;padding:18px;margin:18px 0;">'
summary_html+='<h3 style="color:#0837A1;margin:0 0 8px">Đối chiếu trách nhiệm hai Chuyên viên trưởng theo cơ cấu 2027</h3>'
summary_html+='<p>Phạm vi quản lý, kiểm chuẩn chuyên môn, trách nhiệm xây dựng văn bản và quyền phê duyệt là bốn loại trách nhiệm khác nhau. Các quy trình, tỷ trọng KPI chưa phê duyệt không được coi là quy định đã ban hành.</p>'
summary_html+='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:14px">'
for id,scope in [
    ("cvt","Quản lý trực tiếp Trưởng nhóm Marketing bệnh viện cả hai nhóm; quản lý Tổ Nội dung và Sáng tạo; điều phối tải, sản lượng, đầu ra và đánh giá theo tuyến."),
    ("cvt-2","Quản lý Tổ Truyền thông và Thương hiệu, Tổ Tăng trưởng số; kiểm chuẩn truyền thông/OOH/phát thanh/màn hình/quảng cáo/kênh số ở cả hai nhóm, không quản lý trực tiếp Trưởng nhóm cơ sở.")
]:
    k=d["kpi_vi_tri"][id]
    summary_html+='<div style="border:1px solid #d4e3f1;border-radius:10px;padding:12px"><h4 style="margin:0 0 6px;color:#0837A1">'+escape(p[id]["ten"])+'</h4>'
    summary_html+='<p>'+escape(scope)+'</p><p><b>KPI:</b> '+escape(k["trang_thai_phe_duyet"])+'</p>'
    summary_html+=documents(id)+learn(id)+'</div>'
summary_html+='</div><p style="margin-bottom:0"><b>Giới hạn:</b> Chủ trì lập/sửa quy trình ≠ người duyệt sản phẩm; người hướng dẫn chuyên môn ≠ quản lý trực tiếp nhân sự cơ sở; kiểm chuẩn quảng cáo ≠ duyệt phát hành/chi phí. Mọi quyết định thực thi căn cứ văn bản phê duyệt có hiệu lực.</p></section>'
src=src[:mm.start(2)]+json.dumps(d,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+src[mm.end(2):]
if 'id="tth-cvt-deep-audit-1911"' not in src:
    marker='<section class="view" data-view="jd" id="v-jd">'
    if marker not in src: raise ValueError("JD section not found")
    index=src.index(marker)+len(marker)
    src=src[:index]+summary_html+src[index:]
# Guard source counts, not only visual content.
d2=json.loads(re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',src).group(1))
assert sum(x.get("chu_tri")=="cvt-2" for x in d2["danh_muc_van_ban"])>=len(cvt2_doc_ids)
assert "tth-cvt-deep-audit-1911" in src and len(d2["vi_tri"])==26
assert len(d2["quy_trinh"])==60
assert not any("Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở2" in json.dumps(x,ensure_ascii=False) for x in d2["vi_tri"])
path.write_text(src,"utf-8")
print("CVT-DEEP-AUDIT PASS",
      "cvt1-SOP",sum(x["chu_tri"]=="cvt" for x in docs),
      "cvt2-SOP",sum(x["chu_tri"]=="cvt-2" for x in docs),
      "CVT2-professional-steps",sum("cvt-2" in json.dumps(b) for q in d2["quy_trinh"] for b in q["buoc"]),
      "KPI",d2["kpi_vi_tri"]["cvt"]["trang_thai_phe_duyet"],"|",
      d2["kpi_vi_tri"]["cvt-2"]["trang_thai_phe_duyet"])
