"""Join each original job-description output to a costed unit, an existing document or a named boundary.
The joins are references only. They must never be added to the workload ledger.
"""
# One or more planning units may occur within a source row. Counts always come from the work ledger.
MAP={
 'tp':'kh-nam=1,15,26 ky=2,3,7,13,14,18,19,21,22,23,31 trinh=4,6,8,9,16,17,24,25 uy-quyen=5 bc-thang=10,20,30 kpi=11,12 gb-tct=27 giao-ban=28 gb-tgd=29',
 'cvt':'baocao=1,16 tai-nd=2,18 @DM-8=3 huan-luyen=4,23,25 @DM-10=5 mau=6,20 suco=7,8,14,21,22,24,26 gt=9,10,11,12,13,17 bv=15 baocao=19',
 'cvt-2':'tai=1 @QC-5=2 ooh=3 kenh=4 chuyen=5 baocao=6 canh-bao=7',
 'qlth-a':'nam=1,24 ke-hoach=28 hangmuc=2,5,12,17,22,27 yeucau=3,29 nghiemthu=4,15 hopdong=6,13,14 tien-do=7,11,18,31,32,33 tongket=8,20,26 doitac=9,16,19,21,23 dn=25 ban-giao=10 hangmuc=30',
 'qlth-bc':'nam=1,21 ke-hoach=11,25 hangmuc=2,5,14,15,19,24,27 yeucau=3,26 nghiemthu=4,17 hopdong=6 tien-do=7,13,16,28,29,30 tongket=8,9,23 @B-2=10 ban-giao=12 doitac=18,20 dn=22',
 'cvtt-a':'bao=1,12,14,15,16,20 ooh=2,5,10,11,13,21 danhgia=3 suco=4,7,8,18,19,24,25 ct=6 ban-giao=9 sukien=17 kol=23 @M-6=22',
 'cvtt-bc':'bao=1 ooh=2,5,8 danhgia=3 suco=4,7,15 ct=6 kol=9,14 ban-giao=10 lich=11,12 @M-6=13',
 'bt-ac':'bai=1,24,28 dv=2,11,25,31,32 sk=3,12 kt=4,17,22,33 web=5,6,19 cc=7,15,20 phaply=8,16,29,30 @M-3=9 ban-giao=10 sua=13,18 loi=21,23 english=26,27',
 'bt-b':'bai=1,19,21 dv=2,20,24,25 sk=3 kt=4,13,17,26 web=5,6,14 cc=7,11,15 phaply=8,12,22,23 ban-giao=9 phat=10 loi=16,18',
 'tk-a':'c2=1,2,6,11,12,13 @B-1=3,7 kiem=4 ban-giao=5 @M-6=10',
 'tk-b':'c2=1,2,5,7,9,10,11 @B-2=3 kiem=4 ban-giao=6 @M-6=8',
 'tk-nt':'banve=1,5,12,13 kiem=2,4,10 @M-6=3,8 thu=6 @DM-3=7 @SO-5=9 ban-giao=11',
 'md-ac':'v2t=1,11,12 v4=2,10 ghi=3,8,9 kho=4 ban-giao=5 pc=13',
 'md-b':'v2t=1,13,14 v4=2,12 ghi=3,8,9 kho=4,5,10,11 ban-giao=6 am=7 pc=15',
 'qc-a':'fb=1,16,17,18,19,26,29,30,31,32 ads=2,4,5,33,34,36,37,38,39 landing=3,35 suco=6,8,10,11,12,13,14,15,20,21,22,27,28 dia-chi=7,23 ban-giao=9',
 'qc-b':'fb=1,14,21,24,25,26,27 ads=2,4,5,28,29,31,32,33,34 landing=3,30 suco=6,8,10,11,12,15,16,17,22,23 dia-chi=7,18 tin=9 ban-giao=13',
 'dl-1':'tuan=1,21 chot=2,6,9,16,18,20 bc=3,12,13 hm=4,14,17,19 kpi=5 phan-tich=7,15 kt=8 ban-giao=10',
 'dl-2':'ds=1,2,7,21 anh-khach=3,15 chatluong=4 thi-truong=5,6,18,19,20,22 sai=8,12,13,14,16,17 @YC-CRM=9 @QĐ-AI-MKT=10 ban-giao=11',
 'qlsps':'kenh=1,10,12 yeucau=2,4,8,14 uat=3 seo=5,6,15 ben-thu-ba=11 @YC-WEB=7 @YC-CRM=9 ban-giao=13',
 'qlml':'vung=1 baocao=2',
 'tn-a':'ke-hoach=1,9 tin=2,15 thaydoi=3,14,16,20 nt-le=4 danh-gia=5,23 sk=6,11,19,21 ban-giao=7 nhucau=8,10,12,13,18 hop=22',
 'tn-b':'ke-hoach=1 tin=2,11 thaydoi=3,10,12,17 nt-le=4 danh-gia=5,20 haucan=6,16 ban-giao=7 phat=8,9 dongy=13 congdong=14,15,18 hop=19',
 'mdcs-a':'anh=1 ban-giao=3 sukien=4,5', 'mdcs-b':'anh=1 ban-giao=3 sukien=4,5',
 'qhcs':'haucan=1,5 dongy=2 congdong=3,4,7,8 ban-giao=6',
 'dmpk':'anh=1 yc=2 ban-giao=3 capnhat=4',
}
BOUNDARY={
 ('bt-ac',14):('cvtt-a/bao','Truyền thông chủ trì thông cáo; Biên tập chỉ làm khi được giao thay, chuyển cùng mã việc.'),
 ('tk-a',8):('bt-ac/phat','Kịch bản MC thuộc Biên tập. Thiết kế chỉ nhận phần file hình nếu có yêu cầu.'),('tk-a',9):('cvtt-a/bao','Bài báo do Truyền thông chủ trì. Không cộng công viết cho Thiết kế.'),
 ('tk-nt',14):('tk-nt/banve','Chỉ nhận phần file ngoại tuyến được phân công, loại phần viết/dựng thuộc chuyên môn khác.'),('tk-nt',15):('tk-a/c2','Mẫu quảng cáo số thuộc Thiết kế theo nhóm. Ngoại tuyến chỉ nhận quy cách in/biển thuộc phạm vi.'),
 ('md-ac',6):('bt-ac/phat','Kịch bản lời/MC thuộc Biên tập. Media nhận bản phân cảnh/kỹ thuật riêng.'),('md-ac',7):('cvtt-a/bao','Bài báo thuộc Truyền thông. Media bàn giao tư liệu, không cộng công viết bài.'),
 ('qc-a',24):('qc-a/fb','Phần xuất bản trên kênh được giao thuộc gói vận hành nền tảng.'),('qc-a',25):('bt-ac/kt','Theo dõi nội dung chuyên môn thuộc Biên tập. Kênh số chỉ thực hiện thao tác phát/dừng.'),('qc-b',19):('qc-b/fb','Phần xuất bản trên kênh được giao thuộc gói vận hành nền tảng.'),('qc-b',20):('bt-b/kt','Kiểm nội dung do Biên tập đúng nhóm, tách thao tác vận hành kênh.'),
 ('dl-1',11):('dl-2','Xem toàn bộ nghiệp vụ dữ liệu. Tổng hợp gộp quỹ giờ vào người giữ hai chức danh.'),('dl-1',22):('tp/giao-ban','Sổ giao ban do người được chỉ định làm thư ký ghi. Chưa có phân công cá nhân, chưa cộng thêm giờ chuyên trách cho đo lường.'),
 ('qlsps',16):('qlsps/uat','Quản lý sản phẩm số kiểm giao diện trang ngôn ngữ; bản dịch do Biên tập theo nhóm bàn giao.'),('qlml',3):('qlml','Tuyến vùng chưa được kích hoạt, không cộng giờ thay thế trước bàn giao.'),
 ('tn-a',17):('qhcs/dongy','Trưởng nhóm kiểm điều kiện trước bàn giao. Chuyên viên Truyền thông thu và lưu một bộ giấy đồng ý.'),
 ('mdcs-a',2):('qhcs/bien','Kiểm tra biển thuộc Truyền thông. Media chỉ hạch toán bộ ảnh độc lập nếu Trưởng nhóm giao.'),('mdcs-b',2):('tn-b/bien','Trưởng nhóm kiêm truyền thông giữ phiếu biển; Media chỉ ghi phần ảnh độc lập theo lệnh.'),('mdcs-a',6):('qhcs/dongy','Truyền thông thu chứng từ. Media kiểm có chứng từ trước quay trong thời gian công đoạn đã tính.'),('mdcs-b',6):('tn-b/dongy','Trưởng nhóm kiêm truyền thông giữ chứng từ. Media kiểm điều kiện trước ghi hình.'),
}
def reconcile(jd,work,documents,roles):
    workids={w['id'] for w in work}; codes={d['code'] for d in documents};out={}
    for role,source in jd.items():
        target={}
        for clause in MAP[role].split():
            code,indices=clause.split('=');key=code if code.startswith('@') else role+'/'+code
            assert (key[1:] in codes if code.startswith('@') else key in workids),(role,key)
            for i in indices.split(','):target[int(i)]=[key,'Dòng liên quan để kiểm tra; chưa xác nhận đã bao phủ đủ mọi công đoạn và giờ của dòng MTCV.']
        for (rid,i),(key,note) in BOUNDARY.items():
            if rid==role:target[i]=[key,note]
        assert set(target)==set(range(1,len(source))),(role,'missing',set(range(1,len(source)))-set(target),'extra',set(target)-set(range(1,len(source))))
        out[role]=[target[i] for i in range(1,len(source))]
    return out
