"""Separate report-template preparation from recurring report production and sign-off.
The source is a planning assumption, not a verified time-and-motion study.
No creation of duplicate report outputs in the 26-position ledger.
"""
from pathlib import Path
import json,re,sys
p=Path(sys.argv[1])/'khung-marketing'/'index.html'
s=p.read_text('utf-8')
marker='tth-report-governance-audit-2027'
if marker in s:
    print('PASS: reporting governance already embedded')
    raise SystemExit(0)
pat=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=pat.search(s)
if not m:raise SystemExit('Missing Muc 05 source payload')
D=json.loads(m.group(2))
model=D['dinh_bien_theo_dau_ra_2027']
roles=model['roles']
works=model['work']
docs=model['docs']
assert len(roles)==26 and len({r['id'] for r in works})==len(works)
assert sum(1 for x in works if x['id']=='dl-1/tuan')==1
assert sum(1 for x in works if x['id']=='tp/bc-thang')==1
assert not any(x['id']=='tp/bc-tuan-kiem' for x in works)
# A weekly executive review is separate from the data specialist's existing 200-minute report.
# 90 minutes is a *provisional* workload estimate, not a confirmed service standard.
works.append(dict(
    role='tp',id='tp/bc-tuan-kiem',code='bc-tuan-kiem',
    name='Kiểm duyệt báo cáo tuần BM-2 và kết luận điều hành',
    q=1,t=[0,30,45,15,0],ref='BM-2 · QT.58 · MTCV Trưởng phòng',
    note='Mỗi tuần một lần: 30 phút trao đổi, 45 phút kiểm số và phân tích, 15 phút kết luận/điều chỉnh. Giả định cần đo lại; không bao gồm giờ soạn BM-2, tạo mẫu hay phê duyệt ngoài thẩm quyền.',
    kind='K',period='w',extra=0,jd=[10,20,30]
))
# Distinguish review complexity for *template revisions*; all numbers remain hypotheses.
# Values are *base minutes before the existing 0.75 modification factor*.
template_review_minutes={'BM-1':100,'BM-2':70,'BM-3':75,'BM-8':110,'BM-9':90,'BM-10':100,'BM-12':150,'BM-13':120,'BM-14':110,'BM-18':120,'BM-27':120}
changed={}
for d in docs:
    if d['code'] not in template_review_minutes or d.get('link'):continue
    if d['kind']!='Biểu mẫu':raise SystemExit('Unexpected template type '+d['code'])
    before=d['profile'][2]
    d['profile'][2]=template_review_minutes[d['code']]
    d['reviewEstimateBasis']='Ước tính rà cấu trúc, phép kiểm và điểm quyết định theo mức phức tạp biểu mẫu. Đây là công sửa mẫu, không phải công lập hoặc kiểm duyệt báo cáo kỳ.'
    changed[d['code']]=[before,d['profile'][2]]
assert set(changed)==set(template_review_minutes),(changed,template_review_minutes)
report_words=('báo cáo','kế hoạch','tổng kết','thuyết minh','bản số','bộ số','chốt kỳ','đối soát','phân tích','hiệu suất','dự toán','kpi','sai lệch','kết quả khảo sát')
report_refs=('BM-1','BM-2','BM-3','BM-8','BM-9','BM-10','BM-12','BM-13','BM-14','BM-18','BM-27')
report_ops=[]
for w in works:
    label=(w['name']+' '+w['ref']).lower()
    if any(t in label for t in report_words) or any(t.lower() in label for t in report_refs):
        report_ops.append(dict(id=w['id'],role=w['role'],title=w['name'],ref=w['ref'],qty=w['q'],
           period=w['period'],minutes=sum(w['t']),segments=w['t'],note=w['note'],
           conditional=not bool(w['q'])))
coverage={rid:sum(1 for x in report_ops if x['role']==rid) for rid in roles}
assert all(any(w['role']==rid for w in works) for rid in roles)
assert all(x['minutes']>0 for x in report_ops if isinstance(x['qty'],(int,float)) and x['qty']>0)
assert any(x['id']=='tp/bc-tuan-kiem' for x in report_ops)
assert any(x['id']=='dl-1/tuan' for x in report_ops)
assert any(x['id']=='dl-1/bc' for x in report_ops)
assert any(x['id']=='tp/bc-thang' for x in report_ops)
assert any(x['id']=='tp/bc-nam' for x in report_ops)
model['reporting_governance_2027']={
 'version':marker,'method':'Tính giờ riêng cho lập/sửa biểu mẫu, sản xuất báo cáo kỳ và kiểm duyệt/trình báo cáo; mỗi mã công việc tính ở đúng một chức danh.',
 'caution':'Định mức kiểm biểu mẫu sửa đổi và 90 phút kiểm báo cáo tuần của Trưởng phòng là giả định lập kế hoạch, phải kiểm chứng trên báo cáo thật trước nghiệm thu định biên.',
 'sourceOfTruth':'model.work cho vận hành; model.docs cho soạn, kiểm và duy trì bộ mẫu; không cộng một lượt sử dụng biểu mẫu vào giờ chỉnh biểu mẫu.',
 'templateReviewMinutes':template_review_minutes,'templateReviewChanges':changed,
 'reportOperations':report_ops,'coverage':coverage,'rolesInspected':len(roles),
 'reportLinesInspected':len(report_ops),'documentsInspected':len(docs),
 'uncoveredReportingRoles':[rid for rid,n in coverage.items() if n==0],
 'uncertainty':'Các đầu ra không có chữ báo cáo không tự động bị kết luận là thiếu nghĩa vụ báo cáo; kiểm lại MTCV và người nhận dữ liệu tại cơ sở.'
}
s=s[:m.start(2)]+json.dumps(D,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+s[m.end(2):]

# Insert a concise visible distinction and a drill-down by the role already selected in the document panel.
anchor='function docsPanel(){'
if s.count(anchor)!=1:raise SystemExit('Cannot find unique reporting panel insertion point')
add=r"""/* tth-report-governance-audit-2027 */
function reportCheck2027(){
 const data=model.reporting_governance_2027,role=u.role;
 const related=data.reportOperations.filter(x=>x.role===role);
 const periods={w:'Mỗi tuần',m:'Mỗi tháng',q:'Mỗi quý',qs:'Đầu quý',y12:'Tháng 12',y9:'Tháng 9', '2w':'Hai tuần/lần'};
 const tab=related.map(x=>[
  '<b>'+e(x.title)+'</b><small>'+e(x.ref)+'</small>',
  e(name(x.role)),
  (typeof x.qty==='number'?format(x.qty,0):e(model.drivers[String(x.qty).replace(/^@/,'')]||x.qty))+' / '+e(periods[x.period]||x.period),
  nu(x.minutes/60,2)+' giờ/lượt',
  e(x.note)
 ]);
 const note='<p class="note"><b>0,7 giờ kiểm chuẩn trong danh mục là giờ sửa BIỂU MẪU, không phải giờ đọc báo cáo đã điền.</b> Thời gian lập báo cáo, đối soát nguồn, kiểm của cấp quản lý, giải trình và trình lãnh đạo phải lấy từ các đầu ra vận hành riêng. Giờ kiểm BM-2 của Trưởng phòng vừa bổ sung 1,5 giờ/tuần là giả định cần đo lại.</p>';
 const matrix=tab.length?table(['Đầu ra và căn cứ','Chức danh tính giờ','Sản lượng/kỳ','Giờ cho một lượt','Phạm vi không cộng trùng'],tab):'<p>Chưa có đầu ra mang tính chất báo cáo riêng trong bảng vận hành của chức danh này. Cần đối chiếu nghĩa vụ cung cấp dữ liệu theo MTCV, không tự phân công sang chức danh khác.</p>';
 return note+detail('Đối soát tải báo cáo thực tế của '+e(name(role))+' ('+related.length+' dòng)',matrix+'<p class="fine">'+e(data.caution)+'</p>',false)
   +'<p class="fine">Đã duyệt danh mục vận hành của '+format(data.rolesInspected,0)+' chức danh; phát hiện '+format(data.reportLinesInspected,0)+' đầu ra/bước có tính chất báo cáo, đối soát hoặc phân tích. Số dòng không phải số báo cáo cần lập thêm; từng công đoạn chỉ hạch toán theo người trực tiếp thực hiện.</p>';
}
"""
s=s.replace(anchor,add+anchor,1)
anchor='+positionDocuments(r)+issuancePlan(r)+'
if s.count(anchor)!=1:raise SystemExit('Cannot find unique document panel composition')
s=s.replace(anchor,'+reportCheck2027()+positionDocuments(r)+issuancePlan(r)+',1)
# Document-stage label indicates explicitly that review minutes are about the template.
anchor="'Kiểm chuẩn độc lập',d.reviewer"
if s.count(anchor)!=1:raise SystemExit('Cannot identify document template review stage')
s=s.replace(anchor,"'Kiểm chuẩn phiên bản mẫu',d.reviewer",1)
# Audit acceptance: all figures in the original operation register stay unchanged except one explicit reviewer line.
if s.count(marker)<2:raise SystemExit('Missing reporting patch markers')
p.write_text(s,'utf-8')
print('PASS: 26 roles,',len(report_ops),'candidate reporting rows, 8 complex template profiles, and separate BM-2 executive check')
