#!/usr/bin/env python3
"""Fix public Website Hotline modal close/reopen without changing phone numbers or other assets."""
import json,re,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '_site')
file=root/'healthcare-website'/'index.html'
s=file.read_text('utf-8')
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',s,re.I|re.S)
if not m:raise SystemExit('Website pagesData missing')
pages=json.loads(m.group(2))
patch=r'''<style id="tth-hotline-close-style-2027">
[data-tth-hotline-dismissed="1"]{display:none!important}
</style>
<script id="tth-hotline-close-handler-2027">
(function(){
 "use strict";
 if(window.__TTH_HOTLINE_CLOSE_HANDLER_2027__)return;
 window.__TTH_HOTLINE_CLOSE_HANDLER_2027__=true;
 let dismissed=null;
 const visible=el=>{if(!el||!el.isConnected)return false;
  const r=el.getBoundingClientRect(),s=getComputedStyle(el);
  return r.width>8&&r.height>8&&s.display!=="none"&&s.visibility!=="hidden"&&s.opacity!=="0";};
 function findHeading(){
  for(const selector of ['h1,h2,h3,h4,h5,strong,b,[role="heading"]','div,span']){
   for(const el of document.querySelectorAll(selector)){
    if(el.textContent.trim()!=="Hotline"||!visible(el))continue;
    if(el.children.length&&[...el.children].some(c=>c.textContent.trim()==="Hotline"))continue;
    return el;
   }
  }
  return null;
 }
 function modal(){
  const h=findHeading();if(!h)return null;
  const vw=innerWidth,vh=innerHeight;
  let panel=h.closest('dialog,[role="dialog"],[aria-modal="true"],.modal-content,.modal-dialog,.hotline-modal');
  if(panel&&panel.getBoundingClientRect().width>Math.max(850,vw*.95))panel=null;
  if(!panel){
   for(let a=h.parentElement;a&&a!==document.body;a=a.parentElement){
    const r=a.getBoundingClientRect(),st=getComputedStyle(a);
    const white=/rgb\(255, 255, 255\)|rgba\(255, 255, 255, 1\)/.test(st.backgroundColor);
    if(r.width>=Math.min(280,vw*.65)&&r.width<=Math.min(850,vw-4)
       &&r.height>=170&&r.height<=vh+30&&(white||parseFloat(st.borderRadius)>=8)){
     panel=a;break;
    }
   }
  }
  if(!panel)return null;
  let backdrop=null;
  for(let a=panel.parentElement;a&&a!==document.body;a=a.parentElement){
   const r=a.getBoundingClientRect(),st=getComputedStyle(a);
   if((st.position==="fixed"||st.position==="absolute")&&r.width>=vw*.75&&r.height>=vh*.68){
    backdrop=a;break;
   }
  }
  return {panel,root:backdrop||panel,backdrop};
 }
 function close(m){
  dismissed=m.root;
  if(dismissed.tagName==="DIALOG"&&dismissed.open){try{dismissed.close()}catch(_){}}
  dismissed.setAttribute("data-tth-hotline-dismissed","1");
  dismissed.setAttribute("aria-hidden","true");
  document.documentElement.style.removeProperty("overflow");
  document.body.style.removeProperty("overflow");
  document.body.classList.remove("modal-open");
 }
 function closeButton(btn,m){
  if(!btn||!m.panel.contains(btn))return false;
  const a=[btn.getAttribute("aria-label"),btn.getAttribute("title"),btn.getAttribute("data-action")].filter(Boolean).join(" ");
  if(/close|đóng|dong|dismiss|thoát/i.test(a))return true;
  const txt=(btn.innerText||btn.textContent||"").trim();
  if(/^[×✕✖✗xX]$/.test(txt))return true;
  if(btn.querySelector("svg")&&/close|x-mark|icon-x/i.test(btn.outerHTML.slice(0,500)))return true;
  const r=btn.getBoundingClientRect(),p=m.panel.getBoundingClientRect();
  return r.width>=18&&r.width<=70&&r.height>=18&&r.height<=70
   &&r.right>=p.right-95&&r.top<=p.top+95&&!txt;
 }
 function opener(btn){
  if(!btn||btn.getAttribute("href")?.startsWith("tel:"))return false;
  const meta=[btn.getAttribute("title"),btn.getAttribute("aria-label"),btn.getAttribute("onclick"),btn.getAttribute("data-action"),btn.className,btn.textContent].join(" ");
  if(/hotline|tổng đài|tong dai|điện thoại|phone|openHotline/i.test(meta))return true;
  if(btn.closest(".tth-cta-fixed")&&btn.matches("a,button")){
   const bg=getComputedStyle(btn).backgroundColor;
   if(/rgb\((?:0, 1[0-7]\d|[0-5]\d), (?:1[1-9]\d|2[0-2]\d), (?:[0-9]\d|1[0-5]\d)\)/.test(bg))return true;
  }
  return false;
 }
 document.addEventListener("click",function(e){
  const t=e.target;
  if(!(t instanceof Element))return;
  const btn=t.closest('button,a,[role="button"],[onclick],input[type="button"]');
  const m=modal();
  if(m&&btn&&closeButton(btn,m)){
   e.preventDefault();e.stopImmediatePropagation();close(m);return;
  }
  if(m&&m.backdrop&&!m.panel.contains(t)&&m.backdrop.contains(t)){
   e.preventDefault();e.stopImmediatePropagation();close(m);return;
  }
  if(dismissed&&btn&&opener(btn)){
   dismissed.removeAttribute("data-tth-hotline-dismissed");
   dismissed.removeAttribute("aria-hidden");
   dismissed=null;
  }
 },true);
 document.addEventListener("keydown",function(e){
  if(e.key!=="Escape")return;
  const m=modal();if(!m)return;
  e.preventDefault();e.stopImmediatePropagation();close(m);
 },true);
})();
</script>'''
n=0
for name,doc in pages.items():
 if 'id="app"' not in doc or 'class="gh"' not in doc:continue
 if 'tth-hotline-close-handler-2027' in doc:raise SystemExit('Double Hotline patch: '+name)
 if '</body>' not in doc:raise SystemExit('Invalid Website document: '+name)
 pages[name]=doc.replace('</body>',patch+'</body>',1)
 n+=1
if n<100:raise SystemExit('Unexpected Website page count '+str(n))
packed=json.dumps(pages,ensure_ascii=False,separators=(',',':')).replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
file.write_text(s[:m.start(2)]+packed+s[m.end(2):],'utf-8')
print('WEBSITE_HOTLINE_CLOSE_2027','patched_pages',n,'controls','close/backdrop/Escape/reopen')
