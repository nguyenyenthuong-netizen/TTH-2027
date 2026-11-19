#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm toán sâu 25 điểm giao hai CVT và 568 đầu ra mẫu.
Không giả định đã có mã nhân viên, ủy quyền hay số giờ thực đo.
"""
import csv,json,re,sys
from collections import Counter
from pathlib import Path
from html import escape
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s)
assert m
D=json.loads(m.group(2))
R={x["id"]:x for x in D["vi_tri"]}
ND,TT=R["cvt"]["ten"],R["cvt-2"]["ten"]
def key(x):return str(x).split("|",1)[0]
# Ma trận từng bước; giá trị là phạm vi CVT Nội dung, phạm vi CVT Truyền thông,
# trigger phối hợp, chủ việc thực tế/bàn giao. Không thay người duyệt hiện hành.
M={
 ("vang-mat",4):("Đối chiếu tải và nguồn người thay của Nội dung – Sáng tạo/Marketing cơ sở","Đối chiếu tải và nguồn người thay của Tổ Truyền thông và Thương hiệu/Tổ Tăng trưởng số","Chỉ phối hợp phần nhân sự thuộc đúng tuyến","Trưởng phòng chốt phương án tạm trong thẩm quyền; Nhân lực xác nhận theo quy chế"),
 ("vang-mat",5):("Kiểm sổ bàn giao việc và người trở lại thuộc tuyến Nội dung/cơ sở","Kiểm việc, quyền kênh và người trở lại thuộc hai tổ TCT phụ trách","Nếu người vắng thuộc tuyến khác, phải chuyển chủ trì quản lý đúng tuyến","Người được phân quyền thu hồi quyền làm thay; một sổ bàn giao"),
 ("co-so-moi",4):("Điều phối phần nhân sự cơ sở và kho mẫu/nguồn sản xuất","Kiểm chuẩn kênh, quảng cáo, PR và quyền tác nghiệp truyền thông tại cơ sở","Chỉ khi công việc chạm cả cơ sở và chuẩn kênh","Chuyên viên quảng cáo/Quản lý sản phẩm số thực hiện; cấp quyền theo ma trận"),
 ("nghi-viec",2):("Tiếp nhận hồ sơ bàn giao người thuộc tuyến sản xuất/cơ sở","Tiếp nhận hồ sơ bàn giao người thuộc hai tổ TCT phụ trách","Chỉ chọn một quản lý trực tiếp theo người nghỉ việc; không mặc định Nội dung","Người được giao thay nhận hồ sơ; Nhân lực xác nhận theo quy chế"),
 ("nghi-viec",4):("Kiểm kê kho sản xuất và quyền thư mục thuộc tuyến mình","Đối soát quyền kênh/trang quảng cáo, kiểm điều kiện thu hồi","Chia theo tài sản, không gộp quyền kho và quyền kênh","Người có quyền cấp/thu hồi thực hiện; Trưởng phòng/cấp được ủy quyền chốt theo ma trận"),
 ("nghi-viec",6):("Kiểm kê kho tư liệu và bàn giao file sản xuất","Kiểm quyền kênh, quảng cáo sau thu hồi","Chỉ tham gia đúng loại tài sản","Công nghệ/Quản lý sản phẩm số thao tác theo đúng quyền hệ thống"),
 ("phap-luat",3):("Cung cấp phần nguồn file sản xuất khi chính sách ảnh hưởng nội dung, hình ảnh","Kiểm chuẩn chính sách quảng cáo, nền tảng và áp dụng trên kênh","Tuyến Nội dung chỉ tham gia khi phải sửa file sản xuất","Quản lý sản phẩm số cập nhật; Pháp chế xác nhận pháp luật"),
 ("su-kien-co-so",2):("Đánh giá năng lực sản xuất, triển khai cơ sở khi có yêu cầu","Kiểm chuẩn nghiệp vụ truyền thông, PR và kênh sự kiện","Chỉ phối hợp đúng nguồn lực và loại rủi ro liên quan","Ban Giám đốc cơ sở quyết định phần thuộc thẩm quyền; phát hành/y khoa tách riêng"),
 ("chuyen-quyen",1):("Đối chiếu danh mục file, kho tư liệu sản xuất","Chủ trì danh mục kênh/tài khoản quảng cáo, đối soát quyền kênh","Chỉ giao một đầu mối hồ sơ tổng hợp; tách chứng từ tài sản","Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số lập hồ sơ; quyền cấp/thu hồi riêng"),
 ("chuyen-quyen",2):("Cung cấp danh sách quyền kho sản xuất theo phân quyền","Kiểm chuẩn yêu cầu quyền kênh, tài khoản quảng cáo","Theo loại tài sản và quyền cần cấp","Trưởng phòng hoặc người được chỉ định có hiệu lực cấp quyền đúng ma trận"),
 ("chuyen-quyen",7):("Bàn giao phiếu đối chiếu kho tư liệu sản xuất","Chủ trì biên bản chuyển quyền kênh và danh sách quyền","Một biên bản tổng hợp, không hai đầu mối chủ trì","Phê duyệt/cấp/thu hồi quyền theo ma trận, không mặc nhiên giao CVT"),
 ("xung-dot-lich",3):("Điều phối phần năng lực sản xuất và nhân sự cơ sở trong tuyến","Xác nhận tải, mức ưu tiên và rủi ro của hai tổ mình quản lý","Chỉ khi phát sinh tranh chấp hai tuyến hoặc nguồn lực chung","Trưởng phòng quyết định xung đột vượt hai tuyến; lưu phiếu ưu tiên duy nhất"),
 ("yeu-cau-gap",4):("Điều phối nhân lực sản xuất/cơ sở và khả năng cung ứng","Điều phối hai tổ mình phụ trách và kiểm chuẩn yêu cầu phát hành","Chỉ khi việc gấp cần cả hai nguồn lực","Trưởng phòng quyết định thay đổi hạng mục trọng điểm hoặc vượt thẩm quyền"),
 ("noi-bo-phong-ban",2):("Phân tải viết, thiết kế, media khi đơn vị chủ quản yêu cầu","Kiểm chuẩn phần PR/kênh truyền thông nội bộ khi phát sinh","Không mặc định cả hai CVT cùng duyệt tất cả nội dung nội bộ","Quản lý thương hiệu phụ trách phần mục tiêu; đơn vị chủ quản xác nhận nguồn"),
 ("bgd-coso-de-nghi",4):("Chịu trách nhiệm điều phối nhân sự cơ sở thuộc danh sách quản lý","Kiểm chuẩn thông điệp và kênh nếu bất đồng chạm nghiệp vụ hai tổ","Chỉ phối hợp khi có yêu cầu chuyên môn truyền thông/số","Trưởng phòng quyết định bất đồng mục tiêu/thông điệp vượt tuyến"),
 ("doi-ten-chuyen-nhom",5):("Đối chiếu quyền kho mẫu/file, sản xuất lại tư liệu nếu cần","Kiểm chuẩn đổi tên kênh, quyền tài khoản, nội dung kênh số","Bàn giao theo tài sản và nhóm thương hiệu mới","Chuyên viên quảng cáo/Quản lý sản phẩm số thao tác, phê duyệt theo ma trận"),
 ("thanh-tra-kiem-tra",3):("Cung cấp file nguồn, lịch sử biên tập, chứng từ sản xuất","Cung cấp nhật ký phát hành, quyền kênh, quảng cáo và hồ sơ truyền thông","Chỉ phối hợp theo loại hồ sơ bị thanh tra yêu cầu","Biên tập/quảng cáo cung cấp chứng từ; Pháp chế và cấp có quyền phản hồi"),
 ("he-thong-gian-doan",1):("Kiểm phạm vi ảnh hưởng kho tư liệu, phần việc sản xuất/cơ sở","Kiểm phạm vi ảnh hưởng kênh quảng cáo, truyền thông và hai tổ","Chỉ theo hệ thống/tài sản bị gián đoạn","Quản lý sản phẩm số/Công nghệ tiếp nhận sự cố đúng tuyến; một mã sự cố"),
 ("he-thong-gian-doan",2):("Điều phối bản ghi tạm của tổ sản xuất và Marketing cơ sở","Điều phối bản ghi tạm hai tổ và kênh mình phụ trách","Chỉ tổ/tuyến bị ảnh hưởng tham gia, không ra lệnh kép","Tổ trưởng giao việc theo nhật ký chung; không thay quy trình duyệt"),
 ("he-thong-gian-doan",6):("Đối chiếu nhập bù phần sản xuất/cơ sở và chứng từ","Đối chiếu nhập bù truyền thông, quảng cáo và kênh số","Theo dữ liệu/tuyến có phát sinh, không kiểm trùng","Chuyên viên Đo lường và đối soát xác minh độc lập nhật ký sau khôi phục"),
 ("nhan-viec-moi",2):("Giao CNNV, hồ sơ phân công nhân sự thuộc tuyến mình","Giao CNNV, hồ sơ phân công nhân sự thuộc hai tổ mình","Một quản lý theo tổ của người nhận việc, không mặc định Nội dung","Nhân lực kiểm điều kiện tiếp nhận và quyết định nhân sự"),
 ("nhan-viec-moi",3):("Xác nhận yêu cầu quyền kho sản xuất theo phạm vi vị trí","Xác nhận yêu cầu quyền kênh số/quảng cáo theo phạm vi vị trí","Một quản lý theo nhân sự nhận việc; phân quyền theo loại tài sản","Người có quyền cấp hệ thống thao tác; không để CVT tự cấp quyền cao nhất"),
 ("nhan-viec-moi",4):("Hướng dẫn chuẩn sản xuất và phối hợp cơ sở đúng nhân sự","Hướng dẫn chuẩn truyền thông/thương hiệu/số đúng nhân sự","Chỉ đào tạo đúng nội dung áp dụng cho người nhận việc","Nhân lực và người hướng dẫn tổ xác minh kết quả"),
 ("nhan-viec-moi",5):("Bàn giao sản xuất/cơ sở, xác nhận đúng tuyến","Bàn giao truyền thông/số, xác nhận đúng tuyến","Chỉ một quản lý của người tiếp nhận chủ trì hồ sơ","Trưởng phòng xác nhận nếu thực sự liên tuyến, không duyệt mặc định"),
 ("nhan-viec-moi",6):("Đánh giá phát triển kỹ năng người thuộc tuyến sản xuất/cơ sở","Đánh giá phát triển kỹ năng nhân sự hai tổ truyền thông/số","Chỉ đánh giá người thuộc tuyến của mình","Tổ trưởng cung cấp bằng chứng; quản lý đúng tuyến đánh giá, không đánh giá kép"),
}
assert len(M)==25
Q={q["id"]:q for q in D["quy_trinh"]}
both=[]
for q in D["quy_trinh"]:
 for n,b in enumerate(q["buoc"],1):
  all_roles={key(b.get("chu_tri_chinh"))}|{key(x) for x in b.get("thuc_hien",[])}|{key(x) for x in b.get("phoi_hop",[])}
  if {"cvt","cvt-2"}<=all_roles:both.append((q["id"],n))
assert set(both)==set(M),("25 steps changed: missing",set(both)-set(M),"stale",set(M)-set(both))
conditional={("vang-mat",5),("nghi-viec",2)}
report=[]
for qid,n in both:
 b=Q[qid]["buoc"][n-1]
 nd,tt,trigger,who=M[(qid,n)]
 lead=key(b.get("chu_tri_chinh"))
 detail={
  "quy_trinh":qid,"ten_quy_trinh":Q[qid]["ten"],"buoc":n,
  "chu_tri_ma_trong_so_do":lead,
  "cvt_noi_dung":nd,"cvt_truyen_thong":tt,
  "dieu_kien_cung_tham_gia":trigger,"chu_tri_thuc_thi_va_quyen":who,
  "quy_tac_chong_chong_cheo":"Một mã việc; mỗi tuyến chịu sản phẩm/giờ riêng; kiểm độc lập nếu có; không cùng duyệt cuối.",
  "trang_thai":"CHỜ CHỌN MỘT TUYẾN THEO NHÂN SỰ" if (qid,n) in conditional or qid=="nhan-viec-moi" else
               "ĐÃ ĐỊNH NGHĨA RANH GIỚI, CHỜ KIỂM CHỨNG HỒ SƠ THỰC TẾ"
 }
 b["phan_dinh_hai_cvt_chi_tiet_2027"]=detail
 if (qid,n) in conditional:
  b["chu_tri_thuc_te_theo_tuyen_cvt_2027"]={
   "nhan_su_noi_dung_sang_tao_hoac_marketing_co_so":"cvt",
   "nhan_su_truyen_thong_thuong_hieu_hoac_tang_truong_so":"cvt-2",
   "dieu_kien":"Phải gắn mã vị trí và quyết định nhân sự, chỉ một quản lý trực tiếp tại thời điểm phát sinh"}
  for a,z in zip(b.get("thuc_hien",[]),b.get("doi_soat_tung_dau_ra_2027",[])):
   if key(a)=="cvt":
    z["chu_tri_01"]="CHỜ CHỌN MỘT TUYẾN theo người liên quan: "+ND+" hoặc "+TT+"; chọn duy nhất bằng mã nhân sự"
    z["tuyen_quan_ly_01"]="Trưởng phòng Marketing → "+ND+" hoặc "+TT+"; không đồng thời"
    z["dieu_kien_phat_lenh_2027"]="CHẶN nếu chưa chọn tổ, mã người và một tuyến quản lý có hiệu lực"
 report.append(detail)
D["doi_soat_25_buoc_lien_tuyen_hai_cvt_2027"]={
 "pham_vi":"25 bước có đồng thời hai mã CVT trong 407 bước quy trình",
 "ket_luan":"Đã phân định riêng nghĩa vụ từng tuyến; không tự suy ra người duyệt hay nhân sự thực.",
 "can_chot_nguoi":len([x for x in report if x["trang_thai"].startswith("CHỜ CHỌN")]),
 "danh_sach":report
}
# Làm việc cần chốt 568 đầu ra thành danh mục chứng từ có thể lọc/xếp ưu tiên.
items=[]
counts=Counter()
for q in D["quy_trinh"]:
 for n,b in enumerate(q["buoc"],1):
  for role,z in zip(b["thuc_hien"],b["doi_soat_tung_dau_ra_2027"]):
   status=z.get("can_cu_phan_vai_2027","")
   counts[status]+=1
   if status=="CHƯA ĐỦ CĂN CỨ PHÂN TÁCH, CHẶN GIAO VIỆC":priority="P0 – chặn giao việc"
   elif status=="ĐẦU RA CẦN ĐƠN VỊ CHỦ QUẢN XÁC NHẬN":priority="P1 – xác nhận đơn vị chủ quản"
   elif status=="PHÂN VAI MẪU, CẦN XÁC NHẬN":priority="P1 – chuyên biệt theo chức danh"
   else:priority="P2 – đối chiếu chứng từ"
   z["muc_uu_tien_doi_soat_chuyen_biet_2027"]=priority
   items.append({
    "Mã đầu ra":z["ma_dau_ra"],"Quy trình":q["ten"],"Mã quy trình":q["id"],"Bước":n,
    "Mã vai trò":key(role),"Diễn giải":z.get("dien_giai",""),
    "Căn cứ phân vai":status,"Ưu tiên":priority,
    "Chủ trì":z.get("chu_tri_01",""),"Tuyến quản lý":z.get("tuyen_quan_ly_01",""),
    "Bằng chứng cần thu":z.get("chung_tu_thuc_te",""),
    "Trạng thái":z.get("trang_thai_nghiem_thu_2027","")
   })
assert len(items)==568
assert sum(counts.values())==568
needs=sum(v for k,v in counts.items() if k in
 ("CHƯA ĐỦ CĂN CỨ PHÂN TÁCH, CHẶN GIAO VIỆC","ĐẦU RA CẦN ĐƠN VỊ CHỦ QUẢN XÁC NHẬN",
  "PHÂN VAI MẪU, CẦN XÁC NHẬN"))
assert needs>=450
D["kiem_toan_568_dau_ra_chuyen_biet_2027"]={
 "can_xac_nhan":needs,"tong":len(items),"theo_can_cu":dict(counts),
 "nguyen_tac":"Không tự biến mô tả mẫu thành đã xác minh; chốt từng mã người, sản phẩm, người duyệt và chứng từ trước khi giao/duyệt."}
m=rx.search(s)
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]
out=root/"khung-marketing"
(out/"doi-soat-25-buoc-hai-cvt-2027.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
with (out/"danh-sach-568-dau-ra-can-doi-chieu-2027.csv").open("w",encoding="utf-8-sig",newline="") as f:
 writer=csv.DictWriter(f,fieldnames=list(items[0]),lineterminator="\n")
 writer.writeheader();writer.writerows(items)
# Một mục thu gọn, không làm trang rộng hơn; mọi bước có link tới quy trình.
marker='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
assert s.count(marker)==1 and "id=\"tth-cvt-cross-25-review-2027\"" not in s
pos=s.index("</h3>",s.index(marker))+5
box=['<details id="tth-cvt-cross-25-review-2027" style="max-width:100%;min-width:0;box-sizing:border-box;border:1px solid #d6e1ef;border-radius:8px;margin:14px 0;padding:12px;background:#fff;overflow-wrap:anywhere">']
box.append('<summary style="cursor:pointer;color:#0837A1;font-weight:700">Đối chiếu 25 bước phối hợp hai Chuyên viên trưởng và trách nhiệm tuyến dưới</summary>')
box.append('<p>Danh mục sau là ranh giới trách nhiệm ở cấp quy trình. Chỉ tham gia khi đủ điều kiện nghiệp vụ, không đồng chủ trì, không thêm cửa phê duyệt, không tính lặp giờ. Hồ sơ thực tế phải xác nhận mã người và quyền còn hiệu lực.</p>')
for x in report:
 box.append('<details style="max-width:100%;border-top:1px solid #e4eaf2;padding:9px 0"><summary style="cursor:pointer;font-weight:600">'+escape(x["ten_quy_trinh"]+" – bước "+str(x["buoc"]))+'</summary>')
 box.append('<p><b>'+escape(ND)+':</b> '+escape(x["cvt_noi_dung"])+'</p>')
 box.append('<p><b>'+escape(TT)+':</b> '+escape(x["cvt_truyen_thong"])+'</p>')
 box.append('<p><b>Điều kiện phối hợp:</b> '+escape(x["dieu_kien_cung_tham_gia"])+'</p>')
 box.append('<p><b>Chủ trì và quyền:</b> '+escape(x["chu_tri_thuc_thi_va_quyen"])+'</p>')
 box.append('<p><a href="#vh-qt-'+escape(x["quy_trinh"])+'" style="color:#0837A1;text-decoration:underline">Mở quy trình gốc</a></p></details>')
box.append('<p><b>Đối soát ngữ nghĩa:</b> '+str(needs)+' trong 568 đầu ra vẫn cần xác nhận đặc thù; không được coi là đã nghiệm thu. <a href="danh-sach-568-dau-ra-can-doi-chieu-2027.csv">Tải danh mục đối soát đầu ra (CSV)</a>.</p></details>')
s=s[:pos]+''.join(box)+s[pos:]
assert s.count('id="tth-cvt-cross-25-review-2027"')==1
p.write_text(s,"utf-8")
print("PASS 25-CVT-DEEP:",len(report),"cross steps;",needs,"outputs need confirmation;",
      dict(counts),"conditional routes",D["doi_soat_25_buoc_lien_tuyen_hai_cvt_2027"]["can_chot_nguoi"])
