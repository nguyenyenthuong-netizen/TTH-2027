#!/usr/bin/env python3
"""Đối soát mâu thuẫn liên mục của khung Marketing 2027; sửa phần có đủ căn cứ.

Chạy sau khung_cvt_deep_audit_2027.py; không cấp quyền chi, phát hành,
không thay quyết định sử dụng lao động, không chế ra số giờ thực đo.
"""
from pathlib import Path
import json, re, sys
from html import escape
from collections import Counter
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
file=root/"khung-marketing"/"index.html"
s=file.read_text("utf-8")
m=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',s)
if not m: raise RuntimeError("Missing CSDL source")
D=json.loads(m.group(2))
vt={p["id"]:p for p in D["vi_tri"]}
title1=vt["cvt"]["ten"]
title2=vt["cvt-2"]["ten"]

def repl(field, a, b, msg, required=True):
    if a not in field:
        if required: raise ValueError("Source changed: "+msg)
        return field
    return field.replace(a,b)

# 1. Fixed structure versus previous staffing scenario: NEVER infer 56+2 = 58.
assert D["phan_dinh_quan_ly_hai_cvt_19112026"]["dinh_bien"]=={
    "tct":22,"benh_vien":14,"tong":36,"cvt":2,"to_chuyen_mon":3
}, "Changed staffing baseline: re-evaluate manually"
scenario=D["lo_trinh_dinh_bien"]
assert scenario["buoc"][0]["tong"]==34 and scenario["buoc"][-1]["tong"]==56
scenario["trang_thai_sau_co_cau_2_cvt_1911"]=(
 "LỘ TRÌNH THAM CHIẾU TỪ PHƯƠNG ÁN 34 SUẤT CŨ; KHÔNG PHẢI LỘ TRÌNH ĐỊNH BIÊN ĐÃ ĐỐI SOÁT "
 "CHO CƠ CẤU 36 SUẤT (22 Tổng công ty + 14 cơ sở). Các mốc 34/40/43/50/53/56 "
 "không tự có hiệu lực tuyển dụng hoặc phân vùng."
)
scenario["can_cu"]=scenario["trang_thai_sau_co_cau_2_cvt_1911"]+" "+scenario["can_cu"]
scenario["dieu_kien_tinh_lai"]=[
 "Làm rõ hai suất chênh giữa 34 và 36 theo vị trí, cơ sở và giờ làm trong mô hình mới",
 "Đo tải quản lý cả hai Chuyên viên trưởng; xác định định mức giờ theo nguồn phát sinh",
 "Tính riêng tải sản xuất, truyền thông, tăng trưởng số và việc kiêm nhiệm tại từng cơ sở",
 "Tính từng bước mở cơ sở, không cộng cơ học hai suất vào mọi mốc cũ",
 "Tách số suất mục tiêu, số người hiện có và số suất cần tuyển; phê duyệt lại lộ trình"
]
for i,x in enumerate(scenario["buoc"]):
    x["goc_truoc_dieu_chinh"]="Phương án lộ trình 34 suất cũ; số liệu tham chiếu, chưa có hiệu lực cho cơ cấu 36 suất"
    x["buoc"]="Tham chiếu lịch sử – "+x["buoc"]
D["quan_ly_mang_luoi_vung"]["suat_dinh_bien"]=(
 "01 suất Quản lý mạng lưới vùng thuộc KỊCH BẢN MỞ RỘNG CŨ 56 suất, không thuộc "
 "định biên cố định 36 suất hiện tại. Chưa xác lập ngưỡng tuyển dụng mới sau bổ sung CVT thứ hai."
)
D["quan_ly_mang_luoi_vung"]["chan"]=[
 repl(x,"Tổng số người vượt 56 mà chưa có quyết định sửa định biên",
      "Vượt định biên được phê duyệt tại thời điểm thực hiện (mốc 56 chỉ là kịch bản cũ)",
      "staffing cap",False) for x in D["quan_ly_mang_luoi_vung"]["chan"]
]
vt["qlml"]["gio_ke_hoach"]=repl(vt["qlml"]["gio_ke_hoach"],
    "01 suất trong mốc 56 người",
    "01 suất dự kiến trong kịch bản mở rộng 56 người cũ, phải tính lại sau cơ cấu 36 suất",
    "regional headcount")
# Fix wrong str concat /2 in clinic contact: not one role named ".../2".
vt["dmpk"]["bao_cao_cho"]=repl(vt["dmpk"]["bao_cao_cho"],
    "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở/2 hướng dẫn theo từng loại đầu ra Marketing",
    title1+" hướng dẫn phần tổ chức sản xuất; "+title2+
    " kiểm chuẩn phần truyền thông, thương hiệu và kênh số qua đầu mối phòng khám",
    "clinic weird CVT/2")
D["phan_cap_duyet_17112026"]["cac_cua_kiem_soat"][0]["nguoi_lam"]=repl(
  D["phan_cap_duyet_17112026"]["cac_cua_kiem_soat"][0]["nguoi_lam"],
  "ma trận 25 vị trí","ma trận 26 loại vị trí","25 to 26")

# 2. Complete four missing KPI rubrics as NOT APPROVED, no numeric quotas fabricated.
rubrics={
"tp":[
 ("Tỷ lệ mục tiêu toàn phòng có kế hoạch, người phụ trách và nguồn đo được xác nhận",20),
 ("Tỷ lệ điều hành ngân sách và danh mục Hạng mục đúng phân cấp, không vượt hạn mức",20),
 ("Tỷ lệ xung đột giữa nhóm/cơ sở giải quyết đúng hạn có biên bản",15),
 ("Tỷ lệ rủi ro pháp lý – thương hiệu được chặn, xử lý đúng quy trình",15),
 ("Tỷ lệ rà soát định biên, quy trình và báo cáo điều hành đúng kỳ",10)],
"dl-2":[
 ("Tỷ lệ dữ liệu khách hàng/thị trường có nguồn, phạm vi dùng và kiểm tra chất lượng",20),
 ("Tỷ lệ yêu cầu cung cấp dữ liệu/phân tích được đối soát, trả đúng hạn",20),
 ("Tỷ lệ nghiên cứu thị trường có phương pháp, cỡ mẫu và hạn chế được nêu rõ",15),
 ("Tỷ lệ bản ghi trùng/thiếu dữ liệu được phát hiện, xử lý có nhật ký",15),
 ("Tỷ lệ yêu cầu sử dụng dữ liệu cá nhân có căn cứ, giới hạn quyền và cơ chế rút đồng ý",10)],
"qlml":[
 ("Tỷ lệ cơ sở được bàn giao đúng quyết định, một tuyến quản lý tại mỗi thời điểm",20),
 ("Tỷ lệ Trưởng nhóm trong vùng có kế hoạch, tải và báo cáo được xác nhận",20),
 ("Tỷ lệ vấn đề chuyển tuyến/vượt tải được xử lý đúng hạn",15),
 ("Tỷ lệ đánh giá theo nhân sự thuộc vùng có dữ liệu nguồn, không hồi tố",15),
 ("Tỷ lệ đào tạo và khắc phục chất lượng Marketing cơ sở đúng hạn",10)],
"dmpk":[
 ("Tỷ lệ yêu cầu của phòng khám được ghi nhận nguồn, hạn và chuyển đúng tuyến",20),
 ("Tỷ lệ cập nhật thông tin phòng khám có xác nhận của đơn vị chủ dữ liệu",20),
 ("Tỷ lệ tư liệu/sản phẩm bàn giao đủ hồ sơ, sử dụng mẫu đã duyệt",15),
 ("Tỷ lệ phản ánh hoặc sai lệch thông tin phát hiện và báo đúng hạn",15),
 ("Tỷ lệ nhiệm vụ kiêm nhiệm có nhật ký tải, không tính trùng nguồn lực",10)]
}
for id, rows in rubrics.items():
    if id in D["kpi_vi_tri"]: continue
    personal=[{"chi_tieu":label+" (chỉ số đề xuất, chưa có mức mục tiêu)",
               "nguon":"Sổ công việc, chứng cứ và xác nhận của đầu mối có thẩm quyền; chưa có bộ số liệu thực đo",
               "ty_trong":weight} for label,weight in rows]
    common=[{"chi_tieu":"Kết quả chung của Phòng Marketing theo bộ KPI được phê duyệt; không nhận trùng đầu ra của vị trí khác",
             "nguon":"Báo cáo KPI toàn phòng đã được đối soát",
             "ty_trong":20}]
    D["kpi_vi_tri"][id]={
        "ca_nhan":personal,"chung":common,
        "nguon_quyet_dinh":"Đề xuất kỹ thuật hoàn thiện bộ chỉ tiêu 26 vị trí; không có quyết định giao KPI",
        "trang_thai_phe_duyet":"DỰ THẢO MỚI – chưa phê duyệt, chưa có mức mục tiêu và chưa đủ số liệu; không dùng tính lương/thưởng",
        "quy_tac_ap_dung":"Tỷ trọng chỉ để rà soát độ bao phủ; phải có quyết định, chỉ tiêu số, nguồn đo, chu kỳ, ngoại lệ và người chốt trước khi áp dụng"
    }
    vt[id]["trang_thai_kpi"]="Có bảng KPI đề xuất, CHƯA PHÊ DUYỆT, chưa xác lập mục tiêu và dữ liệu thực đo."
assert all(id in D["kpi_vi_tri"] for id in vt), "KPI position coverage must be 26/26"
for id in vt:
    k=D["kpi_vi_tri"][id]
    total=sum(x.get("ty_trong",0) for x in k.get("ca_nhan",[])+k.get("chung",[]))
    assert total==100, f"KPI total wrong {id} {total}"

# 3. Align evidence forms: technical stewardship is distinct from signed document approval.
move_forms={
 "BM-5":"Chuẩn lịch đăng và điều kiện vận hành kênh; nội dung bài vẫn do Biên tập và Quản lý thương hiệu chịu trách nhiệm phù hợp",
 "BM-24":"Biên bản chuyển quyền kênh, tài khoản quảng cáo; quyền quản trị cấp cao và duyệt thay theo ma trận",
 "M-5":"Quy chuẩn nghiệp vụ thuê vị trí quảng cáo OOH; Phòng Tài chính/Pháp chế và cấp ký giữ quyền hợp đồng",
 "QC-5":"Chuẩn quan hệ công chúng, phát ngôn; không mặc nhiên có quyền phát ngôn",
 "DS-2":"Danh sách tiêu chí người trực sự cố truyền thông tầng 1, có Trưởng phòng duyệt",
 "SO-3":"Sổ theo dõi sự cố truyền thông và lịch trực; báo sự cố cấp hệ thống lên Trưởng phòng"
}
for f in D["danh_muc_tai_lieu"]:
    id=f["ma"]
    if id in move_forms:
        if f.get("nam_giu")!="cvt": raise ValueError("Form owner changed "+id)
        f["nam_giu"]="cvt-2"
        for key in ("xay_dung","cap_nhat"):
            if key in f: f[key]=["cvt-2" if x=="cvt" else x for x in f[key]]
        if "co_che_quan_tri" in f:
            c=f["co_che_quan_tri"]
            c["nguoi_nam_giu"]="cvt-2"
            for key in ("nguoi_lap",):
                if key in c: c[key]=["cvt-2" if x=="cvt" else x for x in c[key]]
        f["ranh_gioi_cvt_1911"]=move_forms[id]+"; tài liệu dự thảo, chưa thay người phê duyệt."
    if id in ("BM-7","SO-1","BM-21","BM-23","DM-8","DM-5","DS-4"):
        f["phoi_hop_cvt2_1911"]=(
            "Cần CVT Truyền thông – Thương hiệu và Tăng trưởng số xác nhận nghiệp vụ đối với "
            "các phần truyền thông/quan hệ công chúng/OOH/quảng cáo/kênh số trước khi CVT Nội dung – Cơ sở tổng hợp mẫu chung; "
            "quyền ban hành/chi/phát hành theo ma trận riêng."
        )
    for field in f.get("truong",[]):
        code=field.get("ma_truong","")
        typ=field.get("loai_du_lieu")
        if code in ("ly_do_gap","ly_do","ly_do_thay","ly_do_ngoai_le","ghi_chu","noi_dung_phan_anh") and typ=="date":
            field["loai_du_lieu"]="text"
            field["quy_tac_kiem_tra"]="Ghi rõ nội dung/lý do bằng chữ, có nguồn và người xác nhận; không kiểm tra theo định dạng ngày"
        if code=="nhom_nguoi_lam" and typ=="user":
            field["loai_du_lieu"]="enum"
            field["quy_tac_kiem_tra"]="Chọn mã nhóm từ danh mục nhóm thương hiệu của vị trí người làm, không phải mã cá nhân"
# Cross-check form control source when notes say changed.
assert next(x for x in D["danh_muc_tai_lieu"] if x["ma"]=="BM-5")["nam_giu"]=="cvt-2"
assert next(f for f in D["danh_muc_tai_lieu"] if f["ma"]=="BM-21")["truong"][3]["loai_du_lieu"]=="text"

# 4. Single lead for a step and specialist checks separate from deployment rights.
q={x["id"]:x for x in D["quy_trinh"]}
step=q["su-co-tai-khoan"]["buoc"][5]
assert step["chu_tri_chinh"]=="cvt"
step["chu_tri_chinh"]="cvt-2"
step["thuc_hien"]=["cvt-2"]
step["noi_dung"]=repl(step["noi_dung"],
    "Rà soát danh sách quyền toàn hệ thống sau sự cố; thu hồi quyền không còn dùng.",
    title2+" chủ trì rà soát danh sách quyền kênh/quảng cáo sau sự cố. "
    "Người có thẩm quyền cấp/thu hồi theo ma trận có hiệu lực thực hiện; "
    "CVT Nội dung – Cơ sở đối chiếu quyền kho tư liệu sản xuất. Có nhật ký thu hồi và xác nhận độc lập.",
    "account incident")
# Operational steps previously defaulted to CVT1: don't create duplicate owner IDs.
for i in (0,6):
    step=q["chuyen-quyen"]["buoc"][i]
    step["phan_vai_theo_tai_san_1911"]={
      "kenh_va_quang_cao":"cvt-2 – kiểm chuẩn và đối soát nghiệp vụ",
      "kho_tu_lieu_va_file_san_xuat":"cvt – quản lý hồ sơ và nguồn lực sản xuất",
      "cap_quyen_quan_tri":"Trưởng phòng/người được ủy quyền tại quyết định có hiệu lực",
      "bao_cao":"Chỉ một biên bản nghiệm thu và một bản cập nhật quyền cho mỗi tài sản"
    }
# Process of research has no automatic green-light: align new specialist lane.
research=q["nghien-cuu-thi-truong"]["buoc"][1]
research["noi_dung"]=repl(research["noi_dung"],"Chuyên viên trưởng duyệt.",
 title2+" kiểm chuẩn phương pháp/nguồn thu; Trưởng phòng hoặc người có ủy quyền còn hiệu lực phê duyệt trước khi khảo sát; chi phí theo ma trận tài chính.",
 "research approval")
research["phoi_hop"]=[
 ( "cvt-2|kiểm phương pháp, phạm vi thu dữ liệu, cảnh báo rủi ro" if str(x).startswith("cvt|") else x)
 for x in research.get("phoi_hop",[])
]
q["nghien-cuu-thi-truong"]["kiem_soat"]=[
 repl(x,"Chuyên viên trưởng duyệt",
       "đầu mối chuyên môn kiểm chuẩn; cấp có thẩm quyền phê duyệt",
       "research checkpoint",False) if isinstance(x,str) else x
 for x in q["nghien-cuu-thi-truong"].get("kiem_soat",[])
]
# Existing staffing/HR and channel decisions: fail closed without valid authorization.
for qid,changes in {
 "chuyen-quyen":[("Trưởng phòng – chưa có: Chuyên viên trưởng",
                  "Trưởng phòng; khi chưa có Trưởng phòng, chỉ người được Ban Tổng Giám đốc chỉ định bằng văn bản"),
                 ("quyền đăng bài, trả lời tin nhắn: Chuyên viên trưởng",
                  "quyền đăng bài, trả lời tin nhắn: người được phân quyền cấp/thu hồi theo ma trận còn hiệu lực")],
 "nhan-viec-moi":[("quyền đăng bài, trả lời tin nhắn, kho tư liệu: Chuyên viên trưởng",
                   "quyền đăng bài, trả lời tin nhắn, kho tư liệu: đúng người được giao cấp quyền theo ma trận còn hiệu lực")],
 "phat-thanh-man-hinh":[("cvt|duyệt kế hoạch phát",
                        "cvt-2|kiểm chuẩn nghiệp vụ lịch phát; duyệt phát hành theo ma trận còn hiệu lực")]
}.items():
    for row in q[qid]["buoc"]:
        for old,new in changes:
            for field in ("noi_dung",):
                if old in row.get(field,""):row[field]=row[field].replace(old,new)
            row["phoi_hop"]=[x.replace(old,new) for x in row.get("phoi_hop",[])]
# Trigger proper management line for every onboarding source + backups.
D["ma_tran_giao_nhan_viec_1911"]={
 "nhan_su_noi_dung_sang_tao":["cvt","Tổ trưởng Tổ Nội dung và Sáng tạo"],
 "nhan_su_truyen_thong_thuong_hieu_tang_truong_so":["cvt-2","Tổ trưởng của tổ tương ứng"],
 "truong_nhom_marketing_benh_vien":["cvt","Ban Giám đốc cơ sở xác nhận dữ liệu tại chỗ"],
 "dau_moi_phong_kham":["Quản lý trực tiếp tại phòng khám","Marketing TCT hướng dẫn theo lĩnh vực, không duyệt chấm công"],
 "trang_thai":"Ánh xạ điều hành theo cơ cấu; người thay và quyền hệ thống phải kiểm quyết định cá nhân"
}

# 5. Repair semantic ambiguity without enlarging approval scope.
for t in D.get("mang_viec",[]):
    name=t.get("ten","")
    if name=="Nghiên cứu thị trường, khảo sát nhận biết":
        t["duyet"]=title2+" kiểm chuẩn phương pháp/nguồn dữ liệu; cấp có thẩm quyền duyệt phương án trước khi khảo sát, duyệt chi độc lập"
    elif name=="Kênh số":
        t["duyet"]="Quản lý thương hiệu nghiệm thu lịch; "+title2+" kiểm chuẩn kênh; cấp, thu hồi quyền do người được phân quyền theo ma trận có hiệu lực; Trưởng phòng quản trị cao nhất"
    elif name=="Quy tắc ứng xử mạng xã hội của nhân viên":
        t["thuc_hien"]="Chuyên viên truyền thông từng nhóm soạn phần của nhóm; "+title2+" kiểm chuẩn truyền thông; Phòng Nhân lực sở hữu quy tắc nhân sự"
    elif name=="Quản trị nghiệp vụ phần mềm":
        t["thuc_hien"]=title1+" chủ trì nghiệp vụ phần mềm Marketing (phân công, mẫu Hạng mục); "+title2+" xác nhận yêu cầu nghiệp vụ hai tổ và quyền kênh; Chuyên viên dữ liệu khách hàng và thị trường giữ chuẩn dữ liệu"
        t["duyet"]="Trưởng phòng duyệt ma trận quyền và mẫu Hạng mục; cấp quyền chỉ theo người được ủy quyền; thay đổi quy tắc phần mềm phải được Trưởng phòng chấp thuận"
    elif name=="Theo dõi thay đổi pháp luật quảng cáo y tế, chính sách nền tảng":
        t["duyet"]="Pháp chế xác nhận danh sách kiểm pháp lý; Trưởng phòng phê duyệt quy tắc áp dụng Marketing; "+title2+" kiểm chuẩn chính sách nền tảng, không tự duyệt nội dung pháp luật"
    elif name=="Mạo danh bệnh viện, bác sĩ, thương hiệu trên mạng (trang Facebook, tài khoản, website, quảng cáo giả)":
        t["thuc_hien"]=t["thuc_hien"].replace("mạo danh cả hai nhóm: Chuyên viên trưởng chủ quy trình (QT.27)",
            "mạo danh cả hai nhóm: Trưởng phòng chủ trì xử lý liên nhóm; "+title2+" làm đầu mối nghiệp vụ truyền thông và kênh số (QT.27)")
    elif name=="Nhà cung cấp, hợp đồng, thanh toán":
        t["thuc_hien"]=t["thuc_hien"].replace("Chuyên viên trưởng (danh sách nhà cung cấp đã phê duyệt)",
             title1+" kiểm phần nhà cung cấp sản xuất; "+title2+" kiểm phần nhà cung cấp truyền thông, thương hiệu và tăng trưởng số; Trưởng phòng kiểm danh sách dùng chung")
    elif name=="Sự kiện, cộng đồng, học đường, đối tác địa phương":
        t["duyet"]=t["duyet"].replace("Chuyên viên trưởng;",
         "người được phân quyền duyệt phát hành theo loại nội dung; "+title2+" kiểm chuẩn truyền thông; "+title1+" điều phối tải;")
# Schedule is 63 entries and should never imply "CVT" = automatic deputy.
for x in D["lich_van_hanh"]:
    v=x.get("viec","")
    if "Giao ban nội bộ phòng tại Tổng công ty" in v:
        x["phu_trach"]="Trưởng phòng chủ trì; khi vắng, một trong hai Chuyên viên trưởng chỉ chủ trì theo phân công/ủy quyền còn hiệu lực. Marketing cơ sở giao ban do Trưởng nhóm tại chỗ."
    elif "Cập nhật danh sách từ khóa, hình ảnh, video bị cấm" in v or "Cập nhật chính sách các nền tảng" in v:
        x["phu_trach"]="Quản lý sản phẩm số cập nhật; "+title2+" kiểm chuẩn kênh; Pháp chế xác nhận pháp lý khi áp dụng; Trưởng phòng/cấp được phân quyền phê duyệt quy tắc. Quảng cáo và kênh số của nhóm triển khai."
    elif "Hội thảo chia sẻ giữa các cơ sở" in v:
        x["phu_trach"]=title1+" điều phối lịch, tài liệu; "+title2+" đào tạo phần truyền thông/thương hiệu/kênh số."
    elif "Thu hồi quyền kênh 01 ngày / 48 giờ" in v:
        x["phu_trach"]="Quyền quản trị cao nhất: Trưởng phòng/người được chỉ định; "+title2+" kiểm chuẩn yêu cầu kênh; cấp/thu hồi quyền thao tác bởi người có quyền theo ma trận. Kho tư liệu: "+title1+" phối hợp chủ thư mục."
    elif "Tổng hợp mạo danh trên mạng" in v:
        x["phu_trach"]="Chuyên viên truyền thông đúng nhóm tổng hợp; "+title2+" kiểm chuẩn hai nhóm; khủng hoảng liên nhóm báo Trưởng phòng."
    elif "Theo dõi giờ dự phòng" in v:
        x["phu_trach"]="Tổ trưởng mỗi tổ theo dõi tải; "+title1+" tổng hợp phần Nội dung/Cơ sở; "+title2+" tổng hợp hai tổ Truyền thông/Tăng trưởng số. Dự phòng quá 02 tuần báo Trưởng phòng."
    elif "Rà soát định biên trong 10 ngày" in v:
        x["phu_trach"]=title1+" tổng hợp giờ Nội dung/Cơ sở, "+title2+" xác nhận giờ hai tổ; Chuyên viên đo lường và đối soát kiểm chứng; Trưởng phòng trình/duyệt trong thẩm quyền."
    elif "Phiếu góp ý quý của Ban Giám đốc cơ sở" in v:
        x["phu_trach"]=title1+" chủ trì theo tuyến quản lý Trưởng nhóm; "+title2+" cung cấp nhận xét nghiệp vụ, không lập phiếu đánh giá thứ hai."
    elif "Giao ban Tổng công ty 11:00 thứ Hai" in v:
        x["phu_trach"]="Trưởng phòng dự; khi khuyết/vắng, chỉ Chuyên viên trưởng được ủy quyền bằng văn bản tham gia với vai trò phụ trách tạm thời."
    elif "Giao ban với Tổng Giám đốc thứ Tư" in v:
        x["phu_trach"]="02 tuần/lần: Trưởng phòng, cả hai Chuyên viên trưởng và Tổ trưởng được phân công; 04 tuần/lần: cả phòng."
    elif "Báo cáo giờ làm chéo nhóm" in v:
        x["phu_trach"]=title1+" kiểm phần sản xuất và cơ sở; "+title2+" kiểm phần truyền thông, số; Chuyên viên đo lường và đối soát xác nhận một dòng giờ/mã việc."
    elif "Cho phép làm thay chéo nhóm có thời hạn" in v:
        x["phu_trach"]="Người trung lập theo RC-1 (Tổ Nội dung: "+title1+"; Tổ Tăng trưởng số: người được chỉ định theo quyết định). Quyền tạm do người được cấp quyền theo ma trận thu hồi đúng hạn."
# Generic people who can make formal decisions should never appear as a free-form fallback.
for r in D["quy_tac"]:
    text=r.get("noi_dung","")
    if "việc mức Trưởng phòng khi chưa có Trưởng phòng: Chuyên viên trưởng duyệt" in text:
        r["noi_dung"]=text.replace(
          "việc mức Trưởng phòng khi chưa có Trưởng phòng: Chuyên viên trưởng duyệt",
          "việc thuộc thẩm quyền Trưởng phòng khi khuyết/vắng: chỉ người được phân quyền/ủy quyền cụ thể còn hiệu lực được duyệt; nếu không có thì trình cấp trên có thẩm quyền")
    elif "Trưởng phòng – chưa có: Chuyên viên trưởng" in text:
        r["noi_dung"]=text.replace(
          "Trưởng phòng – chưa có: Chuyên viên trưởng",
          "Trưởng phòng hoặc người được Ban Tổng Giám đốc phân công rõ bằng văn bản khi khuyết vị trí")
# Two Chuyên viên trưởng each cover their own training and period; no double direct manager.
D["doi_chieu_mau_va_luong_cvt_1911"]={
 "nguon":"Đối chiếu chủ trì văn bản, người nắm giữ biểu mẫu, việc định kỳ, thủ tục và 26 bảng chỉ số từ cùng CSDL",
 "nguyen_tac":"Một mã việc một người chủ trì; hai CVT có thể kiểm lĩnh vực khác nhau nhưng không duyệt/phân tải/đánh giá trùng",
 "chuc_danh":{id:{"ten":vt[id]["ten"],"to_phu_trach":["nd","coso"] if id=="cvt" else ["th","ts"]}
                for id in ("cvt","cvt-2")},
 "du_lieu_bat_buoc":["manager_id","nguoi_chu_tri_cong_viec","nguoi_kiem_chuyen_mon",
 "nguoi_nghiem_thu","nguoi_duyet_phat_hanh","nguoi_duyet_chi","ngay_hieu_luc",
 "ma_uy_quyen","nguoi_thay","han_muc_quyen","ma_ban_ghi_gio","nguon_so_lieu_KPI"],
 "canh_bao_khi_chua_co_phe_duyet":"Thiếu văn bản ủy quyền, định mức giờ, quyết định KPI, dự toán mở cơ sở ⇒ không tự động đánh dấu đủ điều kiện vận hành/đã duyệt"
}
# Make all referenced id links resolve, and no declared role missing.
assert len(D["vi_tri"])==26
assert len(D["quy_trinh"])==60
assert all(x.get("chu_tri_chinh") for z in D["quy_trinh"] for x in z["buoc"])
assert len(D["kpi_vi_tri"])==26

# Render present-day staffing separately from the old chart 34 → 56, which is not reconciled.
old_phase=scenario["buoc"]
rows="".join("<tr><td>"+escape(x["buoc"].replace("Tham chiếu lịch sử – ",""))+
 "<td>"+str(x["tct"])+"</td><td>"+str(x["co_so"])+"</td><td>"+str(x["tong"])+
 "</td></tr>" for x in old_phase)
header='<div class="card" id="tth-dinh-bien-corrected-1911" style="border-left:5px solid #ED3237">'
header+='<h3 style="color:#0837A1;margin-top:0">Định biên cơ cấu hiện tại: 36 suất (phương án trình, chưa ban hành quyết định sử dụng nhân sự)</h3>'
header+='<p><strong>22 suất tại Tổng công ty + 14 suất tại cơ sở.</strong> Bao gồm 02 Chuyên viên trưởng và 03 tổ chuyên môn. Không cộng Tổ trưởng kiêm nhiệm thành suất riêng nếu đã tính trong định mức.</p>'
header+='<p><strong>Chưa có lộ trình mở rộng thay thế sau khi điều chỉnh cơ cấu.</strong> Mốc 34/40/43/50/53/56 là kịch bản trước điều chỉnh, không được sử dụng làm số liệu hiện hành, so sánh biến động hoặc tự động ra quyết định tuyển dụng.</p>'
header+='<details><summary style="cursor:pointer;color:#0837A1;font-weight:700">Xem lộ trình tham chiếu cũ (không áp dụng để bố trí người)</summary><div class="tbl"><table class="t"><thead><tr><th>Mốc tham chiếu cũ</th><th>TCT</th><th>Cơ sở</th><th>Tổng</th></tr></thead><tbody>'+rows+'</tbody></table></div></details></div>'
rx=r'<div class="card"><figure class="chart"><figcaption><b>Định biên theo lộ trình mở rộng</b>[\s\S]*?</figure></div>'
if len(re.findall(rx,s))!=1: raise ValueError("Staffing legacy chart changed")
s=re.sub(rx,header,s,count=1)
s=s.replace('<div class="stat"><b>56</b><span>khi đủ 10 bệnh viện; gồm 01 Quản lý mạng lưới vùng</span></div>',
 '<div class="stat"><b>Chưa chốt</b><span>lộ trình mở rộng thay thế sau cơ cấu 36 suất</span></div>')
s=s.replace('<div class="stat"><b>56</b><span>khi đủ 10 bệnh viện, 02 phòng khám (gồm Quản lý mạng lưới vùng)</span></div>',
 '<div class="stat"><b>Chưa chốt</b><span>lộ trình mở rộng; 56 là kịch bản tham chiếu cũ</span></div>')
s=s.replace('<section class="doc-sec" data-title="21. Quy tắc định biên, ngưỡng và lộ trình bổ sung" id="m-21">',
 '<section class="doc-sec" data-title="21. Quy tắc định biên, ngưỡng và lộ trình bổ sung" id="m-21"><p style="padding:12px;border-left:4px solid #ED3237;background:#FFF9F9"><b>Lưu ý đối soát:</b> Các mốc 34 → 56 trong mục này thuộc phương án cũ; khi đổi sang 02 Chuyên viên trưởng và định biên hiện tại 36 suất, chưa thể coi các con số tiếp theo là lộ trình được chốt. Phải tính lại giờ thực đo theo từng chức danh/cơ sở và trình phê duyệt.</p>')
# KPI extra data must remain read-only proposal, not a salary policy.
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]
check=json.loads(re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s).group(1))
assert len(check["kpi_vi_tri"])==26
assert check["danh_muc_tai_lieu"][0]["ma"]==D["danh_muc_tai_lieu"][0]["ma"]
assert "tth-dinh-bien-corrected-1911" in s
assert check["lo_trinh_dinh_bien"]["trang_thai_sau_co_cau_2_cvt_1911"].startswith("LỘ TRÌNH THAM CHIẾU")
file.write_text(s,"utf-8")
c=Counter(x.get("nam_giu") for x in check["danh_muc_tai_lieu"])
print("CROSS-SECTION-CONSISTENCY PASS:",
 "26 KPI frameworks", "staffing 36 proposed/old 34-56 archived in presentation",
 "docs: CVT1",c["cvt"],"CVT2",c["cvt-2"],
 "incident access rights CVT2",check["quy_trinh"][38]["buoc"][-1]["chu_tri_chinh"])
