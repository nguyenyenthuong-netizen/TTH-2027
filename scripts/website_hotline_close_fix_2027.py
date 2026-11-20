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
/* Never hide the Website root or its content: only a diagnosed Hotline layer. */
[data-tth-hotline-dismissed="1"]{display:none!important;visibility:hidden!important;pointer-events:none!important}
</style>
<script id="tth-hotline-close-handler-2027">
(function(){
 "use strict";
 if(window.__TTH_HOTLINE_CLOSE_HANDLER_2027__)return;
 window.__TTH_HOTLINE_CLOSE_HANDLER_2027__=true;
 let dismissed=[];
 const visible=el=>{if(!el||!el.isConnected)return false;
  const r=el.getBoundingClientRect(),s=getComputedStyle(el);
  return r.width>8&&r.height>8&&s.display!=="none"&&s.visibility!=="hidden"&&s.opacity!=="0";};
 const protectedRoot=el=>!el||el.matches?.('html,body,main,header,footer,nav,#app,#root,[id="site-content"]')||
  Boolean(el.querySelector?.('header.gh'));
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
  if(!panel||protectedRoot(panel))return null;
  const layers=new Set([panel]);let mask=null;
  // Ancestor fullscreen layer: the dialog and shade belong to one overlay.
  for(let a=panel.parentElement;a&&a!==document.body;a=a.parentElement){
   const r=a.getBoundingClientRect(),st=getComputedStyle(a);
   if(protectedRoot(a))break;
   const fullscreen=r.width>=vw*.74&&r.height>=vh*.65;
   if(fullscreen&&(st.position==="fixed"||st.position==="absolute"||
      /modal|backdrop|overlay|shade|scrim|mask/i.test(String(a.className||"")))){
    layers.add(a);mask=a;break;
   }
  }
  // Important: the original modal may render its gray backdrop as a SEPARATE
  // sibling of the white dialog; hiding only panel leaves a gray blank screen.
  const ancestors=new Set();for(let a=panel;a&&a!==document.body;a=a.parentElement)ancestors.add(a);
  document.querySelectorAll('body *').forEach(function(el){
   if(el===panel||el.contains(panel)||panel.contains(el)||protectedRoot(el)||!visible(el))return;
   const r=el.getBoundingClientRect(),st=getComputedStyle(el);
   if(r.width<vw*.74||r.height<vh*.65)return;
   const cls=String(el.className||"")+" "+String(el.id||"");
   const named=/modal|backdrop|overlay|shade|scrim|mask|dim-layer/i.test(cls);
   const positioned=st.position==="fixed"||st.position==="absolute";
   if(!positioned&&!named)return;
   const bg=st.backgroundColor||"";
   const alpha=/rgba?\([^)]*,\s*(0?\.\d+|1)\)/.exec(bg);
   const translucent=Boolean(alpha&&parseFloat(alpha[1])>0&&parseFloat(alpha[1])<1);
   const darkSolid=/rgb\(\s*(\d+),\s*(\d+),\s*(\d+)\s*\)/.exec(bg);
   const grayMask=Boolean(darkSolid&&[1,2,3].every(i=>Number(darkSolid[i])<205)&&
    (el.innerText||"").trim().length<80);
   const near=[el.parentElement,el.parentElement?.parentElement].some(x=>ancestors.has(x));
   if((named||translucent||grayMask)&&(positioned||near)){
    layers.add(el);if(!mask)mask=el;
   }
  });
  return {panel,layers:Array.from(layers),mask};
 }
 function close(m){
  dismissed=m.layers.filter(el=>el&&el.isConnected&&!protectedRoot(el));
  dismissed.forEach(function(el){
   if(el.tagName==="DIALOG"&&el.open){try{el.close()}catch(_){}}
   el.setAttribute("data-tth-hotline-dismissed","1");
   el.setAttribute("aria-hidden","true");
  });
  // Re-enable the Website behind the modal; do NOT alter page content.
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
  return false;
 }
 function restore(){
  dismissed.forEach(function(el){if(!el.isConnected)return;
   el.removeAttribute("data-tth-hotline-dismissed");el.removeAttribute("aria-hidden");});
  dismissed=[];
 }
 document.addEventListener("click",function(e){
  const t=e.target;
  if(!(t instanceof Element))return;
  const btn=t.closest('button,a,[role="button"],[onclick],input[type="button"]');
  const m=modal();
  if(m&&btn&&closeButton(btn,m)){
   e.preventDefault();e.stopImmediatePropagation();close(m);return;
  }
  if(m&&!m.panel.contains(t)){
   e.preventDefault();e.stopImmediatePropagation();close(m);return;
  }
  if(dismissed.length&&btn&&opener(btn)){
   e.preventDefault();e.stopImmediatePropagation();restore();return;
  }
 },true);

 // The Hotline is a NON-MODAL floating information panel. Preserve the
 // underlying home page visually on open as well as after close.
 function undim(){
  const m=modal();if(!m)return;
  m.layers.forEach(function(el){
   if(el===m.panel)return;
   el.style.setProperty("background-color","transparent","important");
   el.style.setProperty("backdrop-filter","none","important");
   el.style.setProperty("-webkit-backdrop-filter","none","important");
   el.style.setProperty("box-shadow","none","important");
   el.style.setProperty("pointer-events","none","important");
  });
  m.panel.style.setProperty("pointer-events","auto","important");
  document.body.classList.remove("modal-open");
  document.body.style.removeProperty("overflow");
  document.documentElement.style.removeProperty("overflow");
 }
 let scheduled=false;
 function scheduleUndim(){
  if(scheduled)return;scheduled=true;
  requestAnimationFrame(function(){scheduled=false;undim();});
 }
 if(document.readyState==="loading"){
  document.addEventListener("DOMContentLoaded",scheduleUndim,{once:true});
 }else scheduleUndim();
 const watch=new MutationObserver(scheduleUndim);
 watch.observe(document.documentElement,{subtree:true,childList:true,attributes:true,
  attributeFilter:["class","style","hidden","aria-hidden"]});

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
