#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chốt ranh giới hai CVT, loại bỏ lỗi tên và ngăn trùng trách nhiệm ở MTCV.

pre: chạy sau ghép HTML, trước kiểm thử sâu.
post: chạy sau chuẩn hóa CNNV, trước công bố Pages.
Mã cvt/cvt-2 là khóa kỹ thuật; không dùng làm chức danh hiển thị.
"""
import json
import re
import sys
from pathlib import Path

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
mode=sys.argv[2] if len(sys.argv)>2 else "post"
file=root/"khung-marketing"/"index.html"
src=file.read_text("utf-8")
RX=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
ND="Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở"
TT="Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số"
BAD=ND+"2"

def get_data():
    m=RX.search(src)
    if not m: raise RuntimeError("Không tìm thấy CSDL khung")
    return json.loads(m.group(2))

def put_data(d):
    global src
    m=RX.search(src)
    if not m: raise RuntimeError("Mất CSDL khung")
    raw=json.dumps(d,ensure_ascii=False,separators=(",",":")).replace("</script>","<\\/script>")
    src=src[:m.start(2)]+raw+src[m.end(2):]

def check_shape(d):
    assert len(d["vi_tri"])==26 and len(d["quy_trinh"])==60
    assert len(d["danh_muc_van_ban"])==83
    assert sum(len(q["buoc"]) for q in d["quy_trinh"])==407
    v={x["id"]:x for x in d["vi_tri"]}
    assert v["cvt"]["ten"]==ND and v["cvt-2"]["ten"]==TT
    return v

# Lỗi nối "CVT 12" thành "tên CVT + 2" phải sửa trước mọi kiểm thử khác.
src=src.replace(
    "Giới hạn "+BAD+"; Quản lý vùng 15 người trực tiếp.",
    "Giới hạn quản lý trực tiếp của "+ND+": tối đa 12 Trưởng nhóm; "
    "Quản lý mạng lưới theo vùng: tối đa 15 Trưởng nhóm trong danh sách đã bàn giao."
)
src=src.replace(
    "Trần "+BAD+" người, Quản lý mạng lưới vùng 15 người;",
    "Trần quản lý trực tiếp của "+ND+" là 12 người; "
    "Quản lý mạng lưới theo vùng tối đa 15 người;"
)
assert BAD not in src, "Còn lỗi tên chức danh bị nối số 2"

if mode=="pre":
    d=get_data()
    v=check_shape(d)

    # Chỉ có một tuyến quản lý dọc trực tiếp. Quản lý vùng là giai đoạn sau,
    # chỉ nhận đúng danh sách đã bàn giao bằng văn bản, không quản lý song song.
    v["cvt"]["muc_dich"]=v["cvt"]["muc_dich"].replace(
        "Quản lý trực tiếp các Trưởng nhóm Marketing bệnh viện thuộc cả Nhóm 1 và Nhóm 2;",
        "Quản lý trực tiếp các Trưởng nhóm Marketing bệnh viện thuộc cả Nhóm 1 và Nhóm 2 "
        "chưa được bàn giao hợp lệ cho Quản lý mạng lưới theo vùng;"
    )
    v["cvt"]["phan_dinh_chu_tri_dau_ra"]=v["cvt"]["phan_dinh_chu_tri_dau_ra"].replace(
        "Quản lý trực tiếp toàn bộ Trưởng nhóm Marketing bệnh viện (bao gồm Trưởng nhóm Nhóm 2 kiêm Truyền thông);",
        "Quản lý trực tiếp các Trưởng nhóm Marketing bệnh viện chưa có quyết định bàn giao "
        "sang Quản lý mạng lưới theo vùng (bao gồm Trưởng nhóm Nhóm 2 kiêm Truyền thông); "
        "sau bàn giao quản lý qua Quản lý mạng lưới, không đánh giá trực tiếp trùng cùng một người;"
    )
    v["cvt"]["phan_dinh_chu_tri_dau_ra"]=v["cvt"]["phan_dinh_chu_tri_dau_ra"].replace(
        "đánh giá KPI Trưởng nhóm theo dữ liệu có xác nhận của cơ sở;",
        "đánh giá KPI Trưởng nhóm còn thuộc tuyến trực tiếp theo dữ liệu đã xác nhận; "
        "Trưởng nhóm đã bàn giao được Quản lý mạng lưới đánh giá cấp 1, "
        "Chuyên viên trưởng kiểm tra và tổng hợp theo tuyến;"
    )
    v["cvt-2"]["muc_dich"]=v["cvt-2"]["muc_dich"].replace(
        "ban hành/hướng dẫn tiêu chuẩn",
        "chủ trì soạn, kiểm chuẩn, hướng dẫn áp dụng và trình cấp có thẩm quyền ban hành tiêu chuẩn"
    )
    v["qlml"]["phan_dinh_ban_giao_dau_vao"]=(
        "Chỉ nhận danh sách cơ sở, Trưởng nhóm, chỉ tiêu và kỳ đánh giá theo quyết định phân vùng "
        "có hiệu lực; báo cáo lên "+ND+". Không có bàn giao thì không phát sinh tuyến quản lý."
    )
    v["qlml"]["thay_chinh"]=(
        "cvt|Chỉ điều phối tạm thời khi có quyết định phân công, còn giới hạn số người "
        "đánh giá trực tiếp; không tự động thu hồi toàn bộ tuyến vùng."
    )
    v["qlml"]["muc_dich"]=(
        "Quản lý trực tiếp Trưởng nhóm Marketing cơ sở trong danh sách nhóm/vùng đã được cấp "
        "có thẩm quyền phê duyệt và bàn giao; chịu quản lý chuyên môn, báo cáo về "+ND+
        ". Một Trưởng nhóm chỉ có một người đánh giá trực tiếp tại một thời điểm."
    )

    # Đường hỗ trợ dự phòng phải theo đúng chuyên môn tổ. Đây không phải
    # quyền phê duyệt/hành chính hoặc thay người khi thiếu văn bản phân công.
    for rid in ("qlth-a","qlth-bc","cvtt-a","cvtt-bc"):
        v[rid]["du_phong"]=[
            "cvt-2|Chỉ phối hợp hoặc nhận thay nghiệp vụ theo văn bản phân công còn hiệu lực; "
            "không tự động được duyệt phát hành, chi phí hay ký hợp đồng"
        ]
    v["dl-1"]["du_phong"]=[
        z.replace("do Chuyên viên trưởng kiểm","do "+TT+" kiểm độc lập")
        for z in v["dl-1"]["du_phong"]
    ]
    for rid in ("cvtt-a","cvtt-bc"):
        for key in ("viec_chung","muc_dich"):
            if key in v[rid]:
                v[rid][key]=v[rid][key].replace(
                    "Chuyên viên trưởng tổng hợp",TT+" tổng hợp"
                ).replace("Chuyên viên trưởng giữ",TT+" quản trị phiên bản")
    v["tp"]["phan_dinh_ban_giao_dau_vao"]=(
        "Nhận báo cáo quản trị nội dung và Marketing cơ sở từ "+ND+
        "; báo cáo quản trị truyền thông, thương hiệu và tăng trưởng số từ "+TT+
        "; nhận dữ liệu kết quả từ Quản lý thương hiệu và Đo lường. "
        "Quyền ký, duyệt chỉ theo ma trận thẩm quyền còn hiệu lực."
    )

    # Phân biệt quy mô cơ sở 2 người và 3 người: khi chỉ có 2 người
    # Trưởng nhóm kiêm truyền thông, không giao lặp cho Media.
    v["tn-a"]["muc_dich"]=v["tn-a"]["muc_dich"].replace(
        "quản lý trực tiếp 02 thành viên Marketing tại cơ sở.",
        "quản lý trực tiếp nhân sự Marketing theo định biên được phê duyệt; "
        "cơ sở đủ 03 người có 01 Trưởng nhóm, 01 Media, 01 Truyền thông; "
        "cơ sở 02 người có 01 Trưởng nhóm kiêm Truyền thông và 01 Media."
    )
    for rid in ("tn-a","tn-b"):
        v[rid]["phan_dinh_kiem_duyet"]=v[rid]["phan_dinh_kiem_duyet"].replace(
            "theo phân cấp "+ND, "theo phân cấp. "+ND
        ).replace("nghiệm thu sản phẩm/lịch "+ND,
                  "nghiệm thu sản phẩm/lịch theo phạm vi. "+ND)
    v["cvt"]["quy_tac_phan_vung_2027"]=(
        "Tuyến quản lý trực tiếp Trưởng nhóm chỉ thuộc một trong hai người: "
        "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở (trước bàn giao) "
        "hoặc Quản lý mạng lưới Marketing cơ sở theo vùng (sau bàn giao, trong danh sách "
        "có quyết định). Tuyến chuyên môn Truyền thông – Thương hiệu và Tăng trưởng số "
        "chỉ kiểm chuẩn, không tạo người đánh giá thứ hai."
    )
    put_data(d)

elif mode=="post":
    # Bước CNNV chạy sau kiểm tra tên, vì vậy phải khóa tên thêm lần cuối,
    # cả phần nội dung JSON mới phát sinh lẫn bảng HTML tĩnh.
    src=src.replace(
        "không gán cho Chuyên viên trưởng theo chức danh",
        "không mặc nhiên giao thẩm quyền cho "+ND+" hoặc "+TT
    )
    src=src.replace(
        "hai chức danh Chuyên viên trưởng",
        ND+" và "+TT
    )
    d=get_data()
    v=check_shape(d)
    # CNNV thêm mới các trường sau bước chuẩn hóa tên; đổi đúng theo
    # từng tuyến thay vì phép thay toàn cục có thể cấp nhầm quyền.
    for node in (
        v["bt-ac"],
        v["bt-ac"].get("cnnv_2027",{}),
    ):
        for key in ("phan_dinh_ban_giao_dau_vao","dau_vao_va_ban_giao"):
            if isinstance(node.get(key),str):
                node[key]=node[key].replace("Chuyên viên trưởng",ND)
    for x in d.get("cnnv_kiem_soat_nghiep_vu_2027",[]):
        if isinstance(x.get("phe_duyet"),str):
            x["phe_duyet"]=x["phe_duyet"].replace(
                "không duyệt mặc nhiên bởi Chuyên viên trưởng",
                "không mặc nhiên giao quyền phê duyệt cho "+ND+" hoặc "+TT
            )
    ng=d.get("cnnv_nguyen_tac_2027",{})
    for key in ("to_truong_noi_dung","ba_tang_tai","kpi"):
        if isinstance(ng.get(key),str):
            if key=="to_truong_noi_dung":
                ng[key]=ng[key].replace("Chuyên viên trưởng",ND)
            else:
                ng[key]=ng[key].replace(
                    "Chuyên viên trưởng",ND+" và "+TT
                )
    put_data(d)
    # CNNV đã dựng thêm bảng HTML tĩnh từ dữ liệu trước chuẩn hóa.
    # Đồng bộ đúng các đoạn HTML mới với CSDL, không sửa JS hoặc ID.
    src=src.replace(
        "không duyệt mặc nhiên bởi Chuyên viên trưởng",
        "không mặc nhiên giao quyền phê duyệt cho "+ND+" hoặc "+TT
    )
    pat=re.compile(
        r'(<div class="cnnv-vt" id="cnnv-vt-bt-ac"[\s\S]*?</div>)',
        re.I
    )
    src=pat.sub(lambda m: re.sub(
        r'Chuyên viên trưởng(?!\s+(?:Nội dung|Truyền thông))',
        ND,m.group(0),flags=re.I),src)
    d=get_data()
    v=check_shape(d)
    assert BAD not in src
    # Tránh tái nhập mã/nhãn chung qua CNNV hoặc các bước dựng cuối.
    bad=re.compile(r'Chuyên viên trưởng(?!\s+(?:Nội dung|Truyền thông))',re.I)
    unresolved=[]
    def walk(obj,path="CSDL"):
        if isinstance(obj,str):
            if bad.search(obj): unresolved.append((path,obj[:150]))
        elif isinstance(obj,list):
            for i,z in enumerate(obj): walk(z,path+"["+str(i)+"]")
        elif isinstance(obj,dict):
            for k,z in obj.items(): walk(z,path+"."+k)
    walk(d)
    assert not unresolved, "Còn Chuyên viên trưởng không định danh: "+repr(unresolved[:8])
    assert all(z.split("|")[0]=="cvt-2" for rid in
               ("qlth-a","qlth-bc","cvtt-a","cvtt-bc")
               for z in v[rid]["du_phong"])
    assert "chưa được bàn giao" in v["cvt"]["muc_dich"]
    assert "Một Trưởng nhóm chỉ có một" in v["qlml"]["muc_dich"]
    assert "03 người" in v["tn-a"]["muc_dich"]
    assert "Trưởng phòng/cấp có thẩm quyền" in v["qlml"]["phan_dinh_kiem_duyet"]
    assert "Không viết kịch bản lời" in v["mdcs-a"]["phan_dinh_khong_thuoc_trach_nhiem"] or "không viết kịch bản lời" in v["mdcs-a"]["phan_dinh_khong_thuoc_trach_nhiem"]
    assert "màn hình" in v["qhcs"]["muc_dich"] and "phát thanh" in v["qhcs"]["muc_dich"]
    static=re.sub(r'<(?:script|style)\b[^>]*>[\s\S]*?</(?:script|style)>',' ',src,flags=re.I)
    static=re.sub(r'<[^>]+>',' ',static)
    assert not bad.search(static),"HTML tĩnh còn CVT chung: "+repr([static[max(0,m.start()-55):m.end()+75] for m in list(bad.finditer(static))[:6]])
    assert not re.search(r'\bCVT\s*[12]\b|Chuyên viên trưởng\s+(?:[12]|thứ nhất|thứ hai)\b',
                         static,re.I),"Còn chức danh đánh số"
    print("PASS CVT POSTBUILD: 26 chức danh, 60 quy trình, 407 bước, 83 văn bản; "
          "tên đầy đủ; 1 tuyến quản lý; dự phòng đúng tổ; phân quyền độc lập.")
else:
    raise SystemExit("mode phải là pre hoặc post")

file.write_text(src,"utf-8")
