#!/usr/bin/env python3
"""Fix accidental UI overlays in TTH 2027 demo pages, preserving slide content."""
from pathlib import Path
import re
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
base="""/* 18/11/2026: no overlays over headings, content, input. */
html {scroll-behavior:auto}
:focus-visible {outline-offset:2px}
"""
styles={
"khung-marketing":"""
#main .pp-h,#main .jd-d[open]>.jd-head{position:relative!important;top:auto!important;z-index:auto!important;box-shadow:none!important}
#main table thead,#main table thead tr,#main table thead th{position:static!important;top:auto!important;z-index:auto!important}
#main table thead th{background:#EDF4FC!important;color:#183556!important;vertical-align:top!important}
#main .view,#main .card,#main .doc-sec{overflow-wrap:anywhere!important;min-width:0!important}
#main .view h1,#main .view h2,#main .view h3{line-height:1.35!important;min-height:0!important}
#main table th,#main table td{line-height:1.5!important;min-height:0!important;max-height:none!important;overflow-wrap:anywhere!important;white-space:normal!important}
@media(max-width:900px){.side .search{position:relative!important;z-index:4!important}}
""",
"crm-da-kenh":"""
#ux-search-launch{position:static!important;top:auto!important;right:auto!important;bottom:auto!important;width:100%!important;box-sizing:border-box!important;margin:6px 0 12px!important;box-shadow:none!important;border:1px solid #b5cce7!important;z-index:auto!important}
body.ux-crm-min #ux-search-launch{display:none!important}
#ux-search-panel{top:64px!important;right:16px!important;max-height:calc(100dvh - 80px)!important}
@media(max-width:640px){#ux-search-panel{top:12px!important;right:12px!important;width:calc(100vw - 24px)!important;max-height:calc(100dvh - 24px)!important}}
""",
"healthcare-app":"""
html,body{margin:0!important;min-height:100dvh!important}
#screen{display:block!important;width:100%!important;height:calc(100dvh - 52px)!important;margin-top:52px!important;box-sizing:border-box!important}
.toptools{position:fixed!important;top:0!important;bottom:auto!important;right:0!important;left:0!important;z-index:800!important;min-height:52px!important;box-sizing:border-box!important;display:flex!important;flex-wrap:nowrap!important;gap:8px!important;align-items:center!important;justify-content:flex-end!important;background:#f5f9ff!important;border-bottom:1px solid #d5e3f5!important;padding:5px 12px!important;box-shadow:none!important;opacity:1!important}
.toptools button{min-height:39px!important;border-radius:9px!important;font-size:13px!important;padding:7px 12px!important}
#drawer{position:fixed!important;top:56px!important;bottom:auto!important;right:10px!important;left:auto!important;max-height:calc(100dvh - 64px)!important;z-index:850!important}
#status{display:none!important}
@media(max-width:480px){.toptools{justify-content:space-between!important}.toptools button{flex:1!important;font-size:12.5px!important}#screen{height:calc(100dvh - 52px)!important}}
""",
"healthcare-website":"""
html,body{margin:0!important;min-height:100dvh!important}
#frame{display:block!important;width:100%!important;height:calc(100dvh - 52px)!important;margin-top:52px!important;box-sizing:border-box!important}
#tools{position:fixed!important;top:0!important;bottom:auto!important;left:0!important;right:0!important;z-index:800!important;min-height:52px!important;box-sizing:border-box!important;display:flex!important;justify-content:flex-end!important;align-items:center!important;gap:8px!important;background:#f5f9ff!important;border-bottom:1px solid #d5e3f5!important;padding:5px 12px!important;box-shadow:none!important}
#tools button{min-height:39px!important;border-radius:9px!important;font-size:13px!important;padding:7px 12px!important;box-shadow:none!important}
#catalog{position:fixed!important;top:56px!important;bottom:auto!important;right:10px!important;left:auto!important;max-height:calc(100dvh - 64px)!important;z-index:850!important}
@media(max-width:480px){#tools{justify-content:space-between!important}#tools button{flex:1!important;font-size:12.5px!important}#frame{height:calc(100dvh - 52px)!important}}
"""
}
for folder,css in styles.items():
 p=root/folder/"index.html"
 text=p.read_text(encoding="utf-8")
 text,n1=re.subn(r'<style\s+id=["\']tth-pages-return-style["\'][^>]*>.*?</style>','',text,count=1,flags=re.I|re.S)
 text,n2=re.subn(r'<a\s+href=["\']\.\./["\']\s+id=["\']tth-pages-return["\'][^>]*>.*?</a>','',text,count=1,flags=re.I|re.S)
 if n2!=1: raise RuntimeError(folder+": stray floating cross-interface link not found")
 if folder!="crm-da-kenh":
  for tag,pattern in (
   ("style",r'<style\s+id=["\']ux-advanced-search-style["\'][^>]*>.*?</style>'),
   ("button",r'<button\s+id=["\']ux-search-launch["\'][^>]*>.*?</button>'),
   ("section",r'<section\s+id=["\']ux-search-panel["\'][^>]*>.*?</section>'),
   ("script",r'<script\s+id=["\']ux-advanced-search["\'][^>]*>.*?</script>')):
   text,count=re.subn(pattern,'',text,count=1,flags=re.I|re.S)
   if count!=1: raise RuntimeError(folder+": redundant search "+tag+" not found")
 text=text.replace("</head>",'<style id="tth-layout-repair-1811">'+base+css+"</style></head>",1)
 if folder=="crm-da-kenh":
  js="""<script id='tth-crm-search-inline'>(function(){const b=document.getElementById('ux-search-launch');const s=document.querySelector('.layout aside');if(b&&s){s.insertBefore(b,s.querySelector('.identity'));}})();</script>"""
  text=text.replace("</body>",js+"</body>",1)
 assert "tth-layout-repair-1811" in text and len(text)>100000
 p.write_text(text,encoding="utf-8")
 print("PASS",folder, len(text))
print("Slides kept unchanged. Completed four layout repairs.")
