#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chốt tên đầy đủ hai chức danh và chống giao việc trùng với chuyên viên/tổ trưởng.

Chạy sau toàn bộ bước dựng nguồn và CSS; KHÔNG đổi mã kỹ thuật cvt/cvt-2,
không tự cấp quyền phát hành, tài chính hoặc duyệt nhân sự.
"""
from pathlib import Path
from html import escape
import json,re,sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
html=p.read_text("utf-8")
m=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',html)
if m is None: raise ValueError("Mất cơ sở dữ liệu nhúng")
D=json.loads(m.group(2))
R={r["id"]:r for r in D["vi_tri"]}
NOI_DUNG=R["cvt"]["ten"]
TRUYEN_THONG=R["cvt-2"]["ten"]
assert NOI_DUNG=="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
assert TRUYEN_THONG=="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
assert len(R)==26 and len(D["quy_trinh"])==60 and len(D["danh_muc_van_ban"])==83

# Chỉ thay câu chữ hiển thị. Không thay các mã định danh, tên trường, khóa liên kết.
def fix_label(s):
    if not isinstance(s,str):return s
    replaces=[
      (r'\bCVT\s*1\s*/\s*2\b', 'hai chức danh Chuyên viên trưởng'),
      (r'\bChuyên viên trưởng\s*(?:1|2)\s*/\s*(?:1|2)\b', 'hai chức danh Chuyên viên trưởng'),
      (r'\bChuyên viên trưởng\s+thứ\s+hai\b', TRUYEN_THONG),
      (r'\bChuyên viên trưởng\s+thứ\s+nhất\b', NOI_DUNG),
      (r'\bChuyên viên trưởng\s+(?:số\s*)?2\b', TRUYEN_THONG),
      (r'\bChuyên viên trưởng\s+(?:số\s*)?1\b', NOI_DUNG),
      (r'\bCVT\s*[-.]?\s*2\b',TRUYEN_THONG),
      (r'\bCVT\s*[-.]?\s*1\b',NOI_DUNG),
      (r'\bChuyên viên trưởng Nội dung\s*[–-]\s*Cơ sở\b',NOI_DUNG),
      (r'\bCVT Nội dung\s*[–-]\s*Cơ sở\b',NOI_DUNG),
      (r'\bCVT Truyền thông\s*[–-]\s*Số\b',TRUYEN_THONG),
      (r'\bChuyên viên trưởng Truyền thông\s*[–-]\s*Số\b',TRUYEN_THONG),
      (r'\bCVT Nội dung\s*[–-]\s*Sáng tạo\b',NOI_DUNG),
    ]
    for pat,new in replaces:
        flags=0 if pat.startswith(r'\bCVT') else re.I
        s=re.sub(pat,lambda _m:new,s,flags=flags)
    return s

# Chỉ tác động chuỗi văn bản, KHÔNG thay các khóa "CVT1"/"CVT2" trong dữ liệu
# nguồn đã dùng làm liên kết; hiển thị toàn bộ bằng tên vị trí đầy đủ.
def walk(node):
    if isinstance(node,str):
        if node in ("cvt","cvt-2","cvt2"):return node
        if node.startswith(("cvt|","cvt-2|")):return node
        return fix_label(node)
    if isinstance(node,list):return [walk(x) for x in node]
    if isinstance(node,dict):return {k:walk(v) for k,v in node.items()}
    return node
D=walk(D)

# KIỂM TOÁN 19/11: tải Tổ trưởng và tuyến báo cáo tự tham chiếu là lỗi,
# không được 'chốt đủ tải' khi chưa đo phần điều phối kiêm nhiệm.
brand2=next(x for x in D["vi_tri"] if x["id"]=="qlth-bc")
digital=next(x for x in D["vi_tri"] if x["id"]=="qlsps")
assert "88–91" in brand2["gio_ke_hoach"] and "19 giờ" in digital["gio_ke_hoach"]
brand2["gio_ke_hoach"]=(
 "≈ 88–91 giờ/tháng là tải chuyên môn Quản lý thương hiệu nhóm 2 theo phương án trước; "
 "CHƯA cộng giờ kiêm Tổ trưởng Tổ Truyền thông và Thương hiệu. "
 "Phải ghi riêng số lượt giao việc, xử lý xung đột, họp tổ, rà tiến độ và giờ thực đo; "
 "chưa được kết luận tổng tải hoặc giờ dư."
)
brand2["bao_cao_cho"]=(
 TRUYEN_THONG+" quản lý chuyên môn và kiểm soát tải cả chức danh Quản lý thương hiệu nhóm 2 "
 "lẫn vai trò kiêm Tổ trưởng Tổ Truyền thông và Thương hiệu. "
 "Không có tuyến báo cáo 'Tổ trưởng báo cáo cho chính mình'. "
 "Trong vai trò Quản lý thương hiệu, chịu trách nhiệm hạng mục nhóm 2; trong vai trò Tổ trưởng, "
 "chỉ điều phối lịch của tổ, không kiểm/duyệt độc lập sản phẩm do mình làm; "
 "Trưởng phòng xử lý xung đột vượt quyền."
)
digital["bao_cao_cho"]=(
 TRUYEN_THONG+" quản lý trực tiếp về nghiệp vụ, tiến độ và tải việc "
 "của Quản lý sản phẩm số, bao gồm phần kiêm Tổ trưởng Tổ Tăng trưởng số. "
 "Không tự đánh giá hoặc tự phê duyệt phần việc, chi phí, quyền hệ thống của mình; "
 "Trưởng phòng xử lý vượt quyền theo ma trận."
)
D["kiem_toan_tai_quan_ly_2027"]={
 "trang_thai":"CHƯA ĐỦ SỐ GIỜ ĐO THỰC TẾ; không công bố đủ tải hay dư tải của hai Chuyên viên trưởng",
 "co_so_cau_truc":"26 mã chức danh; 36 suất định biên mục tiêu (22 Tổng công ty, 14 cơ sở); 3 tổ; 2 nhóm thương hiệu. Mã chức danh không đồng nghĩa số nhân sự.",
 "tien_de_bat_buoc":[
  "Mã việc duy nhất; tổ phụ trách; người làm; người kiểm; người phê duyệt; tần suất tháng; định mức phút/lượt; chứng từ giờ thực tế",
  "Giờ người thực hiện và giờ Tổ trưởng kiêm nhiệm không cộng vào giờ Chuyên viên trưởng; phần họp/phối hợp chỉ ghi một lần cho một người",
  "Với cơ sở: phân biệt số bệnh viện, số Trưởng nhóm trực thuộc, số nhân viên cơ sở, loại bệnh viện và số yêu cầu phát sinh",
  "Số buổi kiểm chuẩn thực tế và số lỗi tái diễn; tách báo cáo định kỳ với xử lý sự cố",
  "Chưa đủ giờ đo thì chỉ ghi tải dự kiến/nguồn giả định và cảnh báo, không khẳng định định biên 36 là đủ nhân sự thực tế"
 ],
 "cong_thuc":"Tổng giờ quản trị/tháng = tổng theo nhóm việc (số lượt thực tế × số phút quản trị chuẩn/lượt ÷ 60) + thời gian quản trị định kỳ duy nhất + thời gian đào tạo, xử lý phát sinh thực đo - phần giờ đã ghi trùng. Không lấy giờ sản xuất của tổ làm giờ quản trị.",
 "tuyen_noi_dung":{
  "chuc_danh":NOI_DUNG,
  "danh_muc":"Điều phối tải Tổ Nội dung và Sáng tạo; quản lý Trưởng nhóm bệnh viện hai nhóm; họp/đánh giá; kiểm soát chất lượng sản xuất; rủi ro; phát sinh liên cơ sở",
  "khong_duoc_tinh":"Giờ Biên tập/Thiết kế/Media trực tiếp sản xuất; giờ Tổ trưởng nhóm 1 phân công đã hạch toán"},
 "tuyen_truyen_thong":{
  "chuc_danh":TRUYEN_THONG,
  "danh_muc":"Quản lý 2 tổ Truyền thông và Thương hiệu, Tăng trưởng số; kiểm chuẩn truyền thông/cơ sở; rủi ro PR/OOH/kênh số; đào tạo; đánh giá chất lượng vận hành",
  "khong_duoc_tinh":"Giờ PR, quản trị quảng cáo, sản phẩm số và giờ 2 Tổ trưởng điều phối đã hạch toán"},
 "bat_cap_cu_the":[
  "Quản lý thương hiệu nhóm 2 kiêm Tổ trưởng nhưng trường 88–91 giờ trước đây ghi rõ 'không kiêm Tổ trưởng'; hiện đã đánh dấu thiếu tải kiêm nhiệm",
  "Quản lý thương hiệu nhóm 2 và Quản lý sản phẩm số kiêm Tổ trưởng không được ghi cấp trên là chính Tổ trưởng do mình đảm nhiệm",
  "Tổ trưởng Tổ Nội dung và Sáng tạo đang điều phối chủ yếu nhóm 1, nhóm 2/ngoại tuyến bị đẩy lên Chuyên viên trưởng làm điều phối hằng ngày: cần chốt văn bản giao phạm vi điều phối và người dự phòng, không tự thêm suất định biên"
 ]
}

# Ánh xạ tên người quản lý trong trường diễn giải, không đánh số chức danh.
legacy=D.get("phan_dinh_quan_ly_hai_cvt_19112026",{}).get("tuyen",{})
if "CVT1" in legacy and "CVT2" in legacy:
    D["phan_dinh_quan_ly_hai_cvt_19112026"]["tuyen_hien_thi"]=[
        {"ten_chuc_danh":NOI_DUNG,"pham_vi":legacy["CVT1"]},
        {"ten_chuc_danh":TRUYEN_THONG,"pham_vi":legacy["CVT2"]},
    ]
D["ranh_gioi_khong_trung_viec_2027"]={
 "ten_chuc_danh":[NOI_DUNG,TRUYEN_THONG],
 "quan_ly_va_thuc_hien":"Chuyên viên trưởng chịu trách nhiệm quản lý mục tiêu, chuẩn, tải việc và kiểm soát theo tuyến; Tổ trưởng điều phối việc hằng ngày; chuyên viên trực tiếp tạo ra sản phẩm. Không nhân đôi đầu ra hoặc điểm KPI.",
 "dau_ra_quan_ly_noi_dung":"Kế hoạch tải và điều phối nguồn lực sản xuất, bộ tiêu chuẩn Biên tập–Thiết kế–Media, biên bản xử lý xung đột và báo cáo Marketing cơ sở; không mặc định viết bài, thiết kế, quay dựng thay thành viên.",
 "dau_ra_quan_ly_truyen_thong":"Bộ chuẩn PR, OOH, phát thanh, màn hình, quảng cáo, kênh số; báo cáo rủi ro, chất lượng thực thi và hiệu quả hai tổ thuộc Tổng công ty; không mặc định sản xuất nội dung, vận hành quảng cáo hoặc tác nghiệp truyền thông thay chuyên viên.",
 "nguoi_giao_viec_co_so":"Trưởng nhóm Marketing cơ sở giao nhiệm vụ trực tiếp cho người tại bệnh viện. "+NOI_DUNG+" quản lý tuyến, duyệt điều phối trong phạm vi được giao; "+TRUYEN_THONG+" gửi yêu cầu nghiệp vụ qua đúng tuyến, không tạo lệnh thứ hai.",
 "khong_trung_voi_quan_ly_thuong_hieu":"Quản lý thương hiệu giữ mục tiêu, thông điệp và nghiệm thu hạng mục thương hiệu. Cả hai Chuyên viên trưởng không tự động thay quyền nghiệm thu của Quản lý thương hiệu.",
 "khong_trung_voi_chuyen_vien_truyen_thong":"Chuyên viên truyền thông triển khai PR, báo chí, đối tác, OOH, phát thanh/màn hình và hồ sơ hiện trường theo phân công; Chuyên viên trưởng quản lý chuẩn, rủi ro và chất lượng, không mặc định thay người thực hiện.",
 "khong_trung_voi_chuyen_vien_tang_truong_so":"Chuyên viên quảng cáo/kênh số trực tiếp vận hành, tối ưu và báo cáo chiến dịch; Chuyên viên trưởng kiểm soát tiêu chuẩn, tải và rủi ro, không ghi cùng một sản phẩm thành hai đầu ra.",
 "phan_quyen":"Phân biệt người làm, kiểm biên tập/kỹ thuật, xác nhận y khoa/pháp lý, nghiệm thu mục tiêu thương hiệu, duyệt phát hành và duyệt chi; không có quyền duyệt chỉ vì chức danh quản lý.",
 "xung_dot":"Có một đầu mối giao việc cho mỗi nhân sự; bất đồng giữa hai tuyến hoặc thay đổi ngân sách, mục tiêu, thẩm quyền phải trình Trưởng phòng/cấp được ủy quyền bằng văn bản.",
}

# Nguồn JSON được gắn lại trước khi sửa chữ hiển thị, bảo toàn script nhúng.
html=html[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")+html[m.end(2):]
# Bỏ các cách gọi đánh số ở văn bản HTML tĩnh mà không chạm dữ liệu JS/CSS/attributes.
blocks=re.split(r'(<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>)',html,flags=re.I)
for i in range(0,len(blocks),2):
    items=re.split(r'(<[^>]+>)',blocks[i])
    for j in range(0,len(items),2):
        items[j]=fix_label(items[j])
    blocks[i]="".join(items)
html="".join(blocks)

# Dùng bảng ranh giới ngay trong phần đã có, không thêm menu/đường dẫn mới.
marker='<section id="tth-cvt-deep-audit-1911"'
if marker not in html: raise ValueError("Thiếu mục đối chiếu trách nhiệm chức danh")
if 'id="tth-cvt-cross-role-boundaries-2027"' not in html:
    cases=[
      ("Quản lý chuyên môn", "Quản lý chuẩn Nội dung–Sáng tạo, tải sản xuất và Trưởng nhóm Marketing cơ sở cả hai nhóm", "Quản lý chuẩn Truyền thông–Thương hiệu, Tăng trưởng số và hai tổ tại Tổng công ty", "Tổ trưởng giao việc từng ngày; người làm chịu trách nhiệm sản phẩm"),
      ("Biên tập, Thiết kế, Media", "Điều phối năng lực, quy chuẩn kỹ thuật và xử lý xung đột lịch sản xuất", "Chỉ kiểm chuẩn nghiệp vụ thông điệp/kênh khi liên quan", "Biên tập, Thiết kế, Media trực tiếp tạo/sửa/kiểm sản phẩm trong phạm vi được giao"),
      ("PR, OOH, phát thanh, màn hình", "Bố trí năng lực sản xuất/điều phối Marketing cơ sở khi có đầu việc", "Kiểm chuẩn nghiệp vụ, rủi ro, tuân thủ và kết quả hai tổ", "Chuyên viên truyền thông thực hiện, tổ chức hiện trường, quản lý hồ sơ và báo cáo"),
      ("Quảng cáo, kênh số", "Phối hợp cung ứng nội dung, thiết kế, media theo yêu cầu đã ghi nhận", "Quản lý tiêu chuẩn vận hành, tiến độ, chất lượng và rủi ro", "Chuyên viên quảng cáo/kênh số thiết lập, tối ưu, đăng và báo cáo theo quyền"),
      ("Marketing tại bệnh viện", "Quản lý trực tiếp Trưởng nhóm, điều phối tải và chốt một lịch công việc", "Hướng dẫn nghiệp vụ thông qua tuyến quản lý, không giao lệnh trực tiếp nhân viên cơ sở", "Trưởng nhóm cơ sở giao việc, kiểm hiện trường; Ban Giám đốc cơ sở quản lý hành chính theo phân cấp"),
      ("Thông điệp và phê duyệt", "Kiểm chuẩn đầu ra sản xuất; không thay nghiệm thu thương hiệu", "Kiểm chuẩn truyền thông/kênh; không tự duyệt phát hành", "Quản lý thương hiệu nghiệm thu mục tiêu/thông điệp; cấp có thẩm quyền duyệt y khoa, pháp lý, phát hành và chi phí riêng"),
    ]
    cells="".join("<tr>"+"".join("<td>"+escape(c)+"</td>" for c in row)+"</tr>" for row in cases)
    section=('<div id="tth-cvt-cross-role-boundaries-2027" style="margin:13px 0 0">'
      '<h4 style="color:#0837A1;margin:0 0 7px;font-size:17px">Ranh giới trách nhiệm với các tổ và vị trí liên quan</h4>'
      '<p style="margin:0 0 9px">Chuyên viên trưởng chịu trách nhiệm quản lý theo tuyến; Tổ trưởng phân công tác nghiệp; chuyên viên tạo sản phẩm. Một đầu ra chỉ có một người chịu trách nhiệm chính, không nhận trùng KPI.</p>'
      '<div class="tbl" style="max-width:100%;overflow-x:auto"><table class="t wide" style="min-width:1080px;width:100%;table-layout:auto">'
      '<thead><tr><th>Đầu việc</th><th>'+escape(NOI_DUNG)+'</th><th>'+escape(TRUYEN_THONG)+'</th><th>Người trực tiếp thực hiện và cấp có thẩm quyền</th></tr></thead>'
      '<tbody>'+cells+'</tbody></table></div></div>')
    # Place immediately after heading of the existing review section, not nested inside another card/table.
    start=html.index(marker)
    offset=html.index('</p>',start)+4
    html=html[:offset]+section+html[offset:]


# Kiểm tra bổ sung: xoá hoàn toàn tên gọi Chuyên viên trưởng chung trong CSDL
# và HTML hiển thị. Không biến chức danh thành cấp có quyền duyệt mặc nhiên.
GENERIC_CVT=re.compile(r'Chuyên viên trưởng(?!\s+(?:Nội dung|Truyền thông))',re.I)
BOTH_CVT=NOI_DUNG+' và '+TRUYEN_THONG+' (phân vai theo đúng tuyến)'
AUTH_CVT='người được phân quyền theo ma trận thẩm quyền có hiệu lực'
SIGN_CVT='cấp có thẩm quyền phê duyệt theo phân cấp có hiệu lực'
STANDIN_CVT='người được Ban Tổng Giám đốc giao phụ trách bằng văn bản còn hiệu lực'
FLOW_ND=set('hang-muc yeu-cau-le tin-trong-ngay bo-nhan-dien ke-hoach-nam ho-tro-lien-co-so xung-dot-lich yeu-cau-gap ra-soat-noi-dung-y-khoa'.split())
FLOW_TT=set('kol su-kien-co-so tuyen-dung le-tet mua-truyen-thong bao-chi-bac-si noi-bo-phong-ban mao-danh phat-thanh-man-hinh dinh-chinh su-co-tai-khoan doi-tac phat-truc-tiep dich-benh-thien-tai quang-cao-san-pham quang-cao-tra-phi phap-luat nghien-cuu-thi-truong'.split())

def remove_generic(text,role=None):
    if not isinstance(text,str) or not GENERIC_CVT.search(text): return text
    text=re.sub(r'một trong hai Chuyên viên trưởng\b',
        'một trong hai chức danh ('+NOI_DUNG+' hoặc '+TRUYEN_THONG+') theo văn bản ủy quyền',text,flags=re.I)
    text=re.sub(r'Chuyên viên trưởng còn lại\b',
        'người giữ chức danh còn lại, nếu có văn bản giao quyền',text,flags=re.I)
    text=re.sub(r'(?:hai|02|2)\s+Chuyên viên trưởng\b',BOTH_CVT,text,flags=re.I)
    def sub(m):
        l=text[max(0,m.start()-125):m.start()].lower()
        r=text[m.end():m.end()+140].lower()
        a=l+' '+r
        if re.search(r'^\s*(?:duyệt|phê duyệt|ký|ban hành)\b',r):return SIGN_CVT
        if re.search(r'^\s*(?:cấp|thu hồi|quản quyền)\b',r) or ('quyền:' in l[-18:]):
            return AUTH_CVT
        if 'chưa có trưởng phòng' in l or 'trưởng phòng vắng' in l or 'phụ trách phòng' in r[:55]:
            return STANDIN_CVT
        if role in ('cvt','cvt-2'):
            return NOI_DUNG if role=='cvt' else TRUYEN_THONG
        nd=any(w in a for w in ('biên tập','thiết kế','media','tổ nội dung','trưởng nhóm',
               'marketing cơ sở','lịch sản xuất','nguồn lực sản xuất','kho tư liệu'))
        tt=any(w in a for w in ('truyền thông','quảng cáo','báo chí','kênh số',
               'phát thanh','màn hình','quan hệ công chúng','chính sách nền tảng'))
        if nd and not tt:return NOI_DUNG
        if tt and not nd:return TRUYEN_THONG
        return BOTH_CVT
    return GENERIC_CVT.sub(sub,text)

# CSDL nguồn: phân loại theo vị trí, quy trình, mã văn bản chủ trì; biểu mẫu
# người xem phải thể hiện từng tuyến, không tự cấp quyền đọc toàn hệ thống.
def resolve_generic(obj,role=None,section=''):
    if isinstance(obj,str):
        if obj in ('cvt','cvt-2','cvt2'):return obj
        if obj.startswith(('cvt|','cvt-2|')) and '|' in obj:
            id_,desc=obj.split('|',1)
            return id_+'|'+remove_generic(desc,id_)
        return remove_generic(obj,role)
    if isinstance(obj,list):
        out=[]
        for x in obj:
            r=role
            if section=='vi_tri' and isinstance(x,dict):
                r=('cvt' if x.get('to') in ('nd','coso') or x.get('id')=='qlml'
                   else 'cvt-2' if x.get('to') in ('th','ts')
                   else None)
                if x.get('id') in ('cvt','cvt-2'):r=x['id']
            elif section=='quy_trinh' and isinstance(x,dict):
                r=('cvt' if x.get('id') in FLOW_ND else
                   'cvt-2' if x.get('id') in FLOW_TT else None)
            elif section=='danh_muc_van_ban' and isinstance(x,dict):
                r=x.get('chu_tri') if x.get('chu_tri') in ('cvt','cvt-2') else None
            elif section=='mang_viec' and isinstance(x,dict):
                n=x.get('so')
                if n in (3,4,5,6,7,9,28,37):r='cvt'
                elif n in (2,10,11,12,13,14,15,19,20,23,25,26,27,39,41,42):r='cvt-2'
                else:r=None
            elif section=='buoc' and isinstance(x,dict):
                lead=str(x.get('chu_tri_chinh','')).split('|')[0]
                if lead in ('cvt','cvt-2'):r=lead
            out.append(resolve_generic(x,r,section+'[]'))
        return out
    if isinstance(obj,dict):
        return {k:resolve_generic(v,role,k) for k,v in obj.items()}
    return obj

mm=re.search(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)',html)
source=json.loads(mm.group(2))
source=resolve_generic(source)
# Mã kỹ thuật vẫn là mã kỹ thuật, KHÔNG đổi bất kỳ định danh vị trí nào.
assert {v['id'] for v in source['vi_tri']}=={v['id'] for v in D['vi_tri']}
assert len(source['quy_trinh'])==60 and len(source['danh_muc_van_ban'])==83
html=html[:mm.start(2)]+json.dumps(source,ensure_ascii=False,separators=(',',':')).replace('</script>','<\\/script>')+html[mm.end(2):]
# Thay trong TEXT NODE của HTML tĩnh, bỏ qua thuộc tính CSS/JS để không
# làm hỏng cơ chế tương tác và màu nền tiêu đề đã được duyệt.
hparts=re.split(r'(<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>)',html,flags=re.I)
for i in range(0,len(hparts),2):
    nodes=re.split(r'(<[^>]+>)',hparts[i])
    for j in range(0,len(nodes),2):
        nodes[j]=remove_generic(nodes[j])
    hparts[i]=''.join(nodes)
html=''.join(hparts)
# Các nhãn cũ được JS dựng lên khi người dùng bấm mở danh sách quy trình.
# Chỉ thay giá trị nhãn; không sửa khóa tra cứu role ID.
html=html.replace("d.chu_tri==='cvt'?'Chuyên viên trưởng'",
                  "d.chu_tri==='cvt'?'"+NOI_DUNG+"'")
html=html.replace("'ql':['tp','cvt']","'ql':['tp','cvt','cvt-2']")
html=html.replace("'ql':['Trưởng phòng, Chuyên viên trưởng và Tổ trưởng có liên quan']",
                  "'ql':['Trưởng phòng, "+NOI_DUNG+" và "+TRUYEN_THONG+"; Tổ trưởng có liên quan đúng tuyến']")
html=html.replace("'Chuyên viên trưởng':'Chức danh kiểm soát chuyên môn, phối hợp liên tổ và quản lý văn bản theo phân công;",
                  "'Chuyên viên trưởng':'"+NOI_DUNG+" và "+TRUYEN_THONG+" là hai chức danh quản lý khác nhau;")
# Chặn xuất bản khi văn bản nhập lại tiếp tục tạo vai trò chung.
verify=json.loads(re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',html).group(1))
remaining=[]
def check_generic(obj,path=''):
    if isinstance(obj,str):
        if obj not in ('cvt','cvt-2','cvt2') and GENERIC_CVT.search(obj):
            remaining.append(path)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):check_generic(v,path+'['+str(i)+']')
    elif isinstance(obj,dict):
        for k,v in obj.items():check_generic(v,path+'.'+k)
check_generic(verify)
visible=re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>',' ',html,flags=re.I)
visible=re.sub(r'<[^>]+>',' ',visible)
if GENERIC_CVT.search(visible):remaining.append('HTML tĩnh')
if remaining:raise ValueError('Còn tên chức danh chung: '+', '.join(remaining[:18]))
print('FULL-TITLE-AUDIT PASS: 26 vị trí, 60 quy trình, 83 văn bản; không còn Chuyên viên trưởng chung trong dữ liệu và HTML tĩnh')

# Cập nhật các nhãn mô tả tải/chức danh đã sinh sẵn trong sơ đồ HTML gốc.
# Bản dữ liệu động đọc D nên chỉ thay chữ tĩnh đúng mẫu, không thay thuộc tính.
html=html.replace(
 "≈ 88–91 giờ/tháng (không kiêm Tổ trưởng; chỉ nghiệm thu, không kiểm lời)",
 "≈ 88–91 giờ/tháng tải chuyên môn; CHƯA cộng tải kiêm Tổ trưởng (đo riêng trước khi kết luận tải)")
# Không để hồ sơ chức danh giữ mẫu tự tham chiếu.
assert "Không có tuyến báo cáo 'Tổ trưởng báo cáo cho chính mình'." in D["vi_tri"][4]["bao_cao_cho"]
assert "Không tự đánh giá" in D["vi_tri"][18]["bao_cao_cho"]

# Tự động từ chối nếu còn tên đánh số trong vùng chữ hiển thị hoặc CSDL dạng văn bản.
all_names=json.dumps(D,ensure_ascii=False)
# ID kỹ thuật còn được phép tồn tại: mã, khóa JSON, nhóm thương hiệu.
view=re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>',' ',html,flags=re.I)
view=re.sub(r'<[^>]+>',' ',view)
bad=re.search(r'Chuyên viên trưởng\s+(?:thứ\s+(?:nhất|hai)|(?:số\s*)?[12]\b)|\bCVT\s*[12]\b|Chuyên viên trưởng Nội dung\s*[–-]\s*Cơ sở\b',view,re.I)
if bad:raise ValueError("Còn cách gọi chức danh sai trong phần hiển thị: "+bad.group(0))
assert html.count('id="tth-cvt-cross-role-boundaries-2027"')==1
assert len(D["vi_tri"])==26 and len(D["quy_trinh"])==60
p.write_text(html,"utf-8")
print("ROLE-NAMES-BOUNDARY PASS: two exact job titles, distinct managers, 26 positions / 60 processes / 83 documents, no numbered job titles visible")
