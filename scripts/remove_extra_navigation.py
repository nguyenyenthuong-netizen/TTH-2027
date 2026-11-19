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
 extra="""/* No secondary navigation bar: native application remains full-size. */
#tth-pages-return{display:none!important}
"""
 if page=="healthcare-app":
  extra+="""
#screen{height:100dvh!important;width:100vw!important;margin:0!important}
.toptools{display:none!important}
#drawer{display:none!important}
"""
 elif page=="healthcare-website":
  extra+="""
#frame{height:100dvh!important;width:100vw!important;margin:0!important}
#tools{display:none!important}
#catalog{display:none!important}
"""
 s=s.replace("</head>",'<style id="tth-remove-extra-nav">'+extra+"</style></head>",1)
 assert s.count('id="tth-remove-extra-nav"')==1, page
 assert 'id="tth-pages-return"' not in s, page
 p.write_text(s,encoding="utf-8")
 print("PASS remove auxiliary nav:",page,len(s))
