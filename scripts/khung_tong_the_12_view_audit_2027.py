#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm toán liên phần Khung Marketing 2027 (HTML cuối pipeline).
Bảo vệ 12 phần, 5 tên tổ bệnh viện, 13+1 suất, 26 MTCV,
60 luồng/407 bước/83 văn bản, quyền kiểm chuẩn/ban hành.
Không coi luồng đề án là văn bản đã ban hành hoặc gán nhân sự cá nhân.
"""
import json,re,sys
from pathlib import Path
from html import unescape

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
path=root/"khung-marketing"/"index.html"
html=path.read_text("utf-8")
pattern=r'<script id="csdl" type="application/json">([\s\S]*?)</script>'
match=re.search(pattern,html)
assert match,"Không có CSDL nhúng của Khung"
data=json.loads(match.group(1))
issues=[]

def ck(ok, msg):
    if not ok: issues.append(msg)

views=re.findall(r'<section class="view" data-view="([^"]+)" id="v-([^"]+)"',html)
expected_views=[
  "overview","org","jd","assign","staffing","relations",
  "coord","ops","roadmap","pay","software","decisions"
]
ck([x[0] for x in views]==expected_views and all(a==b for a,b in views),
   "Sai hoặc thiếu 12 phần chính/ID")
ck(all(html.count('data-target="'+z+'"')>=1 for z in expected_views),
   "12 phần thiếu liên kết tab điều hướng")
roles={r["id"]:r for r in data["vi_tri"]}
ck(len(roles)==26,"Không đủ 26 mã chức danh")
ck(len(data["quy_trinh"])==60,"Không đủ 60 luồng quy trình")
ck(sum(len(x["buoc"]) for x in data["quy_trinh"])==407,"Không đủ 407 bước")
ck(len(data["danh_muc_van_ban"])==83,"Không đủ 83 văn bản tham chiếu")
ND="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
TT="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
ck(roles["cvt"]["ten"]==ND and roles["cvt-2"]["ten"]==TT,
   "Sai hai tên chức danh chính thức")
ck(all(r.get("cnnv_2027") and r.get("cnnv_quan_tri_quy_trinh_2027")
       for r in roles.values()),"Có MTCV thiếu chuẩn hóa CNNV hoặc quản trị quy trình")

naming=data.get("cnnv_ten_to_marketing_benh_vien_2027",{})
catalog=naming.get("danh_muc_dang_hoat_dong",[])
ck(len(catalog)==5,"Sai số 5 tổ Marketing bệnh viện")
ck(naming.get("tong_so_suat_to_benh_vien")==13 and
   naming.get("suat_dau_moi_phong_kham")==1 and
   naming.get("tong_suat_marketing_co_so")==14,
   "14 suất cơ sở chưa phân biệt 13 bệnh viện + 1 phòng khám")
ck([x.get("suat_co_cau_de_xuat") for x in catalog]==[3,3,3,2,2],
   "Suất theo 5 bệnh viện không phải 03/03/03/02/02")

org_units=[x for x in data.get("don_vi",[])
           if x.get("loai")=="to_marketing_benh_vien"]
ck(len(org_units)==5,"Danh mục đơn vị JSON không có đúng 5 tổ bệnh viện")
canonical={x.get("ten_to") for x in catalog}
ck({x.get("ten") for x in org_units}==canonical,
   "Tên đơn vị JSON không thống nhất bảng tên chuẩn")
ck(len(canonical)==5 and all(
   x.get("ten_to")=="Tổ Marketing "+x.get("benh_vien","")
   for x in catalog),"Tên tổ không phải Tổ Marketing + tên đầy đủ bệnh viện")

html_without_data=html[:match.start()]+html[match.end():]
cards=[
 ("Tổ Marketing Bệnh viện Đa khoa TTH Vinh", "03"),
 ("Tổ Marketing Bệnh viện Đa khoa TTH Hà Tĩnh","03"),
 ("Tổ Marketing Bệnh viện Đa khoa TTH Quảng Bình","03"),
 ("Tổ Marketing Bệnh viện Y học cổ truyền Nguyên Phúc","02"),
 ("Tổ Marketing Bệnh viện Răng hàm mặt và Phẫu thuật tạo hình thẩm mỹ Thái Thượng Hoàng","02"),
]
found=[(unescape(a.strip()),b) for a,b in re.findall(
   r'<div class="hosp-h">([^<]+?)\s*<b>\((\d+)\)</b></div>',
   html_without_data)]
ck(found==cards,"Sơ đồ Bộ máy không hiển thị đủ 5 tên chuẩn và suất thực")
ck('<summary>Các Tổ Marketing tại bệnh viện <b>(13)</b>' in html_without_data,
   "Nhóm bệnh viện không ghi 13 suất")
ck('13 suất tại 05 tổ bệnh viện + 01 suất đầu mối kiêm nhiệm phòng khám' in html_without_data,
   "Mục 8 chưa phân biệt 13 bệnh viện và 01 đầu mối phòng khám")
ck('22 Tổng công ty + 14 cơ sở' in html_without_data,
   "Tiêu đề Bộ máy ghi 14 bệnh viện thay vì 14 cơ sở")
ck('<span>Tổ Marketing tại 5 bệnh viện</span>' not in html_without_data,
   "Thẻ thống kê 14 suất còn ghi sai thuộc 5 tổ bệnh viện")
ck("Tổ Marketing Bệnh viện Răng Hàm Mặt" not in html,
   "Tên đơn vị Thái Thượng Hoàng còn sai kiểu chữ")
ck(ND+" Nội dung – Sáng tạo và Marketing cơ sở" not in html_without_data,
   "Lỗi lặp tên Chuyên viên trưởng trong bảng cơ cấu")
ck("Tổ Marketing chi nhánh" not in html_without_data,
   "Tên đơn vị chung không đúng chuẩn còn hiển thị")
ck("Trưởng nhóm Marketing cơ sở" in html_without_data,
   "Đã nhầm tên chức danh Trưởng nhóm với tên đơn vị")

cnnv=data.get("cnnv_quan_tri_danh_muc_quy_trinh_2027",{})
ck(len(cnnv.get("phan_cong",[]))==8 and len(cnnv.get("chu_trinh",[]))==7,
   "Thiếu quyền đề xuất, soạn, kiểm chuẩn, trình ban hành quy trình")
ck(len(cnnv.get("danh_muc_luong_tham_chieu",[]))==60,
   "Không đủ 60 quy trình được gắn trạng thái tham chiếu")
ck('id="cnnv-quan-tri-danh-muc-quy-trinh-2027"' in html_without_data,
   "Mục 4.1 thiếu hướng dẫn quản lý quy trình")
ck(len(data.get("cnnv_kiem_soat_luong_va_tham_quyen_2027",[]))==6,
   "Thiếu 6 điểm kiểm soát quyền và vận hành")
ck(len(data.get("cnnv_quan_tri_2_chuyen_vien_truong_3_to_2027",{}).get("tinh_huong",[]))==9,
   "Thiếu 9 tình huống xung đột hai chức danh")
ck(len(data.get("cnnv_nhanh_xung_dot_hai_to_2027",{}).get("buoc",[]))==6,
   "Thiếu nhánh 6 bước giải quyết xung đột hai tổ")

standards=data.get("bo_quy_chuan_da_dong_bo",[])
ck({x.get("ma") for x in standards}=={"Content","QC-4","Xuat-ban-nen-tang","DS-3"},
   "Bảng quy chuẩn thiếu 4 đầu mối kiểm")
for x in standards:
    z=x.get("ma","?")
    ck(ND in x.get("kiem","") or TT in x.get("kiem",""),
       "Bảng quy chuẩn "+z+" còn người kiểm chung")
    ck("chưa có ủy quyền hiệu lực" in x.get("phe_duyet","").lower(),
       "Bảng quy chuẩn "+z+" thiếu điều kiện khóa quyền ban hành")
    ck(not re.search(r'Chuyên viên trưởng(?! Nội dung| Truyền thông)',
       x.get("kiem","")+" "+x.get("phe_duyet","")),
       "Bảng quy chuẩn "+z+" có tên Chuyên viên trưởng chung")
steps=[b for q in data["quy_trinh"] for b in q["buoc"]]
ck(sum(bool(b.get("ma_vi_tri_nhom_1_2027") and b.get("ma_vi_tri_nhom_2_2027"))
       for b in steps)==95,"Thiếu 95 bước cần xác định nhân sự/nhóm")
ck(sum(b.get("chan_trung_nguoi_2027") is True for b in steps)==14,
   "Thiếu 14 điều kiện kiểm độc lập")
ck(sum(bool(b.get("chu_tri_thuc_te_theo_tuyen_cvt_2027")) for b in steps)==7,
   "Thiếu 7 bước cần chốt tuyến hai chức danh")
ck(len([z for b in steps for z in b.get("doi_soat_tung_dau_ra_2027",[])])==568,
   "Không đủ 568 đầu ra")
ck(data.get("cnnv_tai_hai_chuc_danh_2027",{}).get("khoa_ket_luan") is not None,
   "Tải quản trị hai Chuyên viên trưởng chưa có điểm khóa")

if issues:
    raise AssertionError("KHUNG 12-PHAN FAIL ("+str(len(issues))+"): "+
                         json.dumps(issues,ensure_ascii=False))
print("PASS KHUNG 12-PHAN: 12 phần; 5 tên tổ đúng, 13+1=14 cơ sở; "+
      "26 vị trí; 60 quy trình/407 bước/83 văn bản/568 đầu ra; "+
      "quy chuẩn, quản trị quy trình, hai tuyến và điều kiện khóa.")
