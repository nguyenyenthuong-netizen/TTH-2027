"""CMS, assets and authority inventory for the 2027 staffing decision.
All missing volumes are None (unknown), NEVER zero. Placeholder asset IDs are NOT verified assets.
Every time rate is a labelled scenario assumption until source worklogs confirm it.
"""
TYPES=[
 {"id":"bac-si","name":"Hồ sơ bác sĩ/người hành nghề","first":2,
  "mins":[25,55,25,18,12,12,7,12],"maint":[18,30,16,14,9,9,5,8],
  "external":"Chủ dữ liệu nhân sự/người hành nghề và chuyên môn đơn vị"},
 {"id":"chuyen-khoa","name":"Hồ sơ chuyên khoa","first":1,
  "mins":[30,85,30,22,14,14,8,12],"maint":[20,45,18,15,10,10,5,8],
  "external":"Khoa/phòng chuyên môn; Ban Giám đốc cơ sở"},
 {"id":"dich-vu","name":"Dịch vụ, kỹ thuật, gói khám","first":2,
  "mins":[35,95,35,25,16,16,8,15],"maint":[25,55,25,18,12,12,6,10],
  "external":"Khoa/phòng chuyên môn, Kế toán/giá, Pháp chế khi liên quan quảng cáo"},
 {"id":"chuong-trinh","name":"Chương trình/ưu đãi có điều kiện","first":3,
  "mins":[35,85,30,25,16,16,10,15],"maint":[25,50,22,18,12,12,8,10],
  "external":"Chủ chương trình, Ban Giám đốc cơ sở, Pháp chế và Kế toán theo thẩm quyền"},
 {"id":"co-so","name":"Thông tin cơ sở, địa điểm, giấy phép","first":1,
  "mins":[30,75,30,22,16,16,8,12],"maint":[25,50,20,16,12,12,6,10],
  "external":"Ban Giám đốc cơ sở, Hành chính/Pháp chế và chủ dữ liệu giấy phép"}
]
# minutes sequence: request/source intake, edit, CMS structure entry, independent QA,
# website view, App view, authorized publish, handover.
STAGES=["Tiếp nhận nguồn đã xác nhận","Biên tập/hiệu đính nội dung","Nhập CMS dữ liệu có cấu trúc",
 "Kiểm độc lập đối chiếu nguồn","Kiểm hiển thị website","Kiểm hiển thị App",
 "Công bố sau đủ cửa duyệt","Bàn giao và hướng dẫn cập nhật"]
# Planned new brands/sites are explicitly conditional; do not activate merely on a forecast date.
UNITS=[
 {"id":"vinh","name":"Bệnh viện Đa khoa TTH Vinh","group":"g1","site":"vinh","state":"dang-hoat-dong","intake":"tn-a@vinh"},
 {"id":"hatinh","name":"Bệnh viện Đa khoa TTH Hà Tĩnh","group":"g1","site":"hatinh","state":"dang-hoat-dong","intake":"tn-a@hatinh"},
 {"id":"quangbinh","name":"Bệnh viện Đa khoa TTH Quảng Bình","group":"g1","site":"quangbinh","state":"dang-hoat-dong","intake":"tn-a@quangbinh"},
 {"id":"nguyenphuc","name":"Bệnh viện Y học cổ truyền Nguyên Phúc","group":"g2","site":"nguyenphuc","state":"dang-hoat-dong","intake":"tn-b@nguyenphuc"},
 {"id":"thaithuonghoang","name":"Bệnh viện Răng hàm mặt và Phẫu thuật tạo hình thẩm mỹ Thái Thượng Hoàng","group":"g2","site":"thaithuonghoang","state":"dang-hoat-dong","intake":"tn-b@thaithuonghoang"},
 {"id":"khetre","name":"TTH Clinic Khe Tre","group":"g1","site":"clinic","state":"can-xac-minh-moc","intake":"dmpk@clinic"},
 {"id":"aluoi","name":"TTH Clinic A Lưới","group":"g1","site":"clinic","state":"can-xac-minh-moc","intake":"dmpk@clinic"},
 {"id":"winmed","name":"Winmed","group":"g2","site":None,"state":"can-xac-minh-moc","intake":"nguon-doi-tac"},
 {"id":"tueducthien","name":"Tuệ Đức Thiện","group":"g2","site":None,"state":"can-xac-minh-moc","intake":"nguon-doi-tac"},
 {"id":"nguyenchau","name":"Nguyên Châu – dự kiến","group":"g2","site":None,"state":"chua-kich-hoat","intake":"nguon-doi-tac"},
 {"id":"nguyenthao","name":"Nguyên Thảo – dự kiến","group":"g2","site":None,"state":"chua-kich-hoat","intake":"nguon-doi-tac"},
 {"id":"nguyentri","name":"Nguyên Trí – dự kiến","group":"g2","site":None,"state":"chua-kich-hoat","intake":"nguon-doi-tac"},
 {"id":"hue","name":"Bệnh viện Quốc tế TTH Huế – dự kiến","group":"g1","site":None,"state":"chua-kich-hoat","intake":"nguon-doi-tac"},
 {"id":"ductho","name":"Bệnh viện TTH Đức Thọ – dự kiến","group":"g1","site":None,"state":"chua-kich-hoat","intake":"nguon-doi-tac"}
]
# Source channel ledger has 20 group 1 and 10 group 2 rows by platform; the names
# below are placeholder inventory positions, NOT claim the channel exists.
CHANNEL_BANDS=[
 ("g1","Facebook",6,"qc-a"),
 ("g1","TikTok",4,"qc-a"),
 ("g1","Zalo/YouTube/LinkedIn/Threads – loại đang chờ đối chiếu",10,"qc-a"),
 ("g2","Facebook",4,"qc-b"),
 ("g2","TikTok",2,"qc-b"),
 ("g2","Zalo/YouTube/LinkedIn/Threads – loại đang chờ đối chiếu",4,"qc-b")
]
def inventory():
    assets=[]
    for group,kind,count,role in CHANNEL_BANDS:
        for n in range(1,count+1):
            assets.append(dict(id=f"K-KK-{group.upper()}-{role.upper()}-{len(assets)+1:02d}",
                name=f"Vị trí kiểm kê {kind} {n:02d} (chưa đối chiếu URL)",
                kind="Kênh số",group=group,unit="Chờ định danh",owner="Chờ xác minh pháp nhân sở hữu",
                keeper=role,status="Chưa xác minh",date=None,shared="Chưa xác minh",
                output="Lịch nội dung; quyền kênh; theo dõi; báo cáo; phục hồi khi sự cố",
                counted_by=role+"/fb, /tik hoặc /khac theo đúng loại kênh; không cộng lặp giờ"))
    for group in ["g1","g2"]:
        for kind,keeper,output in [
          ("Website / CMS","qlsps","Bản ghi dịch vụ, bác sĩ, chuyên khoa, cơ sở; lịch cập nhật và kiểm hiển thị"),
          ("App / CMS","qlsps","Bản ghi thông tin có cấu trúc; kiểm hành trình và hiển thị App"),
          ("CRM / Contact Center / HIS","qlsps","Yêu cầu nghiệp vụ, kiểm liên kết mã và bàn giao; kỹ thuật ngoài Marketing"),
          ("Phần mềm Quản trị Marketing","qlsps","Danh mục hệ thống, luồng, quyền và ca thử; kỹ thuật ngoài Marketing"),
          ("Tên miền / chứng chỉ bảo mật","qlsps","Danh mục bàn giao; triển khai kỹ thuật và gia hạn ngoài Marketing"),
          ("Trang đích / biểu mẫu số","qc-a" if group=="g1" else "qc-b","Kiểm liên kết, chiến dịch, dữ liệu nguồn và mẫu được duyệt"),
          ("Kho ảnh/video/bản quyền","md-ac" if group=="g1" else "md-b","Kiểm quyền, biên mục, phân quyền và phiên bản")]:
            assets.append(dict(id=f"TS-{group.upper()}-{len(assets)+1:03d}",name=f"{kind} · Nhóm {group[1]}",
              kind=kind,group=group,unit="Dùng chung hoặc chờ định danh theo đơn vị",owner="Chờ đối chiếu hồ sơ quản trị",
              keeper=keeper,status="Chưa kiểm kê trạng thái",date=None,shared="Cần xác nhận phạm vi dùng chung",
              output=output,counted_by="Ghi đúng mã đầu ra; chưa tính thêm giờ nếu đã nằm trong W hoặc sổ CMS"))
    for u in UNITS:
        for kind,keeper,output in [
          ("Biển bảng/OOH","cvtt-a" if u["group"]=="g1" else "cvtt-bc","Điểm vị trí, thiết kế, ảnh nghiệm thu, lịch kiểm và xử lý hỏng"),
          ("Màn hình nội viện / phát thanh","cvtt-a" if u["group"]=="g1" else "cvtt-bc","Kiểm lịch phát, tài liệu nguồn, hiển thị và báo lỗi")]:
            assets.append(dict(id=f"TS-{u['id'].upper()}-{len(assets)+1:03d}",name=kind+" · "+u["name"],
              kind=kind,group=u["group"],unit=u["id"],owner="Chờ xác minh chủ sở hữu",
              keeper=keeper,status="Chưa xác minh / theo mốc kích hoạt",date=None,shared="Theo địa điểm",
              output=output,counted_by="Đối chiếu QT.13, QT.29 và tải tại cơ sở; không cộng một lượt kiểm hai lần"))
    return assets
def build_cms():
    return dict(types=TYPES,stages=STAGES,units=UNITS,assets=inventory(),
        source="Đầu vào CMS chưa có hồ sơ định danh, số lượng và ngày vận hành đã xác nhận.",
        billing="CMS ban đầu là việc bổ sung theo giai đoạn; CMS duy trì chỉ ghi phần thay đổi vượt khối lượng W biên tập web/SEO đã mô phỏng cho đến khi đối soát tránh trùng.",
        rates="Phút/công đoạn là GIẢ ĐỊNH tính tải; chưa phải định mức ban hành.",
        approval="Chủ dữ liệu chuyên môn/giấy phép/giá xác nhận nguồn; Quản lý thương hiệu kiểm độc lập; Quản lý sản phẩm số công bố sau đủ quyền. Kỹ thuật do Phòng Số hóa/Phòng Công nghệ.")
