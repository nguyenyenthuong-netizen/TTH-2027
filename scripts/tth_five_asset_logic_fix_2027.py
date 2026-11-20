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
  # Font rules belong to the actual website/app documents inside srcdoc,
  # not merely to the surrounding HTML iframe wrapper.
  if 'id="tth-embedded-vietnamese-font-2027"' not in h:
   font_css='''<style id="tth-embedded-vietnamese-font-2027">
html,body,button,input,select,textarea,h1,h2,h3,h4,h5,h6,p,li,td,th,label{
 font-family:Arial,"Segoe UI",Tahoma,"DejaVu Sans",sans-serif!important
}
html{font-size:16px}
body{font-size:16px;line-height:1.5;text-rendering:optimizeLegibility}
button,input,select,textarea{font-size:inherit}
</style>'''
   if re.search(r'</head\s*>',h,re.I):
    h=re.sub(r'</head\s*>',lambda m:font_css+m.group(0),h,count=1,flags=re.I)
   elif re.search(r'<body\b',h,re.I):
    h=re.sub(r'(<body\b[^>]*>)',lambda m:m.group(0)+font_css,h,count=1,flags=re.I)
   else:h=font_css+h
  data[name]=h
 value=json.dumps(data,ensure_ascii=True,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
 return s[:m.start(2)]+value+s[m.end(2):]
patch('khung-marketing',khung);patch('trinh-chieu-marketing',slide);patch('crm-da-kenh',crm)
patch('healthcare-app',lambda s:pages(s,'pageData'))
patch('healthcare-website',lambda s:pages(s,'pagesData'))

# Final published slide is assembled from pages-overrides/2027-1911-final,
# which has legacy CSS hiding its native controls. Restore AFTER all overrides
# and after the organizational-tree slide has been inserted.
def restore_slide_navigation(s):
 if 'id="tth-slide-controls-restored-2027"' in s:return s
 if 'id="controls"' not in s or 'id="overview"' not in s or 'id="fullscreen"' not in s:
  raise ValueError('Missing native slide navigation DOM; do not add duplicate controls')
 if '<div class="progress"><div class="bar"></div></div>' not in s:
  raise ValueError('Missing native progress bar')
 s=s.replace('<div class="progress"><div class="bar"></div></div>',
  '<div class="progress"><div class="bar"></div><input type="range" id="slideScrubber" min="1" max="28" value="1" step="1" aria-label="Kéo thanh ngang để chuyển trang slide" title="Kéo để chọn trang slide"></div>',1)
 css='''<style id="tth-slide-controls-restored-2027">
:root{--tth-slide-nav-h:76px}
html,body{overflow:hidden!important}
#viewport{inset:0 0 var(--tth-slide-nav-h) 0!important;left:0!important;right:0!important;
 width:100vw!important;height:calc(100dvh - var(--tth-slide-nav-h))!important}
#controls.controls{display:flex!important;visibility:visible!important;opacity:1!important;
 position:fixed!important;top:auto!important;bottom:0!important;left:0!important;right:0!important;
 width:100%!important;height:var(--tth-slide-nav-h)!important;min-height:var(--tth-slide-nav-h)!important;
 z-index:1200!important;box-sizing:border-box!important;background:#0837A1!important;
 border:0!important;border-top:3px solid #ED3237!important;padding:10px 18px!important;
 gap:12px!important;flex-wrap:nowrap!important;align-items:center!important;
 justify-content:center!important}
#controls button{display:inline-flex!important;align-items:center!important;justify-content:center!important;
 visibility:visible!important;opacity:1!important;flex:0 0 auto!important;
 min-width:85px!important;min-height:40px!important;height:40px!important;
 font-size:15px!important;line-height:1.2!important;white-space:normal!important;
 padding:7px 13px!important}
#controls #counter{display:block!important;color:white!important;min-width:65px!important;
 font-size:15px!important;text-align:center!important}
#controls .progress{position:relative!important;display:flex!important;align-items:center!important;
 min-width:96px!important;max-width:430px!important;width:auto!important;flex:1 1 300px!important;
 height:26px!important;background:transparent!important;overflow:visible!important}
#controls .progress .bar{position:absolute!important;left:0!important;top:11px!important;height:5px!important;
 max-width:100%!important;border-radius:4px!important;background:#ED3237!important;pointer-events:none!important}
#slideScrubber{appearance:none;-webkit-appearance:none;position:relative;z-index:1;
 margin:0;width:100%;height:28px;background:transparent;cursor:pointer;touch-action:pan-x}
#slideScrubber::-webkit-slider-runnable-track{height:6px;border-radius:7px;background:rgba(255,255,255,.52)}
#slideScrubber::-moz-range-track{height:6px;border-radius:7px;background:rgba(255,255,255,.52)}
#slideScrubber::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:20px;height:20px;
 margin-top:-7px;border-radius:50%;border:3px solid white;background:#ED3237;box-shadow:0 1px 5px #00285a}
#slideScrubber::-moz-range-thumb{width:15px;height:15px;border-radius:50%;
 border:3px solid white;background:#ED3237}
#controls .help{display:none!important}
.tth-floating-arrows{display:none!important;visibility:hidden!important}
#index.index{bottom:var(--tth-slide-nav-h)!important;z-index:1100!important}
.slide .head h2{font-size:35px!important;line-height:1.14!important}
.slide .head p{font-size:18px!important;line-height:1.31!important}
.slide .card h3{font-size:22px!important;line-height:1.17!important}
.slide .card .bodycopy{font-size:20px!important;line-height:1.35!important}
.slide .pt b{font-size:19px!important}.slide .pt span{font-size:18px!important}
.slide .card .muted,.slide .line p{font-size:17px!important}
.slide .tagrow span{font-size:16px!important}
.slide .tth-tree-chief span,.slide .tth-tree-node span{font-size:16px!important}
.slide .tth-tree-node small{font-size:14px!important}
.slide .content{overflow-y:auto!important;overflow-x:hidden!important;scrollbar-width:thin}
.slide .content .card{overflow-y:auto!important;overscroll-behavior:contain;scrollbar-width:thin}
@media(max-width:920px){
 #controls.controls{gap:7px!important;padding:8px!important}
 #controls button{font-size:13px!important;min-width:68px!important;padding:6px 8px!important}
 #controls .progress{flex-basis:120px!important}
}
@media(max-width:620px){
 :root{--tth-slide-nav-h:112px}
 #controls.controls{display:grid!important;
 grid-template-columns:repeat(4,minmax(0,1fr))!important;grid-template-rows:49px 30px!important;
 gap:5px 7px!important;padding:9px 10px!important;align-content:center!important}
 #controls button{width:100%!important;min-width:0!important;min-height:44px!important;
 height:46px!important;font-size:12.5px!important;padding:4px 3px!important}
 #controls #prev{grid-column:1;grid-row:1}#controls #next{grid-column:2;grid-row:1}
 #controls #overview{grid-column:3;grid-row:1}#controls #fullscreen{grid-column:4;grid-row:1}
 #controls #counter{grid-column:1;grid-row:2;min-width:0!important}
 #controls .progress{grid-column:2/span 3;grid-row:2;min-width:0!important;
 width:100%!important;max-width:none!important}
 #index.index{padding:16px!important}
 #index .index-list{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))!important}
}
@media print{#controls.controls{display:none!important}
 #viewport{position:static!important;width:100%!important;height:auto!important}}
</style>'''
 js='''<script id="tth-slide-scrubber-2027">
(function(){
 const scrub=document.getElementById('slideScrubber');
 const stage=document.getElementById('stage');
 if(!scrub||!stage)return;
 const list=[...stage.querySelectorAll('.slide')];
 scrub.max=String(list.length);
 function sync(){
  const index=list.findIndex(x=>x.classList.contains('active'));
  const current=index<0?1:index+1;
  scrub.value=String(current);
  scrub.setAttribute('aria-valuetext',String(current)+' / '+list.length);
 }
 scrub.addEventListener('input',function(){if(typeof show==='function')show(Number(scrub.value)-1);sync()});
 scrub.addEventListener('change',sync);
 new MutationObserver(sync).observe(stage,{subtree:true,attributes:true,attributeFilter:['class']});
 window.addEventListener('hashchange',sync);
 sync();
})();
</script>'''
 if '</head>' not in s or '</body>' not in s:raise ValueError('Invalid slide document')
 s=s.replace('</head>',css+'</head>',1)
 s=s.replace('</body>',js+'</body>',1)
 for q in ('id="overview"','id="fullscreen"','id="slideScrubber"','id="tth-slide-scrubber-2027"'):
  if q not in s:raise ValueError('Restored slide control missing '+q)
 return s
patch('trinh-chieu-marketing',restore_slide_navigation)

(root/'logic-check-19112026.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),'utf8')
print('TTH_5_LOGIC_FIX',changed)
