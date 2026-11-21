"""Mục 05: kiểm toán nguồn tải theo CNNV/MTCV, đầu ra, công đoạn và giờ.
Mục tiêu: chỉ ra rủi ro không tính/nhân đôi, không tự động cắt giờ hoặc đánh dấu đã nghiệm thu.
Chạy SAU khung_reporting_governance_2027.py trên bản HTML đã dựng.
"""
from pathlib import Path
from collections import Counter, defaultdict
from html import escape
import json, re, sys

p=Path(sys.argv[1])/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
marker="tth-mkt-dedup-scope-audit-2027"
if marker in s:
    print("PASS DEDUP AUDIT: already present")
    raise SystemExit(0)
source_rx=re.compile(r'(<script id="csdl" type="application/json">)([\s\S]*?)(</script>)')
m=source_rx.search(s)
assert m, "Missing embedded data"
db=json.loads(m.group(2))
model=db["dinh_bien_theo_dau_ra_2027"]
roles=model["roles"]
works=model["work"]
docs=model["docs"]
jd=model["jd"]
links=model["crosswalk"]
assert len(roles)==len(jd)==len(links)==26
assert len({w["id"] for w in works})==len(works)

# A link from one MTCV clause into a costed work item is not itself a time entry.
# Some source rows legitimately reference the same deliverable, with distinct expected evidence.
rows=[]
status=Counter()
for rid in roles:
    clauses=links[rid]
    source=jd[rid]
    assert len(clauses)==len(source)-1,(rid,len(clauses),len(source))
    for n,record in enumerate(clauses,1):
        target,note=record
        isdoc=target.startswith("@")
        match=[d for d in docs if d["code"]==target[1:]] if isdoc else [w for w in works if w["id"]==target]
        # Boundary crosswalk entries can point at another role or a non-costed future role;
        # do not silently accept broken references as verified.
        valid=bool(match) or target in roles or target in ("dl-2", "qlml")
        state="Có điểm đối chiếu, cần kiểm chứng phạm vi/giờ" if valid else "Thiếu dòng định mức hoặc chứng từ phân tuyến"
        if ("chưa xác nhận" in str(note).lower() or not valid):state="Chưa xác minh bao phủ công đoạn"
        status[state]+=1
        rows.append({"role":rid,"line":n,"ref":target,"sourceText":str(source[n][0])[:180] if source[n] else "",
            "workLinked":bool(match),"type":"Danh mục mẫu" if isdoc else "Vận hành/MTCV","status":state,"evidence":str(note)[:230]})
assert all(x["workLinked"] or x["ref"] in roles for x in rows),(sum(1 for x in rows if x["workLinked"]),len(rows))

# Detect *candidates*, not duplicate proofs. Reusing BM-10 by different steps is legitimate.
token_rx=re.compile(r'(?<![A-Z0-9])(?:BM|SO|HS|DM|QC|DS|B)-\d+\b')
refgroups=defaultdict(list)
for w in works:
    for code in set(token_rx.findall(w["ref"])):
        refgroups[(w["role"],code,w["period"])].append(w)
candidates=[]
for (rid,code,period),vals in sorted(refgroups.items()):
    if len(vals)<2:continue
    candidates.append({"role":rid,"ref":code,"period":period,"ids":[v["id"] for v in vals],
        "titles":[v["name"] for v in vals],
        "issue":"Các bước có cùng mã biểu mẫu; xác nhận mỗi mã việc và công đoạn không hạch toán hai lần"})
# Some sources are not tasks held by Marketing, not omissions.
contracts=[z for f in db["quy_trinh"] for b in f["buoc"] for z in b["doi_soat_tung_dau_ra_2027"]]
assert len(contracts)==568
marketing=0;outside=0;unverified=0
perroleworkflow=Counter()
for z in contracts:
    owner=str(z.get("chu_tri_01",""))
    if owner in roles: marketing+=1;perroleworkflow[owner]+=1
    else: outside+=1
    evidence=" ".join(str(z.get(k,"")) for k in ("can_cu_phan_vai_2027","trang_thai_duyet","nguon_kiem_chung"))
    if "CẦN" in evidence.upper() or "CHƯA" in evidence.upper():
        unverified+=1
# Cross-check the historical audit result without conflating 'outside 26 roles' with missing work.
assert marketing+outside==len(contracts)

# Real implementation inputs not yet grounded: retain "unknown", never assume zero.
channels=[x for x in model["cms"]["assets"] if x.get("kind")=="Kênh số"]
unverified_channels=sum(1 for x in channels if "Chưa" in str(x.get("status","")))
conditional=[w for w in works if isinstance(w["q"],(int,float)) and w["q"]==0]
perrole=[]
for rid,role in roles.items():
    rworks=[w for w in works if w["role"]==rid]
    aswriter=sum(d["writer"]==rid for d in docs)
    asreview=sum(d["reviewer"]==rid for d in docs)
    asowner=sum(d["owner"]==rid for d in docs)
    perrole.append({"id":rid,"name":role["name"],"seats":role["seats"],
      "mtcv":len(links[rid]),"operations":len(rworks),
      "docWriter":aswriter,"docReviewer":asreview,"docOwner":asowner,
      "processOutputs":perroleworkflow[rid],
      "zeroQty":sum(isinstance(w["q"],(int,float)) and w["q"]==0 for w in rworks),
      "dynamicQty":sum(not isinstance(w["q"],(int,float)) for w in rworks)})
assert len(perrole)==26
open_items=[
 {"priority":"Cao","area":"568 đầu ra quy trình","issue":"Nhiều dòng đang chờ đơn vị xác nhận phân vai, đầu vào/chứng từ và quyền duyệt. Liên kết mã chưa chứng minh tải được tính đủ.","gate":"Chủ nghiệp vụ xác nhận từng đầu ra có sản lượng, công đoạn, chủ trì và dấu vết duyệt."},
 {"priority":"Cao","area":"Khối lượng CMS website và App","issue":"Số lượng hồ sơ bác sĩ, chuyên khoa, dịch vụ, gói, sửa đổi, sử dụng lại theo đơn vị chưa có dữ liệu đã xác nhận.","gate":"Chốt số hồ sơ nguồn, lượt tái sử dụng và phần tăng thêm ngoài công việc W để tránh đếm hai lần."},
 {"priority":"Cao","area":"Kênh, tài sản và biển bảng","issue":"30 vị trí kênh là khung kiểm kê; tên miền, URL, chủ sở hữu, người vận hành, tình trạng chưa được nhận diện đủ.","gate":"Định danh theo mã tài sản, đơn vị, người sở hữu và lịch vận hành thực tế."},
 {"priority":"Cao","area":"Tải kiêm nhiệm và nhân sự thực có","issue":"Quỹ giờ người phụ trách Clinic, lịch nhận người, người giữ hai chức danh và thời gian bàn giao chưa xác nhận.","gate":"Mỗi cá nhân chỉ có một quỹ giờ; tách rõ giờ theo đơn vị và giai đoạn."},
 {"priority":"Cao","area":"Quy trình/mẫu cũ","issue":"Phương án sửa/gộp/xây mới vẫn dựa trên giả định nếu chưa thấy bản gốc và quyết định còn hiệu lực.","gate":"Đối chiếu bản gốc, cấp ban hành, phiên bản và bằng chứng áp dụng trước khi khóa giờ thiết lập."},
 {"priority":"Cao","area":"Công đoạn và giờ phối hợp","issue":"MTCV đã có liên kết tra cứu nhưng thiếu nhật ký mã việc/người/khoảng thời gian để chứng minh không tính trùng.","gate":"Khóa khóa định danh: mã việc + phiên bản + đơn vị + công đoạn + người + kỳ; đo thử thời gian."},
 {"priority":"Trung bình","area":"Giai đoạn cơ sở/thương hiệu mới","issue":"Phạm vi Winmed, Tuệ Đức Thiện, từng Clinic và cơ sở dự kiến chưa có lịch kích hoạt và khối lượng thực tế.","gate":"Chỉ kích hoạt có điều kiện, phân biệt nhu cầu hiện hành với tương lai."},
 {"priority":"Trung bình","area":"Báo cáo tuần/tháng/năm","issue":"Đã tách soạn mẫu và lập/kiểm báo cáo, nhưng giờ là ước tính và cần theo dõi sau khi sử dụng.","gate":"Đo thực tế tối thiểu một kỳ báo cáo tiêu biểu, không cộng trùng giờ kiểm."}
]
audit={
 "version":marker,"roles":len(roles),"mtcvLines":len(rows),"mtcvLinked":sum(x["workLinked"] for x in rows),
 "mtcvNeedsVerification":sum(x["status"]!="Có điểm đối chiếu, cần kiểm chứng phạm vi/giờ" for x in rows),
 "workflowOutputs":len(contracts),"workflowMarketing":marketing,"workflowExternal":outside,
 "workflowUnverifiedFlagged":unverified,"documents":len(docs),"channels":len(channels),
 "channelsUnverified":unverified_channels,"zeroQuantityConditional":len(conditional),
 "candidateOverlapGroups":len(candidates),"candidates":candidates,"perRole":perrole,
 "openItems":open_items,
 "status":"CHƯA NGHIỆM THU ĐỦ TẢI; các lượt tính không có mã công đoạn/người thực tế chưa thể chứng minh tuyệt đối không trùng.",
 "method":"Không cộng các dòng MTCV hoặc đầu ra quy trình vào quỹ giờ nếu chưa xác định công đoạn có sản lượng. Bảng W, hồ sơ mẫu và CMS là ba nguồn giờ độc lập; mọi giao nhau cần có mã hồ sơ duy nhất và điều kiện không trùng."
}
model["dedup_scope_audit_2027"]=audit
s=s[:m.start(2)]+json.dumps(db,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")+s[m.end(2):]

# Keep audit inside the existing "Căn cứ và kiểm toán" pane; avoid another nav tab.
start='<script id="tth-staffing-app">'
end='</script>'
a=s.index(start)
b=s.index(end,a)
script=s[a+len(start):b]
anchor="const panels={roadmap:"
assert script.count(anchor)==1
inject=r"""
/* tth-mkt-dedup-scope-audit-2027 */
const originalAuditPanel2027=auditPanel;
function dedupAuditPanel2027(){
 const x=model.dedup_scope_audit_2027;
 const keyRows=x.openItems.map(v=>[
   '<b>'+e(v.priority)+'</b>',
   e(v.area),e(v.issue),e(v.gate)
 ]);
 const roleRows=x.perRole.map(v=>[
   e(v.name),nu(v.mtcv,0),nu(v.operations,0),
   nu(v.docWriter,0)+' / '+nu(v.docReviewer,0),
   nu(v.processOutputs,0),nu(v.zeroQty,0),nu(v.dynamicQty,0)
 ]);
 const candRows=x.candidates.slice(0,45).map(v=>[
   e(name(v.role)),e(v.ref),e(periodName(v.period)),
   v.ids.map((id,i)=>'<b>'+e(id)+'</b> · '+e(v.titles[i])).join('<br>'),
   'Cần đối chiếu nhật ký sản phẩm/công đoạn, KHÔNG tự loại giờ'
 ]);
 const heading='<h3>Kiểm toán không trùng, không sót theo CNNV và MTCV</h3>'
   +'<p class="note"><b>Chưa thể nghiệm thu đủ tải.</b> Đã lập bảng tra '+format(x.mtcvLines,0)+' dòng MTCV của '+x.roles+' chức danh, '
   +format(x.workflowOutputs,0)+' bản ghi đầu ra quy trình. Trong đó '+format(x.workflowMarketing,0)+' bản ghi thuộc mã chức danh Marketing, '
   +format(x.workflowExternal,0)+' bản ghi thuộc vai trò/đơn vị khác; nhóm sau <b>không tự coi là việc Marketing bị bỏ sót</b>. '
   +'Các điểm trùng có thể có là <b>cảnh báo cần xác minh</b>, không tự giảm giờ để làm đẹp định biên.</p>';
 const summary=table(['Kiểm soát','Kết quả','Nguyên tắc'],[
 ['Chức danh',nu(x.roles,0),'Đối chiếu CNNV/MTCV theo đúng chức danh và người phụ trách'],
 ['Dòng MTCV tra cứu',nu(x.mtcvLines,0),'Có liên kết nhưng chưa chứng minh đã tính đủ từng bước'],
 ['Đầu ra quy trình',nu(x.workflowOutputs,0),'Không coi mỗi bước là một sản phẩm mới'],
 ['Kênh chưa xác minh',nu(x.channelsUnverified,0),'Không tự suy ra số URL đang vận hành'],
 ['Nhóm giao thoa cần xem',nu(x.candidateOverlapGroups,0),'Không tự kết luận trùng chỉ vì cùng mã biểu mẫu'],
 ['Dòng sản lượng 0 có điều kiện',nu(x.zeroQuantityConditional,0),'Chưa kích hoạt trong tải nền, không coi là không có nhiệm vụ']
 ],[1]);
 const risks=detail('Các điều kiện chưa hoàn tất trước khi chốt định biên',table(['Ưu tiên','Phạm vi','Rủi ro/thiếu căn cứ','Điều kiện khóa'],keyRows),true);
 const rolesTable=detail('Đối chiếu từng chức danh – 26 vị trí',table(['Chức danh','Dòng MTCV','Đầu việc W','Soạn/kiểm bộ mẫu','Đầu ra quy trình','Sản lượng 0','Sản lượng biến'],roleRows,[1,2,4,5,6]),false);
 const overlap=detail('Danh sách cảnh báo giao thoa cùng mã biểu mẫu ('+x.candidateOverlapGroups+' nhóm)',candRows.length?table(['Chức danh','Mã dùng chung','Chu kỳ','Nhóm việc cần phân tách công đoạn','Trạng thái'],candRows):'<p>Chưa có nhóm giao thoa theo tiêu chí mã biểu mẫu và kỳ.</p>',false);
 return heading+summary+risks+rolesTable+overlap+originalAuditPanel2027();
}
"""
script=script.replace(anchor,inject+anchor,1)
target="audit:auditPanel,full:"
assert script.count(target)==1
script=script.replace(target,"audit:dedupAuditPanel2027,full:",1)
s=s[:a+len(start)]+script+s[b:]
assert s.count(marker)==2,(s.count(marker),marker)
p.write_text(s,"utf-8")
print("PASS SCOPE/DEDUP AUDIT:",len(roles),"roles,",len(rows),"MTCV links,",marketing,"Marketing workflow rows,",outside,"other rows,",len(candidates),"overlap candidates,",len(open_items),"evidence gates")
