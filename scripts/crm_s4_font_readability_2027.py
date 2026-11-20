#!/usr/bin/env python3
"""Enlarge only CRM responsibility rule and 1900 booking workflow typography.
Keep existing text, colors and diagram; allow natural wrapping and height.
"""
import re,sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"crm-da-kenh"/"index.html"
s=p.read_text("utf-8")
for marker in ('class="role-rule"','class="tier-example"','class="tier-example-label"','class="tier-example-flow"'):
 if s.count(marker)!=1:raise SystemExit(f"CRM_TYPO: missing/duplicate target {marker}: {s.count(marker)}")
css='''<style id="tth-crm-s4-readability-2027">
/* Responsibility statement: larger, readable at 100% zoom. */
#s4 .role-rule{
  display:flex!important;flex-wrap:wrap!important;align-items:center!important;
  gap:9px 18px!important;padding:16px 19px!important;
  height:auto!important;min-height:90px!important;max-height:none!important;
  overflow:visible!important;box-sizing:border-box!important;
}
#s4 .role-rule>span{
  font-size:14px!important;line-height:1.42!important;
  letter-spacing:.065em!important;flex:0 1 190px!important;
  min-width:140px!important;white-space:normal!important;
}
#s4 .role-rule>strong{
  font-size:17px!important;line-height:1.48!important;
  font-weight:760!important;flex:1 1 560px!important;min-width:0!important;
  white-space:normal!important;overflow-wrap:break-word!important;
}
#s4 .tier-example{
  height:auto!important;min-height:0!important;max-height:none!important;
  padding:16px 19px!important;overflow:visible!important;box-sizing:border-box!important;
}
#s4 .tier-example-label{
  font-size:15px!important;line-height:1.42!important;letter-spacing:.045em!important;
  font-weight:800!important;margin-bottom:11px!important;white-space:normal!important;
}
#s4 .tier-example-flow{
  align-items:stretch!important;gap:8px!important;min-width:0!important;
  height:auto!important;min-height:0!important;max-height:none!important;
  overflow:visible!important;
}
#s4 .tier-example-flow>span{
  font-size:16px!important;line-height:1.45!important;min-width:0!important;
  min-height:77px!important;height:auto!important;max-height:none!important;
  padding:12px 13px!important;box-sizing:border-box!important;
  white-space:normal!important;overflow-wrap:break-word!important;
  display:flex!important;flex-direction:column!important;justify-content:center!important;
}
#s4 .tier-example-flow>span>b{
  font:800 16px/1.38 Arial,"Segoe UI",sans-serif!important;
  display:inline!important;
}
#s4 .tier-example-flow>i{
  font-size:20px!important;align-self:center!important;line-height:1!important;
  flex:0 0 auto!important;
}
#s4 .tier-example>p{
  font-size:15px!important;line-height:1.5!important;margin-top:11px!important;
  color:#344C73!important;overflow-wrap:break-word!important;
}
#s4 .tier-example>p strong{font-weight:800!important;color:#173E80!important}
@media(max-width:1050px){
  #s4 .tier-example-flow{display:flex!important;flex-direction:column!important;align-items:stretch!important}
  #s4 .tier-example-flow>span{min-height:0!important;padding:11px 13px!important}
  #s4 .tier-example-flow>i{transform:rotate(90deg)!important;margin:0 auto!important}
  #s4 .role-rule{align-items:flex-start!important}
  #s4 .role-rule>span{flex:1 1 100%!important}
  #s4 .role-rule>strong{flex:1 1 100%!important}
}
@media(max-width:700px){
  #s4 .role-rule{padding:12px!important}
  #s4 .role-rule>strong{font-size:16px!important}
  #s4 .tier-example{padding:12px!important}
  #s4 .tier-example-flow>span{font-size:15px!important}
}
</style>'''
if 'id="tth-crm-s4-readability-2027"' in s:raise SystemExit("CRM_TYPO already applied")
if "</head>" not in s:raise SystemExit("CRM_TYPO no head to inject style")
s=s.replace("</head>",css+"</head>",1)
p.write_text(s,"utf-8")
print("CRM_S4_FONTS_OK rule=17px flow-cards=16px headings=14-15px exception=15px; dynamic card height")
