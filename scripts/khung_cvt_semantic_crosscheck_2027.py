#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đối soát cấu trúc và ngữ nghĩa hai Chuyên viên trưởng trên bản HTML xuất bản.
Không coi kiểm thử tĩnh là xác nhận nhân sự/đo hiệu suất thực tế.
"""
import json,re,sys
from collections import Counter
from pathlib import Path

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',s)
assert m, "Thiếu dữ liệu nhúng"
D=json.loads(m.group(1))
R={v["id"]:v for v in D["vi_tri"]}
ND=R["cvt"]["ten"]; TT=R["cvt-2"]["ten"]
assert ND=="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
assert TT=="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
assert len(R)==26 and len(D["quy_trinh"])==60 and len(D["danh_muc_van_ban"])==83
all_steps=[(q["id"],i,b) for q in D["quy_trinh"] for i,b in enumerate(q["buoc"],1)]
assert len(all_steps)==407
def code(v):return str(v).split("|",1)[0]
errors=[]
warnings=[]
stats=Counter()
cvt_step=[]
suspicious_both=[]
lead_cvt2=[]
output_cvt2=[]
for qid,i,b in all_steps:
 owner=code(b.get("chu_tri_chinh",""))
 actors=[code(x) for x in b.get("thuc_hien",[])]
 assistants=[code(x) for x in b.get("phoi_hop",[])]
 if len(assistants)!=len(set(assistants)):
  errors.append({"ma":"TRUNG_MA_PHOI_HOP","quy_trinh":qid,"buoc":i,"danh_sach":assistants})
 if qid=="nhan-viec-moi" and i in (2,3,4,5,6):
  a=b.get("chu_tri_thuc_te_theo_tuyen_cvt_2027",{})
  if a.get("nhan_su_noi_dung_sang_tao_hoac_marketing_co_so")!="cvt" or a.get("nhan_su_truyen_thong_thuong_hieu_hoac_tang_truong_so")!="cvt-2":
   errors.append({"ma":"NHAN_VIEC_MAC_DINH_MOT_CVT","quy_trinh":qid,"buoc":i})
  zlist=b.get("doi_soat_tung_dau_ra_2027",[])
  if not any("CHỜ CHỌN MỘT TUYẾN" in x.get("chu_tri_01","") for x in zlist):
   errors.append({"ma":"DAU_RA_NHAN_VIEC_THIEU_CHON_TUYEN","quy_trinh":qid,"buoc":i})
 present=set([owner]+actors+assistants)&{"cvt","cvt-2"}
 if present:
  stats["buoc_lien_quan_hai_cvt"]+=1
  cvt_step.append({"quy_trinh":qid,"buoc":i,"chu_tri":owner,"cvt_lien_quan":sorted(present)})
 if present=={"cvt","cvt-2"}:
  stats["buoc_co_ca_hai_cvt"]+=1
  suspicious_both.append({"quy_trinh":qid,"buoc":i,"chu_tri":owner,
    "mo_ta":str(b.get("noi_dung",""))[:330],
    "thuc_hien":actors,"phoi_hop":assistants})
 if owner in ("cvt","cvt-2"):
  stats["buoc_chu_tri_"+owner]+=1
 if qid=="chuyen-quyen" and i in (1,7):
  if not (owner=="cvt-2" and actors==["cvt-2"] and "cvt" in assistants):
   errors.append({"ma":"CHUYEN_QUYEN_LECH_CVT","quy_trinh":qid,"buoc":i,
                  "chu_tri":owner,"thuc_hien":actors,"phoi_hop":assistants})
 if owner=="cvt-2":
  lead_cvt2.append({"quy_trinh":qid,"buoc":i,"thuc_hien":actors,
    "phoi_hop":assistants,"noi_dung":str(b.get("noi_dung",""))[:320],
    "ghi_nhan":str(b.get("ghi_nhan",""))[:140]})
 if owner in assistants:
  stats["buoc_chu_tri_trung_ma_phoi_hop"]+=1
  if not b.get("chan_trung_nguoi_2027"):
   errors.append({"ma":"TU_KIEM","quy_trinh":qid,"buoc":i,"chu_tri":owner})
 for z,actor in zip(b.get("doi_soat_tung_dau_ra_2027",[]),actors):
  stats["dau_ra"]+=1
  desc=z.get("dien_giai","")
  if actor=="cvt-2":
   stats["dau_ra_vai_tro_cvt_truyen_thong"]+=1
   output_cvt2.append({"quy_trinh":qid,"buoc":i,"ma_dau_ra":z.get("ma_dau_ra"),"dien_giai":desc[:260]})
   if desc.startswith("Phần nghiệp vụ của Quản lý Nội dung"):
    errors.append({"ma":"NHAM_CVT_TREN_DAU_RA","quy_trinh":qid,"buoc":i,
                   "id":z.get("ma_dau_ra"),"dien_giai":desc[:180]})
  if actor=="cvt" and desc.startswith("Phần nghiệp vụ của Quản lý Truyền thông"):
   errors.append({"ma":"NHAM_CVT_TREN_DAU_RA","quy_trinh":qid,"buoc":i,"id":z.get("ma_dau_ra")})
  if actor in ("cvt","cvt-2"):
   stats["dau_ra_chuyen_vien_truong"]+=1
  if z.get("trang_thai_nghiem_thu_2027")!="CHƯA NGHIỆM THU HỒ SƠ THỰC TẾ":
   errors.append({"ma":"TU_NHAN_NGHIEM_THU","id":z.get("ma_dau_ra")})
assert stats["dau_ra"]==568
assert stats["buoc_chu_tri_trung_ma_phoi_hop"]==14
assert stats["buoc_chu_tri_cvt"]>=1 and stats["buoc_chu_tri_cvt-2"]>=1
assert stats["buoc_co_ca_hai_cvt"]<=407
# Một Trưởng nhóm chỉ có một người quản lý trực tiếp trong danh sách, theo thời điểm bàn giao.
if "Mọi thay đổi tuyến quản lý chỉ có hiệu lực khi có quyết định" not in R["cvt"].get("phan_dinh_chu_tri_dau_ra","") or "không tự chuyển sang Quản lý mạng lưới theo vùng" not in R["cvt"].get("phan_dinh_chu_tri_dau_ra",""):
 errors.append({"ma":"QL_CO_SO_2_TUYEN","vi_tri":"cvt","noi_dung":"MTCV thiếu điều kiện bàn giao"})
if "đánh giá nghiệp vụ các Trưởng nhóm Marketing cơ sở theo một tuyến" not in R["cvt"].get("phan_dinh_chu_tri_dau_ra","") or "không tạo tuyến chỉ huy nghiệp vụ thứ hai" not in R["cvt"].get("phan_dinh_chu_tri_dau_ra",""):
 errors.append({"ma":"QL_CO_SO_2_DANH_GIA","vi_tri":"cvt"})
if "Một Trưởng nhóm chỉ có một" not in R["qlml"].get("muc_dich",""):
 errors.append({"ma":"QLML_KHONG_KHOA_1_TUYEN","vi_tri":"qlml"})
if "Không giao việc trực tiếp" not in R["cvt-2"].get("muc_dich",""):
 errors.append({"ma":"C2_GIAO_VIEC_CO_SO","vi_tri":"cvt-2"})
if "không lập lệnh giao việc thứ hai" not in R["cvt-2"].get("viec_chung",""):
 errors.append({"ma":"C2_LENH_TRUNG_CO_SO","vi_tri":"cvt-2"})
if "Không tự phát sinh quyền" not in R["cvt-2"].get("phan_dinh_kiem_duyet",""):
 errors.append({"ma":"C2_DUYET_MAC_NHIEN","vi_tri":"cvt-2"})
# Chức danh và đầu ra quản trị không được chỉ dựa trên tên gọi chung trong CSDL.
generic=re.compile(r'Chuyên viên trưởng(?!\s+(?:Nội dung|Truyền thông))',re.I)
bad=[]
def walk(z,path="D"):
 if isinstance(z,str):
  if generic.search(z):bad.append(path)
 elif isinstance(z,list):
  for i,v in enumerate(z):walk(v,path+"["+str(i)+"]")
 elif isinstance(z,dict):
  for k,v in z.items():walk(v,path+"."+str(k))
walk(D)
if bad:errors.append({"ma":"TEN_CVT_CHUNG","duong_dan":bad[:12],"tong":len(bad)})
# Hồ sơ giữ vai trò chủ quản không bị tự chuyển thành CVT kiểm chuẩn.
monitored={"BM-5","BM-24","M-5","QC-5","DS-2","SO-3"}
forms={f["ma"]:f for f in D.get("danh_muc_tai_lieu",[])}
for fid in monitored:
 f=forms[fid]
 holder=f.get("nam_giu")
 c=f.get("co_che_quan_tri",{})
 if c and c.get("nguoi_nam_giu")!=holder:
  errors.append({"ma":"MAU_2_NGUOI_GIU","mau":fid,"dau":holder,
                 "co_che":c.get("nguoi_nam_giu")})
 if holder in ("cvtt","qc","tk-nt"):
  stats["mau_don_vi_van_hanh_giu_nguyen"]+=1
 if holder=="cvt":
  errors.append({"ma":"MAU_GIU_SAI_TUYEN","mau":fid})
# Phạm vi sơ đồ và mô tả trách nhiệm của CVT Truyền thông không đẩy đầu ra về sản xuất.
if not D.get("hieu_suat_cvt_truyen_thong_tang_truong_so_2027"):
 errors.append({"ma":"THIEU_HIEU_SUAT_HAI_TO"})
if len(D.get("vi_du_van_hanh_hai_chuyen_vien_truong_2027",[]))!=14:
 errors.append({"ma":"THIEU_TINH_HUONG"})
# Còn việc cần chốt bằng tài liệu thực tế, không tự nhận là đã hoàn thành.
for qid,i,b in all_steps:
 if b.get("ma_vi_tri_nhom_1_2027") and b.get("ma_vi_tri_nhom_2_2027"):
  stats["buoc_vai_tro_theo_nhom_chua_chon_ca_nhan"]+=1
 if b.get("chu_tri_thuc_te_theo_tuyen_cvt_2027"):
  stats["buoc_phan_tuyen_cvt_khi_nhan_viec"]+=1
 if b.get("chan_trung_nguoi_2027"):
  stats["buoc_kiem_tra_nguoi_doc_lap"]+=1
stats["dau_ra_cho_ho_so"]=sum(
 z.get("trang_thai_nghiem_thu_2027")=="CHƯA NGHIỆM THU HỒ SƠ THỰC TẾ"
 for _,_,b in all_steps for z in b.get("doi_soat_tung_dau_ra_2027",[]))
cross=D.get("doi_soat_25_buoc_lien_tuyen_hai_cvt_2027",{})
assert len(cross.get("danh_sach",[]))==25
assert cross.get("can_chot_nguoi")==7
semantic=D.get("kiem_toan_568_dau_ra_chuyen_biet_2027",{})
assert semantic.get("tong")==568 and semantic.get("can_xac_nhan")==512
assert s.count('id="tth-cvt-cross-25-review-2027"')==1
assert stats["buoc_vai_tro_theo_nhom_chua_chon_ca_nhan"]==95
assert stats["buoc_phan_tuyen_cvt_khi_nhan_viec"]==7
warnings.append({"ma":"PHAN_VAI_TRO_THEO_NHOM","so_buoc":95,
  "ghi_chu":"Chọn nhóm, cơ sở, chức danh và mã nhân sự thật trước khi giao"})
warnings.append({"ma":"CHOT_CHUYEN_VIEN_TRUONG_THEO_NGUOI_NHAN_VIEC_VA_BAN_GIAO","so_buoc":7,
  "ghi_chu":"Năm bước tiếp nhận nhân sự và hai bước vắng mặt/nghỉ việc phải chọn đúng tuyến theo mã nhân sự, không mặc định Nội dung"})
if stats["buoc_kiem_tra_nguoi_doc_lap"]:
 warnings.append({"ma":"CHUA_XAC_NHAN_HAI_NGUOI_KHAC_NHAU","so_buoc":stats["buoc_kiem_tra_nguoi_doc_lap"]})
if stats["dau_ra_cho_ho_so"]:
 warnings.append({"ma":"CHUA_NGHIEM_THU_THUC_TE","so_dau_ra":stats["dau_ra_cho_ho_so"]})
report={
 "nguon":"HTML xuất bản từ main, dùng dữ liệu 26 chức danh, 60 quy trình, 407 bước và 568 đầu ra mẫu",
 "trang_thai":"LỖI CẦN SỬA" if errors else "ĐẠT KIỂM TRA CẤU TRÚC; CHỜ XÁC MINH HỒ SƠ THỰC TẾ",
 "thong_ke":dict(stats),
 "loi":errors,
 "can_xac_minh":warnings,
 "buoc_co_ca_hai_cvt":suspicious_both,
 "buoc_cvt_truyen_thong_chu_tri":lead_cvt2,
 "dau_ra_cvt_truyen_thong":output_cvt2,
 "quy_tac":"Một chủ trì, một tuyến quản lý trực tiếp, người kiểm độc lập, quyền duyệt theo văn bản; không cộng trùng giờ sản xuất/điều phối/quản trị."
}
dest=root/"khung-marketing"/"doi-soat-hai-chuyen-vien-truong-2027.json"
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
print("CVT-ROLE-CHECK:",json.dumps({"lead_cvt_truyen_thong":lead_cvt2,
 "dau_ra_cvt_truyen_thong":output_cvt2,"cung_tham_gia":suspicious_both},ensure_ascii=False))
print("CVT-SEMANTIC-AUDIT:",json.dumps({"trang_thai":report["trang_thai"],
 "thong_ke":dict(stats),"loi":errors[:12],"can_xac_minh":warnings},ensure_ascii=False))
assert not errors,"Còn trộn tuyến CVT/biểu mẫu: "+str(errors[:5])
