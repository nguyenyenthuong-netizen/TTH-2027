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
.slide .content .minor[data-tth-overflow="1"],.slide .content .org-child[data-tth-overflow="1"],
.slide .content .decision-list[data-tth-overflow="1"]{overflow-y:auto!important;overscroll-behavior:contain}
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
      // Restore measured baseline before each resize/slide activation.
      // Otherwise fonts only shrink and never recover when space grows.
      nodes.forEach(function(el){
        if(el.dataset.tthBaseFont){el.style.setProperty('font-size',el.dataset.tthBaseFont+'px','important');}
      });
      delete box.dataset.tthOverflow;
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
    }else if(content){content.style.removeProperty('overflow-y');content.style.removeProperty('overscroll-behavior');}
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
   if(!destination){
     // Never send users to an absent local .html page (404 or blank iframe).
     // Keep external links, in-page anchors, phone and email actions intact.
     if(typeof raw==="string" && !/^(?:https?:|\\/\\/|mailto:|tel:|sms:|data:|blob:|javascript:|#)/i.test(raw.trim()) &&
        /\\.html(?:[?#]|$)/i.test(raw.trim())){
       ev.preventDefault();ev.stopImmediatePropagation();
       var note=document.getElementById("tth-missing-page-notice");
       if(!note){
         note=document.createElement("div");note.id="tth-missing-page-notice";
         note.setAttribute("role","status");note.setAttribute("aria-live","polite");
         note.style.cssText="position:fixed;bottom:18px;left:12px;right:12px;max-width:480px;margin:auto;padding:13px 17px;background:#fff;color:#0837A1;border:2px solid #ED3237;border-radius:10px;box-shadow:0 8px 30px #001b4140;z-index:2147483647;font:600 14px/1.45 Arial,sans-serif";
         document.body.appendChild(note);
       }
       note.textContent="Trang này chưa có trong bản giới thiệu. Vui lòng chọn mục khác.";
       clearTimeout(window.__tthMissingPageTimer);
       window.__tthMissingPageTimer=setTimeout(function(){note.remove();},5000);
     }
     return;
   }
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

    # Structural audit covers the embedded pages, not merely the host shell.
    for entry in ("Main.html", "DatLich_XacNhan.html" if shell=="healthcare-app" else "DatLich.html"):
        if entry not in original: continue
        doc=original[entry]
        head=doc[:min(30000,len(doc))]
        summary={
            "chars":len(doc),
            "scroll_hidden":len(re.findall(r'overflow(?:-[xy])?\s*:\s*hidden',head,flags=re.I)),
            "scroll_auto":len(re.findall(r'overflow(?:-[xy])?\s*:\s*(?:auto|scroll)',head,flags=re.I)),
            "sliders":len(re.findall(r'(?i)swiper|slider|carousel|type\s*=\s*["\']range',doc)),
            "buttons":len(re.findall(r'<button\b',doc,flags=re.I)),
            "links":len(re.findall(r'<a\b',doc,flags=re.I)),
        }
        print("AUDIT-INNER",shell,entry,summary)
    img_m=re.search(r'<script\b[^>]*\bid=["\'](?:imageData|imagesData)["\'][^>]*>(.*?)</script>',full,flags=re.I|re.S)
    if img_m:
        image_keys=set(json.loads(img_m.group(1)).keys())
        refs={}
        for p,h in original.items():
            for asset in re.findall(r'../assets/img/([^"\'\s\)]+)',h):
                asset=asset.split('?')[0]
                if asset not in image_keys: refs[asset]=refs.get(asset,0)+1
        print("AUDIT-IMAGES",shell,"images",len(image_keys),"unresolved",len(refs),"sample",list(sorted(refs.items(),key=lambda z:-z[1]))[:10])



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


# 19/11/2026: Final slide corrections. Target the deployed 27-slide override
# after assembly, so the full slide HTML, logos and other content stay intact.
s=slide.read_text("utf-8")
if s.count('<section class="slide')!=27:
    raise AssertionError("Expected 27 slides before final corrections")
old_status='<div class="minor future"><b>ĐANG NGHIÊN CỨU</b><p>TTH Đức Thọ · TTH Quốc tế Huế</p></div>'
new_status='<div class="minor future"><b>ĐANG XÂY DỰNG</b><p>TTH Đức Thọ · TTH Quốc tế Huế</p></div>'
if old_status not in s: raise AssertionError("Expected hospital construction-status text absent")
s=s.replace(old_status,new_status,1)
old_brands='Nguyên Phúc · Thái Thượng Hoàng · các thương hiệu chuyên khoa, Winmed, Tuệ Đức Thiện...'
new_brands='Bệnh viện Y học cổ truyền Nguyên Phúc · Bệnh viện Răng Hàm Mặt và Phẫu thuật Tạo hình Thẩm mỹ Thái Thượng Hoàng · các thương hiệu chuyên khoa khác, Winmed, Tuệ Đức Thiện...'
if old_brands not in s:raise AssertionError("Expected group 2 names absent")
s=s.replace(old_brands,new_brands,1)
# Explicitly identify the two management lines on the role-boundary slide:
# the second chief coordinates local communications professionally, but
# does not directly manage local Marketing staff.
chief_line="""<div class="tth-chief-strip" aria-label="Hai tuyến Chuyên viên trưởng">
<div class="tth-chief tth-chief-1"><strong>Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở</strong><span>Quản lý trực tiếp Tổ Nội dung và Sáng tạo, cùng tuyến Marketing cơ sở thuộc cả hai nhóm.</span></div>
<div class="tth-chief tth-chief-2"><strong>Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số</strong><span>Quản lý các tổ chuyên môn tương ứng tại Tổng công ty; phối hợp nghiệp vụ, không quản lý trực tiếp nhân sự Marketing cơ sở.</span></div>
</div>"""
m=re.search(r'<section class="slide" data-index="7">.*?</section>',s,flags=re.S)
if not m:raise AssertionError("Role-boundary slide not found")
section=m.group(0)
needle='<div class="cols cols3"><article class="card left-blue"><h3>QUẢN LÝ THƯƠNG HIỆU'
if needle not in section:raise AssertionError("Expected 3-card content on role-boundary slide absent")
section=section.replace(needle,chief_line+'<div class="cols cols3 tth-card-row"><article class="card left-blue"><h3>QUẢN LÝ THƯƠNG HIỆU',1)
section=section.replace('Ba vị trí có chức năng, phạm vi thẩm quyền và đầu ra riêng.','Hai Chuyên viên trưởng theo tuyến; ba vị trí chuyên môn có nhiệm vụ, thẩm quyền và đầu ra riêng.',1)
for a,b in (
 ('Duyệt toàn bộ sản phẩm hoặc chi phí.','Không tự động duyệt mọi sản phẩm hay chi phí; thực hiện theo phân quyền từng hạng mục.'),
 ('Phát ngôn, ký hợp đồng hoặc trực tiếp ra lệnh nhân viên cơ sở.','Không tự ý phát ngôn, ký hợp đồng hoặc giao việc vượt tuyến quản lý nhân sự cơ sở.'),
 ('Duyệt phát hành, duyệt chi hay quản lý kênh số toàn hệ thống.','Không tự duyệt phát hành, chi phí hay quản lý kênh số toàn hệ thống.'),
):
    if a not in section:raise AssertionError("Role-boundary disclaimer not found: "+a)
    section=section.replace(a,b,1)
s=s[:m.start()]+section+s[m.end():]
# The old full-width bottom bar stays hidden (explicit user requirement).
# Add two functional controls within the existing side-gutter arrow cluster.
css=r"""<style id="tth-slide-chief-line-and-nav-2027">
.slide[data-index="7"] .content:has(.tth-chief-strip){display:flex!important;flex-direction:column!important;gap:12px!important;overflow:hidden!important}
.slide[data-index="7"] .tth-chief-strip{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;flex:0 0 auto;min-width:0}
.slide[data-index="7"] .tth-chief{border:1px solid #cbd9e9;border-left:6px solid #0837a1;border-radius:11px;background:#fff;padding:10px 14px;min-width:0;min-height:104px;display:flex;flex-direction:column;gap:6px}
.slide[data-index="7"] .tth-chief-2{border-left-color:#ed3237}
.slide[data-index="7"] .tth-chief strong{font-size:16px;line-height:1.18;color:#0837a1;font-weight:800}
.slide[data-index="7"] .tth-chief span{font-size:14px;line-height:1.27;color:#203750}
.slide[data-index="7"] .tth-card-row{flex:1 1 auto!important;min-height:0!important;height:auto!important}
.slide[data-index="7"] .tth-card-row .bodycopy{font-size:15px!important}
.slide[data-index="7"] .tth-card-row .pt b{font-size:16px!important}
.slide[data-index="7"] .tth-card-row .pt span{font-size:15px!important;line-height:1.3!important}
.slide[data-index="4"] .card .bodycopy p{overflow-wrap:break-word}
.tth-floating-arrows .tth-extra-control{display:flex!important;align-items:center!important;justify-content:center!important;flex-direction:column!important;gap:1px!important;color:#fff!important;background:#0837a1!important;cursor:pointer!important;pointer-events:auto!important;border-radius:10px!important;min-height:45px!important;min-width:44px!important;padding:4px!important}
.tth-floating-arrows .tth-extra-control svg{width:19px;height:19px}
.tth-floating-arrows .tth-extra-control small{font:700 9px/1.1 Arial,sans-serif;letter-spacing:0;white-space:nowrap}
.tth-floating-arrows .tth-extra-control:focus-visible{outline:3px solid #ed3237!important;outline-offset:2px!important}
body #index.index.open{display:block!important;visibility:visible!important;position:fixed!important;left:66px!important;right:auto!important;top:10px!important;bottom:10px!important;width:min(430px,calc(100vw - 78px))!important;height:auto!important;padding:22px!important;background:#f7f9fd!important;box-shadow:0 8px 28px #10335440!important;border:1px solid #cbd9e9!important;z-index:1500!important;overflow:auto!important}
body #index.index.open .index-list{display:grid!important;grid-template-columns:1fr!important;gap:7px!important}
body #index.index.open .index-list button{display:block!important;width:100%!important;text-align:left!important;padding:9px 12px!important;font-size:13px!important;line-height:1.35!important}
@media(max-width:849px){
 body #index.index.open{left:10px!important;right:10px!important;top:10px!important;bottom:72px!important;width:auto!important}
 .tth-floating-arrows .tth-extra-control{min-width:44px!important}
}
</style>"""
navjs=r"""<script id="tth-slide-chief-line-and-nav-2027">
(function(){
 "use strict";
 const nav=document.querySelector('.tth-floating-arrows');
 if(!nav)return;
 function button(label,subtitle,path){
   const b=document.createElement('button');
   b.type='button';b.className='tth-floating-arrow tth-extra-control';
   b.setAttribute('aria-label',label);b.title=label;
   b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+path+'</svg><small>'+subtitle+'</small>';
   return b;
 }
 const list=button('Danh sách 27 slide','Danh sách','<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>');
 const full=button('Toàn màn hình','Toàn màn hình','<path d="M8 3H5a2 2 0 0 0-2 2v3M16 3h3a2 2 0 0 1 2 2v3M3 16v3a2 2 0 0 0 2 2h3M21 16v3a2 2 0 0 1-2 2h-3"/>');
 nav.insertBefore(full,nav.firstChild);
 nav.insertBefore(list,full);
 list.addEventListener('click',()=>{document.getElementById('overview')?.click();});
 full.addEventListener('click',()=>{document.getElementById('fullscreen')?.click();});
 document.addEventListener('fullscreenchange',()=>{full.setAttribute('aria-pressed',String(!!document.fullscreenElement));});
})();
</script>"""
if "tth-slide-chief-line-and-nav-2027" in s:raise AssertionError("Final controls already present unexpectedly")
if "</head>" not in s or "</body>" not in s:raise AssertionError("Missing slide boundaries")
s=s.replace("</head>",css+"</head>",1).replace("</body>",navjs+"</body>",1)
if s.count('<section class="slide')!=27 or 'tth-chief-strip' not in s or 'ĐANG XÂY DỰNG' not in s:
    raise AssertionError("Post-update slide QA failed")
slide.write_text(s,"utf-8")
print("PASS-SLIDE chief positions, three role disclaimers, correct labels, menu and fullscreen; slides=27")
