#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tich hop phu luc CTDA 2027 vao Ke hoach 2027 va Khung Muc 05.
Dữ liệu bổ sung là đối chiếu chờ duyệt; KHÔNG cộng tải hay doanh thu lần hai.
"""
import json
import csv
import sys
from pathlib import Path

PROG = [
 ("TD27-01","Dự án","Kiến trúc, bộ nhận diện thương hiệu và thư viện chuẩn","Thương hiệu/Nền tảng","TTH Healthcare; TTH Hospital; TTH Clinic; chuyên khoa độc lập","Quản lý thương hiệu đúng nhóm","Bộ chuẩn theo thương hiệu; số bộ mẫu chuẩn; tỷ lệ tuân thủ","Q1 nền tảng → Q2 ban hành → Q3-Q4 kiểm soát","Kế thừa CTDA-2026-037"),
 ("TD27-02","Dự án","Triển khai ứng dụng nhận diện tại các điểm chạm","Thương hiệu/Triển khai","Bệnh viện, phòng khám, kênh, tài sản","Quản lý thương hiệu đúng nhóm","Tài sản được nghiệm thu; điểm chạm đạt chuẩn","Q1 kiểm kê → Q2 ưu tiên → Q3-Q4 triển khai","Dùng mẫu gốc của TD27-01"),
 ("TD27-03","Chương trình","Ra mắt bệnh viện, phòng khám và cơ sở mới","Nhận biết/Tạo khách","7 cơ sở; kích hoạt có điều kiện theo ngày khai trương","Quản lý thương hiệu đúng nhóm; một chủ dự án/cơ sở","Điều kiện mở; khách hợp lệ; sử dụng dịch vụ T+30/T+90","T-120 → T+90; không tự gán tháng","Mỗi cơ sở một mã con; dùng bộ nhận diện có sẵn"),
 ("TD27-04","Chương trình","Nâng nhận biết, uy tín và niềm tin thương hiệu","Thương hiệu/Kết quả","Toàn hệ thống và từng nhóm thương hiệu","Quản lý thương hiệu đúng nhóm","Nhận biết/cân nhắc; branded search; nhu cầu thương hiệu","Q1 đo nền → Q2-Q3 triển khai → Q4 đo tác động","Không coi số bài/video là kết quả thương hiệu"),
 ("TD27-05","Chương trình","Phát triển thị trường cho chuyên khoa và dịch vụ chiến lược","Tạo nhu cầu","Đơn vị, chuyên khoa và dịch vụ ưu tiên","Quản lý thương hiệu đúng nhóm","Nhu cầu hợp lệ; lịch hẹn; sử dụng dịch vụ","Q1 chọn danh mục → Q2-Q4 theo đợt","Khác chiến dịch chuyển đổi TD27-06"),
 ("TD27-06","Chương trình","Chiến dịch chuyển đổi, thu hút khách hàng và doanh thu","Tăng trưởng/Doanh thu","Theo cơ sở, thương hiệu, dịch vụ","Quản lý thương hiệu đúng nhóm","Lead hợp lệ → hẹn → đến viện → dịch vụ → doanh thu đối soát","Theo tháng/quý khi đã có chỉ tiêu và nền dữ liệu","Không cộng trùng doanh thu/lead với thường xuyên và TD27-05"),
 ("TD27-07","Chương trình","Kết nối cộng đồng, doanh nghiệp và nguồn khách giới thiệu","Cộng đồng/Tạo nguồn","Địa bàn cơ sở, đối tác, trường học","Quản lý thương hiệu đúng nhóm; Trưởng nhóm Marketing cơ sở","Đối tác hoạt động; khách hợp lệ; khách quay lại","Theo quý và các sự kiện được phê duyệt","Sự kiện thường xuyên hạch toán ở sổ thường xuyên"),
 ("TD27-08","Chương trình mẹ","Chuyển đổi số công tác quản trị Marketing 2027","Nền tảng/Số hóa","Ba dự án TD27-09, TD27-10, TD27-11","Trưởng phòng Marketing","Tiến độ nghiệm thu ba dự án con","Q1-Q4 giám sát các cổng giai đoạn","Mã CHA; không tạo giờ/đầu ra hoặc doanh thu riêng"),
 ("TD27-09","Dự án","Website và TTH App: hoàn thiện, nhập liệu, khai thác","Nền tảng/Tạo khách","Website, App, CMS và dữ liệu bác sĩ/dịch vụ","Quản lý sản phẩm số","Hồ sơ CMS chuẩn; đặt lịch; truy vết nguồn","GĐ1 hoàn thiện/nhập liệu → GĐ2 tối ưu","Hồ sơ nguồn một lần; sử dụng đúng tích hợp"),
 ("TD27-10","Dự án","CRM, Contact Center và tích hợp HIS","Nền tảng/Chuyển đổi","CRM + Call Center + HIS; các nâng cấp theo phạm vi duyệt","Quản lý sản phẩm số","Liên kết mã HIS; chất lượng chăm sóc; dữ liệu cuộc gọi","GĐ1 CRM+Call Center+HIS → GĐ2 cần chốt phạm vi","Không ghi khách/doanh thu hai lần; AI/đa kênh chờ duyệt"),
 ("TD27-11","Dự án","Phần mềm quản trị Marketing, giao việc và đo tải","Nền tảng/Quản trị","2 phân hệ trọng điểm/thường xuyên + 4 nền dùng chung","Quản lý sản phẩm số","Truy vết công việc; tải giờ; đúng hạn; nhật ký duyệt","GĐ1 trọng điểm/lõi → GĐ2 thường xuyên/đo tải","Giữ nguyên mã gốc MTCV, CNNV và sổ giờ"),
 ("TD27-12","Dự án","Chuẩn hóa quy trình, biểu mẫu, bộ mẫu và quản trị dữ liệu","Năng lực/Quản trị","Tất cả chức danh, đơn vị và thương hiệu","Trưởng phòng Marketing; chủ nghiệp vụ từng quy trình","Mới/sửa/hợp nhất; ban hành; tỷ lệ áp dụng","Q1 đối chiếu → Q2 ban hành → Q3-Q4 áp dụng","Quy trình cũ phải đối chiếu; bộ mẫu TD27-01 không đếm lại"),
 ("TD27-13","Dự án","Chuẩn hóa KPI, nguồn dữ liệu và báo cáo hiệu quả Marketing","Đo lường/Quản trị","Mọi chương trình, kênh, đơn vị","Chuyên viên đo lường Marketing","Dữ liệu hoàn chỉnh; KPI xác minh; truy vết MKT–DV–DT","Q1 định nghĩa → Q2 thử → Q3-Q4 đối soát","Định nghĩa nghiệp vụ khác thao tác phát triển phần mềm")
]
LAUNCH = [
 ("M01","Bệnh viện Đa khoa Quốc tế TTH Huế","TTH Hospital","Bệnh viện","Trưởng nhóm Marketing cơ sở từ T-90"),
 ("M02","Bệnh viện Đa khoa TTH Đức Thọ","TTH Hospital","Bệnh viện","Trưởng nhóm Marketing cơ sở từ T-90"),
 ("M03","Bệnh viện Mắt Nguyên Châu","Nguyên Châu","Chuyên khoa độc lập","Trưởng nhóm Marketing theo mốc mở"),
 ("M04","Bệnh viện Răng hàm mặt Nguyên Thảo","Nguyên Thảo","Chuyên khoa độc lập","Trưởng nhóm Marketing theo mốc mở"),
 ("M05","Bệnh viện Tai Mũi Họng Nguyên Trí","Nguyên Trí","Chuyên khoa độc lập","Trưởng nhóm Marketing theo mốc mở"),
 ("M06","Phòng khám Đa khoa TTH Khe Tre","TTH Clinic","Phòng khám","Đầu mối kiêm nhiệm, không tự cộng một suất"),
 ("M07","Phòng khám Đa khoa TTH A Lưới","TTH Clinic","Phòng khám","Đầu mối kiêm nhiệm, không tự cộng một suất")
]
OUTPUTS = {
 "TD27-01":[
 "Biên bản kiểm kê bộ nhận diện đã ban hành và hiệu lực áp dụng",
 "Sơ đồ kiến trúc thương hiệu và phạm vi pháp lý được đối chiếu",
 "Bộ quy chuẩn nhận diện TTH Healthcare / Hospital / Clinic",
 "Bộ quy chuẩn nhận diện thương hiệu chuyên khoa độc lập",
 "Thư viện logo chuẩn, âm bản, tỷ lệ và phiên bản kỹ thuật",
 "Danh mục mẫu 2D/3D, định danh và thông số in/thi công",
 "Báo cáo đào tạo, kiểm tra tuân thủ nhận diện theo cơ sở"],
 "TD27-02":[
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Biển hiệu/OOH/nội viện",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Không gian tiếp đón/chỉ dẫn",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Ấn phẩm hành chính",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Biểu mẫu, tài liệu người bệnh",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Đồng phục, thẻ tên",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Vật phẩm, bao bì và quà tặng",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Kênh số/website/app",
 "Kiểm kê, triển khai và nghiệm thu ứng dụng: Phương tiện, sự kiện và trưng bày"],
 "TD27-04":[
 "Bộ mục tiêu đối tượng, thông điệp và đường cơ sở nhận biết",
 "Kế hoạch truyền thông thương hiệu cấp hệ thống theo đợt",
 "Bộ nội dung uy tín bác sĩ/chuyên môn có chứng cứ xác nhận",
 "Chương trình PR/cộng đồng về năng lực chuyên môn",
 "Đợt truyền thông tăng tìm kiếm thương hiệu/độ cân nhắc",
 "Báo cáo tác động thương hiệu theo KPI kết quả"],
 "TD27-05":[
 "Danh sách chuyên khoa/dịch vụ chiến lược được phê duyệt",
 "Phân tích nhu cầu–năng lực–công suất theo cơ sở",
 "Đề án định vị và thông điệp dịch vụ/chuyên gia",
 "Hồ sơ nội dung và tài liệu tư vấn chuẩn chuyên môn",
 "Chương trình giáo dục nhu cầu–tạo quan tâm theo dịch vụ",
 "Đánh giá nhu cầu, lịch hẹn, khách phát sinh theo dịch vụ"],
 "TD27-06":[
 "Kế hoạch doanh thu/khách theo bệnh viện, dịch vụ, đợt",
 "Chiến dịch chuyển đổi có mã nguồn khách nhất quán",
 "Đề bài nội dung, quảng cáo, trang đích và tư vấn",
 "Bộ kịch bản tiếp nhận và chăm sóc khách được duyệt",
 "Bảng số liệu lead hợp lệ–lịch hẹn–đến viện–DV–DT",
 "Biên bản nghiệm thu chi phí/đầu ra và bài học sau chiến dịch"],
 "TD27-07":[
 "Danh sách và phân loại đối tác/khu vực ưu tiên",
 "Đề án/chương trình cộng đồng hoặc hợp tác địa bàn",
 "Bộ tài liệu truyền thông và phân công hiện trường",
 "Báo cáo người tham gia, lead hợp lệ, khách sử dụng DV",
 "Hồ sơ nghiệm thu sự kiện/đối tác và cơ chế duy trì"],
 "TD27-09":[
 "Danh mục dữ liệu bác sĩ, khoa, dịch vụ và cơ sở cần nhập CMS",
 "Quy chuẩn cấu trúc, ảnh, nội dung, phân quyền duyệt CMS",
 "Giao diện, điều hướng, kiểm thử truy cập website/app",
 "Bản ghi hồ sơ CMS đã nhập, kiểm chứng, công bố",
 "Luồng đăng ký, nhận yêu cầu, gọi/nhắn và theo dõi chuyển đổi",
 "Đối soát website/app với CRM và nguồn dữ liệu",
 "Báo cáo SEO, tốc độ, nội dung và nhu cầu hợp lệ",
 "Kế hoạch tối ưu định kỳ theo dữ liệu thực tế"],
 "TD27-10":[
 "Tài liệu luồng CRM+Contact Center+HIS và thẩm quyền",
 "Định nghĩa mã bệnh nhân, định danh và chống trùng hồ sơ",
 "Kịch bản tư vấn và phản hồi dịch vụ được duyệt",
 "Kiểm thử liên kết bệnh nhân HIS–CRM",
 "Kiểm thử chuyển giao lead tới lịch hẹn/đến viện",
 "Báo cáo chất lượng nhân viên, thời hạn phục vụ và dữ liệu cuộc gọi",
 "Danh mục nâng cấp GĐ2: phạm vi AI/đa kênh theo duyệt",
 "Báo cáo nghiệm thu và khả năng truy vết CRM–DT"],
 "TD27-11":[
 "Định nghĩa cấu trúc CTDA–giai đoạn–công việc–đầu ra",
 "Phân hệ hạng mục trọng điểm: giao việc, phê duyệt, nghiệm thu",
 "Phân hệ thường xuyên: sản lượng, định mức, công đoạn",
 "Danh mục dùng chung: đơn vị, thương hiệu, chức danh, tài sản, kênh",
 "Kiểm soát và rà soát: quyền, phiên bản, cảnh báo, chặn",
 "Đo lường, KPI, báo cáo và liên kết dữ liệu nguồn",
 "Quản trị hệ thống và nhật ký phân quyền",
 "Biên bản kiểm thử 26 chức danh và luồng thực tế"],
 "TD27-12":[
 "Bảng đối chiếu quy trình/biểu mẫu hiện có và quy trình cần thiết",
 "Danh mục quy trình mới/sửa/hợp nhất/giữ lại theo chủ nghiệp vụ",
 "Bộ quy trình kiểm soát giao việc, kiểm chuyên môn, phát hành",
 "Danh mục bộ mẫu, biểu mẫu theo chức danh",
 "Bộ hướng dẫn triển khai và đào tạo vận hành",
 "Sổ đăng ký mã, ngày hiệu lực, thẩm quyền, phiên bản",
 "Báo cáo mức áp dụng, lỗi và khắc phục theo kỳ"],
 "TD27-13":[
 "Thư viện định nghĩa KPI thương hiệu, khách, doanh thu, hiệu suất",
 "Quy tắc phân biệt lead thô/lead hợp lệ/khách sử dụng DV",
 "Quy tắc tính nguồn khách và ghi nhận doanh thu từ MKT",
 "Bảng đối soát dữ liệu CRM, HIS, Ads, Website, Kế toán",
 "Mẫu báo cáo ngày/tuần/tháng/quý/năm theo đúng cấp dùng",
 "Bảng điều hành đa chiều đơn vị–thương hiệu–chương trình–vị trí",
 "Báo cáo chất lượng dữ liệu và công bố chỉ số sau chốt kỳ"]
}
LAUNCH_STEPS = [
 "hồ sơ thị trường, năng lực và thông điệp ra mắt",
 "kế hoạch truyền thông, KPI, ngân sách, kế hoạch nhân sự",
 "danh mục điểm chạm/bộ nhận diện sẵn sàng",
 "trang đích, hồ sơ bác sĩ/dịch vụ và luồng chuyển đổi",
 "chiến dịch truyền thông trước khai trương",
 "sự kiện/hoạt động ra mắt có nghiệm thu",
 "báo cáo nguồn khách, chuyển đổi, hiệu quả 30 ngày",
 "báo cáo hiệu quả 90 ngày và phương án duy trì"]
STEPS = [
 "Nghiên cứu/biên soạn/sản xuất",
 "Kiểm chuẩn chuyên môn Marketing",
 "Chỉnh sửa theo vòng phản hồi hợp lệ",
 "Duyệt/phát hành theo thẩm quyền",
 "Bàn giao, lưu nguồn và đối chiếu nghiệm thu"]
LAUNCH_TIME = ["T-120","T-120","T-90","T-60","T-30","T0","T+30","T+90"]
GATES = ["Chờ xác nhận ngày khai trương","Pháp lý và năng lực y khoa","KPI, ngân sách và công suất","Nhân sự hiện trường","Nội dung/y khoa và định danh nguồn khách","Biên bản nghiệm thu"]
def performer(pg,n):
    """Trả về đúng vị trí sản xuất theo hàng S1 của phụ lục gốc."""
    if pg=="TD27-03":
        k=(n-1)%8
        if k==3:return "Quản lý sản phẩm số"
        if k==5:return "Trưởng nhóm/đầu mối MKT cơ sở"
        if k==6:return "Chuyên viên đo lường"
        return "Quản lý thương hiệu đúng nhóm"
    if pg=="TD27-09":
        if n==4:return "Biên tập TCT"
        if n==7:return "Chuyên viên kênh số"
        return "Quản lý sản phẩm số"
    if pg=="TD27-12":return "Chủ nghiệp vụ đúng CNNV/MTCV"
    if pg=="TD27-13":return "Chuyên viên đo lường/đầu mối dữ liệu Marketing"
    if pg in ("TD27-10","TD27-11"):return "Quản lý sản phẩm số"
    return "Quản lý thương hiệu đúng nhóm"

def reviewer(pg,n):
    if pg=="TD27-01" and n in (5,6):return "Thiết kế TCT"
    if pg=="TD27-02":return "Thiết kế/Truyền thông theo công đoạn – chưa chỉ định người kiểm"
    if pg=="TD27-03" and (n-1)%8==5:return "CVT Nội dung – Sáng tạo và Marketing cơ sở"
    if pg in ("TD27-11","TD27-12"):
        return "CVT Truyền thông – Thương hiệu và Tăng trưởng số (chính); CVT Nội dung – Sáng tạo và Marketing cơ sở (phối hợp, cần tách giờ)"
    return "CVT Truyền thông – Thương hiệu và Tăng trưởng số"

def build(site: Path):
    p=site/"ke-hoach-mkt-2027/data.json"
    d=json.loads(p.read_text(encoding="utf-8"))
    before=(len(d["portfolio"]["programs"]),len(d["portfolio"]["projects"]),len(d["portfolio"]["tasks"]),len(d["roles"]),len(d["monthlyActions"]))
    assert before[:4]==(6,24,288,26), before
    programs=[dict(code=a,level=b,name=c,objective=e,scope=f,owner=g,kpi=h,roadmap=i,crosswalk=j,approval="CHUA_DUYET",hoursCanBeAdded=False) for a,b,c,e,f,g,h,i,j in PROG]
    launches=[dict(code=a,name=b,brand=c,facilityType=e,lead=f,plannedOpeningDate=None,approval="CHUA_DUYET",activation="THEO_NGAY_T",start="T-120",end="T+90",gates=GATES) for a,b,c,e,f in LAUNCH]
    outputs=[]
    for pg, names in OUTPUTS.items():
        owner=next(q["owner"] for q in programs if q["code"]==pg)
        for n,name in enumerate(names,1):
            outcode=f"{pg}-SP{n:03d}"
            outputs.append(dict(code=outcode,programId=pg,title=name,facilityId=None,relativeMilestone=None,owner=performer(pg,n),reviewer=reviewer(pg,n),approver="Người có thẩm quyền theo phân cấp",quantityPlan=None,hoursPerUnit=None,acceptance="Bàn giao được xác nhận; có mã nguồn, phiên bản và bằng chứng",status="CHUA_DUYET",workloadBooking="CHI_TINH_SAU_DOI_CHIEU_MA_GOC"))
    pg="TD27-03"
    for facility in launches:
        for n,name in enumerate(LAUNCH_STEPS):
            seq=(int(facility["code"][1:])-1)*8+n+1
            code=f"{pg}-SP{seq:03d}"
            outputs.append(dict(code=code,programId=pg,title=facility["name"]+": "+name,facilityId=facility["code"],relativeMilestone=LAUNCH_TIME[n],owner=performer(pg,seq),reviewer=reviewer(pg,seq),approver="Người có thẩm quyền theo phân cấp",quantityPlan=None,hoursPerUnit=None,acceptance="Đủ nguồn chứng minh và xác nhận cơ sở; không tự gán ngày T",status="CHUA_DUYET",workloadBooking="CHI_TINH_KHI_DU_DIEU_KIEN_MO"))
    outputs.sort(key=lambda x:(x["programId"],x["code"]))
    ops=[]
    for o in outputs:
        for i,name in enumerate(STEPS,1):
            nonmkt=i==4
            ops.append(dict(code=o["code"]+f"-S{i}",outputId=o["code"],programId=o["programId"],stepNo=i,step=name,owner="Theo thẩm quyền; cần xác minh có thuộc Marketing" if nonmkt else (o["reviewer"] if i==2 else o["owner"]),hourType="CHUA_XAC_MINH" if nonmkt else "MKT",quantity=None if i==3 else 1,standardHours=None,extraHours=None,chargeableHours=None,status="CHUA_CO_DINH_MUC",duplicateCode=False,bookingRule="Không cộng tải vào sổ giờ hiện hành khi chưa có mã đối chiếu và giờ chuẩn"))
    assert len(programs)==13 and len(launches)==7 and len(outputs)==132 and len(ops)==660,(len(programs),len(launches),len(outputs),len(ops))
    ids=[x["code"] for x in outputs+ops]
    assert len(ids)==len(set(ids))
    assert sum(x["hourType"]=="MKT" for x in ops)==528
    assert sum(x["hourType"]=="CHUA_XAC_MINH" for x in ops)==132
    appendix={"schemaVersion":"2027-11-21.1","revisionNote":"Phụ lục dự thảo đối chiếu; KHÔNG tự tăng số giờ/định biên","source":"Phu_luc_chot_CTDA_Marketing_TTH_2027.xlsx","programs":programs,"launchFacilities":launches,"outputs":outputs,"operations":ops,"workloadPolicy":{
        "existingPrograms":6,"existingProjects":24,"newAddendumPrograms":13,"newAddendumOutputs":132,
        "bookingStatus":"CHUA_CHO_PHEP_CONG_TAI","normalWorkingHourBase":"Mục 05 – sổ giờ MTCV gốc",
        "overlapRule":"Mã sản phẩm và bước đối chiếu 6 CT/24 DA hiện có trước khi hạch toán. Không cộng hai lần.",
        "parentCode":"TD27-08 – không ghi giờ/tổng doanh thu","outOfMarketingHours":"Chưa xác minh, tuyệt đối không cộng vào giờ Marketing",
        "reserve25pct":"Tính trên quỹ giờ hữu dụng sau khi chốt giờ chuẩn và lịch triển khai; không mặc định đủ tải",
        "activation":"Chỉ đưa vào kế hoạch tháng khi chốt ngày mở cơ sở, chủ trì, KPI, ngân sách, năng lực",
        "approvalStatus":"CHUA_PHE_DUYET","crosswalkStatus":"CHUA_CHOT_MA_TUONG_DUONG_6_24"},
        "counts":{"programs":13,"launchFacilities":7,"outputs":132,"steps":660,"mktStepsMissingHour":528,"unclassifiedHourSteps":132},
        "nextApprovalGates":["Đối chiếu dự án đã có và mã gốc","Khóa sản lượng theo tài sản, thương hiệu, cơ sở",
            "Gán chức danh trong 26 vị trí; không để tuyến quản lý chung chung",
            "Chốt định mức từng công đoạn, số vòng sửa và người duyệt",
            "Đối soát theo từng người/tháng: thường xuyên + trọng điểm + phát sinh",
            "Phê duyệt ngân sách, KPI, nguồn dữ liệu, ngày khai trương",
            "Nghiệm thu luồng giao việc, báo cáo, bàn giao và chống trùng"]}
    assert "ctdaAddendum" not in d or d["ctdaAddendum"].get("schemaVersion")==appendix["schemaVersion"]
    d["ctdaAddendum"]=appendix
    after=(len(d["portfolio"]["programs"]),len(d["portfolio"]["projects"]),len(d["portfolio"]["tasks"]),len(d["roles"]),len(d["monthlyActions"]))
    assert after==before, (before,after)
    p.write_text(json.dumps(d,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    export=site/"ke-hoach-mkt-2027"
    with (export/"phu-luc-trong-diem-2027.csv").open("w",encoding="utf-8-sig",newline="") as f:
        wr=csv.writer(f);wr.writerow(["Mã sản phẩm","Hạng mục","Đầu ra","Cơ sở","Mốc","Chủ trì","Định mức","Tình trạng"])
        for o in outputs:wr.writerow([o["code"],o["programId"],o["title"],o["facilityId"] or "",o["relativeMilestone"] or "",o["owner"],"Chưa chốt","Chưa duyệt"])
    with (export/"phu-luc-cong-doan-2027.csv").open("w",encoding="utf-8-sig",newline="") as f:
        wr=csv.writer(f);wr.writerow(["Mã bước","Mã sản phẩm","Công đoạn","Người thực hiện","Loại giờ","Giờ chuẩn","Hạch toán"])
        for op in ops:wr.writerow([op["code"],op["outputId"],op["step"],op["owner"],op["hourType"],"Chưa chốt","Không cộng trùng"])
    print("PASS CTDA: 13 hang muc, 7 co so, 132 dau ra, 660 cong doan; 6/24/288 giu nguyen, chua cong tai.")
if __name__=="__main__":
    build(Path(sys.argv[1] if len(sys.argv)>1 else "_site"))
