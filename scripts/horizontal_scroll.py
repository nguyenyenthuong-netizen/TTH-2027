#!/usr/bin/env python3
"""Add accessible non-overlay horizontal scroll controls to long TTH Marketing tables."""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
p=root/"khung-marketing"/"index.html"
s=p.read_text("utf-8")
style=r"""
<style id="tth-horizontal-scroll-style">
/* Scroll controls occupy their own row, never cover any table or heading. */
.tth-scroll-tools{display:flex;justify-content:flex-end;align-items:center;gap:8px;margin:8px 0 5px;min-height:34px}
.tth-scroll-tools[hidden]{display:none!important}
.tth-scroll-tools button{display:inline-flex;align-items:center;justify-content:center;width:35px;height:32px;padding:0;border:1px solid #9bb8df;border-radius:8px;background:#fff;color:#0837A1;font-size:19px;font-weight:800;line-height:1;cursor:pointer}
.tth-scroll-tools button:hover:not(:disabled){background:#e9f2ff}
.tth-scroll-tools button:disabled{opacity:.35;cursor:default}
.tth-scroll-tools .tth-scroll-label{font-size:12px;color:#45617d;margin-right:4px}
#main .tbl,#main .rel-scroll{overflow-x:auto!important;max-width:100%!important;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
@media(max-width:900px){.tth-scroll-tools{justify-content:center;gap:12px}.tth-scroll-tools button{width:42px;height:36px}}
@media print{.tth-scroll-tools{display:none!important}}
</style>
"""
script=r"""
<script id="tth-horizontal-scroll">
(function(){
  function init(){
    var nodes=document.querySelectorAll('#main .tbl,#main .rel-scroll,.side .tabs');
    nodes.forEach(function(el){
      if(el.dataset.tthScrollReady==='1')return;
      el.dataset.tthScrollReady='1';
      var bar=document.createElement('div');bar.className='tth-scroll-tools';bar.hidden=true;
      var label=document.createElement('span');label.className='tth-scroll-label';label.textContent='Trượt ngang';
      var prev=document.createElement('button');prev.type='button';prev.textContent='‹';prev.setAttribute('aria-label','Trượt sang trái');
      var next=document.createElement('button');next.type='button';next.textContent='›';next.setAttribute('aria-label','Trượt sang phải');
      bar.append(label,prev,next);el.parentNode.insertBefore(bar,el);
      function update(){
        var max=Math.max(0,el.scrollWidth-el.clientWidth);
        bar.hidden=max<=3;
        prev.disabled=el.scrollLeft<=2;
        next.disabled=el.scrollLeft>=max-2;
      }
      function move(dir){el.scrollBy({left:dir*Math.max(220,el.clientWidth*.72),behavior:'smooth'});}
      prev.addEventListener('click',function(){move(-1)});
      next.addEventListener('click',function(){move(1)});
      el.addEventListener('scroll',update,{passive:true});
      var drag=null;
      el.addEventListener('pointerdown',function(e){
        if(e.pointerType!=='mouse'||e.button!==0||e.target.closest('button,a,input,select,textarea,summary,[role="button"]'))return;
        drag={x:e.clientX,left:el.scrollLeft};
      });
      el.addEventListener('pointermove',function(e){
        if(!drag||!(e.buttons&1))return;
        if(Math.abs(e.clientX-drag.x)>4){el.scrollLeft=drag.left+(drag.x-e.clientX);update();}
      });
      ['pointerup','pointercancel','pointerleave'].forEach(function(type){el.addEventListener(type,function(){drag=null})});
      if(window.ResizeObserver){var ro=new ResizeObserver(update);ro.observe(el);if(el.firstElementChild)ro.observe(el.firstElementChild);}
      update();
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  window.addEventListener('resize',init);
  document.addEventListener('click',function(e){if(e.target.closest('.tab,.side-toggle'))setTimeout(init,30)});
})();
</script>
"""
s=s.replace('<style id="tth-horizontal-scroll-style">','<style id="tth-horizontal-scroll-style-old">') if False else s
if 'id="tth-horizontal-scroll-style"' in s or 'id="tth-horizontal-scroll"' in s:
    raise SystemExit("Scroll controls already installed; inspect before reinjecting")
if "</head>" not in s or "</body>" not in s:
    raise SystemExit("Invalid HTML")
s=s.replace("</head>",style+"</head>",1).replace("</body>",script+"</body>",1)
p.write_text(s,"utf-8")
print("PASS: responsive horizontal scroll arrows and drag inserted",len(s))
