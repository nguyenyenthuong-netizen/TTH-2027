#!/usr/bin/env python3
"""Website only: Hotline popup without navigation; card, button and media proportions."""
import re,json,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
path=root/'healthcare-website'/'index.html'
source=path.read_text('utf-8')
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',source,re.I|re.S)
if not m:raise SystemExit('Website pagesData missing')
pages=json.loads(m.group(2))

popup_html=r'''<aside id="tth-hotline-popup-2027" role="dialog" aria-modal="false" aria-label="Hotline các cơ sở" aria-hidden="true" hidden>
<section class="tth-hotline-card" aria-label="Hotline">
<div class="tth-hotline-head"><h2>Hotline</h2><button type="button" aria-label="Đóng" title="Đóng cửa sổ">×</button></div>
<div class="tth-hotline-row"><div><strong>Tổng đài TTH Healthcare</strong><small>Tư vấn, đặt lịch toàn hệ thống</small></div><div class="tth-hotline-numbers"><a href="tel:19002675">1900 2675</a></div></div>
<div class="tth-hotline-row"><div><strong>Bệnh viện Đa khoa TTH Vinh</strong><small>Đặt lịch, chăm sóc khách hàng</small></div><div class="tth-hotline-numbers"><a href="tel:0948956622">0948 956 622</a><a class="emergency" href="tel:0976295115">Cấp cứu 0976 295 115</a></div></div>
<div class="tth-hotline-row"><div><strong>Bệnh viện Đa khoa TTH Hà Tĩnh</strong><small>Đặt lịch</small></div><div class="tth-hotline-numbers"><a href="tel:0911929192">0911 92 91 92</a></div></div>
<div class="tth-hotline-row"><div><strong>Bệnh viện Đa khoa TTH Quảng Bình</strong><small>Đặt lịch</small></div><div class="tth-hotline-numbers"><a href="tel:0967260115">0967 260 115</a><a class="emergency" href="tel:0857867222">Cấp cứu 0857 867 222</a></div></div>
<div class="tth-hotline-row"><div><strong>Khám sức khỏe doanh nghiệp</strong><small>Tư vấn gói khám theo đơn vị</small></div><div class="tth-hotline-numbers"><a href="tel:19002675">1900 2675</a></div></div>
<div class="tth-hotline-actions"><a href="HuongDan_DatLich.html">Hướng dẫn đặt lịch</a><a href="HuongDan_LienHe.html">Gửi yêu cầu liên hệ</a></div>
<p class="tth-hotline-emergency"><a href="TienIch_CapCuu.html">Cần cấp cứu? Gọi 115 hoặc xem số cấp cứu từng bệnh viện</a></p>
<p class="tth-hotline-note">Thông tin liên hệ theo bản giao diện đã cung cấp; các nghiệp vụ chưa kết nối CRM/HIS không tự tạo yêu cầu hoặc lịch hẹn.</p>
</section></aside>'''
popup_style=r'''<style id="tth-hotline-native-popup-layout-2027">
#tth-hotline-popup-2027[hidden]{display:none!important}
#tth-hotline-popup-2027{position:fixed!important;top:50%!important;left:50%!important;
 transform:translate(-50%,-50%)!important;z-index:2147483400!important;
 width:min(490px,calc(100vw - 24px))!important;max-height:min(82dvh,740px)!important;
 overflow-y:auto!important;overflow-x:hidden!important;background:#fff!important;
 box-sizing:border-box!important;border-radius:18px!important;border:1px solid #DAE4F3!important;
 box-shadow:0 16px 48px rgba(8,36,82,.2)!important;scrollbar-width:thin!important}
#tth-hotline-popup-2027 .tth-hotline-card{box-sizing:border-box;padding:22px 24px!important;
 margin:0!important;max-width:100%!important;width:100%!important;background:white!important;
 font:14px/1.45 Arial,sans-serif;color:#14213D}
#tth-hotline-popup-2027 .tth-hotline-head{display:flex;align-items:center;justify-content:space-between;
 gap:14px;margin-bottom:12px}
#tth-hotline-popup-2027 .tth-hotline-head h2{color:#0837A1;font-size:26px;margin:0;font-weight:800}
#tth-hotline-popup-2027 .tth-hotline-head button{border:1px solid #3F8CFF;background:#fff;
 border-radius:50%;width:42px;height:42px;flex:0 0 42px;cursor:pointer;font-size:21px}
#tth-hotline-popup-2027 .tth-hotline-row{display:grid;grid-template-columns:minmax(0,1fr) auto;
 align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid #E5ECF8}
#tth-hotline-popup-2027 strong{font-weight:650;font-size:14px}
#tth-hotline-popup-2027 small{display:block;font-size:12px;color:#53627A;margin-top:2px}
#tth-hotline-popup-2027 .tth-hotline-numbers{display:flex;flex-direction:column;
 align-items:flex-end;gap:3px;white-space:nowrap}
#tth-hotline-popup-2027 .tth-hotline-numbers a{color:#0837A1;font-weight:700;text-decoration:none}
#tth-hotline-popup-2027 .tth-hotline-numbers .emergency{color:#C71622;font-size:12px}
#tth-hotline-popup-2027 .tth-hotline-actions{display:flex;flex-wrap:wrap;gap:10px;padding:16px 0}
#tth-hotline-popup-2027 .tth-hotline-actions a{background:#0837A1;color:white;
 display:inline-flex;align-items:center;justify-content:center;flex:1 1 170px;min-height:42px;
 padding:9px 13px;border-radius:9px;text-align:center;text-decoration:none;
 font-size:13px;font-weight:700;line-height:1.3}
#tth-hotline-popup-2027 .tth-hotline-emergency{margin:0;padding:10px 12px;border-radius:10px;
 background:#FEF0F0;text-align:center}
#tth-hotline-popup-2027 .tth-hotline-emergency a{color:#B3141B;text-decoration:none;font-size:12px;font-weight:700}
#tth-hotline-popup-2027 .tth-hotline-note{font-size:11px;color:#5B6880;line-height:1.4;margin:10px 0 0}
@media(max-width:520px){
 #tth-hotline-popup-2027{max-height:calc(100dvh - 22px)!important}
 #tth-hotline-popup-2027 .tth-hotline-card{padding:15px!important}
 #tth-hotline-popup-2027 .tth-hotline-row{grid-template-columns:minmax(0,1fr);gap:4px}
 #tth-hotline-popup-2027 .tth-hotline-numbers{align-items:flex-start}
}
</style>'''

css=r'''<style id="tth-balanced-card-layout-2027">
#app main [style*="grid-template-columns"]:has(> article.card){
 align-items:start!important;grid-auto-rows:max-content!important
}
#app main article.card{min-width:0!important;max-width:100%!important;
 height:auto!important;align-self:start!important}
#app main article.card img{max-width:100%!important;object-fit:cover!important}
#app main article.card img[alt*="16:9"],
#app main article.card img[alt*="Ảnh video"],
#app main article.card img[alt*="Ảnh chương trình"]{
 width:100%!important;height:auto!important;aspect-ratio:16/9!important;
 max-height:230px!important;object-fit:cover!important;object-position:center!important}
#app main article.card img[alt*="chân dung"]{
 width:100%!important;height:clamp(170px,17vw,220px)!important;
 object-fit:cover!important;object-position:center 26%!important}
#app main .btn,#app main .btn2,#app main .btns{
 display:inline-flex!important;align-items:center!important;justify-content:center!important;
 gap:7px!important;box-sizing:border-box!important;min-height:44px!important;
 max-width:100%!important;text-align:center!important;line-height:1.35!important;
 vertical-align:middle!important;white-space:normal!important}
#app main .btn svg,#app main .btn2 svg,#app main .btns svg{flex-shrink:0!important}
@media(min-width:1080px){
 #app main [style*="grid-template-columns"]:has(> article.card){
  grid-template-columns:repeat(auto-fill,minmax(min(100%,255px),345px))!important;
  justify-content:start!important;gap:clamp(14px,1.1vw,22px)!important}
 #app main [style*="grid-template-columns"]:has(> article.card img[alt*="chân dung"]){
  grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),275px))!important}
}
@media(max-width:740px){
 #app main [style*="grid-template-columns"]:has(> article.card){
  grid-template-columns:repeat(auto-fit,minmax(min(100%,245px),1fr))!important}
 #app main article.card img[alt*="16:9"],#app main article.card img[alt*="Ảnh video"],
 #app main article.card img[alt*="Ảnh chương trình"]{max-height:220px!important}
}
</style>'''
script=r'''<script id="tth-hotline-nav-interlock-2027">
(function(){'use strict';
function popup(show){
 const box=document.getElementById('tth-hotline-popup-2027');if(!box)return;
 box.hidden=!show;box.setAttribute('aria-hidden',show?'false':'true');
 document.querySelectorAll('a[href="TienIch_Hotline.html"]').forEach(a=>a.setAttribute('aria-expanded',String(show)));
 if(show){const close=box.querySelector('[aria-label="Đóng"]');if(close)close.focus({preventScroll:true});}
}
window.addEventListener('message',ev=>{
 if(ev.source!==window.parent||!ev.data||ev.data.type!=='TTH_WEBSITE_OPEN_HOTLINE')return;
 popup(true);
});
window.addEventListener('click',ev=>{
 const n=ev.target instanceof Element?ev.target:null;
 if(n&&n.closest('#tth-hotline-popup-2027 [aria-label="Đóng"]')){
  ev.preventDefault();ev.stopImmediatePropagation();popup(false);
 }
},true);
window.addEventListener('keydown',ev=>{
 const b=document.getElementById('tth-hotline-popup-2027');
 if(ev.key==='Escape'&&b&&!b.hidden){ev.preventDefault();ev.stopImmediatePropagation();popup(false);}
},true);
})();
</script>'''
count=0
for name,doc in pages.items():
 if 'id="app"' not in doc or 'class="gh"' not in doc:continue
 if 'tth-balanced-card-layout-2027' in doc:raise SystemExit('Repeated layout patch '+name)
 if 'id="tth-hotline-popup-2027"' not in doc:doc=doc.replace('</body>',popup_html+'</body>',1)
 if '</head>' not in doc or '</body>' not in doc:raise SystemExit('Broken Website page '+name)
 pages[name]=doc.replace('</head>',css+popup_style+'</head>',1).replace('</body>',script+'</body>',1)
 count+=1
if count<100:raise SystemExit('Unexpected public page count '+str(count))
packed=json.dumps(pages,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
source=source[:m.start(2)]+packed+source[m.end(2):]
needle="function go(target,historyUpdate){const route=String(target||'Main.html'),name=route.split(/[?#]/)[0].split('/').pop();"
if source.count(needle)!=1:raise SystemExit('Wrapper route dispatcher changed; manual review required')
guard="""if(name==='TienIch_Hotline.html'){
 const show=()=>frame.contentWindow.postMessage({type:'TTH_WEBSITE_OPEN_HOTLINE'},'*');
 if(!frame.srcdoc){frame.addEventListener('load',show,{once:true});go('Main.html',false);}
 else show();
 return;
}"""
source=source.replace(needle,needle+guard,1)
path.write_text(source,'utf-8')
print('WEBSITE_HOTLINE_LAYOUT','pages',count,'popup_without_route',True,'no_backdrop',True,'card_width_cap',345,'image_aspect',True,'buttons_centered',True)
