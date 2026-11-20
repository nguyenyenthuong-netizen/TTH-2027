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
 if 'id="tth-hotline-popup-2027"' not in doc:raise SystemExit('Missing native Hotline popup '+name)
 if '</head>' not in doc or '</body>' not in doc:raise SystemExit('Broken Website page '+name)
 pages[name]=doc.replace('</head>',css+'</head>',1).replace('</body>',script+'</body>',1)
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
