#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Khóa các mâu thuẫn vận hành còn sót sau vòng chuẩn hóa CNNV.
Giai đoạn: cuối pipeline trước khi công bố GitHub Pages.
Không tự tạo quyền phê duyệt, không tự nhận đã có quyết định bổ nhiệm/ủy quyền.
"""
import json,re,sys
from collections import Counter
from html import escape
from pathlib import Path

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
f=root/"khung-marketing"/"index.html"
s=f.read_text("utf-8")
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s)
if not m: raise RuntimeError("Mất dữ liệu khung")
d=json.loads(m.group(2))
vs={v["id"]:v for v in d["vi_tri"]}
ND=vs["cvt"]["ten"]
TT=vs["cvt-2"]["ten"]
assert len(vs)==26 and len(d["quy_trinh"])==60 and len(d["danh_muc_van_ban"])==83
assert sum(len(q["buoc"]) for q in d["quy_trinh"])==407
assert d["phan_dinh_quan_ly_hai_cvt_19112026"]["dinh_bien"]["tong"]==36

# 1. Tổ trưởng Nội dung và Sáng tạo phải điều phối toàn tổ, không đẩy phần
# nhóm 2/ngoại tuyến thành công việc điều phối hằng ngày thường trực của CVT.
tr=next(x for x in d["vai_tro"] if x["id"]=="tt-nd")
tr["viec"]=(
    "Một Tổ trưởng được chỉ định điều phối lịch và phân công nghiệp vụ sản xuất cho toàn Tổ Nội dung "
    "và Sáng tạo: Biên tập, Thiết kế, Media của cả hai nhóm và Thiết kế ngoại tuyến; "
    "lịch dùng thiết bị Media chung; ghi mã việc và giờ đúng người làm. "
    "Có quyền điều phối ưu tiên trong tải được phê duyệt; không tự sản xuất chéo nhóm, "
    "không tự duyệt pháp lý, y khoa, phát hành, ngân sách hoặc nghỉ phép ngoài phân quyền. "
    "Trường hợp phát sinh xung đột năng lực liên nhóm hoặc vượt định mức, "
    "trình "+ND+" kiểm tra và xử lý theo tuyến. "
    "Chỉ kích hoạt phạm vi điều phối cả tổ sau khi có văn bản phân công cá nhân, "
    "ngày hiệu lực, người thay và giới hạn quyền."
)
tr["gio"]=(
    "Chưa đủ giờ thực đo của vai trò kiêm Tổ trưởng trên toàn tổ; "
    "không sử dụng ước tính 17 giờ và 13 giờ/tháng của phương án chia việc cũ để khẳng định tải."
)
tr["dieu_kien_giu_tam"]=(
    "Chỉ người có tên trong phân công có hiệu lực và đủ năng lực/không xung đột lợi ích; "
    "trong thời gian vắng, cấp có thẩm quyền chỉ định người thay có thời hạn. "
    "Không mặc nhiên chuyển quyền sang "+ND+" hoặc người trong nhóm."
)
d["quy_tac_to_truong_to_noi_dung_2027"]={
    "pham_vi":"01 đầu mối điều phối thường lệ cho Biên tập–Thiết kế–Media của cả hai nhóm và Thiết kế ngoại tuyến",
    "chu_the":"Người đang giữ vai trò Tổ trưởng Tổ Nội dung và Sáng tạo theo quyết định phân công có hiệu lực; chức danh gốc: Chuyên viên biên tập nhóm 1",
    "nhan_su":"Không lập thêm suất; giờ kiêm nhiệm tính riêng ngoài giờ trực tiếp biên tập, không cộng trùng giờ "+ND,
    "gio":"Chưa có nhật ký thời gian thực đo cho phạm vi mở rộng; cần thử tải trước khi giao chỉ tiêu",
    "vuot_tai":"Tổ trưởng chuyển xung đột và đề xuất ưu tiên lên "+ND+"; việc chạm ranh giới truyền thông/số phối hợp "+TT,
    "chan":"Chưa có quyết định phân công đầy đủ thì không coi Tổ trưởng có quyền giao việc chéo nhóm, duyệt nghỉ hoặc duyệt phát hành."
}
# Giữ thông tin cũ dưới nhãn lịch sử (nếu hệ thống cần truy vết), không dùng như định mức hiện hành.
for x in d.get("kiem_toan_tai_quan_ly_2027",{}).get("bat_cap_cu_the",[]):
    assert isinstance(x,str)
vs["cvt"]["phan_dinh_chu_tri_dau_ra"] += (
    " Điều phối liên nhóm chỉ khi vượt khả năng giải quyết của Tổ trưởng Tổ Nội dung và Sáng tạo; "
    "không tự nhận giờ phân công hằng ngày của Tổ trưởng làm đầu ra quản trị."
) if "Điều phối liên nhóm chỉ khi vượt" not in vs["cvt"]["phan_dinh_chu_tri_dau_ra"] else ""

# 2. Mỗi mã vai trò tổng quát trong quy trình MẪU phải giải được về
# đúng mã vị trí của hai nhóm trước khi mở một mã việc thực tế.
mapping={
 "qlth":("qlth-a","qlth-bc"),
 "cvtt":("cvtt-a","cvtt-bc"),
 "bt":("bt-ac","bt-b"),
 "qc":("qc-a","qc-b"),
 "md":("md-ac","md-b"),
 "tk":("tk-a","tk-b"),
 "tn":("tn-a","tn-b"),
 "mkt-coso":("tn-a","tn-b"),
 "tt-nd":("bt-ac","bt-ac"),
 "mkt-tct":("tp","tp"),
}
assert all(a in vs and b in vs for a,b in mapping.values())
d["ma_tran_chu_tri_theo_nhom_2027"]={
 k:{"nhom_1":a,"nhom_2":b,
    "ghi_chu":("Trưởng nhóm là đầu mối chịu trách nhiệm điều phối tại cơ sở; "
               "chuyên viên Media/Truyền thông thực hiện từng tác vụ được giao."
               if k=="mkt-coso" else
               "Từng vị trí phải cập nhật báo cáo riêng; Trưởng phòng chỉ tổng hợp, "
               "không thay trách nhiệm của từng người lập báo cáo."
               if k=="mkt-tct" else
               "Vai trò kiêm Tổ trưởng chỉ hoạt động khi có quyết định phân công."
               if k=="tt-nd" else
               "Đúng vị trí theo nhóm đã xác nhận, không tự thay người chéo nhóm.")}
 for k,(a,b) in mapping.items()
}
ambiguous=[]
same_role=[]
for q in d["quy_trinh"]:
 for i,b in enumerate(q["buoc"],start=1):
    key=str(b.get("chu_tri_chinh","")).split("|",1)[0]
    if key in mapping:
        a,c=mapping[key]
        if key=="mkt-tct":
            note=("Bước tổng hợp toàn Tổng công ty: TỪNG VỊ TRÍ tự chịu trách nhiệm bản ghi đầu vào; "
                  "Trưởng phòng Marketing chịu trách nhiệm một báo cáo tổng hợp. "
                  "Bắt buộc lưu người lập, người kiểm độc lập và người duyệt theo phân cấp.")
        elif key=="tt-nd":
            note=("Một người giữ vai trò Tổ trưởng Tổ Nội dung và Sáng tạo được chỉ định bằng văn bản "
                  "chịu trách nhiệm điều phối. Không lấy giờ điều phối của người này cộng vào tải "+ND+".")
        else:
            note=("Việc thuộc nhóm 1: "+vs[a]["ten"]+"; thuộc nhóm 2: "+vs[c]["ten"]+
                  ". Một mã việc phải xác định đúng nhóm/cơ sở trước khi giao. "
                  "Trường hợp cả hai nhóm: tách hai gói việc có mã nhánh và người chịu trách nhiệm riêng; "
                  "Trưởng phòng Marketing điều phối, không gộp mơ hồ hai người thành một chủ việc.")
        b["phan_cong_thuc_thi_2027"]=note
        b["ma_vi_tri_nhom_1_2027"]=a
        b["ma_vi_tri_nhom_2_2027"]=c
        b["dieu_kien_giao_viec_2027"]=(
            "Bắt buộc có mã việc, nhóm thương hiệu, cơ sở, cá nhân chủ trì, hạn, "
            "người kiểm/người duyệt và căn cứ phân quyền; nếu thiếu thì khóa giao việc."
        )
        ambiguous.append((q["id"],i,key))
    who=str(b.get("chu_tri_chinh","")).split("|",1)[0]
    dup=[p for p in b.get("phoi_hop",[]) if str(p).split("|",1)[0]==who]
    if dup:
        same_role.append((q["id"],i,who))
        # Giữ mã chức danh của người kiểm nếu hai người cùng chuyên môn; không
        # được hiểu mã giống nhau = cùng một cá nhân. Khi thiếu người thứ hai,
        # bắt buộc xin phân công kiểm độc lập, không cho tự kiểm.
        b["kiem_soat_khong_tu_kiem_2027"]=(
            "Mã chức danh chủ trì trùng mã phối hợp nhưng PHẢI là hai cá nhân khác nhau "
            "nếu đây là bước kiểm/nhận bàn giao. Hệ thống phải đối chiếu mã nhân sự thực tế; "
            "nếu trùng người, khóa nghiệm thu và chuyển người kiểm độc lập đủ năng lực "
            "theo quyết định phân công. Không cấp quyền duyệt vì đổi người kiểm."
        )
        b["chan_trung_nguoi_2027"]=True
# Các bước rõ một chủ trì nhưng có cộng tác cùng chức danh chỉ được coi là
# phối hợp khi có ít nhất hai mã nhân sự khác nhau. Tránh tự duyệt.
assert len(ambiguous)==95, "Số bước dùng mã tổng quát đã thay đổi: "+str(len(ambiguous))
assert len(same_role)==14, "Số bước trùng mã chủ trì/phối hợp thay đổi: "+str(len(same_role))

# 3. Dữ liệu MTCV, người thay và tuyến duyệt phải đúng người; cấm chính mình tự duyệt.
v=vs
v["qc-a"]["phan_dinh_kiem_duyet"]=(
 "Quản lý thương hiệu nhóm 1 nghiệm thu lịch và mục tiêu; "+TT+
 " kiểm chuẩn rủi ro kênh số. Cấp/thu hồi quyền tài khoản, "
 "phê duyệt phát hành và chi phí chỉ do người được phân quyền bằng văn bản còn hiệu lực, "
 "không do người vận hành quảng cáo tự quyết."
)
v["dl-1"]["du_phong"]=[
 z.replace("do Chuyên viên trưởng kiểm","do "+TT+" kiểm độc lập")
 for z in v["dl-1"]["du_phong"]
]
v["qlml"]["phan_dinh_chu_tri_dau_ra"]=(
 "Chỉ đánh giá cấp 1 Trưởng nhóm Marketing cơ sở thuộc danh sách đã được bàn giao có hiệu lực; "
 "điều phối tải và hỗ trợ triển khai trong vùng được giao; "+ND+
 " chịu trách nhiệm kiểm tra và tổng hợp theo tuyến, không cùng đánh giá cấp 1 một người."
)
for code in ("tn-a","tn-b"):
 x=v[code]
 x["phan_dinh_kiem_duyet"]=re.sub(
    r'(theo phân cấp)\s+('+re.escape(ND)+r')',
    r'\1. \2',
    x["phan_dinh_kiem_duyet"]
 )
 x["phan_dinh_kiem_duyet"]=x["phan_dinh_kiem_duyet"].replace(
     "nghiệm thu sản phẩm/lịch "+ND,
     "nghiệm thu sản phẩm/lịch theo đúng cấp. "+ND
 )
# Không thêm vai trò Truyền thông cơ sở độc lập ở bệnh viện nhóm 2 nếu
# định biên vẫn là hai người; Trưởng nhóm kiêm theo mô hình đã chốt.
v["tn-b"]["quy_tac_kiem_nhiem_2027"]=(
 "Bệnh viện hai người: Trưởng nhóm kiêm Truyền thông cơ sở, Media là người sản xuất tư liệu; "
 "không nhân đôi đầu ra biển bảng, phát thanh, màn hình. "
 "Mỗi công việc kiêm nhiệm có mã riêng và giờ thực đo của Trưởng nhóm, "
 "để không gộp sai vào giờ Media hoặc giờ "+TT+"."
)

# 4. Rủi ro phê duyệt/vắng người: người thực hiện không phải người duyệt,
# không tự cấp quyền do quá hạn; chặn trước phát hành.
d["kiem_soat_nguoi_ky_kiem_2027"]={
 "ghi_nhan":"Trong từng mã việc ghi rõ họ tên/mã nhân sự thực hiện, người kiểm độc lập, người xác nhận y khoa/pháp lý khi áp dụng, người nghiệm thu mục tiêu, người duyệt phát hành, người duyệt chi.",
 "phat_hanh":"Thiếu một trường phê duyệt bắt buộc theo loại việc thì trạng thái phải là CHƯA ĐỦ ĐIỀU KIỆN PHÁT HÀNH.",
 "tu_kiem":"Cấm người làm tự kiểm chính sản phẩm khi quy định cần kiểm độc lập; cùng mã chức danh không có nghĩa cùng mã nhân sự.",
 "hai_tuyen":"Chỉ "+ND+" có tuyến quản lý dọc Trưởng nhóm chưa bàn giao; "+TT+" chỉ có quyền kiểm chuẩn nghiệp vụ truyền thông và số.",
 "bao_cao":"KPI đầu ra sản phẩm cho người làm, KPI điều phối cho Tổ trưởng, KPI quản trị cho chuyên viên trưởng theo tuyến; không cộng trùng một giờ của cùng một người.",
 "uy_quyen":"Người thay chỉ được kích hoạt sau văn bản phân công/ủy quyền ghi rõ phạm vi, thời hạn và quyền; nếu chưa có thì chặn việc vượt quyền.",
 "co_so":"Ban Giám đốc cơ sở quản lý hành chính tại chỗ; không mặc nhiên tạo tuyến quản lý Marketing thứ hai.",
 "do_luong":"Định biên 36 suất là phương án cấu trúc, chưa chứng minh đủ tải do thiếu nhật ký giờ thực tế."
}

# 5. Kiểm thử tỷ lệ phủ và chữ bị sai trước khi ghi lại.
assert len(ambiguous)==sum(bool(b.get("phan_cong_thuc_thi_2027")) for q in d["quy_trinh"] for b in q["buoc"])
assert len(same_role)==sum(bool(b.get("chan_trung_nguoi_2027")) for q in d["quy_trinh"] for b in q["buoc"])
assert not re.search(r"Marketing cơ sở2",json.dumps(d,ensure_ascii=False))
assert "Chuyên viên trưởng duyệt" not in json.dumps(d["quy_trinh"],ensure_ascii=False)
assert "Chuyên viên trưởng cấp" not in json.dumps(d["quy_trinh"],ensure_ascii=False)
assert "13 giờ/tháng" not in tr["viec"]  # không giao phần điều phối hằng ngày lại cho CVT

m=rx.search(s)
s=s[:m.start(2)]+json.dumps(d,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]

# 6. Hiển thị ngay trong từng bước quy trình, không để quy tắc mới thành
# dữ liệu ẩn. Giữ nguyên nút, thanh, thiết kế, màu nhận diện đã chốt.
pos=s.find("tx(b.noi_dung)")
if pos<0:
    raise RuntimeError("Không tìm thấy trình dựng bước quy trình để chèn phân quyền")
end_p=s.find("</p>",pos)
if end_p<0 or end_p-pos>500:
    raise RuntimeError("Không tìm thấy thẻ kết thúc mô tả bước quy trình")
# Đoạn '</p><div ...' vốn nằm trong cùng một literal của JS;
# chia literal đúng vị trí để thêm nội dung có điều kiện.
addon=(
 "+(b.phan_cong_thuc_thi_2027?"
 "'<p class=\"ops-resolved-owner\" style=\"border-left:3px solid #0837A1;"
 "padding:8px 10px;background:#f5f9ff;margin:7px 0;overflow-wrap:anywhere\">"
 "<b>Chủ trì theo nhóm:</b> '+tx(b.phan_cong_thuc_thi_2027)+'</p>':'')"
 "+(b.kiem_soat_khong_tu_kiem_2027?"
 "'<p style=\"border-left:3px solid #ED3237;padding:8px 10px;"
 "background:#fff9f9;margin:7px 0;overflow-wrap:anywhere\">"
 "<b>Chặn tự kiểm:</b> '+tx(b.kiem_soat_khong_tu_kiem_2027)+'</p>':'')"
)
s=s[:end_p]+"</p>'"+addon+"+'"+s[end_p+len("</p>"):]

# Thông tin cơ cấu/thẩm quyền có thể xem tại mục CNNV hiện hữu, không tạo menu mới.
mark='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
if mark not in s:raise RuntimeError("Mất mốc mục 4.3")
if 'id="tth-operations-integrity-2027"' not in s:
 panel=(
 '<div id="tth-operations-integrity-2027" style="padding:12px 14px;border:1px solid #cddbec;'
 'border-radius:8px;background:#fff;margin:12px 0 18px;max-width:100%;overflow-wrap:anywhere">'
 '<h4 style="margin:0 0 8px;color:#0837A1">Quy tắc chặn chồng chéo trước khi giao việc</h4>'
 '<p>Trong 60 quy trình mẫu có '+str(len(ambiguous))+
 ' bước dùng mã vai trò theo nhóm. Khi triển khai phải chọn đúng Nhóm 1 hoặc Nhóm 2,'
 ' cơ sở và cá nhân thực hiện; mỗi bước đã hiển thị bảng ánh xạ cụ thể.'
 ' Có '+str(len(same_role))+
 ' bước cần xác nhận người phối hợp khác người chủ trì khi thực hiện kiểm độc lập.</p>'
 '<p><strong>Tổ Nội dung và Sáng tạo:</strong> một Tổ trưởng điều phối thường lệ toàn tổ;'
 ' '+escape(ND)+' xử lý vượt tải và xung đột liên nhóm, không kiêm thường trực phân công sản xuất.'
 ' '+escape(TT)+' kiểm chuẩn truyền thông/số, không giao hai lệnh cho nhân sự cơ sở.</p>'
 '<p><strong>Điều kiện hiệu lực:</strong> quyền nhân sự, người thay, phê duyệt phát hành và'
 ' chi phí chỉ được áp dụng theo văn bản có hiệu lực. Số giờ quản lý/kiêm nhiệm cần thực đo;'
 ' không công bố là đủ tải khi chưa có dữ liệu.</p></div>'
 )
 s=s.replace(mark,panel+mark,1)

chk=json.loads(rx.search(s).group(2))
assert len(chk["vi_tri"])==26 and len(chk["quy_trinh"])==60
assert sum(len(q["buoc"]) for q in chk["quy_trinh"])==407
assert s.count('id="tth-operations-integrity-2027"')==1
assert "ops-resolved-owner" in s
f.write_text(s,"utf-8")
print("PASS INTEGRITY: 26 positions, 60 processes, 407 steps, 83 docs; "
      +str(len(ambiguous))+" generic steps mapped by group; "
      +str(len(same_role))+" same-role collaborations guarded; "
      +"full-team leader clarified; no unauthorized approval.")
