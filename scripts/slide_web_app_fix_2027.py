#!/usr/bin/env python3
"""Post-assembly audit and safe UI repair for the three published interfaces.
Never changes business text, original logos or embedded healthcare data.
"""
from pathlib import Path
import re
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")

def redacted(s):
    return re.sub(r'[A-Za-z0-9+/]{600,}={0,2}', lambda m: '[large-asset:'+str(len(m.group()))+']', s)

# For content-heavy fixed-size slides, fit the actual text that overflows its card.
# No global zoom, no removal of slide content, no added navigation bar.
slide=root/"trinh-chieu-marketing"/"index.html"
s=slide.read_text("utf-8")
if s.count('<section class="slide')!=27:
    raise ValueError("Slide count mismatch: expected 27")
marker="tth-slide-measured-fit-2027"
if marker not in s:
    css=r'''
<style id="tth-slide-measured-fit-style-2027">
/* Keep all slide copy accessible; internal scrolling is the last-resort fallback. */
.slide .content .card,.slide .content .brand-column,.slide .content .minor{scrollbar-width:thin}
.slide .content .card[data-tth-overflow="1"],.slide .content .brand-column[data-tth-overflow="1"],
.slide .content .minor[data-tth-overflow="1"]{overflow-y:auto!important;overscroll-behavior:contain}
.slide .head h2,.slide .head p{overflow-wrap:break-word;white-space:normal}
@media print{.slide .content .card,.slide .content .brand-column,.slide .content .minor{overflow:visible!important}}
</style>
'''
    js=r'''
<script id="tth-slide-measured-fit-2027">
(function(){
  'use strict';
  var timer=0;
  var selectors='.slide.active .content .card,.slide.active .content .brand-column,.slide.active .content .minor,.slide.active .content .org-child,.slide.active .content .decision-list';
  var fontSelectors='.bodycopy,.pt b,.pt span,.card h3,.minor b,.minor p,.brand-banner,.tagrow span,.org-child strong,.org-child small,.line strong,.line p';
  function overflowing(node){return node.clientHeight>0&&node.scrollHeight>node.clientHeight+4;}
  function fit(){
    var slide=document.querySelector('.slide.active');if(!slide)return;
    var boxes=Array.from(document.querySelectorAll(selectors));
    boxes.forEach(function(box){
      var nodes=Array.from(box.querySelectorAll(fontSelectors));
      // Capture original computed fonts once, before fitting.
      nodes.forEach(function(el){
        if(!el.dataset.tthBaseFont){
          var px=parseFloat(getComputedStyle(el).fontSize);
          if(Number.isFinite(px))el.dataset.tthBaseFont=String(px);
        }
      });
      for(var step=0;step<6&&overflowing(box);step++){
        var factor=1-(step+1)*.055;
        nodes.forEach(function(el){
          var base=parseFloat(el.dataset.tthBaseFont);
          if(base)el.style.setProperty('font-size',Math.max(12.5,base*factor).toFixed(2)+'px','important');
        });
      }
      if(overflowing(box))box.dataset.tthOverflow='1';
      else delete box.dataset.tthOverflow;
    });
    var content=slide.querySelector('.content');
    if(content&&overflowing(content)){
      // Avoid silent clipping for layouts denser than their 1280x720 page.
      content.style.setProperty('overflow-y','auto','important');
      content.style.setProperty('overscroll-behavior','contain');
    }else if(content){content.style.removeProperty('overflow-y');}
  }
  function schedule(){cancelAnimationFrame(timer);timer=requestAnimationFrame(function(){requestAnimationFrame(fit)})}
  var stage=document.getElementById('stage');
  if(stage)new MutationObserver(schedule).observe(stage,{subtree:true,attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',schedule);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule);else schedule();
})();
</script>
'''
    if "</head>" not in s or "</body>" not in s:
        raise ValueError("Slide HTML missing boundaries")
    s=s.replace("</head>",css+"</head>",1).replace("</body>",js+"</body>",1)
    slide.write_text(s,"utf-8")
print("FIX-SLIDE fitted overflow cards; total",s.count('<section class="slide'))

# Inspect external app shells; the internal UI may be stored in encoded iframe assets.
# This check prevents inventing a fix for a page that we have not structurally inspected.
for name in ("healthcare-app","healthcare-website"):
    p=root/name/"index.html"
    text=p.read_text("utf-8")
    counts={term:text.lower().count(term.lower()) for term in
        ('<iframe','srcdoc=','data:text/html','atob(','<script','#screen','#frame','#tools','.toptools','blob:','base64,')}
    print("PROBE",name,"bytes",len(text.encode('utf-8')),"counts",counts)
    # A small redacted excerpt of the actual page shell, never large embedded data.
    for pos in (0, text.lower().find("<body"), text.lower().find("<iframe"), max(0,len(text)-900)):
        if pos>=0:
            print("PROBE-EXCERPT",name,pos,redacted(text[pos:pos+1000]).replace("\n"," ")[:1050])
    scripts=re.findall(r'<script\b([^>]*)>(.*?)</script>',text,flags=re.I|re.S)
    for attrs,body in scripts:
        if len(body)<24000 and 'application/json' not in attrs:
            print("PROBE-SCRIPT",name,"attrs",attrs[:150],"length",len(body),"source",redacted(body[:12000]).replace("\n"," ")[:12000])
    for attrs,body in scripts:
        if 'application/json' in attrs:
            print("PROBE-DATA",name,"length",len(body),"start",redacted(body[:350]).replace("\n"," ")[:350])
            break
    if '<iframe' not in text.lower():
        print("PROBE-WARNING",name,"no literal iframe found; review dynamic DOM before changes")
print("FIX-PASS slide/web/app audit completed")
