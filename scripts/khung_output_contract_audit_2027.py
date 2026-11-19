#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đối soát THỰC TẾ từng đầu ra của 60 quy trình.

Một bước có thể có nhiều sản phẩm/vị trí. Tách hợp đồng đầu ra theo
vai trò thực hiện, không nhân đôi số bước quy trình. Không gán quyền
phê duyệt chính thức khi thiếu văn bản và người được phân quyền.
"""
import json,re,sys
from pathlib import Path
from collections import Counter
from html import escape

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
RX=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=RX.search(s)
assert m, "Không tìm thấy cơ sở dữ liệu"
D=json.loads(m.group(2))
R={x["id"]:x for x in D["vi_tri"]}
B={x["id"]:x["ten"] for key in ("chuc_danh","vai_tro","don_vi") for x in D[key]}
B.update({x["id"]:x["ten"] for x in D["vi_tri"]})
assert len(R)==26 and len(D["quy_trinh"])==60
assert sum(len(q["buoc"]) for q in D["quy_trinh"])==407
ND=R["cvt"]["ten"];TT=R["cvt-2"]["ten"]
aliases=D["ma_tran_chu_tri_theo_nhom_2027"]

def key(item):return str(item).split("|",1)[0]
def owner_name(k):return B.get(k,k)
def manager(k):
    if k in ("tp","cvt","cvt-2"):
        return "Ban Tổng Giám đốc" if k=="tp" else "Trưởng phòng Marketing"
    if k=="qlml":return ND
    if k in ("tn-a","tn-b"):
        return (ND+" (trước bàn giao); Quản lý mạng lưới Marketing cơ sở theo vùng "
                "(sau bàn giao có quyết định). CHỈ MỘT tuyến có hiệu lực tại mỗi thời điểm.")
    if k in ("mdcs-a","mdcs-b","qhcs"):
        return "Trưởng nhóm Marketing bệnh viện đúng cơ sở (không đồng thời nhận lệnh trực tiếp của "+TT+")"
    if k=="dmpk":
        return "Người phụ trách phòng khám (quản lý trực tiếp); yêu cầu Marketing đi qua một mã việc về Tổng công ty"
    if k in ("qlth-bc","qlsps"):
        return TT+" (không tự báo cáo cho vai trò Tổ trưởng do chính mình kiêm nhiệm)"
    if k in ("qlth-a","cvtt-a","cvtt-bc"):
        return "Tổ trưởng Tổ Truyền thông và Thương hiệu → "+TT
    if k in ("bt-ac","bt-b","tk-a","tk-b","tk-nt","md-ac","md-b"):
        return "Tổ trưởng Tổ Nội dung và Sáng tạo → "+ND
    if k in ("qc-a","qc-b","dl-1","dl-2"):
        return "Tổ trưởng Tổ Tăng trưởng số → "+TT
    if k=="tt-nd":return ND
    if k=="tt-ts" or k=="tt-th":return TT
    if k=="mkt-tct":
        return "Mỗi vị trí báo cáo theo đúng tuyến; Trưởng phòng nhận bản tổng hợp, không là chủ mọi nhật ký"
    if k in ("mkt-coso","tn"):
        return manager("tn-a")
    if k in ("qlth","cvtt","bt","qc","md","tk"):
        return "Phải phân giải nhóm trước khi xác định người quản lý trực tiếp; không tự tạo tuyến song song"
    return "Thủ trưởng đơn vị chủ quản của "+owner_name(k)+" theo quyết định tổ chức có hiệu lực"

def classify(q,b):
    title=q["ten"].lower()
    body=b.get("noi_dung","").lower()
    if any(w in title for w in ("khủng hoảng","mạo danh","đính chính","báo chí","truyền hình","truyền thanh","thanh tra")):
        return "06/14 – Báo chí, phát ngôn hoặc xử lý sự cố"
    if any(w in title for w in ("biển bảng","màn hình","phát thanh","trang trí","nhận diện")):
        return "08 – OOH, phát thanh, màn hình, vật phẩm"
    if any(w in title for w in ("contact center","crm","kịch bản tư vấn","tư vấn")):
        return "12 – Kịch bản nghiệp vụ tư vấn"
    if any(w in title for w in ("website","app","người hành nghề","thông tin công khai")):
        return "10/11 – Nội dung và dữ liệu website/app"
    if any(w in title for w in ("trực tiếp","video","ca bệnh","người bệnh","hình ảnh trước")):
        return "03 – Ảnh, video, hình ảnh người bệnh"
    if any(w in title for w in ("quảng cáo trả phí","quảng cáo sản phẩm","lịch đăng")):
        return "05 – Quảng cáo, kênh số"
    if any(w in title for w in ("ngân sách","hạng mục","kế hoạch","khai trương")):
        return "01 – Kế hoạch, hạn mức, kết quả"
    if any(w in title for w in ("tuyển dụng","nội bộ","đào tạo")):
        return "13 – Nội dung thuộc chủ quản đơn vị"
    if any(w in title for w in ("sự kiện","hội nghị","lễ","tết")):
        return "07 – Sự kiện và hoạt động tại chỗ"
    if any(w in title for w in ("thiết kế","in ấn","mẫu")):
        return "04 – Ấn phẩm và thiết kế"
    if any(w in title for w in ("quyền","phân quyền","thay người")):
        return "15 – Quyền kênh và thay người"
    if any(w in title for w in ("điều chỉnh","dừng","hủy","tạm ngừng","sửa")):
        return "16 – Thay đổi và thu hồi"
    return "Theo loại sản phẩm, rủi ro và ma trận 16 cửa phát hành"

def approvals(q,b,role):
    cat=classify(q,b)
    if b.get("can_duyet_phat_hanh",False):
        return (
            "DUYỆT PHÁT HÀNH – bắt buộc gắn đúng MỘT cá nhân được phân quyền "
            "theo ma trận 16 loại và văn bản còn hiệu lực. "
            "Chưa có mã người duyệt hợp lệ: KHÓA PHÁT HÀNH.",cat,"CHỜ GẮN QUYỀN"
        )
    if any(term in b.get("noi_dung","").lower() for term in ("ký hợp đồng","duyệt ngân sách","duyệt kế hoạch","trình duyệt chi")):
        return (
          "QUYẾT ĐỊNH NỘI BỘ/CHI – ghi riêng MỘT cấp có thẩm quyền theo loại quyết định "
          "và hạn mức tài chính; nếu vượt phạm vi phải chuyển cấp, không song duyệt cuối.",
          cat,"CHỜ ĐỐI CHIẾU HẠN MỨC")
    return (
        "KHÔNG PHÁT SINH QUYỀN DUYỆT PHÁT HÀNH tại bước này. "
        "MỘT người nhận đầu ra xác nhận bàn giao theo luồng; sản phẩm được đăng hoặc dùng "
        "ngoài phạm vi nội bộ chỉ sau cửa duyệt phát hành riêng.",
        cat,"BÀN GIAO, KHÔNG DUYỆT PHÁT HÀNH")

def load_rule(k):
    extra=""
    if k in ("qlth-bc","qlsps","bt-ac"):
        extra=" Nếu cá nhân kiêm Tổ trưởng, giờ điều phối phải tách khoản mục khỏi giờ chuyên môn."
    if k in ("cvt","cvt-2"):
        extra=" Chỉ hạch toán giờ quản trị của chính người này, không nhận giờ sản xuất của tổ."
    if k in ("tn-b","tn-a"):
        extra=" Việc Trưởng nhóm kiêm Truyền thông tại cơ sở hai người tính một lần cho đúng cá nhân."
    return (
      "Mỗi đoạn công phải lưu mã việc + mã đầu ra + mã cá nhân + vai trò thực hiện "
      "+ thời gian bắt đầu/kết thúc + loại giờ (sản xuất / quản lý / kiểm / kiêm nhiệm). "
      "Một đoạn giờ chỉ được ghi vào một người và một loại giờ, không cộng lặp cho người quản lý."
      +extra+" Chưa có giờ thực đo: để trạng thái CHƯA XÁC NHẬN, không suy ra giờ dư."
    )

output_count=0
multi=0
all_ids=set()
for q in D["quy_trinh"]:
 for step_no,b in enumerate(q["buoc"],1):
    actors=b.get("thuc_hien") or []
    assert actors
    if len(actors)>1:multi+=1
    outputs=[]
    for nth,actor in enumerate(actors,1):
        code=key(actor)
        out_id="DA-"+q["id"]+"-"+str(step_no).zfill(2)+"-"+str(nth).zfill(2)
        assert out_id not in all_ids
        all_ids.add(out_id)
        candidates=aliases.get(code)
        if candidates:
            names={g:candidates[g] for g in ("nhom_1","nhom_2")}
            name=(owner_name(names["nhom_1"])+" (Nhóm 1) / "+
                  owner_name(names["nhom_2"])+" (Nhóm 2), CHỈ CHỌN MỘT theo mã việc")
            chain=(manager(names["nhom_1"])+" [Nhóm 1] / "+
                   manager(names["nhom_2"])+" [Nhóm 2]; chọn đúng một sau phân nhóm")
        else:
            names={"co_dinh":code}
            name=owner_name(code)
            chain=manager(code)
        approval,category,status=approvals(q,b,code)
        notes=actor.split("|",1)[1].strip() if "|" in actor else ""
        evidence=b.get("ghi_nhan") or b.get("chua_co_phan_mem") or "Hồ sơ số gắn mã việc"
        records={
          "ma_dau_ra":out_id,
          "nhom_loai":category,
          "dien_giai":(notes or ("Phần công việc của "+name+" trong bước "+str(step_no)+": "+b.get("noi_dung","")[:215])),
          "chung_tu":evidence,
          "chu_tri_01":name,
          "ma_chu_tri_theo_nhom":names,
          "tuyen_quan_ly_01":chain,
          "quyen_duyet_cuoi_01":approval,
          "trang_thai_duyet":status,
          "cach_hach_toan_tai_01":load_rule(code),
          "ma_viec_duy_nhat":"Phải ghép với mã Hạng mục/Hoạt động, nhóm thương hiệu, cơ sở và cá nhân thực tế trước khi thực hiện",
          "can_xac_nhan_y_te":bool(b.get("can_nguoi_xac_nhan_chuyen_mon")),
          "ngan_sach":"Nếu phát sinh chi: duyệt chi độc lập theo ma trận tài chính, KHÔNG gộp với duyệt phát hành",
          "quy_tac_chong_trung":(
              "Không cho trùng người thực hiện và kiểm độc lập. Một đầu ra, một cá nhân chịu trách nhiệm chính; "
              "người khác chỉ là người phối hợp/kiểm/xác nhận/duyệt."
          )
        }
        outputs.append(records)
        output_count+=1
    assert len(outputs)==len(actors)
    b["doi_soat_tung_dau_ra_2027"]=outputs
    b["nguyen_tac_ban_giao_dau_ra_2027"]=(
      "Mỗi đầu ra con gắn đúng một mã cá nhân chịu trách nhiệm; mọi người cùng làm trong một bước "
      "phải chia đầu ra theo đúng vai trò, không nhận chung KPI/giờ công. "
      "Chỉ ghi tên người duyệt cuối khi có văn bản phân quyền hợp lệ."
    )

assert output_count==sum(len(b["thuc_hien"]) for q in D["quy_trinh"] for b in q["buoc"])
assert len(all_ids)==output_count and multi==121
D["kiem_toan_dau_ra_chi_tiet_2027"]={
 "tong_quy_trinh":60,
 "tong_buoc":407,
 "buoc_da_nhiem_vu":multi,
 "tong_dau_ra_tach_theo_vi_tri":output_count,
 "phan_biet":"Đây là 568 hợp đồng đầu ra mẫu, KHÔNG phải 568 sản phẩm thực đo đã hoàn thành. "
             "Các vai trò theo nhóm chỉ trở thành một chủ trì cụ thể sau khi xác định nhóm/cơ sở/mã nhân sự.",
 "phuong_phap":"Chuyển mỗi vị trí thực hiện của bước thành một bản ghi đầu ra con, "
             "gắn một chủ trì, một tuyến quản lý, một cửa quyết định cuối phù hợp và một quy tắc ghi giờ.",
 "duyet":"Không tự gán quyền phát hành hoặc chi. Chưa có văn bản ủy quyền phải CHẶN.",
 "tai":"Thực đo theo cá nhân–đầu ra–mã việc–loại giờ. Không sử dụng định mức cũ để kết luận tải hoặc nhân sự dư.",
 "ket_luan":"Kiểm thử cấu trúc không thay thế nghiệm thu giao diện, thực tế tác nghiệp và quyết định có hiệu lực."
}

m=RX.search(s)
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+s[m.end(2):]

# Lưu bản hiển thị có thể mở/thu gọn cho từng bước, không kéo vỡ chiều rộng.
needle="'+<div class=\"ops-meta\">"
# Cắm trước phần metadata (đoạn JS chính có '+<div class...'),
# sử dụng vị trí gắn duy nhất theo code hiện có.
idx=s.find("+\'<div class=\"ops-meta\">")
if idx<0:raise RuntimeError("Không tìm thấy điểm chèn giao diện đối soát đầu ra")
fragment=(
 "+(b.doi_soat_tung_dau_ra_2027?"
 "'<details class=\"ops-output-audit\" style=\"margin:9px 0;max-width:100%;overflow-wrap:anywhere\">"
 "<summary style=\"cursor:pointer;color:#0837A1;font-weight:700\">"
 "Đối soát '+b.doi_soat_tung_dau_ra_2027.length+' đầu ra: chủ trì – tuyến quản lý – duyệt – tải</summary>"
 "<div style=\"overflow-x:auto;max-width:100%\"><table class=\"t\" style=\"min-width:740px;table-layout:auto\">"
 "<thead><tr><th>Mã/đầu ra</th><th>Chịu trách nhiệm chính</th>"
 "<th>Tuyến quản lý</th><th>Phê duyệt/bàn giao</th><th>Hạch toán giờ</th></tr></thead><tbody>'"
 "+b.doi_soat_tung_dau_ra_2027.map(function(a){return"
 "'<tr><td><b>'+tx(a.ma_dau_ra)+'</b><p>'+tx(a.dien_giai)+'</p></td>"
 "<td>'+tx(a.chu_tri_01)+'</td><td>'+tx(a.tuyen_quan_ly_01)+'</td>"
 "<td>'+tx(a.quyen_duyet_cuoi_01)+'</td>"
 "<td>'+tx(a.cach_hach_toan_tai_01)+'</td></tr>'}).join('')"
 "+'</tbody></table></div></details>':'')"
)
s=s[:idx]+fragment+s[idx:]

marker='<section class="doc-sec sub" data-title="4.3. Vì sao chia ba tổ như hiện nay" id="m-4-3">'
assert marker in s
panel=(
 '<div id="tth-output-contracts-2027" style="background:#fff;padding:12px 14px;'
 'border:1px solid #d2e2f1;border-radius:8px;margin:14px 0;max-width:100%">'
 '<h4 style="color:#0837A1;margin:0 0 9px">Đối soát từng đầu ra, không tính trùng người và giờ công</h4>'
 '<p>Đã phân rã <b>407 bước</b> thành <b>'+str(output_count)+
 ' hợp đồng đầu ra mẫu</b> (121 bước có nhiều vị trí thực hiện).'
 ' Mỗi bản ghi phân biệt chủ trì, tuyến quản lý trực tiếp, thẩm quyền duyệt cuối và cách ghi giờ.'
 ' Mở từng bước trong Luồng vận hành để xem đối soát.</p>'
 '<p><b>Chặn:</b> chưa chọn nhóm/cơ sở/cá nhân hoặc thiếu quyền phê duyệt hợp lệ'
 ' thì không giao/phát hành. Đây là thiết kế vận hành chưa phải số liệu giờ thực đo'
 ' hay quyết định bổ nhiệm có hiệu lực.</p></div>'
)
if 'id="tth-output-contracts-2027"' not in s:s=s.replace(marker,panel+marker,1)

check=json.loads(RX.search(s).group(2))
assert sum(len(b["doi_soat_tung_dau_ra_2027"]) for q in check["quy_trinh"] for b in q["buoc"])==output_count
assert s.count('id="tth-output-contracts-2027"')==1
assert 'ops-output-audit' in s
p.write_text(s,"utf-8")
print("PASS OUTPUT AUDIT:",len(D["quy_trinh"]),"flows",407,"steps",output_count,"output contracts",
      multi,"multi-owner steps, zero omitted outputs")
