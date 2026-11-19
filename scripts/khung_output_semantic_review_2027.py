#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rà soát NGỮ NGHĨA từng đầu ra sau phân rã, tránh copy cả bước cho 3 vị trí.

Chỉ dẫn suy ra từ MTCV trong đề án. Phần chưa xác minh được để CẦN XÁC NHẬN,
không đổi quyền nhân sự/duyệt; kiểm tra giao diện bằng Chrome ở bước sau.
"""
import json,re,sys
from pathlib import Path
from html import escape
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
RX=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=RX.search(s);assert m
D=json.loads(m.group(2))
R={v["id"]:v for v in D["vi_tri"]}
assert len(R)==26 and len(D["quy_trinh"])==60

def key(text):return str(text).split("|",1)[0]
def family(code):
    return {
    "bt":"Biên tập","tk":"Thiết kế","md":"Media",
    "qc":"Quảng cáo – kênh số","qlth":"Quản lý thương hiệu",
    "cvtt":"Truyền thông","tn":"Trưởng nhóm cơ sở",
    "mkt-coso":"Marketing cơ sở","mkt-tct":"Marketing TCT",
    "cvt":"Quản lý Nội dung – Sáng tạo","cvt-2":"Quản lý Truyền thông – Số",
    "dl":"Đo lường – dữ liệu","qlsps":"Quản lý sản phẩm số",
    "tt-nd":"Tổ trưởng Nội dung","cc":"Contact Center",
    "qhcs":"Truyền thông cơ sở","mdcs":"Media cơ sở",
    "phap-che":"Pháp chế","cnnvy":"Công nghệ – Nghiệp vụ Y",
    "so-hoa":"Số hóa","tp":"Trưởng phòng",
    "gd-coso":"Giám đốc cơ sở",
    }.get(code.split("-")[0],code)

# Mỗi ô nói một sản phẩm/tác nghiệp có thể kiểm tra, dựa đúng MTCV.
# Các tình huống trọng tâm được lập tường minh để không tự suy diễn từ câu dài.
exact={
 ("hang-muc",6,"bt-ac"):"Bài viết và kịch bản lời nhóm 1; hồ sơ nguồn, xác nhận y khoa và phiếu kiểm Biên tập độc lập",
 ("hang-muc",6,"tk-a"):"Bản thiết kế hình ảnh/ấn phẩm nhóm 1 theo nội dung đã xác nhận; file gốc và bản xuất",
 ("hang-muc",6,"md-ac"):"Kịch bản phân cảnh, shot-list và bản dựng video nhóm 1; file tư liệu, bản dựng và phiếu kiểm kỹ thuật độc lập",
 ("hang-muc",8,"qc-a"):"Trang đích và quảng cáo/kênh số nhóm 1 theo kế hoạch đã duyệt; log phân phối, mã nguồn khách",
 ("hang-muc",8,"cvtt-a"):"Hồ sơ triển khai băng rôn, tờ rơi, phát thanh và đối tác tại cơ sở nhóm 1; nhật ký, hợp đồng đúng phân cấp",
 ("hang-muc",8,"qhcs"):"Ảnh/số đo hiện trường, nhật ký treo/phát, biên bản hiện trạng tại bệnh viện nhóm 1",
 ("hang-muc",11,"dl-1"):"Bảng đối soát Lead, lượt khách, doanh thu và nguồn ghi nhận; căn cứ số liệu độc lập",
 ("hang-muc",11,"qlth-a"):"Báo cáo tổng kết Hạng mục nhóm 1 và phân tích mục tiêu – kết quả – bài học",
 ("hang-muc",11,"tp"):"Biên bản nghiệm thu Hạng mục theo thẩm quyền, không thay số liệu của người đối soát",
 ("crm",2,"dl-2"):"Tập yêu cầu trường dữ liệu, consent, phân vai, quy tắc gộp hồ sơ trùng",
 ("crm",2,"dl-1"):"Tập tiêu chí Lead hợp lệ, logic đo nguồn và KPI vận hành",
 ("crm",2,"qlsps"):"Tập yêu cầu giao diện, luồng tích hợp kênh và tiêu chí nghiệm thu sản phẩm số",
 ("crm",4,"cnnvy"):"Biên bản kết nối CRM – tổng đài – HIS – email, xác nhận kỹ thuật và quyền truy cập",
 ("crm",4,"so-hoa"):"Biên bản kết nối website/App/form với CRM và kiểm thử dữ liệu truyền nhận",
 ("bo-nhan-dien",7,"tk-nt"):"Danh mục và cấu trúc thư viện mẫu, quyền phiên bản, danh sách thu hồi mẫu cũ; mẫu biển bảng ngoại tuyến",
 ("bo-nhan-dien",7,"tk-a"):"Mẫu thiết kế sẵn cho sản phẩm số/in của Nhóm 1 theo nhận diện đã duyệt",
 ("bo-nhan-dien",7,"tk-b"):"Mẫu thiết kế sẵn cho sản phẩm số/in của Nhóm 2 theo nhận diện đã duyệt",
 ("bo-nhan-dien",9,"tk-nt"):"File thi công biển bảng, trang trí và phương tiện; phiếu xác nhận kỹ thuật file in",
 ("bo-nhan-dien",9,"tk-a"):"File ấn phẩm, vật phẩm và đồng phục thuộc Nhóm 1",
 ("bo-nhan-dien",9,"tk-b"):"File ấn phẩm, vật phẩm và đồng phục thuộc Nhóm 2",
 ("quang-cao-tra-phi",4,"bt"):"Lời quảng cáo và các biến thể câu chữ; kiểm nội dung, y khoa/pháp lý khi áp dụng",
 ("quang-cao-tra-phi",4,"tk"):"Bộ hình quảng cáo đúng kích thước và nhận diện đã nghiệm thu",
 ("quang-cao-tra-phi",4,"md"):"Video quảng cáo và bản dựng kỹ thuật theo kịch bản lời đã được kiểm",
 ("phat-thanh-man-hinh",5,"tn-b"):"Nhật ký phát thanh/màn hình, đối chiếu lịch đã duyệt tại bệnh viện Nhóm 2 có hai người",
 ("phat-thanh-man-hinh",6,"tn-b"):"Sổ kiểm vận hành, báo hỏng và xác nhận đã thông báo Truyền thông TCT tại cơ sở hai người",
 ("tin-trong-ngay",5,"md-b"):"Bản dựng và phiếu kiểm kỹ thuật clip V2/V3 nếu triển khai; không nhận quyền đăng kênh",
 ("tin-trong-ngay",5,"qc-b"):"Lịch và nhật ký đăng TikTok/YouTube Nhóm 2 trên kênh được phân quyền",
}
action_by_family={
 "Biên tập":"Bản nội dung/kịch bản lời, nguồn thông tin và kiểm tra biên tập đúng nhóm",
 "Thiết kế":"File thiết kế và bản xuất cho đúng nhóm, có mã phiên bản và căn cứ nhận diện",
 "Media":"Tư liệu quay/chụp, kịch bản phân cảnh hoặc bản dựng kỹ thuật đúng nhóm",
 "Quảng cáo – kênh số":"Bản ghi lịch đăng/quảng cáo, nhật ký thiết lập hoặc báo cáo kênh theo quyền được cấp",
 "Quản lý thương hiệu":"Hồ sơ kế hoạch/điều phối hoặc nghiệm thu mục tiêu thương hiệu trong phạm vi nhóm",
 "Truyền thông":"Hồ sơ PR, đối tác, OOH, màn hình/phát thanh hoặc sự kiện theo nhóm được giao",
 "Trưởng nhóm cơ sở":"Thông tin nguồn đã xác nhận, lịch và biên bản triển khai cơ sở trong phạm vi phân công",
 "Marketing cơ sở":"Hồ sơ hiện trường từ cơ sở, ảnh và nhật ký có đầu mối phụ trách",
 "Marketing TCT":"Bản báo cáo/công việc được lập riêng theo chức danh; không gộp hết vào Trưởng phòng",
 "Đo lường – dữ liệu":"Bảng dữ liệu nguồn, đối soát và kiểm tra chất lượng dữ liệu độc lập",
 "Quản lý sản phẩm số":"Hồ sơ đặc tả, kiểm thử hoặc nghiệm thu sản phẩm số đúng phạm vi",
 "Tổ trưởng Nội dung":"Bảng phân công, thứ tự ưu tiên và lịch sản xuất; không ghi sản phẩm của chuyên viên thành giờ Tổ trưởng",
 "Contact Center":"Kịch bản/nhật ký tư vấn, đặt lịch và kết quả tiếp nhận theo phân cấp nghiệp vụ",
 "Truyền thông cơ sở":"Hồ sơ sự kiện, màn hình, phát thanh, OOH và ảnh/số đo hiện trường",
 "Media cơ sở":"Tư liệu quay/chụp hoặc bản dựng cơ sở theo B-7",
 "Pháp chế":"Ý kiến pháp lý, căn cứ và hồ sơ thủ tục thuộc đơn vị pháp chế",
 "Công nghệ – Nghiệp vụ Y":"Biên bản kỹ thuật, quyền hệ thống, nhật ký tích hợp và xác nhận nghiệp vụ công nghệ",
 "Số hóa":"Tài liệu và biên bản kỹ thuật website, App hoặc tích hợp",
 "Trưởng phòng":"Tờ trình, quyết định điều phối hoặc hồ sơ kiểm tra thuộc thẩm quyền đã phân cấp",
 "Giám đốc cơ sở":"Xác nhận nguồn và quyết định thuộc phạm vi cơ sở",
}
def normalize(text,max_len=150):
 text=re.sub(r'\s+',' ',text).strip().strip(".; ")
 return text[:max_len].rstrip(" ,.;") if len(text)>max_len else text

def desc(q,step_no,b,actor):
 code=key(actor)
 special=exact.get((q["id"],step_no,code))
 if special:return special,"ĐỐI CHIẾU MTCV VÀ TÌNH HUỐNG"
 label=family(code)
 action=action_by_family.get(label)
 note=(actor.split("|",1)[1].strip() if "|" in actor else "")
 # Chỉ dùng câu ghi chú có nghĩa, không dùng cả nội dung bước cắt 215 ký tự.
 if note and len(note)>15 and len(note)<220 and ";" not in note:
    return normalize(note,200), "GHI CHÚ CHỨC NĂNG TẠI BƯỚC"
 if action:
    return ((R[code]["ten"] if code in R else label)+": "+action+"; bằng chứng: "+normalize(b.get("ghi_nhan") or "nhật ký công việc",65)),"PHÂN VAI MẪU, CẦN XÁC NHẬN"
 # Đơn vị bên ngoài Marketing không được gán mặc nhiên sản phẩm marketing.
 return ("Phần nghiệp vụ của "+label+" tại bước "+str(step_no)+
         "; kết quả/bằng chứng: "+normalize(b.get("ghi_nhan") or b.get("dau_ra_kiem_chung") or "",90),
         "ĐẦU RA CẦN ĐƠN VỊ CHỦ QUẢN XÁC NHẬN")

n=0
uncertain=0
multi=0
for q in D["quy_trinh"]:
 for i,b in enumerate(q["buoc"],1):
    outputs=b["doi_soat_tung_dau_ra_2027"]
    assert len(outputs)==len(b["thuc_hien"])
    for actor,z in zip(b["thuc_hien"],outputs):
      v,kind=desc(q,i,b,actor)
      assert v and len(v)<340
      z["dien_giai"]=v
      z["can_cu_phan_vai_2027"]=kind
      z["xac_nhan_nguoi_duyet_hieu_luc"]=(
         "Phải gắn mã cá nhân và số văn bản ủy quyền hợp lệ trước khi chuyển sang phát hành/chi phí"
         if z["trang_thai_duyet"]=="CHỜ GẮN QUYỀN" else
         "Không phát sinh quyền duyệt mới; nếu phát hành ở bước sau phải kiểm lại ma trận có hiệu lực"
      )
      z["chung_tu_thuc_te"]=z.get("chung_tu","")
      if kind in ("PHÂN VAI MẪU, CẦN XÁC NHẬN","ĐẦU RA CẦN ĐƠN VỊ CHỦ QUẢN XÁC NHẬN"):uncertain+=1
      n+=1
    if len(outputs)>1:
       multi+=1
       labels={}
       for z in outputs:
         label=z["dien_giai"]
         labels[label]=labels.get(label,0)+1
         if labels[label]>1:
           z["dien_giai"]=label+" — phần đầu ra tiếp theo của cùng chức năng (CẦN XÁC NHẬN tách người/đầu ra)"
           z["can_cu_phan_vai_2027"]="CHƯA ĐỦ CĂN CỨ PHÂN TÁCH, CHẶN GIAO VIỆC"
       assert len({x["dien_giai"] for x in outputs})==len(outputs),(q["id"],i,[x["dien_giai"] for x in outputs])
# Đừng coi tình huống 3 người bệnh viện nhóm 2 là có sẵn Chuyên viên truyền thông
# từ Nhóm 1; vai trò này chỉ hình thành sau khi phân bổ nhân sự hợp lệ.
q=next(q for q in D["quy_trinh"] if q["id"]=="phat-thanh-man-hinh")
b=q["buoc"][5]
b["dieu_kien_nhan_su_thuc_te_2027"]=(
 "Nhóm 2 hiện xác định Trưởng nhóm kiêm Truyền thông tại cơ sở hai người. "
 "Khi bố trí đủ ba người, KHÔNG tự lấy mã Chuyên viên truyền thông cơ sở Nhóm 1; "
 "cần quyết định vị trí, nhóm, người quản lý và bàn giao có hiệu lực trước khi chuyển chủ việc."
)
for x in b["doi_soat_tung_dau_ra_2027"]:
 x["dieu_kien_2_3_nguoi"]=b["dieu_kien_nhan_su_thuc_te_2027"]
D["kiem_toan_mo_ta_dau_ra_2027"]={
 "so_dau_ra":n,"so_buoc_da_nguoi":multi,"so_dau_ra_can_xac_nhan_noi_dung_chuyen_biet":uncertain,
 "nguyen_tac":"Đầu ra có mô tả theo vai trò và chứng từ; phần được suy từ CNNV chỉ là dự kiến, không coi là sản lượng thực hoặc tự cấp quyền.",
 "canh_bao":"Không thể chứng minh 568 kết quả đã tồn tại nếu chưa có mã người thật, chứng từ và giờ thực đo."
}
assert n==568 and multi==121
assert len({x["ma_dau_ra"] for q in D["quy_trinh"] for b in q["buoc"] for x in b["doi_soat_tung_dau_ra_2027"]})==568
m=RX.search(s)
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]

# Làm rõ nguồn xác định trên thẻ; đưa chứng từ vào một dòng riêng,
# tránh ngữ nghĩa một đoạn mô tả bước bị lặp cho ba người.
anchor="<p><b>Chủ trì duy nhất:</b> '+tx(a.chu_tri_01)+'</p>"
if anchor not in s:raise RuntimeError("Thiếu thẻ chủ trì trong giao diện, không tự thay để tránh lỗi hiển thị")
s=s.replace(anchor,
 "<p><b>Căn cứ phân vai:</b> '+tx(a.can_cu_phan_vai_2027)+'</p>"
 "<p><b>Chủ trì duy nhất:</b> '+tx(a.chu_tri_01)+'</p>",1)
assert "can_cu_phan_vai_2027" in s
p.write_text(s,"utf-8")
print("PASS OUTPUT SEMANTICS:",n,"deliverables,",multi,
      "multi-actor steps, descriptions unique per step;",
      uncertain,"require role-specific confirmation.")
