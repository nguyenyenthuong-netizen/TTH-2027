#!/usr/bin/env python3
"""Improve existing CRM advanced search, preserving query, filter and navigation logic.
No extra search trigger; panel opens as a spacious readable dialog.
"""
from pathlib import Path
import sys
p=Path(sys.argv[1] if len(sys.argv)>1 else '_site')/'crm-da-kenh'/'index.html'
s=p.read_text('utf8')
for marker in ('id="ux-advanced-search-style"','#ux-search-panel .ux-res .ux-title','#ux-search-panel .ux-res .ux-excerpt'):
 if marker not in s:raise SystemExit('CRM_SEARCH_UI: expected original search element missing '+marker)
if 'id="tth-crm-search-readability-2027"' in s:raise SystemExit('CRM_SEARCH_UI: duplicate optimization')
css='''<style id="tth-crm-search-readability-2027">
/* Keep only the existing search launcher. Search dialog is intentionally spacious. */
#ux-search-panel{top:clamp(14px,4vh,35px)!important;right:clamp(12px,3vw,42px)!important;
 left:auto!important;bottom:auto!important;transform:none!important;
 width:min(700px,calc(100vw - 32px))!important;
 max-width:calc(100vw - 32px)!important;
 max-height:calc(100dvh - 50px)!important;
 border-radius:16px!important;border-color:#B5C9E9!important;
 box-shadow:0 18px 54px #0C2C6052!important;z-index:2147483001!important}
#ux-search-panel .ux-hd{min-height:60px!important;padding:13px 20px!important;gap:12px!important}
#ux-search-panel .ux-hd strong{font-size:19px!important;line-height:1.35!important}
#ux-search-panel .ux-exit{font-size:14px!important;min-height:35px!important;padding:6px 12px!important}
#ux-search-panel .ux-fields{padding:14px 18px 13px!important;gap:11px!important}
#ux-search-panel input:not([type=checkbox]),#ux-search-panel select{
 min-height:43px!important;font-size:15px!important;padding:10px 13px!important;line-height:1.35!important}
#ux-search-panel .ux-grid{gap:11px!important}
#ux-search-panel label{font-size:14px!important;line-height:1.42!important;gap:8px!important}
#ux-search-panel label.ux-check input{width:18px!important;height:18px!important}
#ux-search-panel .ux-hint{font-size:13px!important;line-height:1.48!important;color:#596F8B!important}
#ux-search-panel .ux-res{padding:7px 10px 12px!important;overflow-x:hidden!important;scrollbar-width:thin!important}
#ux-search-panel .ux-res button{padding:14px 15px!important;border:1px solid #E0E8F4!important;
 border-radius:12px!important;margin:7px 0!important;background:#FFF!important;line-height:1.43!important}
#ux-search-panel .ux-res button:hover,#ux-search-panel .ux-res button:focus-visible{
 background:#F0F5FF!important;border-color:#9DBCE8!important;outline:2px solid #9BC3F2!important}
#ux-search-panel .ux-res .ux-title{display:block!important;font-size:16px!important;
 line-height:1.48!important;font-weight:800!important;margin-top:4px!important;
 white-space:normal!important;overflow-wrap:break-word!important}
#ux-search-panel .ux-res .ux-group{display:inline-block!important;font-size:12px!important;
 line-height:1.4!important;padding:4px 8px!important;margin:0 0 5px!important;
 background:#E8F0FC!important;color:#25517F!important;border-radius:7px!important}
#ux-search-panel .ux-res .ux-excerpt{font-size:14px!important;line-height:1.5!important;
 color:#4B637F!important;max-height:4.5em!important;margin-top:7px!important;
 overflow:hidden!important;overflow-wrap:break-word!important;
 display:-webkit-box!important;-webkit-line-clamp:3!important;-webkit-box-orient:vertical!important}
#ux-search-panel .ux-footer{font-size:13px!important;line-height:1.42!important;padding:9px 18px!important}
@media(max-width:720px){
 #ux-search-panel{top:8px!important;right:8px!important;left:8px!important;
 width:calc(100vw - 16px)!important;max-width:none!important;max-height:calc(100dvh - 16px)!important}
 #ux-search-panel .ux-hd{padding:11px 13px!important}
 #ux-search-panel .ux-hd strong{font-size:17px!important}
 #ux-search-panel .ux-fields{padding:10px 12px!important;gap:9px!important}
 #ux-search-panel .ux-grid{grid-template-columns:1fr!important;gap:8px!important}
 #ux-search-panel .ux-res{padding:4px 7px!important}
 #ux-search-panel .ux-res button{padding:10px 11px!important;margin:6px 0!important}
 #ux-search-panel .ux-res .ux-title{font-size:15px!important}
 #ux-search-panel .ux-res .ux-excerpt{font-size:13px!important}
}
</style>'''
s=s.replace('</head>',css+'</head>',1)
p.write_text(s,'utf8')
print('CRM_SEARCH_UI_OK width <=700px desktop, readable result title 16px, 14px snippets, responsive modal')
