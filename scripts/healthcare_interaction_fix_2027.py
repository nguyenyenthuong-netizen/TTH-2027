#!/usr/bin/env python3
"""Correct Healthcare App and Website assistant-search navigation without inventing AI output.
All 102 App / 125 Website screens and logo assets remain unchanged.
"""
import re,json,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
shared_style=r"""<style id="tth-question-input-ui-2027">
.tth-ai-question{flex:1 1 auto!important;min-width:0!important;width:100%!important;
 border:0!important;outline:0!important;box-shadow:none!important;background:transparent!important;
 color:#16345b!important;font:500 14px/1.45 Arial,"Segoe UI",sans-serif!important;
 padding:0 4px!important;min-height:32px!important;cursor:text!important}
.tth-ai-question:focus-visible{outline:0!important}
.tth-ask-icon-only{font-size:0!important;gap:0!important;justify-content:center!important;
 min-width:36px!important;width:38px!important;flex:0 0 38px!important;
 padding:2px!important;cursor:pointer!important}
.tth-ask-icon-only .tx,.tth-ask-icon-only .t{display:none!important}
.tth-ask-icon-only .av,.tth-ask-icon-only>span:first-child{
 display:inline-flex!important;align-items:center!important;justify-content:center!important;
 width:30px!important;height:30px!important;min-width:30px!important;flex:none!important}
.tth-ask-icon-only svg{display:block!important;max-width:30px!important;max-height:30px!important}
#app header.gh .gsrch .tth-ai-question{min-width:0!important;flex:1 1 110px!important;
 width:auto!important;font-size:13px!important}
#app header.gh .gsrch{display:flex!important;align-items:center!important;gap:4px!important;
 padding-left:9px!important;min-width:0!important}
#app header.gh .gsrch .askai.tth-ask-icon-only{display:inline-flex!important;flex:0 0 38px!important}
form[role="search"] .tth-hidden-extra-submit{display:none!important}
.tth-ai-offline-note{border:1px solid #B9CAE6;border-radius:12px;background:#F0F5FD;
 color:#123A77;padding:10px;margin:8px 0;font:500 13px/1.45 Arial,sans-serif;overflow-wrap:anywhere}
@media(max-width:740px){
 #app header.gh .gsrch{display:flex!important;flex:1 1 140px!important;
  width:auto!important;min-width:0!important;max-width:100%!important;
  padding:0 4px!important;overflow:visible!important}
 #app header.gh .gsrch .tth-ai-question{display:block!important;min-width:0!important;
  flex:1 1 auto!important;font-size:12px!important}
 #app header.gh .gsrch .askai.tth-ask-icon-only{display:inline-flex!important;
  flex:0 0 34px!important;width:34px!important;min-width:34px!important}
}
</style>"""
def child_script(kind):
 assistant="HoTro_TroLy.html" if kind=="app" else "Web_TroLy.html"
 nav_event="TTH_OFFLINE_NAV" if kind=="app" else "TTH_WEBSITE_OFFLINE_NAV"
 return r"""<script id="tth-assistant-search-fixed-2027">
(function(){
'use strict';
const isApp=__IS_APP__, assistantPage="__DEST__", navigateEvent="__NAV_EVENT__";
function iconOnly(node){
 if(!node||node.dataset.tthAssistantBound)return;
 node.dataset.tthAssistantBound="1";
 node.classList.add("tth-ask-icon-only");
 node.setAttribute("href","#tth-only-submit");
 node.setAttribute("role","button");node.setAttribute("tabindex","0");
 node.setAttribute("aria-label","Gửi câu hỏi cho Trợ lý TTH");
 node.setAttribute("title","Gửi câu hỏi cho Trợ lý TTH");
 Array.from(node.childNodes).forEach(function(n){
  if(n.nodeType===Node.TEXT_NODE)n.textContent="";
 });
}
function configureApp(){
 if(!isApp)return;
 const a=Array.from(document.querySelectorAll('a[href="Tim_NhuCau.html"]'))
  .find(x=>/Đau bụng|khám thai/.test(x.textContent||"")&&x.querySelector("svg"));
 if(!a||a.dataset.tthInputPrepared)return;
 const holder=document.createElement("label");
 holder.style.cssText=a.getAttribute("style")||"";
 holder.style.cursor="text";
 holder.setAttribute("aria-label","Nhập câu hỏi cho Trợ lý TTH");
 const svg=a.querySelector("svg");
 if(svg)holder.append(svg.cloneNode(true));
 const input=document.createElement("input");
 input.type="search";input.autocomplete="off";
 input.className="tth-ai-question";input.id="tth-app-inline-question";
 input.placeholder="Hỏi Trợ lý về sức khỏe, lịch khám...";
 input.setAttribute("aria-label","Câu hỏi dành cho Trợ lý TTH");
 holder.append(input);
 const row=a.parentElement;
 a.replaceWith(holder);
 const send=Array.from(row.querySelectorAll('a[aria-label*="Trợ lý"],a[href="HoTro_TroLy.html"]'))[0];
 if(send){iconOnly(send);send.dataset.tthAssistantSubmit="1";send.dataset.tthQuestionSource="tth-app-inline-question";}
}
function configureWebsite(){
 if(isApp)return;
 document.querySelectorAll('header.gh .gsrch').forEach(function(box,i){
  if(box.dataset.tthQuestionReady)return;
  box.dataset.tthQuestionReady="1";
  const old=box.querySelector('a.q[href*="TimKiem.html"]');
  if(old){
   const input=document.createElement("input");
   input.type="search";input.autocomplete="off";input.className="tth-ai-question";
   input.id="tth-web-header-question-"+i;
   input.placeholder="Hỏi Trợ lý TTH...";
   input.setAttribute("aria-label","Nhập câu hỏi dành cho Trợ lý TTH");
   old.replaceWith(input);
  }
  const send=box.querySelector("a.askai");
  if(send){iconOnly(send);send.dataset.tthAssistantSubmit="1";
   send.dataset.tthQuestionSource="tth-web-header-question-"+i;}
 });
 document.querySelectorAll('form[role="search"],.sbox').forEach(function(box,i){
  const input=box.querySelector('input:not([type="hidden"])');
  if(!input)return;
  input.classList.add("tth-ai-question");
  if(!input.id)input.id="tth-web-section-question-"+i;
  const send=box.querySelector('a.askai');
  if(send){iconOnly(send);send.dataset.tthAssistantSubmit="1";
   send.dataset.tthQuestionSource=input.id;}
  if(box.matches('form[role="search"]')){
   Array.from(box.querySelectorAll('a.btn[href^="TimKiem.html"]')).forEach(function(a){
    a.classList.add("tth-hidden-extra-submit");a.setAttribute("tabindex","-1");});
  }
 });
}
function currentInput(sender){
 const id=sender?.dataset?.tthQuestionSource;
 if(id){const found=document.getElementById(id);if(found)return found;}
 const active=document.activeElement;
 if(active?.matches?.('input.tth-ai-question'))return active;
 const parent=sender?.closest?.('.gsrch,.sbox,form,section');
 return parent?.querySelector?.('input.tth-ai-question')||document.querySelector('input.tth-ai-question');
}
function send(sender){
 const inp=currentInput(sender);
 if(!inp){return;}
 const value=inp.value.trim();
 if(!value){inp.focus();return;}
 if(value.length>1200){inp.setCustomValidity("Câu hỏi tối đa 1.200 ký tự");inp.reportValidity();return;}
 inp.setCustomValidity("");
 // No navigation on focus/click; only explicit Enter or assistant-icon submission.
 window.parent.postMessage({type:navigateEvent,target:assistantPage},"*");
 // Keep potentially sensitive medical text out of URL, query strings and browser history.
 window.parent.postMessage({type:"TTH_ASSISTANT_PROMPT",question:value},"*");
}
function configure(){
 configureApp();configureWebsite();
}
window.addEventListener("click",function(ev){
 const btn=ev.target?.closest?.('[data-tth-assistant-submit="1"]');
 if(!btn)return;
 ev.preventDefault();ev.stopImmediatePropagation();send(btn);
},true);
window.addEventListener("keydown",function(ev){
 const btn=ev.target?.closest?.('[data-tth-assistant-submit="1"]');
 if(btn&&(ev.key==="Enter"||ev.key===" ")){
  ev.preventDefault();ev.stopImmediatePropagation();send(btn);return;
 }
 const input=ev.target?.closest?.('input.tth-ai-question');
 if(!input||ev.key!=="Enter"||ev.isComposing)return;
 ev.preventDefault();ev.stopImmediatePropagation();
 const inBox=input.closest('.gsrch,.sbox,form,section');
 const b=inBox?.querySelector?.('[data-tth-assistant-submit="1"]')
  ||document.querySelector('[data-tth-assistant-submit="1"]');
 if(b)send(b);
},true);
window.addEventListener("submit",function(ev){
 if(!ev.target?.matches?.('form[role="search"]'))return;
 const input=ev.target.querySelector('input.tth-ai-question');
 if(!input)return;
 ev.preventDefault();ev.stopImmediatePropagation();
 const b=ev.target.querySelector('[data-tth-assistant-submit="1"]');
 if(b)send(b);
},true);
window.addEventListener("message",function(ev){
 const m=ev.data;
 if(!m||m.type!=="TTH_ASSISTANT_PREFILL"||typeof m.question!=="string")return;
 if(m.question.length>1200)return;
 const field=Array.from(document.querySelectorAll('input[type="text"],input:not([type])'))
  .find(x=>x.offsetParent!==null||x.getBoundingClientRect().height>0);
 if(!field)return;
 field.value=m.question;field.dispatchEvent(new Event("input",{bubbles:true}));
 field.focus({preventScroll:true});
 if(document.querySelector(".tth-ai-offline-note"))return;
 const note=document.createElement("div");note.className="tth-ai-offline-note";note.setAttribute("role","status");
 const title=document.createElement("strong");title.textContent="Câu hỏi đã được chuyển đến giao diện Trợ lý";
 const body=document.createElement("div");body.textContent="Bản mô phỏng chưa kết nối dịch vụ AI hoặc dữ liệu khám thực tế; không tự tạo câu trả lời.";
 note.append(title,body);
 const box=field.closest('label')?.parentElement||field.parentElement;
 if(box&&box.parentNode)box.parentNode.insertBefore(note,box);
});
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",configure,{once:true});
else configure();
})();
</script>""".replace("__IS_APP__","true" if kind=="app" else "false").replace("__DEST__",assistant).replace("__NAV_EVENT__",nav_event)
parent_script=r"""<script id="tth-assistant-question-relay-2027">
(function(){
 "use strict";
 const frame=document.querySelector("iframe#screen,iframe#frame");
 if(!frame)return;
 let draft=null;
 window.addEventListener("message",function(ev){
  if(ev.source!==frame.contentWindow||!ev.data)return;
  if(ev.data.type==="TTH_ASSISTANT_PROMPT"&&typeof ev.data.question==="string"){
   draft=ev.data.question.slice(0,1200);
  }
 });
 frame.addEventListener("load",function(){
  if(draft===null)return;
  const text=draft;draft=null;
  frame.contentWindow?.postMessage({type:"TTH_ASSISTANT_PREFILL",question:text},"*");
 });
})();
</script>"""
for folder,tag,kind in (("healthcare-app","pageData","app"),("healthcare-website","pagesData","web")):
 file=root/folder/"index.html";raw=file.read_text("utf8")
 m=re.search(r'(<script\b[^>]*\bid=["\']'+tag+r'["\'][^>]*>)(.*?)(</script>)',raw,re.S|re.I)
 if not m:raise SystemExit(folder+": missing embedded catalog")
 pages=json.loads(m.group(2))
 expected=102 if kind=="app" else 125
 if len(pages)!=expected:raise SystemExit(folder+": catalog count mismatch "+str(len(pages)))
 out={}
 for name,page in pages.items():
  if 'id="tth-assistant-search-fixed-2027"' not in page:
   if '</head>' not in page or '</body>' not in page:raise SystemExit(folder+": malformed "+name)
   page=page.replace("</head>",shared_style+"</head>",1)
   page=page.replace("</body>",child_script(kind)+"</body>",1)
  out[name]=page
 encoded=json.dumps(out,ensure_ascii=False,separators=(',',':')).replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026")
 raw=raw[:m.start(2)]+encoded+raw[m.end(2):]
 if 'id="tth-assistant-question-relay-2027"' not in raw:
  raw=raw.replace("</body>",parent_script+"</body>",1)
 file.write_text(raw,"utf8")
 print("ASSISTANT_SEARCH_FIXED",folder,len(out),"submit-only","same-screen-on-focus",True)
