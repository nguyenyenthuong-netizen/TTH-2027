#!/usr/bin/env python3
"""Fix cramped/underlined statistic typography in TTH Healthcare home cards.
Retains every statistic and the fact that some values are demonstration data.
"""
from pathlib import Path
import sys,re,json
p=(Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"healthcare-website"/"index.html")
raw=p.read_text("utf-8")
m=re.search(r'(<script\b[^>]*\bid=["\x27]pagesData["\x27][^>]*>)(.*?)(</script>)',raw,re.S|re.I)
if not m:raise SystemExit("WEB_STAT_FONT: pagesData not found")
pages=json.loads(m.group(2))
if len(pages)!=125:raise SystemExit("WEB_STAT_FONT: unexpected number of website screens")
doc=pages.get("Main.html","")
for text in ("120 bác sĩ","Điểm chất lượng 3,8/5","Chụp CT, MRI","3 bệnh viện"):
 if text not in doc:raise SystemExit("WEB_STAT_FONT: missing card "+text)
if 'id="tth-web-stat-font-fix-2027"' in doc:raise SystemExit("WEB_STAT_FONT: duplicate")
css='''<style id="tth-web-stat-font-fix-2027">
/* Dashboard stats: natural text shaping, no faux-underlined trial values. */
article.card > span[style*="Google Sans Flex"] {
  display:block!important;font-family:Arial,"Segoe UI",Tahoma,sans-serif!important;
  font-size:17px!important;font-weight:700!important;line-height:1.52!important;
  letter-spacing:0!important;word-spacing:normal!important;
  color:#16365E!important;text-decoration:none!important;
  white-space:normal!important;overflow-wrap:break-word!important;
  word-break:normal!important;hyphens:none!important;
  -webkit-font-smoothing:antialiased!important;
}
article.card span.thu {
  display:block!important;font-family:Arial,"Segoe UI",Tahoma,sans-serif!important;
  font-weight:700!important;font-size:17px!important;line-height:1.5!important;
  letter-spacing:0!important;word-spacing:normal!important;
  text-decoration:none!important;text-decoration-line:none!important;
  text-decoration-style:solid!important;border:0!important;
  box-shadow:none!important;white-space:normal!important;
  word-break:normal!important;overflow-wrap:break-word!important;
}
article.card span.thu::after {
  content:"Số liệu minh họa";
  display:block;margin-top:5px;font:500 11.5px/1.35 Arial,"Segoe UI",Tahoma,sans-serif;
  color:#60738F;letter-spacing:0;text-decoration:none!important
}
@media(max-width:640px){
 article.card > span[style*="Google Sans Flex"],article.card span.thu {
  font-size:16px!important;line-height:1.52!important
 }
}
</style>'''
if '</head>' not in doc:raise SystemExit("WEB_STAT_FONT: missing Main head")
doc=doc.replace('</head>',css+'</head>',1)
pages["Main.html"]=doc
encoded=json.dumps(pages,ensure_ascii=False,separators=(",",":")).replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026")
p.write_text(raw[:m.start(2)]+encoded+raw[m.end(2):],"utf-8")
print("WEB_STAT_FONT_OK 4 cards 17px desktop/16px mobile; demo labels retained; no dotted/underline styling")
