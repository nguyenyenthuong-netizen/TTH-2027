#!/usr/bin/env python3
"""Remove auxiliary cross-page navigation from all five TTH interfaces.
Restore full viewport for Healthcare App/Website. Preserve the native app UI and slide controls.
"""
from pathlib import Path
import re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
pages=["khung-marketing","trinh-chieu-marketing","crm-da-kenh","healthcare-app","healthcare-website"]
for page in pages:
 p=root/page/"index.html"
 s=p.read_text(encoding="utf-8")
 # old floating return button and style, including stale versions
 s=re.sub(r'<style\s+id=["\']tth-pages-return-style["\'][^>]*>.*?</style>','',s,flags=re.I|re.S)
 s=re.sub(r'<a\b[^>]*\bid=["\']tth-pages-return["\'][^>]*>.*?</a>','',s,flags=re.I|re.S)
 s=re.sub(r'<style\s+id=["\']tth-remove-extra-nav["\'][^>]*>.*?</style>','',s,flags=re.I|re.S)
 # The earlier layout pass inserts a full-width top toolbar but this final pass
 # restores the requested full-size website/app. Remove the conflicting rules
 # and the now-unused resize observer instead of leaving two !important systems.
 if page in ("healthcare-app","healthcare-website"):
  s=re.sub(r'<style\\s+id=["\\\']tth-layout-repair-1811["\\\'][^>]*>.*?</style>','',s,flags=re.I|re.S)
  s=re.sub(r'<script\\s+id=["\\\']tth-measured-toolbar-height-1911["\\\'][^>]*>.*?</script>','',s,flags=re.I|re.S)
  print("tth-clear-conflicting-toolbar",page)
 extra="""/* No secondary navigation bar: native application remains full-size. */
#tth-pages-return{display:none!important}
"""
 if page=="healthcare-app":
  extra+="""
/* Restore original native App controls; remove only external navigation. */
#screen{display:block!important;width:100vw!important;height:100dvh!important;margin:0!important}
.toptools{display:flex!important;position:fixed!important;top:auto!important;bottom:78px!important;left:auto!important;right:9px!important;width:auto!important;min-height:0!important;padding:0!important;background:transparent!important;border:0!important;box-shadow:none!important;z-index:99!important;gap:7px!important;opacity:.98!important}
.toptools button{flex:initial!important;min-height:0!important;cursor:pointer!important;pointer-events:auto!important}
#drawer{position:fixed!important;top:auto!important;bottom:116px!important;right:12px!important;left:auto!important;max-height:55dvh!important;z-index:100!important}
#drawer[hidden]{display:none!important}\n#status{display:none!important}
"""
 elif page=="healthcare-website":
  extra+="""
/* Restore original native Website controls, do not occupy viewport height. */
#frame{display:block!important;width:100%!important;height:100dvh!important;margin:0!important}
#tools{display:flex!important;position:fixed!important;top:auto!important;bottom:10px!important;right:auto!important;left:8px!important;width:auto!important;min-height:0!important;padding:0!important;background:transparent!important;border:0!important;box-shadow:none!important;z-index:500!important;gap:7px!important}
#tools button{flex:initial!important;min-height:0!important;cursor:pointer!important;pointer-events:auto!important}
#catalog{position:fixed!important;top:auto!important;bottom:53px!important;right:auto!important;left:8px!important;max-height:58vh!important;z-index:501!important}
"""
 s=s.replace("</head>",'<style id="tth-remove-extra-nav">'+extra+"</style></head>",1)
 assert s.count('id="tth-remove-extra-nav"')==1, page
 assert 'id="tth-pages-return"' not in s, page
 p.write_text(s,encoding="utf-8")
 print("PASS remove auxiliary nav:",page,len(s))
