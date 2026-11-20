#!/usr/bin/env python3
"""Show a concrete fictional CRM-contact / HIS-patient-ID mapping in workflow 02.
Use the existing expandable 'Chú giải / kết quả' panel, not an overlay on the flow.
No medical data or real ID is created.
"""
from pathlib import Path
import sys,json
p=Path(sys.argv[1] if len(sys.argv)>1 else '_site')/'crm-da-kenh'/'index.html'
s=p.read_text('utf8')
if 'id="tth-crm-his-example-style-2027"' in s:
 raise SystemExit('CRM_HIS_EXAMPLE: duplicate patch')
old="flowDescription.innerHTML='<strong>'+escapeText(f.name)+' · '+escapeText(f.title)+'</strong><p class=\"flow-objective\">'+escapeText(f.objective)+'</p>';"
if s.count(old)!=1:
 raise SystemExit(f'CRM_HIS_EXAMPLE: missing objective renderer ({s.count(old)})')
example='''<div class="tth-his-example" aria-label="Ví dụ liên kết hồ sơ CRM và mã bệnh nhân HIS">
<div class="tth-his-example-head"><b>Ví dụ: Liên kết hồ sơ CRM với mã người bệnh HIS</b>
<small>Dữ liệu giả lập để giải thích nghiệp vụ, không phải dữ liệu bệnh nhân thật</small></div>
<div class="tth-his-mapping-grid">
<div class="tth-his-item"><small>CRM · Hồ sơ người liên hệ</small><strong>CRM-00125</strong>
<span>Người liên hệ A · đề nghị đặt khám cho người bệnh B</span></div>
<div class="tth-his-arrow" aria-hidden="true">↔</div>
<div class="tth-his-item"><small>HIS · Mã người bệnh</small><strong>BN-00876</strong>
<span>Người bệnh B · mã do HIS xác nhận tại cơ sở</span></div></div>
<p class="tth-his-success"><strong>Đủ căn cứ:</strong> người được phục vụ, thông tin định danh và quan hệ/người đại diện (nếu cần) đã được đối soát theo phân quyền. Lưu liên kết <b>CRM-00125 ↔ BN-00876</b>, người xác minh, thời điểm và nhật ký.</p>
<p class="tth-his-warning"><strong>Chưa đủ căn cứ:</strong> cùng số điện thoại liên hệ cho người bệnh khác, ví dụ <b>BN-00444</b>, thì <b>không tự gộp hoặc tự liên kết</b>. Giữ trạng thái <b>Chờ xác minh</b> và chuyển đúng đầu mối.</p>
<p class="tth-his-foot">CRM chỉ lưu mã tham chiếu và thông tin cần thiết theo quyền; HIS là nguồn xác nhận mã người bệnh, lịch và nghiệp vụ y tế. Không sao chép toàn bộ bệnh án.</p>
</div>'''
insertion=(
 old+
 "\nif(flowIndex===1){flowDescription.insertAdjacentHTML('beforeend',"+
 json.dumps(example,ensure_ascii=False)+");}\n"+
 "const metaHelp=document.getElementById('crmFlowMetaToggle');"+
 "if(metaHelp)metaHelp.textContent=flowIndex===1?'Ví dụ CRM ↔ HIS':'Chú giải / kết quả';"
)
s=s.replace(old,insertion)
css='''<style id="tth-crm-his-example-style-2027">
#s3 .tth-his-example{display:flex;flex-direction:column;gap:10px;padding:13px 15px;margin:10px 0 4px;
 border:1px solid #B9CCEB;border-top:3px solid #0837A1;border-radius:12px;background:#F8FBFF;
 color:#163861;max-width:100%;box-sizing:border-box}
#s3 .tth-his-example *{box-sizing:border-box}
#s3 .tth-his-example-head{display:flex;flex-direction:column;gap:3px}
#s3 .tth-his-example-head b{font-size:16px;line-height:1.38;color:#0837A1}
#s3 .tth-his-example-head small{font-size:12px;line-height:1.4;color:#526C8B}
#s3 .tth-his-mapping-grid{display:grid;grid-template-columns:minmax(0,1fr) 40px minmax(0,1fr);align-items:stretch;gap:9px;min-width:0}
#s3 .tth-his-item{min-width:0;display:flex;flex-direction:column;gap:4px;background:#FFF;border:1px solid #C4D5EC;
 border-radius:10px;padding:12px 13px;overflow-wrap:break-word}
#s3 .tth-his-item small{font-size:12px;color:#49688D;font-weight:800}
#s3 .tth-his-item strong{font-size:21px;color:#0939A1;letter-spacing:.02em}
#s3 .tth-his-item span{font-size:14px;line-height:1.45;color:#23476E}
#s3 .tth-his-arrow{display:grid;place-items:center;font-size:28px;font-weight:900;color:#ED3237}
#s3 .tth-his-example p{font-size:14px;line-height:1.48;margin:0;padding:9px 11px;border-radius:8px;overflow-wrap:anywhere}
#s3 .tth-his-success{background:#EAF3FC;color:#133F7B}
#s3 .tth-his-warning{background:#FFF6EE;color:#71401C}
#s3 .tth-his-example p.tth-his-foot{padding:0 2px;color:#4B6484;font-size:13px}
@media(max-width:650px){
 #s3 .tth-his-example{padding:11px}
 #s3 .tth-his-mapping-grid{grid-template-columns:minmax(0,1fr);gap:3px}
 #s3 .tth-his-arrow{font-size:22px;min-height:25px}
 #s3 .tth-his-item strong{font-size:19px}
}
</style>'''
if s.count('</head>')!=1:raise SystemExit('CRM_HIS_EXAMPLE: malformed head')
s=s.replace('</head>',css+'</head>',1)
p.write_text(s,'utf8')
print('CRM_HIS_EXAMPLE_OK: flow 02 mapping CRM-00125 to BN-00876; alternate BN-00444 unlinked without proof')
