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


# Repair navigation inside the actual iframe documents. A normal relative .html
# link inside srcdoc otherwise navigates the iframe to a missing server file.
# Only targets already existing in the embedded page catalog are intercepted.
import json
for shell, tag, event in (
    ("healthcare-app", "pageData", "TTH_OFFLINE_NAV"),
    ("healthcare-website", "pagesData", "TTH_WEBSITE_OFFLINE_NAV"),
):
    file=root/shell/"index.html"
    full=file.read_text("utf-8")
    match=re.search(
        r'(<script\b[^>]*\bid=["\']'+re.escape(tag)+r'["\'][^>]*>)(.*?)(</script>)',
        full,flags=re.I|re.S)
    if not match:
        raise ValueError(shell+": embedded page catalog not found")
    original=json.loads(match.group(2))
    if not isinstance(original,dict) or len(original)<6:
        raise ValueError(shell+": catalog missing expected pages")
    names=sorted(original.keys())
    names_js=json.dumps(names,ensure_ascii=False)
    modified={}
    changes=0
    for page_name,page_html in original.items():
        if not isinstance(page_html,str):
            raise ValueError(shell+": expected HTML string for "+page_name)
        if 'id="tth-offline-link-bridge-2027"' in page_html:
            modified[page_name]=page_html
            continue
        js=r'''<script id="tth-offline-link-bridge-2027">
(function(){
 "use strict";
 var known=new Set(__TTH_KNOWN_PAGES__);
 function linkTarget(raw){
   if(typeof raw!=="string")return null;
   raw=raw.trim();
   if(!raw||/^(?:https?:|\/\/|mailto:|tel:|sms:|data:|blob:|javascript:|#)/i.test(raw))return null;
   var p=raw.split(/[?#]/)[0].split("/").pop();
   if(!known.has(p))return null;
   return p+raw.slice(raw.indexOf(p)+p.length);
 }
 document.addEventListener("click",function(ev){
   var target=ev.target;
   if(!target||!target.closest)return;
   var item=target.closest("a[href],button[data-href],button[data-route],[role=button][data-href]");
   if(!item)return;
   var raw=item.getAttribute("href")||item.getAttribute("data-href")||item.getAttribute("data-route");
   var destination=linkTarget(raw);
   if(!destination)return;
   ev.preventDefault();
   ev.stopImmediatePropagation();
   window.parent.postMessage({type:"__TTH_NAV_EVENT__",target:destination},"*");
 },true);
})();
</script>'''
        js=js.replace("__TTH_KNOWN_PAGES__",names_js).replace("__TTH_NAV_EVENT__",event)
        if re.search(r'</body\s*>',page_html,flags=re.I):
            new=re.sub(r'</body\s*>',lambda m:js+m.group(0),page_html,count=1,flags=re.I)
        elif re.search(r'</html\s*>',page_html,flags=re.I):
            new=re.sub(r'</html\s*>',lambda m:js+m.group(0),page_html,count=1,flags=re.I)
        else:
            new=page_html+js
        modified[page_name]=new
        changes+=1
    encoded=json.dumps(modified,ensure_ascii=False,separators=(',',':'))
    # Keep embedded </script> tokens inert in application/json.
    encoded=(encoded.replace('<',r'\u003c')
                    .replace('>',r'\u003e')
                    .replace('&',r'\u0026'))
    updated=full[:match.start(2)]+encoded+full[match.end(2):]
    if set(json.loads(encoded))!=set(original):
        raise AssertionError(shell+": names changed during repair")
    file.write_text(updated,"utf-8")
    nrefs=0
    missing={}
    for page_name,page_html in original.items():
        for ref in re.findall(r'<a\b[^>]*\bhref=["\']([^"\']+)["\']',page_html,flags=re.I):
            key=re.split(r'[?#]',ref,1)[0].split('/')[-1]
            if key.lower().endswith(".html"):
                nrefs+=1
                if key not in original:missing[key]=missing.get(key,0)+1
    print("FIX-NAV",shell,"pages",len(names),"bridged",changes,
          "html-links",nrefs,"unresolved-targets",list(sorted(missing.items(),key=lambda v:-v[1]))[:12])
    print("FIX-NAV-PAGES",shell,",".join(names)[:3400])


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
