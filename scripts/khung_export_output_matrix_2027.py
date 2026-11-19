#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xuất bảng kiểm kê 568 đầu ra, bốn trách nhiệm và trạng thái xác minh.
CSV không chứa dữ liệu cá nhân, là ma trận triển khai chờ đối chiếu nhân sự.
"""
import csv,json,re,sys
from pathlib import Path
from html import escape
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s);assert m
D=json.loads(m.group(2))
headers=[
 "Mã đầu ra","Quy trình","Bước","Đầu ra cụ thể","Căn cứ phân vai",
 "Mã vai trò thực hiện","Chủ trì theo nhóm/vị trí","Tuyến quản lý duy nhất",
 "Cửa phê duyệt hoặc bàn giao","Trạng thái quyền duyệt",
 "Cách hạch toán giờ","Chứng từ kiểm chứng","Xác nhận chuyên môn y tế",
 "Mã cá nhân thực tế","Quyết định phân công/ủy quyền","Giờ thực đo",
 "Trạng thái hoàn tất hồ sơ","Điều kiện chặn"
]
data=[]
for q in D["quy_trinh"]:
 for no,b in enumerate(q["buoc"],1):
  for actor,x in zip(b["thuc_hien"],b["doi_soat_tung_dau_ra_2027"]):
   tentative="CẦN ĐỐI CHIẾU MTCV" if "CẦN XÁC NHẬN" in x["can_cu_phan_vai_2027"] or "CHƯA ĐỦ CĂN CỨ" in x["can_cu_phan_vai_2027"] else "CẦN GẮN NGƯỜI THỰC TẾ"
   data.append([
    x["ma_dau_ra"],q["ten"],no,x["dien_giai"],x["can_cu_phan_vai_2027"],
    str(actor).split("|",1)[0],x["chu_tri_01"],x["tuyen_quan_ly_01"],
    x["quyen_duyet_cuoi_01"],x["trang_thai_duyet"],
    x["cach_hach_toan_tai_01"],x.get("chung_tu_thuc_te",x.get("chung_tu","")),
    "Có" if x.get("can_xac_nhan_y_te") else "Theo loại đầu ra",
    "CHƯA GẮN","CHƯA XÁC NHẬN","CHƯA ĐO",tentative,
    "Không giao/phát hành nếu thiếu người, tuyến duy nhất hoặc quyền duyệt bắt buộc; không tự kiểm khi cần độc lập"
   ])
assert len(data)==568
assert len({row[0] for row in data})==568
assert all(row[3] and row[6] and row[7] and row[8] and row[10] for row in data)
target=root/"khung-marketing"/"doi-soat-568-dau-ra.csv"
with target.open("w",encoding="utf-8-sig",newline="") as o:
 w=csv.writer(o,lineterminator="\n");w.writerow(headers);w.writerows(data)
target_json=root/"khung-marketing"/"doi-soat-568-dau-ra.json"
target_json.write_text(json.dumps([dict(zip(headers,row)) for row in data],ensure_ascii=False,indent=2),"utf-8")
assert target.exists() and target.stat().st_size>100000
section='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
assert section in s
idx=s.index(section)
at=s.index("</h3>",idx)+5
block=(
 '<p id="tth-output-audit-download" style="margin:10px 0 14px;overflow-wrap:anywhere">'
 '<a href="./doi-soat-568-dau-ra.csv" download="doi-soat-568-dau-ra.csv" '
 'style="color:#0837A1;font-weight:700;text-decoration:underline">'
 'Tải bảng đối soát 568 đầu ra (CSV)</a>'
 ' — gồm chủ trì, tuyến quản lý, phê duyệt, hạch toán tải và cột đối chiếu hồ sơ thực tế. '
 'Bảng là phương án kiểm soát, chưa thay phân công hay ủy quyền có hiệu lực.</p>'
)
if 'id="tth-output-audit-download"' not in s:s=s[:at]+block+s[at:]
p.write_text(s,"utf-8")
print("PASS EXPORT OUTPUT MATRIX: 568 unique rows, 18 columns, CSV+JSON, link in chapter 4.3.")
