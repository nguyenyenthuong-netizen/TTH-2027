#!/usr/bin/env python3
"""Chốt hai tuyến CVT: sửa nghĩa vụ/quyền theo quy trình, chặn chữ CVT chung.

Chạy SAU kiểm tra mâu thuẫn & khóa định biên; TRƯỚC bảng chỉ số tổng hợp.
Không cấp quyền nhân sự/tài chính/phát hành khi thiếu văn bản có hiệu lực.
"""
from pathlib import Path
import json, re, sys
from collections import Counter
from html import escape

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
file=root/"khung-marketing"/"index.html"
src=file.read_text("utf-8")
m=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',src)
if not m: raise RuntimeError("Khong tim thay CSDL khung")
D=json.loads(m.group(2))
V={x["id"]:x for x in D["vi_tri"]}
Q={x["id"]:x for x in D["quy_trinh"]}
C1=V["cvt"]["ten"]
C2=V["cvt-2"]["ten"]
assert len(V)==26 and len(Q)==60 and (D["phan_dinh_quan_ly_hai_cvt_19112026"]["dinh_bien"]["tong"]==36)

# Không có "CVT chung"; mọi hành động được tách quản lý theo tuyến / quyền phê duyệt.
AUTH="người được phân quyền theo ma trận thẩm quyền có hiệu lực"
AUTH_APPROVE="cấp có thẩm quyền phê duyệt theo ma trận còn hiệu lực"
MGMT="người quản lý trực tiếp đúng tuyến theo quyết định phân công có hiệu lực"
CROSS="Trưởng phòng Marketing hoặc người được Ban Tổng Giám đốc ủy quyền bằng văn bản"
def step(qid,n): return Q[qid]["buoc"][n-1]
def replace(qid,n,a,b):
    z=step(qid,n); old=z.get("noi_dung","")
    if a in old: z["noi_dung"]=old.replace(a,b)
    elif b not in old:
        raise ValueError("Doi nguon quy trinh: "+qid+" buoc "+str(n)+" : "+a)
def participants(qid,n,*items):
    z=step(qid,n)
    co=z.setdefault("phoi_hop",[])
    for tag in items:
        role=tag.split("|")[0]
        # Mỗi mã vai trò chỉ một lần tại một bước; ghi chính xác trách nhiệm mới.
        co[:]=[x for x in co if str(x).split("|")[0]!=role]
        co.append(tag)
def setlead(qid,n,role):
    z=step(qid,n)
    z["chu_tri_chinh"]=role

# 1. Quyết định liên hai nhóm: không rơi vào CVT Nội dung do thói quen mô hình cũ.
replace("danh-gia",5,"Trưởng phòng chủ trì (chưa có Trưởng phòng: Chuyên viên trưởng)",
        "Trưởng phòng chủ trì; khi vị trí trống, chỉ người được Ban Tổng Giám đốc chỉ định bằng văn bản điều phối")
replace("bao-cao-giao-ban",3,"chưa có Trưởng phòng: Chuyên viên trưởng dự",
        "chưa có Trưởng phòng: người được Ban Tổng Giám đốc chỉ định bằng văn bản dự và tiếp nhận chỉ đạo")
replace("bao-cao-giao-ban",4,"Trưởng phòng vắng hoặc chưa có: Chuyên viên trưởng",
        "Trưởng phòng vắng hoặc chưa có: người được Ban Tổng Giám đốc chỉ định bằng văn bản chủ trì")
replace("bgd-coso-de-nghi",4,"Chuyên viên trưởng quyết định",
        "Trưởng phòng quyết định phần bất đồng về mục tiêu/thông điệp sau khi nhận ý kiến Quản lý thương hiệu; "
        +C1+" xử lý riêng phần điều phối nhân sự cơ sở theo tuyến")
setlead("bgd-coso-de-nghi",4,"tp")
participants("bgd-coso-de-nghi",4,"cvt|điều phối tuyến Marketing cơ sở","cvt-2|kiểm chuẩn thông điệp/truyền thông; không duyệt thay mục tiêu thương hiệu")
replace("xung-dot-lich",2,"không thống nhất: Chuyên viên trưởng quyết",
        "không thống nhất về nguồn lực trung lập: Trưởng phòng quyết")
replace("xung-dot-lich",3,"Chuyên viên trưởng quyết định phần điều phối nguồn lực trong khối mình quản lý",
        C1+" điều phối nguồn lực sản xuất và cơ sở; "+C2+
        " kiểm chuẩn năng lực, thứ tự ưu tiên của hai tổ phụ trách; xung đột liên tuyến chuyển Trưởng phòng quyết định")
participants("xung-dot-lich",3,"cvt-2|xác nhận tải và ưu tiên của hai tổ phụ trách","tp|quyết định xung đột nguồn lực trung lập/liên tuyến")
replace("yeu-cau-gap",4,"Chuyên viên trưởng điều phối",
        C1+" điều phối phần sản xuất/cơ sở; "+C2+" điều phối phần truyền thông/thương hiệu/tăng trưởng số")
participants("yeu-cau-gap",4,"cvt-2|xác nhận khả năng nhận việc của hai tổ chuyên môn")

# 2. Tách hành chính, quản lý nhân sự, hỗ trợ nghiệp vụ và phê duyệt nghỉ.
replace("vang-mat",1,
        "người nhóm 2, Chuyên viên thiết kế ngoại tuyến của Tổ Nội dung và Sáng tạo: Chuyên viên trưởng",
        "người thuộc Tổ Nội dung và Sáng tạo: "+C1+
        "; người thuộc Tổ Truyền thông và Thương hiệu hoặc Tăng trưởng số: "+C2+
        " quản lý lịch chuyên môn; quyết định nghỉ thuộc người được phân quyền theo quy chế nhân sự")
replace("vang-mat",3,"Tổ Nội dung và Sáng tạo: Chuyên viên trưởng; Tổ Tăng trưởng số: Quản lý sản phẩm số",
        "Tổ Nội dung và Sáng tạo: "+C1+"; Tổ Tăng trưởng số: "+
        C2+" hoặc người được giao xử lý trong tổ bằng văn bản")
replace("vang-mat",4,"Chuyên viên trưởng duyệt thứ tự ưu tiên",
        C1+" sắp xếp ưu tiên sản xuất/cơ sở, "+C2+
        " sắp xếp ưu tiên của hai tổ; phần liên tuyến trình Trưởng phòng")
participants("vang-mat",4,"cvt-2|xác nhận tải và phương án thay người thuộc hai tổ; không phê duyệt nghỉ thay Nhân lực")
replace("vang-mat",5,"Chuyên viên trưởng thu hồi quyền tạm",
        AUTH+" thu hồi đúng loại quyền tạm theo biên bản bàn giao; hai CVT đối soát theo tuyến")
participants("vang-mat",5,"cvt-2|đối soát hết quyền làm thay tạm thuộc hai tổ, không tự thu hồi quyền quản trị")
replace("nhan-viec-moi",2,"Giao mô tả công việc, hồ sơ vị trí, bảng phân công",
        "Người quản lý đúng tuyến giao mô tả công việc, hồ sơ vị trí, bảng phân công (Nội dung/cơ sở: "+
        C1+"; Truyền thông/Thương hiệu/Tăng trưởng số: "+C2+")")
replace("nhan-viec-moi",3,"quyền đăng bài, trả lời tin nhắn, kho tư liệu: Chuyên viên trưởng",
        "quyền đăng bài, trả lời tin nhắn: "+AUTH+
        " cấp theo tài sản/kênh; quyền kho tư liệu do đầu mối được phân quyền theo hệ thống, "+
        C1+" kiểm chuẩn hồ sơ sản xuất và "+C2+" kiểm chuẩn kênh")
replace("nhan-viec-moi",5,"Chuyên viên trưởng xác nhận",
        "người quản lý trực tiếp đúng tuyến xác nhận; trường hợp liên tuyến phải có Trưởng phòng xác nhận")
participants("nhan-viec-moi",2,"cvt-2|nhân sự thuộc Truyền thông, Thương hiệu, Tăng trưởng số")
participants("nhan-viec-moi",3,"cvt-2|đối chiếu vai trò và quyền kênh của hai tổ")
participants("nhan-viec-moi",4,"cvt-2|đào tạo chuẩn truyền thông, thương hiệu, số cho đúng đối tượng")
participants("nhan-viec-moi",5,"cvt-2|xác nhận bàn giao nhân sự thuộc hai tổ")
participants("nhan-viec-moi",6,"cvt-2|đánh giá kỹ năng nhân sự hai tổ theo tuyến")
for n in (2,4,5,6):
    step("nhan-viec-moi",n)["chu_tri_theo_tuyen_1911"]={
      "noi_dung_sang_tao_va_co_so":"cvt",
      "truyen_thong_thuong_hieu_tang_truong_so":"cvt-2",
      "quy_tac":"Mỗi nhân sự chỉ một người quản lý trực tiếp; Nhân lực giữ thẩm quyền nhân sự và Trưởng phòng quyết định liên tuyến."
    }

# 3. Kênh/OOH/quảng cáo/màn hình: CVT2 kiểm chuẩn, không tự phát sinh quyền cấp.
replace("co-so-moi",4,"quyền đăng bài, trả lời tin nhắn: Chuyên viên trưởng cấp theo ma trận",
        "quyền đăng bài, trả lời tin nhắn: "+AUTH+" cấp; "+C2+" kiểm chuẩn cấu hình kênh")
replace("co-so-moi",4,"Chuyên viên trưởng cấp theo ma trận quyền chỉ trả lời tin nhắn",
        AUTH+" cấp quyền chỉ trả lời tin nhắn")
participants("co-so-moi",4,"cvt-2|kiểm chuẩn kênh, quảng cáo, phân quyền; không tự cấp quyền cao nhất")
replace("su-kien-co-so",2,"Nội dung truyền thông: Chuyên viên trưởng duyệt; có báo chí, cấp hệ thống: Trưởng phòng",
        "Nội dung truyền thông: Biên tập kiểm nội dung; Quản lý thương hiệu nghiệm thu mục tiêu/thông điệp; "+
        C2+" kiểm chuẩn nghiệp vụ truyền thông; y khoa và phát hành do người được phân quyền phê duyệt riêng; có báo chí hoặc cấp hệ thống: Trưởng phòng xử lý theo quy chế")
participants("su-kien-co-so",2,"cvt-2|kiểm chuẩn truyền thông sự kiện, không duyệt thay phát hành")
replace("doi-ten-chuyen-nhom",6,"Chuyên viên trưởng duyệt",
        "Quản lý thương hiệu nhóm mới nghiệm thu thông điệp; "+C2+
        " kiểm chuẩn kênh; phát hành do "+AUTH_APPROVE)
participants("doi-ten-chuyen-nhom",6,"cvt-2|kiểm chuẩn thông tin, kênh số khi đổi thương hiệu")
replace("phap-luat",3,"Chuyên viên trưởng duyệt",
        C2+" kiểm chuẩn nghiệp vụ kênh và quảng cáo; bộ phận Pháp chế xác nhận pháp lý, "+
        AUTH_APPROVE+" phần yêu cầu áp dụng chính thức")
participants("phap-luat",3,"cvt-2|kiểm chuẩn chính sách nền tảng, kênh số, quảng cáo; không thay Pháp chế")
replace("nghien-cuu-thi-truong",2,"Chuyên viên trưởng duyệt",
        C2+" kiểm chuẩn phương pháp và nguồn dữ liệu; Trưởng phòng hoặc người được ủy quyền phê duyệt khảo sát; chi phí theo phân cấp riêng")
participants("nghien-cuu-thi-truong",2,"cvt-2|kiểm chuẩn khảo sát, phân tích và kênh thu; không phê duyệt ngân sách")

# 4. Bàn giao tài sản và thu hồi quyền là ba nhóm khác nhau.
setlead("chuyen-quyen",1,"cvt-2")
participants("chuyen-quyen",1,"cvt|lập danh mục kho tư liệu/file sản xuất; đối soát với Trưởng nhóm cơ sở")
replace("chuyen-quyen",2,"Trưởng phòng – chưa có: Chuyên viên trưởng",
        "Trưởng phòng – nếu chức danh trống: người được Ban Tổng Giám đốc chỉ định bằng văn bản")
replace("chuyen-quyen",2,"quyền đăng bài, trả lời tin nhắn: Chuyên viên trưởng cấp",
        "quyền đăng bài, trả lời tin nhắn: "+AUTH+" cấp")
replace("chuyen-quyen",4,"quyền: Chuyên viên trưởng",
        "quyền do "+AUTH+" cấp theo phân quyền kho sản xuất")
replace("chuyen-quyen",6,"quyền đăng bài, trả lời tin nhắn: Chuyên viên trưởng",
        "quyền đăng bài, trả lời tin nhắn: người được phân quyền thu hồi theo ma trận hiệu lực")
setlead("chuyen-quyen",7,"cvt-2")
participants("chuyen-quyen",7,"cvt|đối chiếu kho tư liệu, file sản xuất và hạn bàn giao","tp|nghiệm thu quyền/ủy quyền theo ma trận")
replace("nghi-viec",4,"Thu hồi quyền đăng bài, trả lời tin nhắn: Chuyên viên trưởng (theo ma trận quyền)",
        "Thu hồi quyền đăng bài, trả lời tin nhắn: "+AUTH+
        " thao tác, "+C2+" đối soát theo danh sách tài sản")
replace("nghi-viec",6,"Quyền kho tư liệu: Chuyên viên trưởng",
        "Quyền kho tư liệu: "+AUTH+"; "+C1+" kiểm kê tài sản sản xuất")
participants("nghi-viec",4,"cvt-2|kiểm quyền kênh và quảng cáo của nhân sự nghỉ việc")
participants("nghi-viec",6,"cvt|kiểm kê kho tư liệu sản xuất","cvt-2|kiểm tra quyền kênh sau thu hồi")

# 5. Gián đoạn công nghệ: đơn vị chủ hệ thống, đơn vị nghiệp vụ và người duyệt riêng.
replace("he-thong-gian-doan",1,"phần mềm Quản trị Marketing: Chuyên viên trưởng; kho tư liệu: Chuyên viên trưởng (quyền)",
        "phần mềm Quản trị Marketing: Quản lý sản phẩm số tiếp nhận sự cố công nghệ, Trưởng phòng điều phối nghiệp vụ; kho tư liệu: "+
        C1+" kiểm tài sản sản xuất, quyền hệ thống do "+AUTH)
replace("he-thong-gian-doan",2,"Tổ Truyền thông và Thương hiệu: Chuyên viên trưởng",
        "Tổ Truyền thông và Thương hiệu: Tổ trưởng được giao, chịu quản lý chuyên môn của "+C2)
replace("he-thong-gian-doan",6,"Chuyên viên trưởng kiểm soát việc nhập bù",
        "hai Chuyên viên trưởng kiểm soát nhập bù trong từng tuyến; Chuyên viên đo lường và đối soát đối chiếu độc lập")
participants("he-thong-gian-doan",1,"cvt-2|nhận thông báo sự cố kênh, quảng cáo và hai tổ")
participants("he-thong-gian-doan",2,"cvt-2|điều phối hai tổ nhập sổ tạm, không lệnh trực tiếp xuống Marketing cơ sở")
participants("he-thong-gian-doan",6,"cvt-2|kiểm đủ lịch/kết quả hai tổ","dl-1|đối soát bản ghi tạm và lịch sử phê duyệt")
for n in (1,2,6):
    step("he-thong-gian-doan",n)["phan_tuyen_1911"]={
      "nghiep_vu_san_xuat_co_so":"cvt",
      "nghiep_vu_truyen_thong_so":"cvt-2",
      "su_co_he_thong":"qlsps / don_vi_cong_nghe_duoc_giao",
      "duyet_thay":"Không phát sinh do lỗi phần mềm; chuyển cấp có văn bản ủy quyền."
    }

# 6. Văn bản: đầu mối soạn/quản lý khác chủ trì nghiệp vụ, kiểm chuẩn khác phát hành/chi.
new_doc_leads={
  "QT.19":"Đầu vào yêu cầu truyền thông của đơn vị thuộc nhóm 2; sản xuất bàn giao theo tuyến Nội dung – Cơ sở",
  "QT.23":"Chủ trì phần kênh, quảng cáo và phân quyền; CVT Nội dung – Cơ sở chủ trì nghiệp vụ kho tư liệu sản xuất",
  "QT.35":"Chuẩn truyền thông nội bộ; Phòng Nhân lực hoặc đơn vị sở hữu thông tin nội bộ xác nhận nội dung gốc",
  "QT.55":"Kiểm chuẩn quảng cáo sản phẩm y tế theo kênh; xác nhận y khoa/pháp lý, duyệt phát hành/chi độc lập"
}
doc_map={x["ma"]:x for x in D["danh_muc_van_ban"]}
for code,note in new_doc_leads.items():
    if code not in doc_map: raise ValueError("Thieu van ban "+code)
    doc_map[code]["chu_tri"]="cvt-2"
    doc_map[code]["trach_nhiem_nghiep_vu"]=note
    doc_map[code]["ghi_chu_quyen_1911"]="Chủ trì xây dựng quy trình không đồng nghĩa quyền ký, duyệt, phát hành hoặc duyệt ngân sách."
for d in D["danh_muc_van_ban"]:
    if isinstance(d.get("nguoi_duyet"),str):
        d["nguoi_duyet"]=d["nguoi_duyet"].replace(
          "Chuyên viên trưởng lập khi chưa có Trưởng phòng",
          "Đầu mối chủ trì lập văn bản theo mã vị trí tại danh mục; khi chưa có Trưởng phòng vẫn phải trình đúng cấp")
    if "Chuyên viên trưởng" in str(d.get("nguoi_duyet","")) and not (
        C1 in str(d["nguoi_duyet"]) or C2 in str(d["nguoi_duyet"])):
        d["nguoi_duyet"]=str(d["nguoi_duyet"]).replace(
          "Chuyên viên trưởng",MGMT)
for f in D["danh_muc_tai_lieu"]:
    for fld in f.get("truong",[]):
        for key in ("nguoi_nhap","nguoi_xem","nguoi_duyet"):
            if key in fld and isinstance(fld[key],str):
                fld[key]=fld[key].replace(
                    "Chuyên viên trưởng",
                    C1+" (chỉ hồ sơ sản xuất/cơ sở) hoặc "+C2+
                    " (chỉ truyền thông/thương hiệu/số), theo quyền truy cập được cấp")
    if isinstance(f.get("noi_dung"),str):
        f["noi_dung"]=f["noi_dung"].replace("Chuyên viên trưởng tổng hợp",
            "hai Chuyên viên trưởng cung cấp dữ liệu đúng tuyến, Trưởng phòng tổng hợp")

# 7. Không còn đường tắt dùng tên chức danh chung trong mô tả bước và ngoại lệ.
# Đây là bộ quy tắc an toàn: "duyệt" => cấp phân quyền, "cấp/thu hồi" => chủ quyền tài sản.
GENERIC=re.compile(r'Chuyên viên trưởng(?!\s+(?:Nội dung|Truyền thông))',re.I)
def repair_string(s):
    # Tôn trọng cách gọi tập hợp rõ "hai/02 Chuyên viên trưởng".
    s=s.replace("Chuyên viên trưởng duyệt",AUTH_APPROVE)
    s=s.replace("Chuyên viên trưởng phê duyệt",AUTH_APPROVE)
    s=s.replace("Chuyên viên trưởng cấp",AUTH+" cấp")
    s=s.replace("Chuyên viên trưởng thu hồi",AUTH+" thu hồi")
    s=s.replace("Chuyên viên trưởng quyết định",AUTH+" quyết định")
    s=s.replace("Chuyên viên trưởng chủ trì",MGMT+" chủ trì")
    s=s.replace("Chuyên viên trưởng điều phối",MGMT+" điều phối")
    s=s.replace("Chuyên viên trưởng kiểm soát",MGMT+" kiểm soát")
    s=s.replace("Chuyên viên trưởng đánh giá",MGMT+" đánh giá")
    s=s.replace("Chuyên viên trưởng xem",MGMT+" xem")
    s=s.replace("Chuyên viên trưởng xác nhận",MGMT+" xác nhận")
    s=s.replace("Chuyên viên trưởng xử lý",MGMT+" xử lý")
    s=s.replace("Chuyên viên trưởng giữ",MGMT+" quản lý")
    def rewrite(m):
        before=s[max(0,m.start()-8):m.start()]
        if re.search(r'(hai|02|2)\s*$',before,re.I): return m.group()
        return MGMT
    return GENERIC.sub(rewrite,s)
def walk(obj):
    if isinstance(obj,str):return repair_string(obj)
    if isinstance(obj,list):return [walk(x) for x in obj]
    if isinstance(obj,dict):return {k:walk(v) for k,v in obj.items()}
    return obj
for key in ("quy_trinh","vi_tri","mang_viec","mang_viec_bo_sung",
            "lich_van_hanh","ngoai_le_cheo_nhom","quy_tac","van_hanh_hai_che_do",
            "phuong_an_nguoi_thay","phan_cap_duyet_17112026"):
    if key in D: D[key]=walk(D[key])

# 8. Ma trận tiêu chuẩn, có thể kiểm tra máy, tách 5 cửa quyền và 2 tuyến quản lý.
D["chot_phan_dinh_hai_cvt_19112026"]={
 "trang_thai":"Ranh giới nghiệp vụ được chuẩn hóa để trình duyệt; không thay thế văn bản ủy quyền/ban hành",
 "cvt_noi_dung_co_so":{
  "quan_ly_truc_tiep":"Tổ Nội dung và Sáng tạo, Trưởng nhóm Marketing bệnh viện của cả hai nhóm",
  "co_quyen":"Điều phối tải, hạn, nguồn lực sản xuất và đánh giá theo tuyến; chỉ duyệt khi ma trận quyền có hiệu lực ghi rõ",
  "khong_co_quyen_mac_nhien":"Phát hành truyền thông, duyệt chi, xác nhận y khoa/pháp lý, cấp tài khoản hoặc quản lý nhân sự của hai tổ còn lại"
 },
 "cvt_truyen_thong_so":{
  "quan_ly_truc_tiep":"Tổ Truyền thông và Thương hiệu, Tổ Tăng trưởng số tại Tổng công ty",
  "quan_ly_nghiep_vu":"Chuẩn và kiểm tra truyền thông, PR/OOH, phát thanh, màn hình, quảng cáo, kênh số ở cả hai nhóm",
  "khong_co_quyen_mac_nhien":"Điều lệnh trực tiếp Trưởng nhóm cơ sở, tự duyệt phát hành, ngân sách, xác nhận y khoa/pháp lý hoặc cấp quyền quản trị cao nhất"
 },
 "nam_cua_bat_buoc":["Kiểm biên tập và kỹ thuật đầu ra","Xác nhận chuyên môn y khoa/pháp lý khi áp dụng",
 "Nghiệm thu thông điệp, mục tiêu thương hiệu","Phê duyệt phát hành theo thẩm quyền còn hiệu lực",
 "Phê duyệt chi phí theo phân cấp độc lập"],
 "trinh_tu_vi_du":"Quản lý thương hiệu giao yêu cầu; người sản xuất làm; biên tập/thiết kế/media kiểm kỹ thuật; xác nhận y khoa/pháp lý; quản lý thương hiệu nghiệm thu; người có thẩm quyền phát hành duyệt; người được phân quyền đăng; chi phí duyệt riêng",
 "quy_tac_ngoai_le":"Không có Trưởng phòng hoặc hết hạn xử lý không làm phát sinh quyền duyệt mặc định cho bất kỳ CVT nào.",
 "buoc_bat_buoc_trong_phan_mem":["manager_id","nguoi_chu_tri","nguoi_kiem_chuyen_mon","nguoi_xac_nhan_y_khoa_phap_ly",
 "nguoi_nghiem_thu_thuong_hieu","nguoi_duyet_phat_hanh","nguoi_duyet_chi",
 "ma_uy_quyen","ngay_hieu_luc","nguoi_ban_giao","tai_san_quyen"]
}
# Cập nhật danh mục CVT2 thực sự chủ trì soạn, không để bảng tổng hợp cũ.
if "cvt_phan_cong_van_ban_1911" in D:
    D["cvt_phan_cong_van_ban_1911"]["cvt_2_chu_tri_xay_dung"]=sorted(
        x["ma"] for x in D["danh_muc_van_ban"] if x.get("chu_tri")=="cvt-2")
D["ghi_chu_kiem_soat_chuyen_vien_truong_1911"]={
 "nguon_du_lieu":"60 quy trình, 407 bước, 83 văn bản, 26 mô tả vị trí",
 "phan_biet":"Hai chức danh cụ thể trong quản lý; các cụm gọi chung trong bước nghiệp vụ được thay bằng tuyến quản lý hoặc cấp có quyền rõ ràng",
 "dieu_kien_nghiem_thu":"Kiểm bản hiển thị sau chạy chuỗi xuất bản, hồ sơ ủy quyền, mã quyền, KPI và chứng cứ nghiệm thu"
}

# Ghép JSON: biến đổi nguồn sử dụng khi người dùng chọn Quy trình, Vị trí, Biểu mẫu.
mm=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',src)
src=src[:mm.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+src[mm.end(2):]

# Các bảng HTML dựng sẵn (khác CSDL) phải cùng cách gọi, không thể chỉ sửa JSON.
# Chỉ thay nội dung text ngoài script/style; không thay JS, ID, tên file và lịch sử.
parts=re.split(r'(<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>)',src,flags=re.I)
for i in range(0,len(parts),2):
    x=parts[i]
    # Đối chiếu nhãn quyền nghiêm trọng thường tồn tại trong HTML tĩnh cũ.
    x=x.replace("Trưởng phòng – chưa có: Chuyên viên trưởng",
                "Trưởng phòng; khi trống phải có văn bản chỉ định của Ban Tổng Giám đốc")
    x=x.replace("Tổ Truyền thông và Thương hiệu: Chuyên viên trưởng",
                "Tổ Truyền thông và Thương hiệu: Tổ trưởng được giao; "+C2+" quản lý chuyên môn")
    x=x.replace("Chuyên viên trưởng duyệt nội dung","Người được phân quyền duyệt phát hành; kiểm y khoa, pháp lý và thương hiệu riêng")
    x=x.replace("Chuyên viên trưởng duyệt phương án",C2+" kiểm chuẩn phương án; phê duyệt theo ma trận còn hiệu lực")
    x=x.replace("Chuyên viên trưởng phê duyệt phân công theo văn bản/phạm vi",
                CROSS+" phê duyệt chuyển tuyến theo văn bản phân công")
    x=x.replace("Chuyên viên trưởng duyệt phần thường xuyên theo phân cấp",
                AUTH_APPROVE+" phần thường xuyên theo loại sản phẩm")
    x=x.replace("quá hạn: Chuyên viên trưởng duyệt",
                "quá hạn: chuyển cấp được ủy quyền bằng văn bản; không có duyệt tự động")
    # Các câu duyệt/cấp/phát hành còn gọi CVT chung trong phần hiển thị.
    def text_fix(m):
        return repair_string(m.group(0))
    x=re.sub(r'(?<=>)[^<>]*Chuyên viên trưởng[^<>]*(?=<)',text_fix,x,flags=re.I)
    parts[i]=x
src="".join(parts)

# Bảng đối chiếu dùng cho người nghiệm thu, nằm trong chính tab JD, không thay menu.
if 'id="tth-cvt-authority-guard-1911"' not in src:
    marker='<section class="view" data-view="jd" id="v-jd">'
    assert marker in src,"Tab JD marker lost"
    html=('<section id="tth-cvt-authority-guard-1911" style="border:1px solid #d6e2f1;'
          'border-left:5px solid #0837A1;background:#fff;padding:14px;margin:12px 0;border-radius:10px">'
          '<strong style="color:#0837A1">Hai tuyến Chuyên viên trưởng – quy tắc bắt buộc</strong>'
          '<p><b>'+escape(C1)+'</b>: quản lý Nội dung – Sáng tạo và trực tiếp quản lý Trưởng nhóm cơ sở cả hai nhóm.</p>'
          '<p><b>'+escape(C2)+'</b>: quản lý Truyền thông – Thương hiệu và Tăng trưởng số tại Tổng công ty; '
          'kiểm chuẩn nghiệp vụ toàn hệ thống, không chỉ huy trực tiếp Marketing cơ sở.</p>'
          '<p>Chủ trì quy trình ≠ kiểm chuẩn ≠ nghiệm thu thương hiệu ≠ duyệt phát hành ≠ duyệt chi. '
          'Quyền cấp/thu hồi tài khoản theo ma trận hiệu lực; chức danh Trưởng phòng đang trống '
          'không làm tự phát sinh thẩm quyền cho một Chuyên viên trưởng.</p></section>')
    src=src.replace(marker,marker+html,1)

# Cửa nghiệm thu tự động: sai quy trình sẽ chặn triển khai Pages thay vì công bố sai.
check=json.loads(re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',src).group(1))
q={x["id"]:x for x in check["quy_trinh"]}
assert len(q)==60 and len(check["vi_tri"])==26 and len(check["danh_muc_van_ban"])==83
assert sum(len(x["buoc"]) for x in q.values())==407
assert check["phan_dinh_quan_ly_hai_cvt_19112026"]["dinh_bien"]["tong"]==36
lead=Counter(str(b.get("chu_tri_chinh","")).split("|")[0] for f in q.values() for b in f["buoc"])
assert lead["cvt-2"]>=2, "CVT2 never leads any actual process steps"
assert sum(v.get("chu_tri")=="cvt-2" for v in check["danh_muc_van_ban"])>=18
for qid in ("danh-gia","bao-cao-giao-ban","su-kien-co-so","co-so-moi",
            "chuyen-quyen","nghien-cuu-thi-truong","phap-luat","xung-dot-lich",
            "vang-mat","nhan-viec-moi","doi-ten-chuyen-nhom"):
    for b in q[qid]["buoc"]:
        assert "Chuyên viên trưởng duyệt" not in json.dumps(b,ensure_ascii=False),qid
        assert "chưa có Trưởng phòng: Chuyên viên trưởng" not in json.dumps(b,ensure_ascii=False),qid
allops=json.dumps(q,ensure_ascii=False)
assert not re.search(r'Chuyên viên trưởng (?:duyệt|quyết định|cấp|thu hồi|phê duyệt)\b',allops)
assert "tth-cvt-authority-guard-1911" in src
file.write_text(src,"utf-8")
print("TTH-CVT-FINAL-AUTHORITY PASS",
      "roles",len(check["vi_tri"]),"flows",len(q),"steps",sum(len(x["buoc"]) for x in q.values()),
      "cvt1-lead",lead["cvt"],"cvt2-lead",lead["cvt-2"],
      "cvt2-doc",sum(v.get("chu_tri")=="cvt-2" for v in check["danh_muc_van_ban"]))
