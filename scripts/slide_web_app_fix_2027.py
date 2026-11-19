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
   var suffix=raw.match(/[?#].*$/);
   return p+(suffix?suffix[0]:"");
 }
 document.addEventListener("click",function(ev){
   // Preserve native browser shortcuts and download actions.
   if(ev.defaultPrevented||ev.button!==0||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;
   var target=ev.target;
   if(!target||!target.closest)return;
   var item=target.closest("a[href],button[data-href],button[data-route],[role=button][data-href]");
   if(!item||item.hasAttribute("download")||item.getAttribute("target")==="_blank")return;
   var raw=item.getAttribute("href")||item.getAttribute("data-href")||item.getAttribute("data-route");
   var destination=linkTarget(raw);
   if(!destination){
     // Never send users to an absent local .html page (404 or blank iframe).
     // Keep external links, in-page anchors, phone and email actions intact.
     if(typeof raw==="string" && !/^(?:https?:|\/\/|mailto:|tel:|sms:|data:|blob:|javascript:|#)/i.test(raw.trim()) &&
        /\.html(?:[?#]|$)/i.test(raw.trim())){
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
   // Compact controls: the visible glyph is the SVG only. Tooltip and ARIA carry the full label.
   // Do not create a <small> caption: older CSS could display it outside the 44px button.
   b.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+path+'</svg>';
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
# Preserve native slide navigation. Do not inject extra buttons that
# overlap the slide gutter or duplicate native controls.
s=s.replace("</head>",css+"</head>",1)
assert s.count('<section class="slide')==27
if s.count('<section class="slide')!=27 or 'tth-chief-strip' not in s or 'ĐANG XÂY DỰNG' not in s:
    raise AssertionError("Post-update slide QA failed")
slide.write_text(s,"utf-8")
print("PASS-SLIDE chief positions, three role disclaimers, correct labels, menu and fullscreen; slides=27")


# A single native mobile website menu: reuse the existing hamburger in the
# website header instead of placing a second floating "Danh mục" button over
# the page. The outer HTML-shell tools are QA controls, not product controls.
mobile_css=r"""<style id="tth-responsive-burger-menu-1911">
@media(max-width:960px){
#app header.gh>div:first-child{padding:6px 10px!important;gap:8px!important;box-sizing:border-box!important;max-width:100vw!important}
#app header.gh>div:first-child>a[href="Main.html"]{flex:0 0 auto!important;max-width:94px!important}
#app header.gh>div:first-child>a[href="Main.html"] img{height:44px!important;max-width:94px!important;object-fit:contain!important}
#app header.gh .gsrch{max-width:min(38vw,150px)!important;min-width:0!important;width:min(38vw,150px)!important}
#app header.gh .gsrch .q .t{display:none!important}
#app header.gh .burger{display:flex!important;flex:0 0 40px!important;min-width:40px!important;width:40px!important;max-width:40px!important}
#app header.gh>div:first-child>div:last-child{gap:5px!important;min-width:0!important;flex-shrink:1!important}
.tth-offline-menu-mobile{display:block!important;position:fixed!important;top:150px!important;right:12px!important;bottom:auto!important;left:auto!important;width:auto!important;z-index:2147482500!important}
.tth-offline-menu-mobile>button{display:none!important}
.tth-offline-menu-mobile nav{display:none!important;position:static!important;bottom:auto!important;right:auto!important;width:min(325px,calc(100vw - 24px))!important;max-height:calc(100dvh - 170px)!important}
.tth-offline-menu-mobile[data-open="1"] nav{display:block!important}
}
</style>"""
mobile_js=r"""<script id="tth-responsive-burger-menu-1911">(function(){
 function init(){
  var burger=document.querySelector('header.gh .burger');
  var tray=document.querySelector('.tth-offline-menu-mobile');
  if(!burger||!tray||burger.dataset.tthBurgerConnected==='1')return;
  burger.dataset.tthBurgerConnected='1';
  var pane=tray.querySelector('nav');if(!pane)return;
  pane.id='tth-native-mobile-menu';
  burger.setAttribute('aria-controls',pane.id);burger.setAttribute('aria-expanded','false');
  function setOpen(state){
   tray.dataset.open=state?'1':'0';burger.setAttribute('aria-expanded',String(state));
   if(state){var r=burger.getBoundingClientRect();tray.style.top=Math.min(window.innerHeight-120,Math.max(8,r.bottom+5))+'px';}
  }
  burger.addEventListener('click',function(e){e.preventDefault();setOpen(tray.dataset.open!=='1')});
  document.addEventListener('click',function(e){if(!tray.contains(e.target)&&!burger.contains(e.target))setOpen(false)});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false)});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();</script>"""

for folder, tag in (("healthcare-website","pagesData"),("healthcare-app","pageData")):
    file=root/folder/"index.html"
    full=file.read_text("utf-8")
    if folder=="healthcare-website":
        mt=re.search(r'(<script\b[^>]*\bid=["\']'+tag+r'["\'][^>]*>)(.*?)(</script>)',full,flags=re.I|re.S)
        if not mt:raise AssertionError("website page catalog absent")
        entries=json.loads(mt.group(2))
        fixed=0
        for key,doc in entries.items():
            if 'class="burger"' not in doc or 'tth-offline-menu-mobile' not in doc:continue
            if 'tth-responsive-burger-menu-1911' in doc:continue
            if '</head>' not in doc or '</body>' not in doc:raise AssertionError("website page HTML incomplete: "+key)
            entries[key]=doc.replace('</head>',mobile_css+'</head>',1).replace('</body>',mobile_js+'</body>',1)
            fixed+=1
        if fixed<100:raise AssertionError("Unexpectedly few mobile website menu pages: "+str(fixed))
        encoded=json.dumps(entries,ensure_ascii=False,separators=(',',':'))
        encoded=encoded.replace('<',r'\u003c').replace('>',r'\u003e').replace('&',r'\u0026')
        full=full[:mt.start(2)]+encoded+full[mt.end(2):]
        visibility_css=r"""<style id="tth-hide-demo-tools-1911">
/* Outer catalog controls are for QA only. Keep native website controls visible. */
#tools,#catalog{display:none!important}
html.tth-demo-controls #tools{display:flex!important}
html.tth-demo-controls #catalog.open{display:block!important}
</style>"""
    else:
        visibility_css=r"""<style id="tth-hide-demo-tools-1911">
/* The app has its own navigation. Do not obscure it with prototype controls. */
@media(max-width:1000px){
 .toptools,#drawer{display:none!important}
 html.tth-demo-controls .toptools{display:flex!important}
 html.tth-demo-controls #drawer:not([hidden]){display:block!important}
}
</style>"""
        fixed=0
    demo_js=r"""<script id="tth-demo-control-switch-1911">
(function(){
 if(new URLSearchParams(location.search).get('demo')==='1'){
  document.documentElement.classList.add('tth-demo-controls');
 }
})();
</script>"""
    if "tth-hide-demo-tools-1911" in full:raise AssertionError("Duplicate QA shell rules")
    full=full.replace("</head>",visibility_css+"</head>",1).replace("</body>",demo_js+"</body>",1)
    file.write_text(full,"utf-8")
    print("FIX-MOBILE-MENU-1911",folder,"responsive-pages",fixed,"shell-controls-hidden",True)


# Cross-check the live slide against the current same-commit marketing structure.
# The marketing framework remains read-only here; this stage only updates slide.
print("KHUNG-SLIDE-CROSSCHECK-2027 starting")
framework=(root/"khung-marketing"/"index.html").read_text("utf-8")
slide_doc=slide.read_text("utf-8")
reference_checks=(
    "36 suất (22 TCT + 14 bệnh viện)",
    "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở",
    "Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số",
    "mkt-org-local-row",
    "Tổ Truyền thông và Thương hiệu",
    "Tổ Tăng trưởng số",
)
for expected in reference_checks:
    if expected not in framework:
        raise AssertionError("Framework baseline missing: "+expected)
# Retire the incorrect/obsolete 'Tổ trưởng Marketing cơ sở' naming used in
# earlier deck examples, but preserve the team-leader titles at HQ.
changes={}
for old,new in (
 ("TỔ TRƯỞNG MARKETING CƠ SỞ","TRƯỞNG NHÓM MARKETING CƠ SỞ"),
 ("Tổ trưởng Marketing cơ sở","Trưởng nhóm Marketing cơ sở"),
 ("Tổ trưởng Marketing BVĐK","Trưởng nhóm Marketing BVĐK"),
 ("Ba tổ chuyên môn trực thuộc Trưởng phòng","Ba tổ chuyên môn do 02 Chuyên viên trưởng quản lý theo chức năng; Trưởng phòng Marketing điều hành toàn phòng"),
 ("CVT Nội dung – Cơ sở điều phối chuyên môn Nội dung – Thiết kế – Media tại Tổng công ty và các cơ sở.",
  "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở quản lý trực tiếp Tổ Nội dung và Sáng tạo TCT cùng Trưởng nhóm Marketing cơ sở thuộc cả hai nhóm."),
 ("CVT Truyền thông – Số phụ trách Tổ Truyền thông và Thương hiệu, Tổ Tăng trưởng số; hướng dẫn nghiệp",
  "Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số quản lý hai tổ chuyên môn TCT; hướng dẫn nghiệp"),
 ("Chuyên viên trưởng đúng tuyến (khi có phân quyền)",
  "Chuyên viên trưởng được phân quyền hợp lệ bằng văn bản (không có quyền duyệt mặc định)"),
):
    n=slide_doc.count(old)
    if n:
        slide_doc=slide_doc.replace(old,new)
        changes[old]=n
# The independent Communications role is not a separately allocated post at
# specialized Group 2 hospitals; the on-site Marketing leader handles it.
role_slide=re.search(r'<section class="slide" data-index="7">.*?</section>',slide_doc,re.S)
if not role_slide:raise AssertionError("Missing role-boundary slide")
role_html=role_slide.group(0)
role_needle='<b>Phụ trách hiện trường</b><span>Đối tác địa phương, sự kiện, khảo sát biển bảng, phát thanh/màn hình tại chỗ.</span>'
if role_needle not in role_html:raise AssertionError("Unexpected local communications copy")
role_html=role_html.replace(role_needle,
    '<b>Phụ trách hiện trường</b><span>Đối tác địa phương, sự kiện, biển bảng, màn hình và phát thanh. '
    'Tại bệnh viện chuyên khoa nhóm 2, Trưởng nhóm Marketing cơ sở kiêm nhiệm nhiệm vụ truyền thông.</span>',1)
slide_doc=slide_doc[:role_slide.start()]+role_html+slide_doc[role_slide.end():]
# Validate the decision layer against the actual organization's direct-reporting chain.
expect_deck=[
 "36 suất", "22 TCT", "14 cơ sở", "02 Chuyên viên trưởng",
 "TRƯỞNG NHÓM MARKETING CƠ SỞ",
 "Chuyên viên trưởng Nội dung – Sáng tạo và Marketing cơ sở",
 "Chuyên viên trưởng Truyền thông – Thương hiệu và Tăng trưởng số",
 "Truyền thông cơ sở",
]
for term in expect_deck:
    if term.lower() not in slide_doc.lower():
        raise AssertionError("Slide cross-check missing: "+term)
if "Tổ trưởng Marketing cơ sở" in slide_doc or "TỔ TRƯỞNG MARKETING CƠ SỞ" in slide_doc:
    raise AssertionError("Outdated field leader title survives")
if "34 suất" in slide_doc:
    raise AssertionError("Slide still contains legacy headcount 34")
if slide_doc.count('<section class="slide')!=27:
    raise AssertionError("Cross-check changed deck slide count")
slide.write_text(slide_doc,"utf-8")
print("KHUNG-SLIDE-CROSSCHECK-2027 PASS, changes",changes,
      "framework legacy 34-suat references:",framework.count("34 suất"),
      "slides",slide_doc.count('<section class="slide'))


# BRAND-ARCH-WINMED-TDD-2027 — public source verification 19/11/2026.
# Sources: tthgroup.vn corporate news (23/01/2026); winmed.vn official;
# public business-register listings for Tuệ Đức Thiện.
# Treat these as Group 2 marketing brands/units, not as medical hospitals
# and do not claim a particular parent/subsidiary equity relation.
slide_doc=slide.read_text("utf-8")
framework=(root/"khung-marketing"/"index.html").read_text("utf-8")
for name in ("Winmed Việt Nam","Công ty TNHH Tuệ Đức Thiện"):
    if name not in framework:raise AssertionError("Group 2 brand missing from current framework: "+name)
def update_section(doc,index,fn):
    m=re.search(r'<section class="slide" data-index="'+str(index)+r'">.*?</section>',doc,flags=re.S)
    if not m:raise AssertionError("Missing slide data-index "+str(index))
    section=fn(m.group(0))
    return doc[:m.start()]+section+doc[m.end():]
def update_arch(s):
    old='<div class="brand-banner dark">THƯƠNG HIỆU CHUYÊN KHOA</div>'
    new='<div class="brand-banner dark">THƯƠNG HIỆU CHUYÊN KHOA VÀ ĐƠN VỊ KHÁC</div>'
    if s.count(old)!=1:raise AssertionError("Cannot locate brand architecture right heading")
    s=s.replace(old,new,1)
    marker='<p>Viện dưỡng lão Thái Thượng Hoàng</p></div></div></div></main>'
    replacement=(
      '<p>Viện dưỡng lão Thái Thượng Hoàng</p></div>'
      '<div class="minor tth-group2-other">'
      '<b>DOANH NGHIỆP / THƯƠNG HIỆU KHÁC</b>'
      '<p><strong>Winmed Việt Nam</strong> – thiết bị và giải pháp y tế</p>'
      '<p><strong>Tuệ Đức Thiện</strong> – kiến trúc, tư vấn kỹ thuật</p>'
      '</div></div></div></main>'
    )
    if s.count(marker)!=1:raise AssertionError("Unrecognized brand diagram block")
    return s.replace(marker,replacement,1)
slide_doc=update_section(slide_doc,3,update_arch)
def update_group(s):
    old='Bệnh viện Y học cổ truyền Nguyên Phúc · Bệnh viện Răng Hàm Mặt và Phẫu thuật Tạo hình Thẩm mỹ Thái Thượng Hoàng · các thương hiệu chuyên khoa khác, Winmed, Tuệ Đức Thiện...'
    new=('Bệnh viện Y học cổ truyền Nguyên Phúc · Bệnh viện Răng Hàm Mặt và Phẫu thuật Tạo hình Thẩm mỹ Thái Thượng Hoàng · '
         'các thương hiệu chuyên khoa khác; <strong>Winmed Việt Nam</strong> (thiết bị y tế) và '
         '<strong>Tuệ Đức Thiện</strong> (kiến trúc, tư vấn kỹ thuật).')
    if s.count(old)!=1:raise AssertionError("Group 2 paragraph not found for corrections")
    return s.replace(old,new,1)
slide_doc=update_section(slide_doc,4,update_group)
css=r"""<style id="tth-group2-other-brands-1911">
/* Fit the extra verified Group 2 brands without cutting or tiny fonts. */
.slide[data-index="3"] .brand-column{padding:11px!important}
.slide[data-index="3"] .brand-column .brand-banner{font-size:16px!important;line-height:1.2!important;margin-bottom:8px!important;padding:10px!important}
.slide[data-index="3"] .brand-column>.minor{padding:7px 10px!important;margin-bottom:7px!important}
.slide[data-index="3"] .brand-column>.minor p{font-size:15px!important;line-height:1.24!important;margin:3px 0!important}
.slide[data-index="3"] .brand-column>.minor b{font-size:12px!important;line-height:1.3!important}
.slide[data-index="3"] .tth-group2-other{background:#edf3fc!important;border:1px solid #bfd3f1!important;border-left:4px solid #0837a1!important}
.slide[data-index="3"] .tth-group2-other strong{font-weight:700!important}
.slide[data-index="4"] .card .bodycopy{font-size:17px!important;line-height:1.37!important}
.slide[data-index="4"] .card .bodycopy p{margin:6px 0 10px!important}
</style>"""
if 'tth-group2-other-brands-1911' in slide_doc:raise AssertionError("Duplicate brand CSS")
slide_doc=slide_doc.replace("</head>",css+"</head>",1)
assert slide_doc.count('<section class="slide')==27
assert slide_doc.count('tth-group2-other')>=2
assert "DOANH NGHIỆP / THƯƠNG HIỆU KHÁC" in slide_doc
slide.write_text(slide_doc,"utf-8")
print("BRAND-ARCH-WINMED-TDD-2027 PASS: both brands visible on architecture and group-2 slide")


# Compact icon-only presentation controls prevent the previous small captions
# from painting outside a 44px button and overlapping one another.
slide_doc=slide.read_text("utf-8")
icon_style=r"""<style id="tth-slide-nav-icons-only-1911">
/* NAVIGATION DOCK -- outside the canvas rather than floating above slide text.
   The 1280x720 stage continues scaling with #viewport via its existing fit(). */
:root{--tth-slide-rail-width:72px;--tth-slide-mobile-dock:68px}
@media screen and (min-width:850px){
 #viewport{
   position:fixed!important;inset:0 0 0 var(--tth-slide-rail-width)!important;
   top:0!important;bottom:0!important;left:var(--tth-slide-rail-width)!important;
   right:0!important;width:calc(100vw - var(--tth-slide-rail-width))!important;
   height:100dvh!important;max-height:100dvh!important;
   padding:0!important;box-sizing:border-box!important;
 }
 .tth-floating-arrows{
   position:fixed!important;inset:auto!important;
   left:7px!important;right:auto!important;top:50%!important;bottom:auto!important;
   transform:translateY(-50%)!important;width:58px!important;height:auto!important;
   display:flex!important;flex-direction:column!important;flex-wrap:nowrap!important;
   align-items:center!important;justify-content:center!important;gap:11px!important;
   padding:10px 5px!important;margin:0!important;box-sizing:border-box!important;
   background:#e6eef9!important;border:1px solid #c7d8ec!important;
   border-radius:18px!important;z-index:2000!important;pointer-events:auto!important;
 }
}
@media screen and (max-width:849px){
 #viewport{
   position:fixed!important;inset:0 0 var(--tth-slide-mobile-dock) 0!important;
   top:0!important;left:0!important;right:0!important;
   bottom:var(--tth-slide-mobile-dock)!important;width:100vw!important;
   height:calc(100dvh - var(--tth-slide-mobile-dock))!important;
   max-height:calc(100dvh - var(--tth-slide-mobile-dock))!important;
   padding:0!important;box-sizing:border-box!important;
 }
 .tth-floating-arrows{
   position:fixed!important;inset:auto!important;top:auto!important;
   left:0!important;right:0!important;bottom:0!important;
   transform:none!important;display:flex!important;flex-direction:row!important;
   align-items:center!important;justify-content:center!important;flex-wrap:nowrap!important;
   width:100vw!important;height:var(--tth-slide-mobile-dock)!important;
   min-height:var(--tth-slide-mobile-dock)!important;gap:12px!important;
   margin:0!important;padding:7px 10px!important;box-sizing:border-box!important;
   background:#e6eef9!important;border-top:1px solid #b6c9e3!important;
   border-radius:0!important;z-index:2000!important;pointer-events:auto!important;
 }
}
.tth-floating-arrows .tth-floating-arrow{
 appearance:none!important;position:relative!important;
 display:flex!important;align-items:center!important;justify-content:center!important;
 flex:0 0 44px!important;min-width:44px!important;max-width:44px!important;
 width:44px!important;height:44px!important;min-height:44px!important;max-height:44px!important;
 border-radius:12px!important;border:1px solid #fff!important;
 padding:0!important;margin:0!important;box-sizing:border-box!important;
 overflow:hidden!important;white-space:nowrap!important;
 line-height:1!important;color:#fff!important;background:#0837a1!important;
 font-size:0!important;text-indent:0!important;cursor:pointer!important;
 pointer-events:auto!important;
}
.tth-floating-arrows .tth-floating-arrow svg{
 display:block!important;flex:0 0 22px!important;
 width:22px!important;height:22px!important;min-width:22px!important;
 max-width:22px!important;margin:0!important;padding:0!important;
 color:#fff!important;stroke:#fff!important;
}
.tth-floating-arrows .tth-floating-arrow small{display:none!important}
.tth-floating-arrows .tth-floating-arrow:focus-visible{
 outline:3px solid #ED3237!important;outline-offset:2px!important
}
@media print{
 #viewport{position:static!important;inset:auto!important;width:1280px!important;height:auto!important}
 .tth-floating-arrows{display:none!important}
}
</style>"""
if "tth-slide-nav-icons-only-1911" not in slide_doc:
 slide_doc=slide_doc.replace("</head>",icon_style+"</head>",1)
slide.write_text(slide_doc,"utf-8")
assert slide_doc.count('<section class="slide')==27
print("PASS tth-slide-nav-icons-only-1911: small-label overlap removed; navigation controls retain title and aria-label")


# Prevent regressions: the two floating controls must have SVG icons only,
# full accessible names, no child caption, and should not reinstate #controls.
tth_controls=slide.read_text("utf-8")
if "const list=button('Danh sách 27 slide'" not in tth_controls or "const full=button('Toàn màn hình'" not in tth_controls:
    raise AssertionError("Required slide controls missing")
nav_block=tth_controls.split('const nav=document.querySelector(\'.tth-floating-arrows\');',1)[-1]
if '</svg><small>' in nav_block[:1300]:
    raise AssertionError("Overflowing slide control text is still inserted")
if tth_controls.count('<section class="slide')!=27:
    raise AssertionError("Slide count changed while repairing controls")
print("PASS-SLIDE-NAV-ICONS: two controls are SVG-only and keep accessible labels")


dock_html=slide.read_text("utf-8")
assert 'NAVIGATION DOCK -- outside the canvas' in dock_html
assert 'var(--tth-slide-rail-width)' in dock_html
assert 'var(--tth-slide-mobile-dock)' in dock_html
assert dock_html.count('<section class="slide')==27
print("PASS-SLIDE-DOCK: controls outside slide viewport; 27 slides intact")


# Repair an independently reproducible slide clipping case: fixed 146px headers
# do not expand for long Vietnamese titles or responsive browser font metrics.
# Do not shrink headings below a legible size or alter the business text.
slide_doc=slide.read_text("utf-8")
heading_marker="tth-slide-header-overflow-2027"
if heading_marker not in slide_doc:
    heading_css=r"""<style id="tth-slide-header-overflow-2027">
.slide .head{overflow:visible!important}
.slide .head h2{overflow-wrap:break-word!important;word-break:normal!important;hyphens:none!important}
.slide .head p{overflow-wrap:break-word!important;word-break:normal!important}
.slide .head[data-tth-heading-overflow="1"]{height:auto!important;min-height:146px!important;z-index:4!important}
.slide .head[data-tth-heading-overflow="1"] h2{font-size:clamp(23px,2.25vw,31px)!important;line-height:1.16!important}
.slide .head[data-tth-heading-overflow="1"] p{font-size:14px!important}
.slide .head[data-tth-heading-overflow="1"] + .content{top:190px!important;overflow-y:auto!important}
.slide.cover .head[data-tth-heading-overflow="1"] + .content{top:240px!important}
</style>"""
    heading_js=r"""<script id="tth-slide-header-overflow-2027-js">
(function(){
  "use strict";
  var scheduled=false;
  function measure(){
    scheduled=false;
    var slide=document.querySelector('.slide.active');
    if(!slide)return;
    var head=slide.querySelector('.head'), title=head&&head.querySelector('h2');
    if(!head||!title)return;
    delete head.dataset.tthHeadingOverflow;
    var sub=head.querySelector('p');
    var headBottom=head.getBoundingClientRect().bottom;
    var titleBottom=title.getBoundingClientRect().bottom;
    var subBottom=sub?sub.getBoundingClientRect().bottom:0;
    // Only activate the fallback for content that actually crosses the header boundary.
    if(Math.max(titleBottom,subBottom)>headBottom-5){
      head.dataset.tthHeadingOverflow='1';
    }
  }
  function schedule(){
    if(scheduled)return;scheduled=true;
    requestAnimationFrame(function(){requestAnimationFrame(measure)});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});else schedule();
  window.addEventListener('resize',schedule);
  var stage=document.getElementById('stage');
  if(stage)new MutationObserver(schedule).observe(stage,{subtree:true,attributes:true,attributeFilter:['class']});
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(schedule);
})();
</script>"""
    if "</head>" not in slide_doc or "</body>" not in slide_doc:
        raise AssertionError("Slide heading repair: invalid HTML")
    slide_doc=slide_doc.replace("</head>",heading_css+"</head>",1).replace("</body>",heading_js+"</body>",1)
    if slide_doc.count('<section class="slide')!=27:
        raise AssertionError("Slide heading repair changed slide count")
    slide.write_text(slide_doc,"utf-8")
    print("PASS-SLIDE-HEADINGS: measured overflow fallback installed, 27 slides preserved")


# TTH_WEBSITE_FACILITY_IMAGE_REPAIR_20261119
# Three pages reuse the same six cards. Their inline facs[] arrays use
# /_blob/<hash> URLs from the editor runtime; those endpoints do not exist on
# static GitHub Pages. These are different from the image references checked
# by the earlier AUDIT-IMAGES pass. Replace each URL with a bundled AI
# illustration, then let the existing parent-shell go() replace the
# ../assets/img/<filename> reference with the matching data URI.
webfile=root/"healthcare-website"/"index.html"
web=webfile.read_text("utf-8")
img_match=re.search(
 r'(<script\b[^>]*\bid=["\']imagesData["\'][^>]*>)(.*?)(</script>)',
 web,flags=re.S|re.I)
if not img_match:raise AssertionError("Missing embedded website image catalog")
image_catalog=json.loads(img_match.group(2))
facility_fallbacks={
 "f076225bd9d4fc858d12ce16102e3d08":"csBenhVien.jpg",   # TTH Vinh
 "203615c52fc8f4cef2fc0e8b8d634f73":"csBenhVien2.jpg",  # TTH Ha Tinh
 "0711a3df9be804964020a6b302c02e5a":"matTien.jpg",      # TTH Quang Binh
 "fee1390c29d132559a6836c49b3a44a2":"phoiCanh.jpg",    # TTH Hue (planned)
 "50554d39c7a3bbf954e235095824bd5c":"csPhongKham.jpg", # TTH Khe Tre
 "0a0d52fa4fc32da88995ce5963db6888":"tiepDon.jpg"      # TTH A Luoi
}
for file in facility_fallbacks.values():
 if file not in image_catalog or not image_catalog[file].startswith("data:image/"):
  raise AssertionError("Bundled AI illustration unavailable: "+file)
page_match=re.search(
 r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',
 web,flags=re.S|re.I)
if not page_match:raise AssertionError("Missing embedded website page catalog")
pages=json.loads(page_match.group(2))
pages_to_check=("HeThongYTe.html","Truc_TTHHospital.html","Truc_TTHClinic.html")
changed={}
for page in pages_to_check:
 if page not in pages:raise AssertionError("Missing website facility page: "+page)
 doc=pages[page]
 n=0
 for img_hash,file in facility_fallbacks.items():
  obsolete="/_blob/"+img_hash
  if doc.count(obsolete)!=1:
   raise AssertionError("Expected exactly one facility image reference on "+page+": "+obsolete)
  doc=doc.replace(obsolete,"../assets/img/"+file,1)
  n+=1
 if "/_blob/" in doc:raise AssertionError("Unmapped image URL remains in "+page)
 pages[page]=doc
 changed[page]=n
if sum(changed.values())!=18:
 raise AssertionError("Expected exactly 18 fixed image references across 3 facility pages")
for page,doc in pages.items():
 if "/_blob/" in doc:
  raise AssertionError("Additional unsupported /_blob/ image reference in "+page)
encoded=(json.dumps(pages,ensure_ascii=False,separators=(",",":"))
 .replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026"))
web=web[:page_match.start(2)]+encoded+web[page_match.end(2):]
assert all(("/_blob/"+token) not in web for token in facility_fallbacks)
webfile.write_text(web,"utf-8")
print("PASS WEBSITE FACILITY IMAGES",changed,
 "bundled-image-count",len(image_catalog),
 "unresolved-blob-links",0)


# TTH_WEBSITE_FIXED_COLLAPSIBLE_CTA_1911
# Existing native CTA links (top/Hotline/Zalo/AI) exist on public website
# pages, but their wrapper has inline position:sticky at the bottom.
# Keep the existing links, move their common container to the middle of the
# right viewport edge, and allow expansion/collapse without new fake actions.
website_file=root/"healthcare-website"/"index.html"
website_html=website_file.read_text("utf-8")
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',
            website_html,flags=re.S|re.I)
if not m:raise AssertionError("Website page catalog missing for CTA fix")
website_pages=json.loads(m.group(2))
cta_css=r"""<style id="tth-fixed-cta-center-1911">
html body .fab.tth-cta-fixed{
 position:fixed!important;top:50%!important;
 right:clamp(9px,1.2vw,22px)!important;bottom:auto!important;left:auto!important;
 transform:translateY(-50%)!important;display:block!important;
 width:auto!important;height:auto!important;max-width:calc(100vw - 10px)!important;
 max-height:calc(100dvh - 30px)!important;margin:0!important;padding:0!important;
 z-index:1800!important;pointer-events:none!important
}
html body .fab.tth-cta-fixed .tth-cta-stack{
 display:flex!important;flex-direction:column!important;align-items:flex-end!important;
 gap:10px!important;max-height:calc(100dvh - 30px)!important;
 max-width:calc(100vw - 10px)!important;overflow-y:auto!important;
 overflow-x:visible!important;scrollbar-width:thin!important;
 padding:5px!important;pointer-events:auto!important
}
html body .fab.tth-cta-fixed .tth-cta-stack>sc-if{display:none!important}
html body .fab.tth-cta-fixed a.fabx{
 display:flex!important;flex-direction:row-reverse!important;
 flex:0 0 62px!important;min-width:62px!important;width:62px!important;
 height:62px!important;min-height:62px!important;max-height:62px!important;
 align-items:center!important;justify-content:flex-start!important;
 border-radius:30px!important;overflow:visible!important;box-sizing:border-box!important;
 pointer-events:auto!important
}
html body .fab.tth-cta-fixed a.fabx .ic{
 width:62px!important;height:62px!important;min-width:62px!important;
 flex:0 0 62px!important;display:flex!important;align-items:center!important;
 justify-content:center!important
}
html body .fab.tth-cta-fixed a.fabx .ic>span{
 font-size:18px!important;font-weight:800!important;line-height:1.1!important
}
html body .fab.tth-cta-fixed a.fabx .ic>svg{
 max-width:49px!important;max-height:49px!important
}
html body .fab.tth-cta-fixed a.fabx .lb{
 font-family:Arial,Tahoma,sans-serif!important;font-size:16px!important;
 font-weight:700!important;line-height:1.35!important
}
html body .fab.tth-cta-fixed a.fabx.intro .lb{animation:none!important}
html body .fab.tth-cta-fixed .tth-cta-toggle{
 appearance:none!important;display:flex!important;align-items:center!important;
 justify-content:center!important;gap:0!important;width:36px!important;
 min-width:36px!important;max-width:36px!important;height:36px!important;
 min-height:36px!important;max-height:36px!important;
 padding:0!important;margin:0!important;border-radius:50%!important;
 border:1px solid #9db5d7!important;background:rgba(255,255,255,.95)!important;color:#0837A1!important;
 box-shadow:0 2px 8px rgba(8,55,161,.12)!important;
 font-size:0!important;line-height:1!important;
 cursor:pointer!important;white-space:nowrap!important;pointer-events:auto!important
}
html body .fab.tth-cta-fixed .tth-cta-toggle:focus-visible{
 outline:3px solid #ED3237!important;outline-offset:2px!important
}
html body .fab.tth-cta-fixed[data-collapsed="true"] .tth-cta-stack>a.fabx{
 display:none!important
}
html body .fab.tth-cta-fixed[data-collapsed="true"] .tth-cta-toggle{
 width:36px!important;min-width:36px!important;max-width:36px!important;
 height:36px!important;min-height:36px!important;max-height:36px!important;
 background:rgba(255,255,255,.95)!important;color:#0837A1!important
}
@media(max-width:640px){
 html body .fab.tth-cta-fixed{right:8px!important}
 html body .fab.tth-cta-fixed .tth-cta-stack{gap:7px!important;padding:3px!important}
 html body .fab.tth-cta-fixed a.fabx{
  width:52px!important;height:52px!important;min-height:52px!important;
  max-height:52px!important;min-width:52px!important;flex-basis:52px!important
 }
 html body .fab.tth-cta-fixed a.fabx .ic{
  height:52px!important;width:52px!important;min-width:52px!important;flex-basis:52px!important
 }
 html body .fab.tth-cta-fixed a.fabx .ic>span{font-size:17px!important}
 html body .fab.tth-cta-fixed .tth-cta-toggle{width:36px!important;min-width:36px!important;max-width:36px!important;height:36px!important;min-height:36px!important;max-height:36px!important}
}
</style>"""
cta_js=r"""<script id="tth-fixed-cta-center-1911-js">
(function(){
 "use strict";
 function init(){
  var fab=document.querySelector('.fab.tth-cta-fixed');
  if(!fab||fab.dataset.tthCtaReady==='1')return;
  var stack=fab.firstElementChild;if(!stack)return;
  fab.dataset.tthCtaReady='1';stack.classList.add('tth-cta-stack');
  var btn=document.createElement('button');btn.type='button';btn.className='tth-cta-toggle';
  btn.innerHTML='<svg width="17" height="17" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 5l7 7-7 7"/></svg>';
  var key='tth-healthcare-cta-collapsed-1911';
  function mobile(){return window.matchMedia&&window.matchMedia('(max-width:640px)').matches}
  function stored(){
   try{
    var value=localStorage.getItem(key);
    return value===null?mobile():value==='1';
   }catch(e){return mobile()}
  }
  function save(on){try{localStorage.setItem(key,on?'1':'0')}catch(e){}}
  function apply(on){
   fab.dataset.collapsed=on?'true':'false';
   var arrow=btn.querySelector('svg path');
   if(arrow)arrow.setAttribute('d',on?'M14 5l-7 7 7 7':'M10 5l7 7-7 7');
   btn.setAttribute('aria-expanded',String(!on));
   btn.setAttribute('aria-label',on?'Mở cụm hỗ trợ liên hệ':'Thu gọn cụm hỗ trợ liên hệ');
   btn.title=on?'Mở cụm hỗ trợ':'Thu gọn cụm hỗ trợ';
  }
  btn.addEventListener('click',function(e){
   e.preventDefault();
   var on=fab.dataset.collapsed!=='true';apply(on);save(on);
  });
  stack.insertBefore(btn,stack.firstChild);apply(stored());
 }
 if(document.readyState==='loading')
  document.addEventListener('DOMContentLoaded',init,{once:true});
 else init();
})();
</script>"""
cta_count=0
for page,html in website_pages.items():
    if '<div class="fab"' not in html:continue
    if html.count('<div class="fab"')!=1:raise AssertionError("CTA wrapper count unexpected on "+page)
    if cta_css.split('id="')[1].split('"')[0] in html:
        raise AssertionError("CTA code already injected on "+page)
    if "</head>" not in html or "</body>" not in html:
        raise AssertionError("Incomplete HTML page for CTA: "+page)
    html=html.replace('<div class="fab"','<div class="fab tth-cta-fixed"',1)
    html=html.replace("</head>",cta_css+"</head>",1).replace("</body>",cta_js+"</body>",1)
    website_pages[page]=html
    cta_count+=1
if cta_count<100:
    raise AssertionError("Unexpectedly few public site pages with native CTA: "+str(cta_count))
serialized=(json.dumps(website_pages,ensure_ascii=False,separators=(",",":"))
    .replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026"))
website_html=website_html[:m.start(2)]+serialized+website_html[m.end(2):]
website_file.write_text(website_html,"utf-8")
assert 'tth-cta-fixed' in website_html and cta_count>=100
print("PASS WEBSITE CTA ARROW-ONLY, arrow right to collapse and left to expand, no button label text")
print("PASS TTH WEBSITE FIXED COLLAPSIBLE CTA",
      "pages",cta_count,"links-per-page",4,
      "center-right",True,"persistent-state",True,
      "mobile-default-collapsed",True)


# TTH_WEBSITE_GLOBAL_DISPLAY_AUDIT_20261119
# Global mobile overflow regression identified on public pages by Chromium
# testing at 390px: the search widget's inline/no-shrink styling forces its
# right edge beyond the viewport (at least 18px). Also stabilize the browser
# host's QA tools and CTA preferences across sandboxed iframe navigation.
web_path=root/"healthcare-website"/"index.html"
web_code=web_path.read_text("utf-8")
m=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',
            web_code,flags=re.I|re.S)
if not m:raise AssertionError("Missing website pagesData for global display QA")
page_catalog=json.loads(m.group(2))
global_css=r"""<style id="tth-website-display-qa-1911">
/* Avoid global horizontal clipping: keep all navigation controls within the viewport. */
html,body{max-width:100%!important;overflow-x:clip!important}
#app{max-width:100%!important;min-width:0!important}
#app header.gh{max-width:100vw!important;box-sizing:border-box!important}
#app header.gh .gsrch{min-width:0!important}
#app header.gh .gsrch a.q{min-width:0!important}
#app header.gh nav.mnav{min-width:0!important}
#app .tth-offline-menu-mobile>button{display:none!important}
/* Protect meaning, contrast and native text flow without applying tiny text. */
#app main p,#app main li{word-break:normal!important;overflow-wrap:break-word!important}
#app main .muted,#app main .meta,#app main .subtle{
 color:#405777!important
}
#app a:focus-visible,#app button:focus-visible,#app input:focus-visible,
#app select:focus-visible{outline:3px solid #ED3237!important;outline-offset:2px!important}
@media(max-width:740px){
 #app header.gh>div:first-child{
  display:flex!important;align-items:center!important;
  flex-wrap:nowrap!important;justify-content:space-between!important;
  width:100%!important;min-width:0!important;max-width:100vw!important;
  padding:6px 10px!important;gap:7px!important;box-sizing:border-box!important
 }
 #app header.gh>div:first-child>a[href="Main.html"]{
  display:flex!important;flex:0 0 92px!important;
  width:92px!important;min-width:92px!important;max-width:92px!important
 }
 #app header.gh>div:first-child>a[href="Main.html"] img{
  width:92px!important;max-width:92px!important;height:47px!important;
  object-fit:contain!important;object-position:center left!important
 }
 #app header.gh nav.mnav{display:none!important}
 #app header.gh>div:first-child>div:last-child{
  display:flex!important;align-items:center!important;justify-content:flex-end!important;
  gap:8px!important;margin-left:auto!important;flex:1 1 auto!important;min-width:0!important;
  max-width:calc(100vw - 119px)!important;box-sizing:border-box!important
 }
 #app header.gh .gsrch{
  display:flex!important;flex:0 0 44px!important;
  width:44px!important;min-width:44px!important;max-width:44px!important;
  max-height:44px!important;padding:0!important;margin:0!important;
  box-sizing:border-box!important;overflow:hidden!important
 }
 #app header.gh .gsrch .q{
  display:flex!important;flex:0 0 44px!important;width:44px!important;
  min-width:44px!important;max-width:44px!important;height:44px!important;
  min-height:44px!important;max-height:44px!important;
  padding:0!important;margin:0!important;justify-content:center!important;
  align-items:center!important;box-sizing:border-box!important;border-radius:12px!important
 }
 #app header.gh .gsrch .q .t{display:none!important}
 /* The same AI assistant is still accessible through the persistent CTA. */
 #app header.gh .gsrch .askai{display:none!important}
 #app header.gh a.btn.hideM{display:none!important}
 #app header.gh .burger{
  display:flex!important;flex:0 0 44px!important;width:44px!important;
  min-width:44px!important;max-width:44px!important;height:44px!important;
  min-height:44px!important;max-height:44px!important;
  margin:0!important;padding:0!important;box-sizing:border-box!important
 }
 #app .tth-offline-menu-mobile nav{
  max-width:calc(100vw - 24px)!important;
  max-height:calc(100dvh - 150px)!important;overflow-y:auto!important
 }
}
@media(max-width:355px){
 #app header.gh>div:first-child>a[href="Main.html"]{flex-basis:80px!important;width:80px!important;min-width:80px!important;max-width:80px!important}
 #app header.gh>div:first-child>a[href="Main.html"] img{width:80px!important;max-width:80px!important}
}
</style>"""
global_js=r"""<script id="tth-website-display-qa-1911-js">
(function(){
 "use strict";
 // The srcdoc iframe is sandboxed and does not have access to localStorage.
 // A small message bridge to the parent shell keeps CTA state across pages.
 var allowed="TTH_WEBSITE_CTA_";
 function apply(on){
  var fab=document.querySelector(".fab.tth-cta-fixed");
  if(!fab)return;
  fab.dataset.collapsed=on?"true":"false";
  var b=fab.querySelector(".tth-cta-toggle");
  if(b){
   var icon=b.querySelector("svg path");
   if(icon)icon.setAttribute("d",on?"M14 5l-7 7 7 7":"M10 5l7 7-7 7");
   b.setAttribute("aria-expanded",String(!on));
   b.setAttribute("aria-label",on?"Mở cụm hỗ trợ liên hệ":"Thu gọn cụm hỗ trợ liên hệ");
   b.title=on?"Mở cụm hỗ trợ":"Thu gọn cụm hỗ trợ";
  }
 }
 window.addEventListener("message",function(e){
  if(e.source!==window.parent||!e.data||e.data.type!==allowed+"STATE")return;
  apply(!!e.data.collapsed);
 });
 function start(){
  var fab=document.querySelector(".fab.tth-cta-fixed");
  if(!fab)return;
  var btn=fab.querySelector(".tth-cta-toggle");
  if(btn){
   btn.addEventListener("click",function(){
    setTimeout(function(){
     window.parent.postMessage({type:allowed+"STORE",collapsed:fab.dataset.collapsed==="true"},"*");
    },0);
   });
  }
  window.parent.postMessage({type:allowed+"GET"},"*");
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start,{once:true});
 else start();
})();
</script>"""
admin_css=r"""<style id="tth-website-admin-wide-table-1911">
html,body{max-width:100%!important;overflow-x:clip!important}
.tth-horizontal-table{display:block!important;width:100%!important;max-width:100%!important;
 min-width:0!important;overflow-x:auto!important;overflow-y:visible!important;scrollbar-width:thin!important;
 overscroll-behavior-x:contain!important}
.tth-horizontal-table table{max-width:none!important}
</style>"""
admin_js=r"""<script id="tth-website-admin-wide-table-1911-js">
(function(){
 function wrap(){
  document.querySelectorAll("table").forEach(function(table){
   if(table.closest(".tth-horizontal-table"))return;
   if(table.getBoundingClientRect().width<=document.documentElement.clientWidth-24)return;
   var box=document.createElement("div");box.className="tth-horizontal-table";
   box.setAttribute("role","region");box.setAttribute("aria-label","Bảng dữ liệu có thể cuộn ngang");
   box.setAttribute("tabindex","0");
   table.parentElement.insertBefore(box,table);box.appendChild(table);
  });
 }
 if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",wrap,{once:true});
 else wrap();
 window.addEventListener("resize",wrap);
})();
</script>"""
public_count=0;admin_count=0
for name,doc in page_catalog.items():
 if "tth-website-display-qa-1911" in doc:raise AssertionError("Display guard applied twice")
 if "</head>" not in doc or "</body>" not in doc:
  raise AssertionError("Page malformed before display guard: "+name)
 if 'class="gh"' in doc and 'id="app"' in doc:
  doc=doc.replace("</head>",global_css+"</head>",1).replace("</body>",global_js+"</body>",1)
  public_count+=1
 else:
  doc=doc.replace("</head>",admin_css+"</head>",1).replace("</body>",admin_js+"</body>",1)
  admin_count+=1
 page_catalog[name]=doc
if public_count<100 or public_count+admin_count!=125:
 raise AssertionError("Unexpected global website page split "+str((public_count,admin_count)))
packed=(json.dumps(page_catalog,ensure_ascii=False,separators=(",",":"))
        .replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026"))
web_code=web_code[:m.start(2)]+packed+web_code[m.end(2):]
shell_css=r"""<style id="tth-website-shell-display-cleanup-1911">
/* Prototype navigation is not part of the product UI. Preserve it only for
   the deliberate QA mode ?demo=1. */
html:not(.tth-demo-controls) body #tools,
html:not(.tth-demo-controls) body #catalog{display:none!important;visibility:hidden!important;pointer-events:none!important}
html:not(.tth-demo-controls) body #frame{height:100dvh!important;min-height:100dvh!important;margin:0!important}
</style>"""
shell_js=r"""<script id="tth-website-cta-state-bridge-1911">
(function(){
 "use strict";
 var frame=document.getElementById("frame");
 if(!frame)return;
 var key="tth-healthcare-cta-collapsed-1911", fallback=null;
 var prefix="TTH_WEBSITE_CTA_";
 function get(){
  var stored=fallback;
  try{var x=localStorage.getItem(key);if(x!==null)stored=x==="1"}catch(e){}
  return stored===null?(window.matchMedia&&window.matchMedia("(max-width:640px)").matches):stored;
 }
 function set(on){
  fallback=!!on;
  try{localStorage.setItem(key,on?"1":"0")}catch(e){}
 }
 window.addEventListener("message",function(e){
  if(e.source!==frame.contentWindow||!e.data)return;
  if(e.data.type===prefix+"GET"){
   frame.contentWindow.postMessage({type:prefix+"STATE",collapsed:get()},"*");
  }else if(e.data.type===prefix+"STORE"){
   set(!!e.data.collapsed);
  }
 });
})();
</script>"""
if "tth-website-shell-display-cleanup-1911" in web_code:
 raise AssertionError("Duplicate outer shell repair")
web_code=web_code.replace("</head>",shell_css+"</head>",1).replace("</body>",shell_js+"</body>",1)
web_path.write_text(web_code,"utf-8")
assert 'tth-website-shell-display-cleanup-1911' in web_code
assert 'tth-website-display-qa-1911' in web_code
print("WEBSITE-GLOBAL-DISPLAY-PASS",
      "public-pages",public_count,"admin-pages",admin_count,
      "header-mobile",True,"CTA-state-parent-bridge",True,
      "prototype-tools-hidden",True,"admin-table-scroll",True)


# TTH_WEBSITE_BACK_TO_TOP_FIX_20261119
# The native CTA "Lên đầu trang" uses href="#top" on 115 pages, but the
# markup contains no id="top". A document-level capture handler from the
# original prototype intercepts missing anchors and shows a placeholder
# notification instead of scrolling. Register on window capture (which runs
# before document capture), handle #top and stop the stale placeholder.
webfile=root/"healthcare-website"/"index.html"
websrc=webfile.read_text("utf-8")
datam=re.search(r'(<script\b[^>]*\bid=["\']pagesData["\'][^>]*>)(.*?)(</script>)',
                websrc,re.S|re.I)
if not datam:raise AssertionError("Website page catalog missing for top-button repair")
webpages=json.loads(datam.group(2))
top_js=r"""<script id="tth-website-back-to-top-1911">
(function(){
 "use strict";
 window.addEventListener("click",function(ev){
   var t=ev.target && (ev.target.nodeType===1?ev.target:ev.target.parentElement);
   var a=t&&t.closest?t.closest('a[href="#top"]'):null;
   if(!a)return;
   ev.preventDefault();
   ev.stopImmediatePropagation();
   window.scrollTo(0,0);
   if(document.scrollingElement)document.scrollingElement.scrollTop=0;
 },true);
})();
</script>"""
fixed=[]
for name,doc in webpages.items():
 if '<a class="fabx " href="#top"' not in doc:
  continue
 if 'tth-website-back-to-top-1911' in doc:
  raise AssertionError("Duplicate top-button repair on "+name)
 if "</body>" not in doc:raise AssertionError("Missing body end on "+name)
 doc=doc.replace("</body>",top_js+"</body>",1)
 webpages[name]=doc
 fixed.append(name)
if len(fixed)!=115:
 raise AssertionError("Expected 115 CTA top buttons, got "+str(len(fixed)))
encoded=(json.dumps(webpages,ensure_ascii=False,separators=(",",":"))
 .replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026"))
websrc=websrc[:datam.start(2)]+encoded+websrc[datam.end(2):]
webfile.write_text(websrc,"utf-8")
print("PASS WEBSITE BACK TO TOP 115/115: window capture precedes original document handler")
