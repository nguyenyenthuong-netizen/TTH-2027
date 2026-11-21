"""Release checks for the reporting-hour governance and full-width reader.
Checks both data and embedded JavaScript, not only the source patch marker.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import json,re,subprocess,sys
s=(Path(sys.argv[1])/'khung-marketing'/'index.html').read_text('utf-8')
m=re.search(r'<script id="csdl" type="application/json">(.*?)</script>',s,re.S)
assert m,'Missing model'
D=json.loads(m.group(1));model=D['dinh_bien_theo_dau_ra_2027']
work=model['work'];docs=model['docs'];rg=model['reporting_governance_2027']
assert rg['rolesInspected']==len(model['roles'])==26
assert len({x['id'] for x in work})==len(work)
assert sum(1 for w in work if w['id']=='tp/bc-tuan-kiem')==1
assert sum(1 for w in work if w['id']=='dl-1/tuan')==1
tp=next(w for w in work if w['id']=='tp/bc-tuan-kiem')
assert tp['role']=='tp' and tp['period']=='w' and sum(tp['t'])==90
assert next(w for w in work if w['id']=='dl-1/tuan')['t']==[120,50,30,0,0]
for key,minutes in rg['templateReviewMinutes'].items():
    matching=[d for d in docs if d['code']==key and not d.get('link')]
    assert len(matching)==1 and matching[0]['profile'][2]==minutes,(key,len(matching))
assert all(any(w['role']==r for w in work) for r in model['roles'])
assert rg['reportLinesInspected']==len(rg['reportOperations'])
assert {x['role'] for x in rg['reportOperations']}<=set(model['roles'])
assert sum(model['seats'].values())==36
assert 'Mở rộng bảng' in s and 'reader-wide' in s and 'data-wide="toggle"' in s
assert 'reportCheck2027()' in s and 'Kiểm chuẩn phiên bản mẫu' in s
script=re.search(r'<script id="tth-staffing-app">(.*?)</script>',s,re.S)
assert script,'Missing embedded JS'
with TemporaryDirectory() as d:
    src=Path(d)/'staffing.js'
    src.write_text(script.group(1),'utf-8')
    c=subprocess.run(['node','--check',str(src)],capture_output=True,text=True)
    assert c.returncode==0,c.stderr
# Confirm the row is traced only once and template work remains separate from filled-report work.
assert 'BM-2' in tp['ref'] and tp['id'] not in {d['id'] for d in docs}
print('PASS: full JS parse, 26 roles, 36 positions, one TP BM-2 reviewer, distinct templates, accessible wide view')
print('REPORT_METRICS:',json.dumps({'reporting_lines':len(rg['reportOperations']),'without_independent_reporting':rg['uncoveredReportingRoles'],'template_profiles':rg['templateReviewMinutes']},ensure_ascii=False))
