#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Khóa chồng chéo còn lại sau khi xuất 568 đầu ra và các ví dụ nghiệp vụ.
Không suy diễn người thật, ủy quyền thật, hay giờ thực tế từ mã vị trí mẫu.
"""
import csv,json,re,sys
from pathlib import Path
from html import escape
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=rx.search(s)
assert m,"Không thấy CSDL"
D=json.loads(m.group(2))
Q=D["quy_trinh"]
V={v["id"]:v for v in D["vi_tri"]}
assert len(V)==26 and len(Q)==60 and sum(len(q["buoc"]) for q in Q)==407
assert len(D.get("vi_du_van_hanh_hai_chuyen_vien_truong_2027",[]))==14
aliases=D["ma_tran_chu_tri_theo_nhom_2027"]
assert aliases["mkt-tct"]["nhom_1"]=="tp" and aliases["mkt-tct"]["nhom_2"]=="tp"
ND=V["cvt"]["ten"]
TT=V["cvt-2"]["ten"]
assert ND=="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
assert TT=="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
def key(s):return str(s).split("|",1)[0]
all_outputs={}
num_generic_steps=0
num_collab_codes_merged=0
num_same_role_steps=0
num_multi_steps=0
total_report=0
mkt_tct=0
tt_nd=0
role_group=0
possible_same_codes=[]
for q in Q:
 for step_no,b in enumerate(q["buoc"],1):
  # Hai bản ghi cùng mã chức danh trong phần phối hợp không phải hai người.
  # Gộp mô tả bổ sung, giữ nguyên các vai trò khác và không tạo quyền mới.
  unique={}
  order=[]
  for item in b.get("phoi_hop",[]):
   role_part=key(item)
   detail=str(item).split("|",1)[1].strip() if "|" in str(item) else ""
   if role_part not in unique:
    unique[role_part]=[detail] if detail else []
    order.append(role_part)
   else:
    num_collab_codes_merged+=1
    if detail and detail not in unique[role_part]:unique[role_part].append(detail)
  b["phoi_hop"]=[name+("|"+"; ".join(unique[name]) if unique[name] else "") for name in order]
  assert len({key(x) for x in b["phoi_hop"]})==len(b["phoi_hop"])
  actors=b["thuc_hien"]
  out=b["doi_soat_tung_dau_ra_2027"]
  assert len(out)==len(actors)>0,(q["id"],step_no)
  code=key(b.get("chu_tri_chinh",""))
  if code in aliases:num_generic_steps+=1
  if len(actors)>1:num_multi_steps+=1
  collaborators={key(x) for x in b.get("phoi_hop",[])}
  overlap=code in collaborators
  if overlap:
   num_same_role_steps+=1
   b["xac_minh_kiem_doc_lap_2027"]="BẮT BUỘC hai mã cá nhân khác nhau, không chỉ hai vai trò trên sơ đồ; người kiểm không được tự duyệt."
   assert b.get("chan_trung_nguoi_2027") is True
   possible_same_codes.append(q["id"]+"-"+str(step_no))
  if q["id"]=="nhan-viec-moi" and step_no in (2,3,4,5,6):
   # Mã CVT Nội dung trong SOP mẫu không được là chủ trì mặc định
   # khi nhận nhân sự thuộc Tổ Truyền thông/Thương hiệu hoặc Tăng trưởng số.
   b["chu_tri_thuc_te_theo_tuyen_cvt_2027"]={
    "nhan_su_noi_dung_sang_tao_hoac_marketing_co_so":"cvt",
    "nhan_su_truyen_thong_thuong_hieu_hoac_tang_truong_so":"cvt-2",
    "dieu_kien":"Chọn một mã vị trí, nhóm, tổ, cá nhân và văn bản phân công trước khi giao; không có hai người quản lý trực tiếp."}
   b["phan_cong_thuc_thi_2027"]=(
    "CHỌN MỘT TUYẾN theo người nhận việc: "+ND+" phụ trách nhân sự Nội dung – Sáng tạo/Marketing cơ sở chưa bàn giao; "
    +TT+" phụ trách nhân sự Tổ Truyền thông và Thương hiệu/Tổ Tăng trưởng số. "
    "Trưởng phòng chịu việc vượt tuyến; đơn vị cấp quyền thực hiện theo ma trận có hiệu lực. "
    "Mã CVT Nội dung trong SOP mẫu KHÔNG phải chủ trì mặc định cho hai tổ còn lại.")
  if code=="mkt-tct":
   b["phan_cong_thuc_thi_2027"]=(
    "CHẶN GIAO VIỆC CHUNG: 'Marketing Tổng công ty' không phải cá nhân hay một chức danh. "
    "Mỗi đầu ra phải phân giải về chuyên viên chuyên môn tương ứng; "
    "chỉ báo cáo tổng hợp và quyết định thuộc thẩm quyền mới giao Trưởng phòng Marketing. "
    "Không sử dụng mã kỹ thuật quy đổi Trưởng phòng như quyết định giao sản xuất."
   )
   b["dieu_kien_giao_viec_2027"]=(
    "Phải có mã nhân sự, chức danh thực tế, một tuyến quản lý và đầu ra cụ thể "
    "trước khi chuyển trạng thái giao việc; nếu không thì khóa."
   )
  b["chot_luong_giao_viec_2027"]=(
   "Một mã việc và một tuyến quản lý; Tổ trưởng/Trưởng nhóm giao việc thường lệ; "
   +ND+" chỉ điều phối sản xuất/cơ sở vượt tuyến; "+TT+
   " kiểm chuẩn truyền thông/số và quản lý hai tổ, không tự giao lệnh thứ hai đến cơ sở."
  )
  for i,(actor,z) in enumerate(zip(actors,out),1):
   role=key(actor)
   oid=z["ma_dau_ra"]
   assert oid not in all_outputs
   flags=[]
   if q["id"]=="nhan-viec-moi" and step_no in (2,3,4,5,6) and role=="cvt":
    z["chu_tri_01"]=(
     "CHỜ CHỌN MỘT TUYẾN: "+ND+" nếu nhân sự thuộc Nội dung – Sáng tạo/Marketing cơ sở chưa bàn giao; "
     +TT+" nếu nhân sự thuộc Tổ Truyền thông và Thương hiệu/Tổ Tăng trưởng số. "
     "Không mặc định người ở tuyến Nội dung chịu trách nhiệm cho hai tổ còn lại.")
    z["ma_chu_tri_theo_nhom"]={
     "tuyen_noi_dung_va_marketing_co_so":"cvt",
     "tuyen_truyen_thong_thuong_hieu_va_tang_truong_so":"cvt-2",
     "dieu_kien":"Chọn duy nhất theo mã người và quyết định điều chuyển/tiếp nhận"}
    z["tuyen_quan_ly_01"]="Trưởng phòng Marketing → "+ND+" hoặc "+TT+"; CHỈ MỘT tuyến theo vị trí được tiếp nhận"
    flags.append("CHẶN: chưa chọn mã nhân sự và tuyến quản lý đúng chức danh trong bước nhận việc")
   if role=="mkt-tct":
    mkt_tct+=1
    z["chu_tri_01"]=(
     "CHƯA CHỐT: người làm đúng chức danh tại Tổng công ty theo tính chất công việc; "
     "Trưởng phòng chỉ chủ trì bản tổng hợp hoặc quyết định thuộc thẩm quyền"
    )
    z["tuyen_quan_ly_01"]="CHƯA CHỐT: một tuyến quản lý theo chức danh được phân công thực tế"
    z["ma_chu_tri_theo_nhom"]={"can_phan_giai":"mkt-tct"}
    flags.append("CHẶN: mã Marketing Tổng công ty không được tự quy thành Trưởng phòng")
   elif role=="tt-nd":
    tt_nd+=1
    z["chu_tri_01"]="Tổ trưởng Tổ Nội dung và Sáng tạo được chỉ định bằng văn bản; chức danh gốc Biên tập nhóm 1"
    z["tuyen_quan_ly_01"]=ND+"; chỉ áp dụng trong phạm vi kiêm nhiệm được giao"
    flags.append("CHẶN nếu chưa có văn bản giao điều phối toàn tổ, thời hạn và người dự phòng")
   elif role in aliases:
    role_group+=1
    flags.append("CHỜ: chọn đúng một nhóm thương hiệu, một mã vị trí, một cá nhân và cơ sở")
   else:
    assert role in V or role in {x["id"] for x in D.get("vai_tro",[])}|{x["id"] for x in D.get("don_vi",[])}|{x["id"] for x in D.get("chuc_danh",[])}, (oid,role)
   if overlap and role==code:
    flags.append("CHẶN tự kiểm: người làm và người kiểm phải có hai mã nhân sự khác nhau")
   if z.get("can_cu_phan_vai_2027") in (
      "PHÂN VAI MẪU, CẦN XÁC NHẬN",
      "ĐẦU RA CẦN ĐƠN VỊ CHỦ QUẢN XÁC NHẬN",
      "CHƯA ĐỦ CĂN CỨ PHÂN TÁCH, CHẶN GIAO VIỆC"
   ):
    flags.append("CHỜ xác nhận đầu ra đặc thù bằng MTCV/chủ quản và chứng từ")
   if z["trang_thai_duyet"] in ("CHỜ GẮN QUYỀN","CHỜ ĐỐI CHIẾU HẠN MỨC"):
    flags.append("CHẶN phát hành hoặc chi nếu chưa xác định người duyệt và văn bản còn hiệu lực")
   if z.get("can_xac_nhan_y_te"):
    flags.append("CHẶN phát hành khi chưa có xác nhận nội dung chuyên môn y tế")
   # Thiết kế mẫu không thể tự biết người đang thực hiện, số giờ, hay chữ ký.
   flags.append("CHỜ mã nhân sự, hồ sơ phân công, chứng từ bàn giao và giờ thực đo")
   z["trang_thai_nghiem_thu_2027"]="CHƯA NGHIỆM THU HỒ SƠ THỰC TẾ"
   z["ly_do_chua_nghiem_thu_2027"]="; ".join(dict.fromkeys(flags))
   z["quy_tac_01_chu_01_tuyen_01_duyet_01_gio_2027"]=(
    "Một cá nhân chủ trì mã đầu ra, một cấp quản lý trực tiếp; "
    "mỗi loại quyết định có đúng một thẩm quyền cuối, các cửa khác là kiểm/xác nhận; "
    "mỗi khoảng giờ chỉ ghi một lần cho người và loại giờ thực tế."
   )
   z["nghiep_vu_khong_chong_cheo_2027"]=(
    "Người thực hiện chịu sản phẩm; Tổ trưởng chịu giao việc thường ngày; "
    +ND+" chịu quản trị sản xuất/cơ sở đúng tuyến; "
    +TT+" chịu quản trị truyền thông/thương hiệu/số đúng tuyến; "
    "Quản lý thương hiệu chịu nghiệm thu mục tiêu; phê duyệt phát hành và chi phí độc lập."
   )
   all_outputs[oid]=z
   total_report+=1
assert total_report==568
assert num_generic_steps==95,(num_generic_steps,95)
assert num_same_role_steps==14,(num_same_role_steps,14)
assert num_multi_steps==121,(num_multi_steps,121)
assert len(all_outputs)==568
D["kiem_toan_chong_cheo_chot_2027"]={
 "pham_vi":{"vi_tri":26,"quy_trinh":60,"buoc":407,"dau_ra":568,
  "buoc_ma_vai_tro_chung":num_generic_steps,
  "buoc_can_tach_nguoi_kiem":num_same_role_steps,
  "buoc_co_nhieu_nguoi_thuc_hien":num_multi_steps,
  "dau_ra_mkt_tct_chua_phan_giai":mkt_tct,
  "dau_ra_to_truong_noi_dung_can_phan_cong":tt_nd,
  "dau_ra_theo_nhom_can_chon_nhan_su":role_group,
  "ma_phoi_hop_trung_da_gop":num_collab_codes_merged,
  "buoc_nhan_viec_phai_chon_tuyen":5},
 "ket_luan":"Đã chuẩn hóa điều kiện phân vai và chặn chồng chéo ở cấp đề án; chưa có mã nhân sự, văn bản ủy quyền và số giờ thực đo nên chưa nghiệm thu vận hành.",
 "khong_duoc_suy_ra":"95, 14 và 121 là trường hợp cần kiểm soát, không phải số lỗi thực tế đã xác minh.",
 "noi_dung":"Trưởng phòng không mặc định chủ trì sản phẩm tập thể TCT; CVT không làm Tổ trưởng thường trực; CVT Truyền thông/Số không giao việc trực tiếp tới cơ sở.",
 "nguong_nghiem_thu":"Mỗi mã việc phải có một người chủ trì, một tuyến, duyệt riêng theo loại quyết định, một cách ghi giờ và chứng từ, xác nhận người kiểm độc lập.",
 "kiem_thu_giao_dien":"Tệp này tạo điều kiện kiểm soát, không thay kết quả click/quan sát trên trình duyệt thật."
}
m=rx.search(s)
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]
# Hiện trạng thái ngay trong mỗi thẻ đầu ra, không buộc người xem tải tệp mới biết chưa nghiệm thu.
needle="<p><b>Hạch toán tải:</b> '+tx(a.cach_hach_toan_ngan_2027)+'</p>"
assert s.count(needle)==1,"Thẻ đầu ra đã thay cấu trúc; kiểm tra lại thay vì chèn sai JS"
s=s.replace(needle,needle+
 "<p><b>Trạng thái nghiệm thu:</b> '+tx(a.trang_thai_nghiem_thu_2027)+'</p>"
 "<p><b>Điều kiện còn thiếu:</b> '+tx(a.ly_do_chua_nghiem_thu_2027)+'</p>",1)
# Nhãn điều khiển đóng gọn. Không tạo bảng 1180 px hoặc thanh cuộn ngang trang.
mark='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
assert s.count(mark)==1
loc=s.index(mark)
h=s.index("</h3>",loc)+5
panel=(
 '<details id="tth-final-conflict-audit-2027" style="max-width:100%;'
 'min-width:0;margin:12px 0;border:1px solid #d7e2f0;border-radius:8px;padding:12px;'
 'background:#fff;box-sizing:border-box;overflow-wrap:anywhere">'
 '<summary style="cursor:pointer;color:#0837A1;font-weight:700">'
 'Đối soát trách nhiệm và các điều kiện còn phải xác minh</summary>'
 '<p>Đã rà soát 26 chức danh, 60 quy trình, 407 bước và 568 đầu ra mẫu. '
 '95 bước dùng mã chức danh tổng quát phải chọn nhóm và người thật; '
 '14 bước có nguy cơ tự kiểm cần hai mã cá nhân độc lập; '
 '121 bước nhiều bên phải tách sản phẩm và tải từng người. '
 'Đây là rủi ro cần kiểm soát, không phải khẳng định có bấy nhiêu lỗi thực tế.</p>'
 '<p><b>Chặn:</b> Vai trò Marketing Tổng công ty không được quy mặc định thành '
 'Trưởng phòng. Việc điều phối toàn Tổ Nội dung phải có quyết định kiêm nhiệm. '
 'Báo cáo tải chỉ ghi giờ của cá nhân thực làm. '
 'Chưa gắn người, văn bản phân quyền, chứng từ và giờ thực đo thì trạng thái '
 'là CHƯA NGHIỆM THU, không thể coi là hoàn thành.</p></details>'
)
assert 'id="tth-final-conflict-audit-2027"' not in s
s=s[:h]+panel+s[h:]
# Xuất lại bảng đối soát sau khi sửa đúng 568 bản ghi, tránh bản CSV cũ sai Trưởng phòng.
directory=root/"khung-marketing"
path=directory/"doi-soat-568-dau-ra.csv"
assert path.exists(),"Bảng CSV gốc phải được xuất ở bước trước"
with path.open("r",encoding="utf-8-sig",newline="") as f:
 reader=csv.DictReader(f)
 headers=list(reader.fieldnames or [])
 rows=list(reader)
assert len(rows)==568
extra=["Trạng thái đối soát cuối","Điều kiện còn thiếu","Nguyên tắc chống chồng chéo"]
headers= list(dict.fromkeys(headers+extra))
for row in rows:
 z=all_outputs[row["Mã đầu ra"]]
 row["Chủ trì theo nhóm/vị trí"]=z["chu_tri_01"]
 row["Tuyến quản lý duy nhất"]=z["tuyen_quan_ly_01"]
 row["Trạng thái hoàn tất hồ sơ"]=z["trang_thai_nghiem_thu_2027"]
 row["Trạng thái đối soát cuối"]=z["trang_thai_nghiem_thu_2027"]
 row["Điều kiện còn thiếu"]=z["ly_do_chua_nghiem_thu_2027"]
 row["Nguyên tắc chống chồng chéo"]=z["quy_tac_01_chu_01_tuyen_01_duyet_01_gio_2027"]
with path.open("w",encoding="utf-8-sig",newline="") as f:
 writer=csv.DictWriter(f,fieldnames=headers,lineterminator="\n")
 writer.writeheader();writer.writerows(rows)
(directory/"doi-soat-568-dau-ra.json").write_text(
 json.dumps(rows,ensure_ascii=False,indent=2),"utf-8")
(directory/"ket-qua-doi-soat-trach-nhiem-2027.json").write_text(
 json.dumps(D["kiem_toan_chong_cheo_chot_2027"],ensure_ascii=False,indent=2),"utf-8")
# Chặn chuỗi tên gọi chung còn sót trên cả CSDL và HTML tĩnh.
latest=json.loads(rx.search(s).group(2))
generic=re.compile(r"Chuyên viên trưởng(?!\s+(?:Nội dung|Truyền thông))",re.I)
bad=[]
def walk(x,path="D"):
 if isinstance(x,str) and generic.search(x):bad.append(path)
 elif isinstance(x,dict):
  for k,v in x.items():walk(v,path+"."+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+"["+str(i)+"]")
walk(latest)
static=re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>'," ",s,flags=re.I)
static=re.sub(r'<[^>]+>'," ",static)
if generic.search(static):bad.append("HTML tĩnh")
assert not bad,"Còn chức danh chung: "+str(bad[:10])
assert s.count('id="tth-final-conflict-audit-2027"')==1
assert s.count("a.trang_thai_nghiem_thu_2027")==1
p.write_text(s,"utf-8")
print("PASS FINAL RESPONSIBILITY GATE: 26 roles, 60 flows, 407 steps, 568 outputs; ",
 num_generic_steps,"group-conditional steps,",num_same_role_steps,
 "independent-check conditions,",num_multi_steps,"multi-role steps;",
 mkt_tct,"ambiguous TCT outputs blocked; CSV/JSON refreshed; no generic chief title.")
