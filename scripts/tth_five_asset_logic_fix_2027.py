#!/usr/bin/env python3
import sys,re,json
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
changed={}
def patch(name,fn):
 p=root/name/'index.html'
 if not p.exists():raise SystemExit('Missing '+str(p))
 a=p.read_text('utf8'); b=fn(a)
 if a!=b:p.write_text(b,'utf8')
 changed[name]=(a!=b,len(b))
def slide(s):
 return s.replace('Duyệt toàn bộ sản phẩm hoặc chi phí.','Không mặc nhiên duyệt toàn bộ sản phẩm hoặc chi phí; nghiệm thu không phải quyền duyệt phát hành hoặc duyệt chi.').replace('Phát ngôn, ký hợp đồng hoặc trực tiếp ra lệnh nhân viên cơ sở.','Không mặc nhiên được phát ngôn, ký hợp đồng hoặc trực tiếp ra lệnh nhân viên cơ sở.').replace('Duyệt phát hành, duyệt chi hay quản lý kênh số toàn hệ thống.','Không tự duyệt phát hành, duyệt chi hay quản lý kênh số toàn hệ thống khi chưa có phân quyền.')
def khung(s):
 pairs=[('giảm 03 người, 8%','giảm 01 suất, khoảng 2,7%'),('so với 35 người hiện có: giảm 01','so với 35 người hiện có: tăng 01'),('Tổng công ty 21, cơ sở 13','Tổng công ty 22, cơ sở 14'),('Tổng công ty 21; Marketing cơ sở 13','Tổng công ty 22; Marketing cơ sở 14'),('Tổng công ty 21, Marketing cơ sở 13, tổng 34','Tổng công ty 22, Marketing cơ sở 14, tổng 36')]
 for a,b in pairs:s=s.replace(a,b)
 return s
def crm(s):
 m=re.search(r'const flows\s*=\s*(\[.*?\]);',s,re.S)
 if not m:return s
 flows=json.loads(m.group(1))
 for f in flows:
  ids={n['id'] for n in f['nodes']}
  if f['name'].startswith('02') and 'm' not in ids:
   f['nodes'].append(dict(id='m',c=5,r=4,title='Chưa liên kết HIS – chờ xác minh',kind='end',info='Hồ sơ CRM độc lập; có chủ và hạn xác minh',rule='Không hợp nhất hồ sơ bệnh án',out='Trạng thái chờ xác minh'))
   for n in f['nodes']:
    if n['id']=='l':n.update(title='Đã xác minh liên kết HIS',out='Liên kết có căn cứ')
   for e in f['edges']:
    if e['a']=='k' and e['b']=='l':e['b']='m'
  if f['name'].startswith('03') and 'p' not in ids:
   f['nodes'].append(dict(id='p',c=5,r=4,title='Chưa giải quyết – ticket vẫn mở',kind='end',info='Giữ chủ việc và SLA; chờ phối hợp hoặc xác minh',rule='Chuyển tuyến không phải đóng việc',out='Đang xử lý / chờ xác nhận'))
   for e in f['edges']:
    if e['a']=='j' and e['b']=='m':e['label']='Đủ điều kiện'
   f['edges'].append(dict(a='j',b='p',label='Chưa đủ',kind='exception'))
  if f['name'].startswith('04') and 'o' not in ids:
   for n in f['nodes']:
    if n['id']=='n':n.update(title='Đóng ticket có bằng chứng',out='Đã đóng')
   f['nodes'] += [dict(id='o',c=5,r=3,title='Đủ điều kiện đóng?',kind='decision',info='Đối chiếu kết quả, bằng chứng và quyền',rule='Không đóng nếu chưa hoàn tất',out='Chốt trạng thái'),dict(id='p',c=6,r=4,title='Giữ ticket mở có chủ',kind='end',info='Chờ khách/chờ phối hợp/đang xử lý',rule='SLA vẫn hiệu lực',out='Chưa hoàn tất')]
   for e in f['edges']:
    if e['a']=='m' and e['b']=='n':e['b']='o'
   f['edges'] += [dict(a='o',b='n',label='Đủ',kind='normal'),dict(a='o',b='p',label='Chưa đủ',kind='exception')]
 return s[:m.start()]+'const flows='+json.dumps(flows,ensure_ascii=False,separators=(',',':'))+';'+s[m.end():]
def pages(s,scriptid):
 p=r'(<script\s+(?:id="'+scriptid+r'"\s+type="application/json"|type="application/json"\s+id="'+scriptid+r'")>)(.*?)(</script>)'
 m=re.search(p,s,re.S)
 if not m:return s
 data=json.loads(m.group(2))
 for name,h in data.items():
  if scriptid=='pagesData' and name in ('Main.html','HeThongYTe.html','Truc_TTHClinic.html'):
   for base in ('TTHKheTre','TTHALuoi'):
    a='Microsite_'+base+'.html';b='Microsite_'+base+'_DayDu.html'
    if b in data:h=h.replace('href="'+a+'"','href="'+b+'"').replace("href='"+a+"'","href='"+b+"'")
  if name.startswith(('DatLich_','Web_DatLich')) and 'data-tth-flow-not-live' not in h:
   label='<div data-tth-flow-not-live="1" role="status" style="padding:10px;background:#fff7e8;border:1px solid #e6ceaa;color:#6d3600;font:600 13px Arial">Giao diện mô phỏng: chưa xác nhận lịch thực tế từ HIS; không dùng thay phiếu hẹn.</div>'
   h=re.sub(r'(<body[^>]*>)',lambda x:x.group(1)+label,h,count=1,flags=re.I)
  data[name]=h
 value=json.dumps(data,ensure_ascii=True,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
 return s[:m.start(2)]+value+s[m.end(2):]
patch('khung-marketing',khung);patch('trinh-chieu-marketing',slide);patch('crm-da-kenh',crm)
patch('healthcare-app',lambda s:pages(s,'pageData'))
patch('healthcare-website',lambda s:pages(s,'pagesData'))
(root/'logic-check-19112026.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),'utf8')
print('TTH_5_LOGIC_FIX',changed)
