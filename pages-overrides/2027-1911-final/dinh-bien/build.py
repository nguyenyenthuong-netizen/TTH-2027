"""Embed the source-based staffing model in the framework delivered to both hosts."""
from html import escape, unescape
from pathlib import Path
import json,re,sys
from operations import DRIVERS, SITES, SEATS, HIGH_SITE, HIGH_CLINIC, W
from register import register, EXTERNAL, FACTORS, ACTIONS
from crosswalk import reconcile

HERE=Path(__file__).resolve().parent
ROOT=Path(sys.argv[1])/'khung-marketing'
path=ROOT/'index.html'
s=path.read_text('utf-8')
pat=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)');m=pat.search(s);D=json.loads(m[2]);assert set(SEATS)=={v['id'] for v in D['vi_tri']}
assert 'dinh_bien_theo_dau_ra_2027' not in D,'Run on a freshly generated framework.'
roles={v['id']:{'to':v['to'],'name':v['ten'],'seats':SEATS[v['id']]} for v in D['vi_tri']}
assert sum(v['seats'] for v in roles.values() if v['to']!='coso')==22 and sum(SEATS.values())==36
assert {w['role'] for w in W}==set(roles) and len({w['id'] for w in W})==len(W)

def clean(text):return ' '.join(unescape(re.sub('<[^>]+>',' ',text)).split())
def jd_tables(text):
    out={}
    for a in re.finditer(r'<article\b[^>]*\bid="jd-([^" ]+)"[^>]*>(.*?)</article>',text,re.S):
        rid=a[1]
        if rid not in roles:continue
        t=re.search(r'Phụ lục 1\. Sản phẩm đầu ra.*?<table\b[^>]*>(.*?)</table>',a[2],re.S)
        if not t:raise ValueError('Thiếu phụ lục MTCV '+rid)
        out[rid]=[[clean(v) for v in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>',r,re.S)] for r in re.findall(r'<tr\b[^>]*>(.*?)</tr>',t[1],re.S)]
    assert set(out)==set(roles);return out

jd=jd_tables(s);docs=register(D)
for i,d in enumerate(docs):
    d['order']=i
    for a in [d['owner'],d['writer'],d['reviewer'],d['tester'],*[x[0] for x in d['coauthors']]]: assert a.split('@')[0] in set(roles)|set(EXTERNAL),(a,d['id'])
    assert d['writer']!=d['reviewer'],d['id']
raw=json.loads((ROOT/'doi-chieu-quy-trinh/doi-chieu-60-luong.json').read_text('utf-8'))
data=dict(version='2027.05.8',roles=roles,work=W,docs=docs,jd=jd,crosswalk=reconcile(jd,W,docs,roles),seats=SEATS,drivers=DRIVERS,external=EXTERNAL,factors=FACTORS,actions=ACTIONS,highSite=HIGH_SITE,highClinic=HIGH_CLINIC,sites=[dict(id=id,name=name,group=g,historic=hc,inputs=dict(zip(DRIVERS,amount))) for id,name,g,hc,amount in SITES],old=raw['danh_muc_van_ban_cu'])
assert len(D['quy_trinh'])==60 and sum(len(f['buoc']) for f in D['quy_trinh'])==407
contracts=[c['ma_dau_ra'] for f in D['quy_trinh'] for b in f['buoc'] for c in b['doi_soat_tung_dau_ra_2027']];assert len(contracts)==len(set(contracts))==568
D['dinh_bien_theo_dau_ra_2027']=data
D['doi_chieu_so_luong_nhan_su_19112026']['co_so_chi_tiet']={'benh_vien_chuyen_trach':13,'dau_moi_clinic_kiem_nhiem':1,'gio_phan_bo_clinic':None}
D['lo_trinh_dinh_bien']['can_cu_tai_2027']='Mục 05 tính ba kịch bản từ sản lượng, công đoạn tài liệu và lịch năm. Đối chiếu với 36 suất cơ cấu. Clinic là một đầu mối kiêm nhiệm.'
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+s[m.end(2):]
anchor='dinh-bien-2027'
link='<a href="#'+anchor+'" data-staff-panel="summary">Xem bảng giờ và so sánh ba kịch bản tại Mục 05</a>'
# Clean the entry point rather than stacking extra external-link banners above the view title.
start=s.index('<section class="view" data-view="staffing" id="v-staffing">')
end=s.index('<div class="card" id="tth-dinh-bien-corrected-1911"',start)
main='''<section class="view" data-view="staffing" id="v-staffing"><div class="view-h"><div><div class="eyebrow">PHẦN 05 / ĐỊNH BIÊN</div><h2 class="vt">Định biên theo khối lượng công việc</h2><p class="lede">Phương án 2027 gồm 22 suất tại Tổng công ty, 13 suất chuyên trách ở bệnh viện và một đầu mối TTH Clinic kiêm nhiệm. Sản lượng và thời gian tính thử có thể đối chiếu ngay bên dưới.</p></div></div><div id="dinh-bien-2027" data-version="2027.05.8"><noscript>Vui lòng bật JavaScript để sử dụng bảng tính và các danh mục chi tiết.</noscript></div>'''
s=s[:start]+main+s[end:]
# The older numbers remain identifiable as dated comparisons, outside the active calculation.
a=s.index('id="m-5-2"');b=s.index('</section>',a)
block=s[a:b]
def fixrow(m):
    row=m[0]
    if row.startswith('<tr><td>Lãnh đạo phòng</td>'):return re.sub(r'<td><strong>02</strong></td></tr>$','<td><strong>03</strong> (Trưởng phòng và hai chức danh Chuyên viên trưởng theo hai tuyến)</td></tr>',row)
    if re.match(r'<tr><td>(?:<strong>)?Phòng Marketing Tổng công ty',row):return re.sub(r'<td>(?:<strong>)?21(?:</strong>)?</td></tr>$','<td><strong>22</strong></td></tr>',row)
    if 'Khe Tre' in row:return re.sub(r'<td>[^<]*(?:<strong>)?kiêm nhiệm(?:</strong>)?</td></tr>$','<td>01 đầu mối kiêm nhiệm chung, giờ phân bổ chờ xác nhận</td></tr>',row)
    if re.match(r'<tr><td>(?:<strong>)?Toàn hệ thống',row):return re.sub(r'(<td>(?:<strong>)?36.*?)</td></tr>$','<td><strong>36 suất cơ cấu</strong> = 22 Tổng công ty + 13 bệnh viện + 01 đầu mối Clinic kiêm nhiệm.</td></tr>',row)
    return row
block=re.sub(r'<tr>.*?</tr>',fixrow,block,flags=re.S)
assert re.search(r'Tổng công ty(?:</strong>)?</td><td>10</td><td>18</td><td><strong>22',block)
block=block.replace('37</strong> (số nhân sự thực có năm 2026 (cần đối chiếu hồ sơ nhân sự))','37</strong> suất trong định biên trước đây')
s=s[:a]+block+'<p>'+link+'</p>'+s[b:]
a=s.index('id="m-6"');b=s.index('<p>Căn cứ hai định mức',a)
start=s.index('<p>Giờ khả dụng:',a,b)
s=s[:start]+'''<p>Chế độ tham chiếu trong hồ sơ là 47 giờ/tuần, 6 ngày/tuần. Mô hình năm 2027 tạm trừ 24 ngày nghỉ quy đổi. Chế độ riêng, lịch trực, phép và giờ được phân cho Clinic do Phòng Nhân lực và đơn vị xác nhận. Mô hình giữ số lẻ qua toàn bộ phép tính, tách tải kế hoạch, dự án và sự việc dùng dự phòng.</p><p>Trong bảng dưới, các mức 189/142 giờ, số người và giờ theo nhóm là ước tính lịch sử. Mô hình theo sản phẩm tại đầu Mục 05 dùng một quỹ thời gian cho cùng một người, kể cả phần kiêm Tổ trưởng. '''+link+'''</p>'''+s[b:]
old=re.search(r'<tr><td>Trưởng phòng; người quản lý trực tiếp đúng tuyến[^<]*</td><td>02</td><td>–</td><td>Cơ cấu quản lý</td><td>.*?</td></tr>',s[a:],re.S)
if old:s=s[:a]+s[a:].replace(old[0],'<tr><td>Trưởng phòng Marketing và hai chức danh Chuyên viên trưởng</td><td>03</td><td>Theo sản lượng và lịch quản lý</td><td>MTCV, số tổ và số Trưởng nhóm thuộc tuyến</td><td>'+link+'</td></tr>',1)
s=s.replace('Xem kịch bản định lượng: 02 vị trí ≈ 200 giờ/tháng; 03 vị trí ≈ 306 giờ/tháng (chưa xác nhận)','Phụ lục lịch sử của kịch bản 02/03 vị trí',1)
# Replace the external branch link inside this historical table with the live in-framework breakdown.
s=re.sub(r'<a [^>]*href="https://nguyenyenthuong-netizen.github.io/TTH-2027/khung-marketing/dinh-muc-26-vi-tri/co-so/"[^>]*>Phụ lục lịch sử của kịch bản 02/03 vị trí</a>','<a href="#dinh-bien-2027" data-staff-panel="sites">Xem sản lượng, giờ từng bệnh viện và Clinic ngay trong Mục 05</a>',s,count=1)
for key,panel,txt in [('v-roadmap','roadmap','Tra sản phẩm, người và giờ theo từng giai đoạn'),('v-assign','roles','Đối chiếu KPI và sản lượng từng chức danh'),('v-relations','manage','Xem tải phối hợp và đúng tuyến quản lý'),('v-ops','flows','Đối chiếu 60 luồng, 407 bước và 568 đầu ra với tải công việc')]:
    idx=s.index('id="'+key+'"');idx=s.index('</div></div>',s.index('<div class="view-h">',idx))+12
    s=s[:idx]+f'<p class="db-jump"><a href="#{anchor}" data-staff-panel="{panel}">{txt} tại Mục 05</a></p>'+s[idx:]
for rid in roles:
    a=s.index('id="jd-'+rid+'"');tag='<div class="jd-body">';i=s.index(tag,a)+len(tag)
    s=s[:i]+f'<p class="db-jump"><a href="#{anchor}" data-staff-role="{rid}">Sản lượng, giờ công và nhu cầu nhân sự của vị trí tại Mục 05</a></p>'+s[i:]
# The detailed implementation schedule must use the same starting structure as section 05.
a=s.index('id="v-roadmap"');end=s.index('</section>',s.index('id="m-29"',a))
part=s[a:end]
part=re.sub(r'Tổng công ty 21; bổ sung theo quy tắc định biên', 'Tổng công ty 22 suất theo phương án; bổ sung sau đối chiếu tải theo quy tắc định biên',part)
part=part.replace('Theo ngưỡng (khi đủ 10 bệnh viện, 02 phòng khám: Tổng công ty 28, cơ sở 25)', 'Lộ trình mở rộng chờ tính lại theo sản lượng, địa điểm và quyết định phân vùng.')
part=part.replace('Đủ 10 bệnh viện, 02 phòng khám: 56, gồm', 'Phương án mở rộng cũ, cần tính lại khi đủ điều kiện. Số 56 từng bao gồm')
part=part.replace('Bệnh viện Đa khoa Quốc tế TTH Huế 40;', 'Mốc tham chiếu của phương án mở rộng cũ, cần tính lại trước khi sử dụng. Bệnh viện Đa khoa Quốc tế TTH Huế 40;')
s=s[:a]+part+s[end:]
s=s.replace('22 TCT và 14 bệnh viện','22 suất Tổng công ty, 13 suất bệnh viện và 01 đầu mối Clinic kiêm nhiệm')
s=s.replace('Thiết kế giảm khoảng 150 giờ/tháng (01 người)','Ước tính lịch sử 150 giờ/tháng. Kịch bản hiện hành chỉ ghi nhận thời gian tiết kiệm trên số bản đổi cỡ có bằng chứng trước và sau.')
s=s.replace('<p>Quy tắc định biên theo phương pháp WISN ở mục 6: số người theo từng nhóm và vị trí = làm tròn lên [(giờ việc chính/tháng, chưa gồm kiêm nhiệm Tổ trưởng ÷ 142) + (giờ kiêm nhiệm Tổ trưởng/tháng ÷ 189)]. Không cộng trùng giờ Tổ trưởng vào phần việc chính.', '<p>Tính giờ của người kiêm Tổ trưởng trên cùng quỹ với giờ chuyên môn của người đó. Xem công thức quỹ kế hoạch, quỹ hữu ích và phần vượt theo tháng trong Mục 05.')
css=(HERE/'staffing.css').read_text();js=(HERE/'calculate.js').read_text()+'\n'+(HERE/'view.js').read_text().replace('/* EMBED_DELIVERABLES */',(HERE/'deliverables.js').read_text());s=s.replace('</head>','<script type="text/plain" id="tth-staffing-style">'+css+'</script><style>#dinh-bien-2027{scroll-margin-top:140px;min-width:0}.db-jump{margin:10px 15px;font-size:15px}.db-jump a{color:#0837a1;font-weight:650}</style></head>',1).replace('</body>','<script id="tth-staffing-app">\n'+js+'\n</script></body>',1)
assert len(re.findall(r'<button class="tab"',s))==12 and s.count('id="dinh-bien-2027"')==1
path.write_text(s,'utf-8')
# Historical appendix URLs remain functional, including their raw CSV downloads.
for name,panel in [('dinh-muc-26-vi-tri/index.html','26 chức danh'),('dinh-muc-26-vi-tri/co-so/index.html','từng bệnh viện và Clinic')]:
    p=ROOT/name
    if p.exists():
        h=p.read_text('utf-8');target='../' if '/co-so/' not in name else '../../';h=h.replace('<main>','<main><section><h2>Bảng tính năm 2027 trong Khung</h2><p><a href="'+target+'#dinh-bien-2027">Mở Mục 05 để đọc sản lượng và kết quả theo '+panel+'</a>. Phụ lục bên dưới lưu dữ liệu tham chiếu trước khi tính theo sản lượng.</p></section>',1);p.write_text(h,'utf-8')
print('Mục 05:',len(roles),'chức danh,',len(W),'định mức,',len(docs),'dòng phiên bản/phạm vi, 568 đầu ra.')
