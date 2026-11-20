#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đối soát cấu trúc và ngữ nghĩa hai Chuyên viên trưởng trên bản HTML xuất bản.
Không coi kiểm thử tĩnh là xác nhận nhân sự/đo hiệu suất thực tế.
"""
import csv,json,re,sys
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
# 14 là dữ liệu hiện trạng, không phải tiêu chí "đạt": luôn đối chiếu từng bước.
assert stats["buoc_chu_tri_trung_ma_phoi_hop"]==sum(
 code(b.get("chu_tri_chinh","")) in [code(x) for x in b.get("phoi_hop",[])]
 for _,_,b in all_steps
)
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
# 95 là dữ liệu hiện trạng cần phân vai, không phải một ngưỡng nghiệm thu.
assert stats["buoc_vai_tro_theo_nhom_chua_chon_ca_nhan"]==sum(
 bool(b.get("ma_vi_tri_nhom_1_2027") and b.get("ma_vi_tri_nhom_2_2027"))
 for _,_,b in all_steps
)
assert stats["buoc_phan_tuyen_cvt_khi_nhan_viec"]==7
warnings.append({"ma":"PHAN_VAI_TRO_THEO_NHOM","so_buoc":stats["buoc_vai_tro_theo_nhom_chua_chon_ca_nhan"],
  "ghi_chu":"Chọn nhóm, cơ sở, chức danh và mã nhân sự thật trước khi giao"})
warnings.append({"ma":"CHOT_CHUYEN_VIEN_TRUONG_THEO_NGUOI_NHAN_VIEC_VA_BAN_GIAO","so_buoc":stats["buoc_phan_tuyen_cvt_khi_nhan_viec"],
  "ghi_chu":"Năm bước tiếp nhận nhân sự và hai bước vắng mặt/nghỉ việc phải chọn đúng tuyến theo mã nhân sự, không mặc định Nội dung"})
if stats["buoc_kiem_tra_nguoi_doc_lap"]:
 warnings.append({"ma":"CHUA_XAC_NHAN_HAI_NGUOI_KHAC_NHAU","so_buoc":stats["buoc_kiem_tra_nguoi_doc_lap"]})
if stats["dau_ra_cho_ho_so"]:
 warnings.append({"ma":"CHUA_NGHIEM_THU_THUC_TE","so_dau_ra":stats["dau_ra_cho_ho_so"]})
# Kiểm tra độ phủ theo chức danh thực, không đồng nhất 26 mã với 26 người.
role_coverage={rid:{"ten":v["ten"],"chu_tri":0,"thuc_hien":0,"phoi_hop":0,
 "chuc_nang":bool(v.get("muc_dich")),"dau_ra":bool(v.get("phan_dinh_chu_tri_dau_ra")),
 "quyen_han":bool(v.get("phan_dinh_kiem_duyet")),"bao_cao":bool(v.get("bao_cao_cho")),
 "cnnv":bool(v.get("cnnv_2027")),"du_kien":rid=="qlml"} for rid,v in R.items()}
for qid,i,b in all_steps:
 owner=code(b.get("chu_tri_chinh",""))
 if owner in role_coverage:role_coverage[owner]["chu_tri"]+=1
 for x in b.get("thuc_hien",[]):
  c=code(x)
  if c in role_coverage:role_coverage[c]["thuc_hien"]+=1
 for x in b.get("phoi_hop",[]):
  c=code(x)
  if c in role_coverage:role_coverage[c]["phoi_hop"]+=1
for rid,z in role_coverage.items():
 missing=[k for k in ("chuc_nang","dau_ra","quyen_han","bao_cao","cnnv") if not z[k]]
 if missing:errors.append({"ma":"MTCV_CHUA_DU_CNNV","vi_tri":rid,"truong_thieu":missing})
 if not z["chu_tri"] and not z["thuc_hien"]:
  warnings.append({"ma":"CHUA_CO_BUOC_CHU_TRI_HOAC_THUC_HIEN","vi_tri":rid,
    "tinh_trang":"Cần đối chiếu dự kiến/kiêm nhiệm và hồ sơ giao việc, không tự cấp quyền"})
assert len(role_coverage)==26
gate=D.get("cnnv_dieu_phoi_ngoai_tuyen_2027",{})
load=D.get("cnnv_tai_hai_chuc_danh_2027",{})
if "CHỜ PHÂN TUYẾN" not in gate.get("khoa",""):
 errors.append({"ma":"THIEU_CHAN_DIEU_PHOI_NGOAI_TUYEN"})
if "CHƯA ĐỦ DỮ LIỆU" not in load.get("khoa_ket_luan",""):
 errors.append({"ma":"THIEU_CHAN_KET_LUAN_TAI_CVT"})
if len(D.get("cnnv_kiem_soat_luong_va_tham_quyen_2027",[]))!=6:
 errors.append({"ma":"THIEU_SAU_LOAI_LUONG_VA_QUYEN"})
for rid in ("bt-b","tk-b","md-b","tk-nt"):
 if "đầu mối điều phối" not in R[rid].get("bao_cao_cho",""):
  errors.append({"ma":"NHOM_2_CHUA_CO_CO_CHE_DIEU_PHOI", "vi_tri":rid})
if "/2 hướng dẫn" in R["dmpk"].get("bao_cao_cho",""):
 errors.append({"ma":"PHONG_KHAM_SAI_TUYEN_HUONG_DAN"})
if stats["buoc_chu_tri_trung_ma_phoi_hop"]:
 warnings.append({"ma":"CHUA_XAC_NHAN_NGUOI_KIEM_DOC_LAP",
                  "so_buoc":stats["buoc_chu_tri_trung_ma_phoi_hop"],
                  "yeu_cau":"Đối chiếu hai mã nhân sự thực tế, không dựa vào mã chức danh"})
# Từ cảnh báo số lượng sang DANH MỤC HỒ SƠ CẦN BỔ SUNG có mã
# định danh duy nhất. Chỉ ghi phiếu trắng; dữ liệu nhân sự/ủy quyền/giờ
# thực đo lưu trong hệ thống nội bộ có phân quyền, không xuất công khai.
process_names={q["id"]:q["ten"] for q in D["quy_trinh"]}
evidence_cases=[]
for qid,i,b in all_steps:
 flags=[]
 if b.get("ma_vi_tri_nhom_1_2027") and b.get("ma_vi_tri_nhom_2_2027"):
  flags.append("PHAN_TUYEN_NHOM")
 if b.get("chan_trung_nguoi_2027"):
  flags.append("NGUOI_KIEM_DOC_LAP")
 if b.get("chu_tri_thuc_te_theo_tuyen_cvt_2027"):
  flags.append("CHOT_TUYEN_CVT")
 if not flags:continue
 cand=b.get("chu_tri_thuc_te_theo_tuyen_cvt_2027",{})
 evidence_cases.append({
  "ma_buoc":qid+"-"+str(i).zfill(2),
  "quy_trinh":qid,
  "ten_quy_trinh":process_names[qid],
  "buoc":i,
  "phan_loai":"; ".join(flags),
  "chu_tri_mau":str(b.get("chu_tri_chinh","")),
  "ma_vi_tri_nhom_1":str(b.get("ma_vi_tri_nhom_1_2027","")),
  "ma_vi_tri_nhom_2":str(b.get("ma_vi_tri_nhom_2_2027","")),
  "tuyen_noi_dung":str(cand.get("nhan_su_noi_dung_sang_tao_hoac_marketing_co_so","")),
  "tuyen_truyen_thong_so":str(cand.get("nhan_su_truyen_thong_thuong_hieu_hoac_tang_truong_so","")),
  "can_bo_sung":"mã vị trí/nhóm/cơ sở và quyết định phân công hiệu lực" if "PHAN_TUYEN_NHOM" in flags
                  else "người kiểm độc lập có mã nhân sự khác người thực hiện" if "NGUOI_KIEM_DOC_LAP" in flags
                  else "chức danh, tuyến quản lý và quyết định tiếp nhận/bàn giao có hiệu lực",
  "trang_thai":"CHƯA ĐỦ CHỨNG CỨ – KHÔNG ĐƯỢC COI LÀ ĐÃ GIAO VIỆC/DUYỆT"
 })
count_by_flag=Counter(
 flag for c in evidence_cases for flag in c["phan_loai"].split("; ")
)
assert count_by_flag["PHAN_TUYEN_NHOM"]==stats["buoc_vai_tro_theo_nhom_chua_chon_ca_nhan"]
assert count_by_flag["NGUOI_KIEM_DOC_LAP"]==stats["buoc_kiem_tra_nguoi_doc_lap"]
assert count_by_flag["CHOT_TUYEN_CVT"]==stats["buoc_phan_tuyen_cvt_khi_nhan_viec"]
assert len({c["ma_buoc"] for c in evidence_cases})==len(evidence_cases)
assert len(evidence_cases)<=sum(count_by_flag.values())

dir_=root/"khung-marketing"
case_csv=dir_/"danh-muc-xac-minh-phan-vai-kiem-doc-lap-2027.csv"
columns=("ma_buoc","quy_trinh","ten_quy_trinh","buoc","phan_loai",
         "chu_tri_mau","ma_vi_tri_nhom_1","ma_vi_tri_nhom_2",
         "tuyen_noi_dung","tuyen_truyen_thong_so","can_bo_sung","trang_thai")
with case_csv.open("w",encoding="utf-8-sig",newline="") as h:
 writer=csv.DictWriter(h,fieldnames=columns)
 writer.writeheader()
 writer.writerows({k:v.get(k,"") for k in columns} for v in evidence_cases)
case_json=dir_/"danh-muc-xac-minh-phan-vai-kiem-doc-lap-2027.json"
case_json.write_text(json.dumps({
 "nguon":"60 quy trình/407 bước sau kiểm toán chức năng",
 "chua_du_chung_cu":True,
 "tong_buoc_khac_nhau":len(evidence_cases),
 "so_luot_rui_ro":dict(count_by_flag),
 "ghi_chu":"Số bước không cộng trùng. Có thể dùng một bộ hồ sơ phân công hiệu lực cho nhiều bước cùng vị trí/nhóm; từng bước vẫn lưu tham chiếu.",
 "bao_mat":"Không công khai mã nhân sự cá nhân, nhật ký giờ hoặc văn bản ủy quyền chưa được phép chia sẻ; xác minh trong hệ thống có phân quyền.",
 "danh_muc":evidence_cases
},ensure_ascii=False,indent=2),"utf-8")

# Mẫu duy nhất cho nhật ký giờ quản trị: dữ liệu gốc phải nằm trong
# hệ thống nhân sự/Marketing nội bộ; CSV xuất bản chỉ có tiêu đề.
timesheet_csv=dir_/"mau-nhat-ky-gio-quan-tri-hai-cvt-2027.csv"
time_cols=("ma_yeu_cau","ma_nhan_su_noi_bo","ma_vi_tri","nhom_to_co_so",
 "loai_gio","ngay","so_luot","so_phut_thuc_do","so_phut_dinh_muc_da_duyet",
 "can_cu_dinh_muc","nguon_gio","ma_ghi_nhan_trung_can_loai","tham_chieu_ho_so",
 "nguoi_xac_nhan_noi_bo")
with timesheet_csv.open("w",encoding="utf-8-sig",newline="") as h:
 writer=csv.writer(h);writer.writerow(time_cols)

# Người dùng chỉ tải mẫu công khai, không tải thông tin riêng của nhân sự.
# Không thêm quy trình hoặc chữ ký phê duyệt.
panel_anchor='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
if panel_anchor not in s:errors.append({"ma":"THIEU_NOI_DUNG_DE_HIEN_BANG_XAC_MINH"})
elif 'id="cnnv-danh-muc-chung-cu-2027"' not in s:
 panel=(
  '<div id="cnnv-danh-muc-chung-cu-2027" style="margin:12px 0;padding:12px;'
  'max-width:100%;box-sizing:border-box;overflow-wrap:anywhere;'
  'border:1px solid #d7e2ef;border-radius:8px">'
  '<strong style="display:block;color:#0837A1">Danh mục chứng cứ cần xác minh trước khi giao việc và nghiệm thu</strong>'
  '<p>Rà soát '+str(len(evidence_cases))+' bước khác nhau có điều kiện xác minh; gồm '+
    str(count_by_flag["PHAN_TUYEN_NHOM"])+' bước cần chọn nhóm/nhân sự, '+
    str(count_by_flag["NGUOI_KIEM_DOC_LAP"])+' bước cần xác nhận người kiểm độc lập và '+
    str(count_by_flag["CHOT_TUYEN_CVT"])+' bước cần chốt tuyến quản lý khi tiếp nhận, bàn giao. '
    'Các nhóm điều kiện có thể giao nhau; không cộng số lượng thành tổng lỗi.</p>'
  '<p>Phân vai chức danh theo mẫu không thay thế quyết định phân công; '
  'thiếu mã nhân sự, người kiểm hoặc ủy quyền hiệu lực thì giữ trạng thái chờ. '
  'Không kết luận đủ tải trước khi có giờ thực đo.</p>'
  '<p><a href="./danh-muc-xac-minh-phan-vai-kiem-doc-lap-2027.csv" download>'
  'Danh mục từng bước cần xác minh (CSV)</a> · '
  '<a href="./mau-nhat-ky-gio-quan-tri-hai-cvt-2027.csv" download>'
  'Mẫu nhật ký giờ quản trị (CSV trắng)</a></p>'
  '<p class="mini">Các biểu mẫu tải công khai là mẫu trống hoặc danh mục không có dữ liệu cá nhân. '
  'Thông tin nhân sự, ủy quyền và giờ thực tế phải lưu trong hệ thống nội bộ được phân quyền.</p>'
  '</div>'
 )
 s=s.replace(panel_anchor,panel+panel_anchor,1)
assert s.count('id="cnnv-danh-muc-chung-cu-2027"')==1
p.write_text(s,"utf-8")

report={
 "nguon":"HTML xuất bản từ main, dùng dữ liệu 26 chức danh, 60 quy trình, 407 bước và 568 đầu ra mẫu",
 "trang_thai":"LỖI CẦN SỬA" if errors else "ĐẠT KIỂM TRA CẤU TRÚC; CHỜ XÁC MINH HỒ SƠ THỰC TẾ",
 "thong_ke":dict(stats),
 "danh_muc_chung_cu":{"tong_buoc_khong_trung":len(evidence_cases),"so_luot_phan_loai":dict(count_by_flag),"ten_file_csv":case_csv.name,"mau_gio_csv":timesheet_csv.name},
 "doi_soat_26_ma_chuc_danh":role_coverage,
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
