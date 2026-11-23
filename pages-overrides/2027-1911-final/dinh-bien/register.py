"""Resource plan by unique document, work stage, revision and owner.
Assignments are proposed for testing unless an effective delegation is supplied.
A source/alias row is visible in the register and carries zero additional hours.
"""
from collections import Counter

# Owner, primary writer, independent reviewer, tester. Group tokens resolve before display.
FORM = {
'BM-1':'dl-1 dl-1 tp qlth-a','BM-2':'dl-1 dl-1 tp qlth-bc','BM-3':'cvt qlth-a cvt qlth-bc','BM-4':'bt-ac bt-ac cvt md-ac','BM-5':'qc qc cvt-2 qlth','BM-6':'cvt dl-1 cvt qlth-a','BM-7':'cvt bt-ac cvt tn-a@vinh','SO-1':'cvt qlsps cvt tn-b@nguyenphuc','BM-8':'cvt qlth-a cvt qlth-bc','BM-9':'cvt qlth-a tp dl-1','BM-10':'dl-1 dl-1 tp qlth-bc','BM-11':'cvt tn-a@vinh cvt tn-b@nguyenphuc','BM-12':'tp tp dl-1 qlth-a','BM-13':'dl-1 dl-1 tp qlth-bc','BM-14':'dl-1 dl-1 cvt-2 qc-a','BM-15':'cvt qlth-a cvt tk-nt','BM-16':'cvt bt-ac cvt tn-a@vinh','BM-17':'cvt tn-a@vinh cvt tn-b@nguyenphuc','BM-18':'cvt dl-1 cvt bt-ac','BM-19':'qlsps qlsps cvt-2 dl-2','BM-20':'tk-nt tk-nt cvt-2 cvtt-a','BM-21':'cvt bt-ac cvt qlsps','BM-22':'cvt bt-ac cvt qlth-bc','BM-23':'cvt qlsps cvt-2 dl-2','BM-24':'cvt-2 qc-a cvt-2 qlsps','BM-25':'dl-2 dl-2 phap-che tn-b@nguyenphuc','BM-26':'dl-1 dl-1 tp qlth-bc','BM-27':'dl-1 dl-1 tp qc-a',
'M-1':'cc cc cc-kiem bt-ac','M-2':'cvtt cvtt cvt-2 qlth','M-3':'bt bt cvt qc','M-4':'cvtt cvtt cvt-2 qlth','M-5':'cvt-2 phap-che cvt-2 cvtt-a','M-6':'tk-nt tk-nt cvt tk-a','M-7':'qlsps qlsps cvt-2 qc-a','M-8':'bt bt cvt md','M-9':'cvtt cvtt cvt-2 qlth',
'B-1':'qlth-a tk-a cvt qlth-a','B-2':'qlth-bc tk-b cvt qlth-bc','B-3':'qlth tk cvt qlth','B-4':'qlth cvtt cvt-2 qlth','B-5':'tk-nt tk-nt cvt cvtt-a','B-6':'qlth bt cvt qlth','B-7':'md md cvt mdcs',
'QC-1':'tk-a tk-a cvt qlth-a','QC-2':'tk-b tk-b cvt qlth-bc','QC-3':'tk-nt tk-nt cvt tk-a','QC-4':'cvt md-ac cvt md-b','QC-5':'cvt-2 cvtt-a cvt-2 cvtt-bc','QC-6':'dl-2 dl-2 cvt-2 qc-a',
'DS-1':'phap-che phap-che tp bt-ac','DS-2':'cvt-2 cvtt-a cvt-2 cc','DS-3':'qlsps qlsps cvt-2 qc-a','DS-4':'cvt tk-nt cvt bt-ac','DS-5':'tk-nt tk-nt cvt qlth-a',
'DM-1':'dl-1 dl-1 cvt-2 dl-2','DM-2':'qc qc cvt-2 qlth','DM-3':'tk-nt tk-nt cvt-2 cvtt-a','DM-4':'qlsps qlsps cvt-2 qc-b','DM-5':'cvt cvtt-a cvt dl-1','DM-6':'qlth qlth cvt-2 cvtt','DM-7':'dl-2 dl-2 phap-che qc-b','DM-8':'cvt qlsps cvt-2 bt-ac','DM-9':'tp qlth-a tp qlth-bc','DM-10':'cvt dl-1 cvt bt-ac',
'SO-2':'dl-1 dl-1 tp qlth-bc','SO-3':'cvt-2 cvtt-a cvt-2 qc-a','SO-4':'cvtt cvtt cvt-2 tn','SO-5':'tk-nt tk-nt cvt md-ac','HS-1':'cvt bt-ac cvt qlsps','HS-2':'phap-che dl-2 phap-che qlsps','HS-3':'phap-che bt-ac phap-che qc-a','HS-4':'cvtt cvtt cvt-2 qlth','HS-5':'cvtt cvtt cvt-2 qlth'}
GROUP={'qc':['qc-a','qc-b'],'bt':['bt-ac','bt-b'],'md':['md-ac','md-b'],'tk':['tk-a','tk-b'],'cvtt':['cvtt-a','cvtt-bc'],'qlth':['qlth-a','qlth-bc'],'tn':['tn-a@vinh','tn-b@nguyenphuc'],'mdcs':['mdcs-a@vinh','mdcs-b@nguyenphuc']}
EXTERNAL={'cc':'Contact Center','cc-kiem':'Người kiểm tra nghiệp vụ độc lập của Contact Center','nhan-luc':'Phòng Nhân lực','phap-che':'Pháp chế','btgd':'Ban Tổng Giám đốc','qlcl':'Phòng Quản lý chất lượng','ke-toan':'Kế toán','cong-nghe':'Phòng Công nghệ','so-hoa':'Phòng Số hóa','ky':'Người được giao ký ban hành (chờ văn bản phân cấp)','bgd-coso':'Ban Giám đốc cơ sở','gd-coso':'Giám đốc cơ sở','ptgd-tc':'Phó Tổng Giám đốc phụ trách tài chính','ncc':'Đơn vị thiết kế thuê ngoài','chu-du-lieu':'Chủ dữ liệu chuyên môn, người hành nghề, giá và giấy phép theo phân cấp','nguon-doi-tac':'Đầu mối dữ liệu được ủy quyền tại thương hiệu/đối tác'}
# The flow catalogue owner controls the process, not every technical work stage.
FLOW_WRITERS = '''qlth-a bt-ac tn-a@vinh dl-1 dl-2 cvtt-a bt-ac tn-b@nguyenphuc qlth-a qlth-a tk-a cvtt-a tk-nt qlsps dl-1 cvtt-a qlsps bt-ac qlth-bc cvtt-bc tn-a@vinh cvtt-a qc-a tk-nt dl-2 qlth-a cvtt-bc qlsps cvtt-bc bt-ac bt-ac qlth-a cvtt-a cvtt-bc cvtt-a tn-a@vinh qlth-a bt-ac qc-a dl-2 tp tn-a@vinh cvtt-a qlth-bc bt-ac tn-b@nguyenphuc md-ac bt-ac qlsps dl-2 qlth-a dl-2 bt-b cvtt-a qc-b qc-a qc-a dl-1 bt-ac qlth-a'''.split()
# Extra catalogue rows with links to the costed master, for references covering the same scope.
LINKS = {'QCPN-MKT':'QC-5','QT.05.MKT.TCT':'QT.57','QT-PT-HT':'QT.29','BM-NGANH':'BM-1','29/BB-TTH':'QT.58','QĐPH-SH':'QT.14','QT-PM-HM':'QT.1','QCKPI-MKT':'BM-13','TC-VT':'HS-1','QĐ-DLCN-MKT':'HS-2','QyĐ.04.MKT':'QC-4'}
# Each additional master contributes a distinct deliverable; its reference points back to a source entry.
EXTRA = [
 ('BC-NAM','Mẫu tổng kết Marketing năm và thuyết minh chênh lệch','BM-18 · BM-1 · QT.58','dl-1 dl-1 tp qlth-a','Biểu mẫu',1,'Tổng hợp theo thương hiệu/cơ sở, hạng mục, ngân sách, KPI, so với kế hoạch và năm trước. Bổ sung số giờ, thiếu tải và điều chỉnh năm sau.'),
 ('QC-BT','Quy chuẩn biên tập, văn phong và điểm kiểm y khoa','Ma trận bốn bộ quy chuẩn · B-6 · DS-1','cvt bt-ac cvt bt-b','Quy chuẩn',1,'Khung chung về biên tập. B-6 là từ điển từ ngữ theo thương hiệu, DS-1 là phiếu pháp lý.'),
 ('QC-KS','Quy chuẩn xuất bản nền tảng và thông số bàn giao','Ma trận bốn bộ quy chuẩn · DS-3 · QT.56','cvt-2 qc-a cvt-2 qlsps','Quy chuẩn',1,'Quy cách xuất bản, phân quyền và gỡ thông tin. DS-3 chỉ giữ danh sách các thay đổi/chính sách.'),
 ('MAU-QC','Bộ mẫu thông số quảng cáo theo hai nhóm','QT.57 · BM-14 · M-7','cvt-2 qc-a cvt-2 qc-b','Mẫu',2,'Hai cấu hình thiết lập, mã chiến dịch và phép thử nguồn. Phần hình ảnh sáng tạo lấy từ mẫu thiết kế.'),
 ('DT-01','Bộ bài tập bàn giao, nghiệm thu và chấm thử chuyên môn','QT.59 · BM-16 · DS-4','cvt bt-ac cvt qlsps','Bộ',3,'Ba bài tập theo ba tổ, có đáp án, thang chấm và minh chứng. Thời gian đứng lớp tính theo buổi ở bảng chức danh.'),
 ('YC-CRM','Đặc tả CRM và bộ ca kiểm dữ liệu liên kết HIS','QT.25 · BM-19 · QT-HT01','dl-2 dl-2 cvt-2 dl-1','Hồ sơ',1,'Trường nguồn khách, đồng ý, trùng mã, khớp mã bệnh nhân và kiểm sai liên kết. Phần lập trình và dữ liệu y khoa do chủ hệ thống đảm nhiệm.'),
 ('YC-WEB','Hồ sơ yêu cầu và nghiệm thu nghiệp vụ website','QT.14 · BM-19','qlsps qlsps cvt-2 bt-ac','Hồ sơ',1,'Một gói triển khai ban đầu gồm bản yêu cầu, tiêu chí, ca thử giao diện và biên bản.'),
 ('YC-APP','Hồ sơ yêu cầu và nghiệm thu nghiệp vụ App','QT.14 · BM-19','qlsps qlsps cvt-2 qc-a','Hồ sơ',1,'Kiểm hành trình, thông tin dịch vụ và chuyển yêu cầu, không tính công thiết kế/lập trình của Phòng Công nghệ.'),
 ('YC-PM','Đặc tả phần mềm quản trị Marketing và ca thử','BM-19 · QT-HT01 · QT.49','qlsps qlsps cvt-2 dl-1','Hồ sơ',2,'Hai phân hệ dùng chung bốn phần nền. Kiểm một lần luồng cấp quyền và nhật ký dùng chung.'),
 ('ND-WEB1','Trang dịch vụ gốc xây mới theo đề án nhóm 1','Mục 21.1 · QT.14','qlth-a bt-ac cvt qlsps','Mẫu',8,'Ví dụ tám trang mới có nghiệm thu; nội dung cập nhật trang đang vận hành tính theo đầu ra thường xuyên.'),
 ('ND-WEB2','Trang dịch vụ gốc xây mới theo đề án nhóm 2','Mục 21.1 · QT.14','qlth-bc bt-b cvt qlsps','Mẫu',6,'Ví dụ sáu trang mới cho hai thương hiệu đang hoạt động.'),
 ]
# Standard minutes per unit: check original / author / peer review / pilot / submission / close-out / periodic review.
PROFILES={'Biểu mẫu':[30,150,55,45,20,20,35],'Sổ':[40,210,65,60,20,25,40],'Mẫu':[45,240,75,60,25,30,50],'Bộ':[90,540,120,100,35,45,75],'Quy chuẩn':[70,420,110,90,35,45,75],'Danh sách kiểm tra':[30,135,45,40,15,20,30],'Danh mục':[40,180,60,45,20,25,35],'Hồ sơ':[60,300,90,75,30,35,60],'Quy trình':[60,260,80,70,35,30,55],'Văn bản':[60,210,75,60,30,25,60]}
ACTIONS={'soat':'Đối chiếu bản gốc','moi':'Xây mới có điều kiện','sua':'Sửa đổi','gop':'Hợp nhất','giu':'Duy trì','bo':'Bãi bỏ theo quyết định','link':'Tham chiếu chung'}
FACTORS={'soat':[1,0,0,0,0,0], 'moi':[1,1,1,1,1,1], 'sua':[1,.55,.75,.75,1,.75], 'gop':[1.5,.8,1,1,1,1], 'giu':[1,0,0,0,0,0], 'bo':[1,.2,.45,.25,1,1], 'link':[0]*6}

def register(d):
    items=[]
    def put(code,name,category,kind,scope,jobs,count,action,month,freq,evidence,authority,desc,original,rawrole='',link='',profile=None,cycle='Năm',parts=(),coauthors=()):
        stages=profile or PROFILES[kind]; idx=sum(1 for it in items if it['code']==code)+1
        items.append(dict(id=code+'~'+str(idx),code=code,name=name,category=category,kind=kind,scope=scope,owner=jobs[0],writer=jobs[1],reviewer=jobs[2],tester=jobs[3],count=count,action=action,month=month,freq=freq,evidence=evidence,authority=authority,note=desc,original=original,rawrole=rawrole,link=link,profile=stages,cycle=cycle,parts=list(parts),coauthors=list(coauthors)))
    for i,x in enumerate(d['danh_muc_tai_lieu']):
        code=x['ma'];kind=x['loai'];raw=FORM[code].split(); two=x['pham_vi']=='theo_nhom' and x.get('ban_theo_nhom') is True; variants=[0,1] if two else [1 if x['pham_vi']=='nhom_2' else 0]
        for g in variants:
            jobs=[GROUP.get(a,[a,a])[g] for a in raw]; scope=('Nhóm '+str(g+1)) if two or x['pham_vi'] in ['nhom_1','nhom_2'] else 'Dùng chung';cycle=x['chu_ky_ra_soat'];freq=4 if 'quý' in cycle.lower() else 2 if '06 tháng' in cycle else 12 if 'hằng tháng' in cycle.lower() else 1
            evidence='Có đặc tả trong Khung. Cần bản gốc, phiên bản, người duyệt và phạm vi để chốt cách xử lý.'; count=1;profile=None;desc=x['noi_dung'];parts=[];co=[]
            action='sua' if kind in ['Biểu mẫu','Sổ','Danh sách kiểm tra','Danh mục'] else 'soat' if code in ['M-1','M-5','DS-1','HS-2'] else 'sua';month=1+(i%6)
            if code=='M-1': action='soat';freq=0;desc+=' Phần Marketing cung cấp thông tin. Chủ kho kịch bản là Contact Center.'
            if code=='B-1':count=4;month=1;profile=[90,900,180,120,50,45,90];desc+=' Bốn cấu phần nhận diện của một bộ, khối lượng kiểm thử theo cấu phần.'
            if code=='B-2':count=2;month=2;profile=[90,240,150,100,45,45,75];desc+=' Hai thương hiệu chuyên khoa đang hoạt động. Giờ soạn nội bộ là lập yêu cầu/bàn giao. Thiết kế thuê ngoài theo tờ trình được hạch toán ngoài Marketing.'
            if code=='B-7':count=12;month=3;parts=[v['ma']+' · '+v['ten'] for v in d['danh_muc_video_b7_17112026']];profile=[35,240,65,75,20,20,35];desc+=' Một gói cho mỗi nhóm gồm 7 mẫu V2, 3 mẫu V3, hướng dẫn V1 và đặc tả bàn giao V4. Bản thử được tính ở công đoạn thử.';co=[('tk-a' if g==0 else 'tk-b',35,'Đồ họa dùng trong mẫu dựng')]
            if code=='HS-1':count=26;month=2;profile=[20,75,25,18,10,10,12];desc+=' 26 hồ sơ loại vị trí, mỗi hồ sơ một phiên bản. Hồ sơ cá nhân phát sinh theo giao việc. Rà phiên bản chuẩn 1 lần/năm trong mô hình.';freq=1
            if code=='M-6':count=6;month=4;co=[('tk-a',45,'Mẫu thiết kế nhóm 1'),('tk-b',45,'Mẫu thiết kế nhóm 2')];desc+=' Sáu nhóm mẫu thử, gồm kiểm kê và cấu trúc thư viện. Giờ thiết kế mẫu của hai nhóm là các phần việc riêng.'
            if code=='B-4':co=[(GROUP['bt'][g],80,'Phần nội dung'),(GROUP['tk'][g],100,'Phần dàn trang')]
            if code=='B-3':co=[(GROUP['qlth'][g],45,'Đặc tả mục tiêu của nhóm')]
            if code=='DS-4':co=[('bt-ac',50,'Phiếu kiểm biên tập'),('md-ac',50,'Phiếu kiểm media'),('qc-a',50,'Phiếu kiểm kênh số')]
            if code in ['B-1','B-2','M-7','B-7','BM-19']:month={'B-1':1,'B-2':2,'M-7':4,'B-7':3,'BM-19':2}[code]
            if code in ['SO-4','HS-4','HS-3','BM-2','DM-7']:desc+=' Lượt điền, sử dụng trong nghiệp vụ đã nằm ở bảng chức danh. Chỉ tính riêng kiểm phiên bản của mẫu ở đây.'
            if x['pham_vi']=='theo_nhom' and not two and code!='M-1':
                scope='Một bản gốc, có phần theo hai nhóm'
                desc+=' Khung không đánh dấu hai bản gốc. Giả định nhóm 1 làm đầu mối soạn phần chung, nhóm 2 đóng góp phần riêng trên cùng bản.'
                writer2=GROUP[raw[1]][1] if raw[1] in GROUP else None
                if writer2 and all(c[0]!=writer2 for c in co):co.append((writer2,round(PROFILES[kind][1]/4),'Phần riêng nhóm 2, cùng một bản gốc'))
            # One scenario assumption for the signatory, contingent on verification. Separate authority text from approval of a filled-in form.
            rawapprove=x['duyet'];rawapprove=' / '.join(rawapprove) if isinstance(rawapprove,list) else str(rawapprove)
            auth='Cấp ký ban hành mẫu theo văn bản phân cấp còn hiệu lực, đang chờ đối chiếu. Tuyến duyệt hồ sơ sử dụng mẫu trong Khung: '+rawapprove
            put(code,x['ten'],'74 tài liệu',kind,scope,jobs,count,action,month,freq,evidence,auth,desc,x['can_cu'],str(x['xay_dung'])+' · giữ '+str(x['nam_giu']),profile=profile,cycle=cycle,parts=parts,coauthors=co)
    cross=d['doi_chieu_quy_trinh_cu_2027']['danh_sach'];assert len(FLOW_WRITERS)==len(cross)==60
    for i,x in enumerate(d['danh_muc_van_ban']):
        code=x['ma'];owner=x['chu_tri']; owner='cvt' if owner=='cvt' else owner; isflow=i<60; link=LINKS.get(code,'');scope=x['pham_vi'];month=1+i%6;freq=1
        if isflow:
            c=cross[i];assert c['ma_2027']==d['quy_trinh'][i]['id']; candidates=c['ung_vien_cu']; orig=' · '.join(v['ma']+' ('+v['ngay']+') '+v['ten'] for v in candidates) or 'Chưa thấy ứng viên trong Phụ lục 03';ev=c['tinh_trang_tim_kiem']+'. '+c['tinh_trang_hieu_luc'];writer=FLOW_WRITERS[i];action='sua' if len(candidates)==1 else 'gop' if len(candidates)>1 else 'moi'; desc='Một bộ mô tả luồng, trách nhiệm, điểm giao nhận và ca thử. Phương án '+ACTIONS[action].lower()+' chỉ để tính nguồn lực sau đối chiếu điều khoản.'
            reviewer=owner if owner!=writer else ('tp' if owner!='tp' else 'cvt');tester=('qlsps' if writer!='qlsps' else 'dl-1') if owner in ['dl-1','dl-2','qlsps','cvt-2'] else ('tn-b@nguyenphuc' if writer!='tn-b@nguyenphuc' else 'tn-a@vinh'); co=[]
            if code in d['cvt_phan_cong_van_ban_1911']['phoi_hop_ca_hai']:
                for r in ['cvt','cvt-2']:
                    if r not in [reviewer,writer]:co.append((r,30,'Góp ý đúng phạm vi tuyến trên cùng bản'))
        else:
            orig=str(x.get('van_ban_lien_quan',''));ev='Có tên trong 23 mục quản trị liên quan. Chưa đối chiếu bản có số ký hoặc thẩm quyền.';action='link' if code=='29/BB-TTH' else 'soat';desc='Xác định văn bản, người sở hữu và điều khoản áp dụng. Việc sửa, hợp nhất hoặc thu hồi chỉ được kích hoạt khi có quyết định.';writer=owner;reviewer='qlcl' if owner!='qlcl' else 'nhan-luc';tester='qlsps' if owner not in EXTERNAL else 'tp'; co=[]
        relation=link
        if relation and action!='link':desc+=f' Phạm vi giao với {relation} được tính ở hồ sơ gốc. Dòng này chỉ tính công đối chiếu điều khoản riêng.';link=''
        put(code,x['ten'],'60 quy trình' if isflow else '23 văn bản','Quy trình' if isflow else 'Văn bản',scope,[owner,writer,reviewer,tester],1,action,month,freq,ev,str(x.get('nguoi_duyet','Chờ văn bản phân cấp còn hiệu lực')),desc,orig,x['chu_tri'],link=link,coauthors=co)
    for i,(code,name,source,jobs,kind,n,note) in enumerate(EXTRA):
        if code=='MAU-QC':
            for g in range(2):
                team=['cvt-2',GROUP['qc'][g],'cvt-2','qlsps']
                put(code,name,'Chi tiết bổ sung',kind,'Nhóm '+str(g+1),team,1,'moi',4,1,'Đầu ra đề xuất, cần xác nhận số cấu hình riêng.','Theo văn bản phân cấp còn hiệu lực.',note,source)
            continue
        put(code,name,'Chi tiết bổ sung',kind,'Theo phạm vi của sản phẩm',jobs.split(),n,'moi',3+i%4,1,'Sản phẩm chi tiết đề xuất. Cần đối chiếu bản đã có trước khi giao xây mới.','Người có thẩm quyền theo phân cấp còn hiệu lực, cần hồ sơ giao quyền.',note,source)
    # Proposed 12-month ISSUANCE roadmap, not a claim that documents are approved.
    # Documents with an effective existing edition can be operated under that edition
    # while a replacement is reviewed. Missing / invalid editions block rollout.
    # Priority codes are ordered by operational dependencies, not by catalogue order.
    # A fixed due date for 162 miscellaneous rows at T3 was an unrealistic Q1 load.
    foundation={
        'BM-7':1,'BM-11':1,'BM-12':1,'BM-13':1,'BM-14':1,'BM-15':2,
        'BM-19':1,'BM-25':1,'BM-1':2,'BM-2':2,'BM-3':2,'BM-4':2,
        'DM-1':1,'DM-2':1,'DM-7':2,'SO-1':1,'DS-1':1,'DS-3':2,
        'B-1':1,'B-2':2,'QC-4':1,'QC-1':2,'QC-2':2,'QC-3':3,
        'M-6':3,'B-7':3,'B-3':3,'B-4':3,'B-5':3,'B-6':4,
        'YC-WEB':1,'YC-CRM':1,'YC-APP':2,'YC-PM':1,
        'ND-WEB1':3,'ND-WEB2':3,'QC-BT':2,'QC-KS':2,
        'MAU-QC':4,'M-7':4,'HS-1':3,'BC-NAM':9,
        'BM-27':2,'BM-8':3,'BM-9':3,'BM-10':4,
        'QT.1':1,'QT.2':1,'QT.14':1,'QT.15':1,
        'QT.21':2,'QT.25':2,'QT.46':2,'QT.48':2,
        'QT.49':2,'QT.57':2,'QT.58':2
    }
    # The eight windows organize documentation by true purpose and handover.
    # Numeric flow code is not a dependency; remaining 60 flows are staged by
    # the operating units in the 12-month roadmap, with owner sign-off pending.
    def proposed_month(item,index):
        code=item['code']
        if code in foundation:return foundation[code]
        category=item['category']
        if category=='60 quy trình':
            number=int(code.split('.')[-1]) if code.startswith('QT.') and code.split('.')[-1].isdigit() else index
            return min(10,3+(number-1)//8)
        if category=='23 văn bản':return min(9,2+(index%8))
        if category=='Chi tiết bổ sung':return min(10,4+index%6)
        if code.startswith(('BM-','SO-')):return min(8,3+index%6)
        if code.startswith(('DS-','DM-')):return min(9,4+index%6)
        return min(11,4+index%8)
    hard={'B-1','QC-4','BM-7','BM-11','BM-12','BM-19',
          'DM-1','DM-2','SO-1','YC-CRM','YC-WEB','YC-PM'}
    for index,item in enumerate(items):
        month=proposed_month(item,index)
        item['month']=month
        # First-use deadlines for core prerequisites are HARD GATES. Other
        # deadlines are rollout proposals, explicitly subject to approval.
        item['deadline']=month if item['code'] in hard else min(12,month+1)
        item['phasePriority']=0 if item['code'] in hard else 1 if item['code'] in foundation else 2
        item['issuanceStatus']='Dự kiến; chờ kiểm bản gốc, thẩm quyền và phê duyệt'
        item['phaseReason']='Tiền đề trước triển khai nghiệp vụ' if item['phasePriority']==0 else 'Mẫu/kênh ưu tiên theo giai đoạn' if item['phasePriority']==1 else 'Kiện toàn theo đợt sau khi có mẫu nền'
    assert len({x['code'] for x in items if x['category']=='74 tài liệu'})==74
    assert len({x['code'] for x in items if x['category'] in ['60 quy trình','23 văn bản']})==83
    return items
