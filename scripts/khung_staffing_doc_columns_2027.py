"""Fix the four-column staffing document assignment table without touching model data."""
from pathlib import Path
import re
import sys

p = Path(sys.argv[1]) / 'khung-marketing' / 'index.html'
s = p.read_text('utf-8')
signature = 'function table(headers,rows,numbers=[],mobile=true){return '
if 'doc-responsibility' not in s:
    if s.count(signature) != 1:
        raise SystemExit('Cannot identify unique staffing table renderer')
    s = s.replace(signature,
        "function table(headers,rows,numbers=[],mobile=true){const docTable=headers[0]==='Hồ sơ, phạm vi và hạn';return ", 1)
    dollar = '$'
    old = 'class="tbl ' + dollar + "{mobile?'mobile':''}" + '"'
    new = 'class="tbl ' + dollar + "{mobile?'mobile':''} " + dollar + "{docTable?'doc-responsibility':''}" + '"'
    if s.count(old) != 1:
        raise SystemExit('Cannot identify unique staffing table class')
    s = s.replace(old, new, 1)

marker = '/* tth-2027-doc-columns-v1 */'
style = """
/* tth-2027-doc-columns-v1 */
.tbl.doc-responsibility {width:100%;table-layout:fixed;}
.tbl.doc-responsibility thead th:nth-child(1){width:40%;}
.tbl.doc-responsibility thead th:nth-child(2){width:23%;}
.tbl.doc-responsibility thead th:nth-child(3){width:12%;}
.tbl.doc-responsibility thead th:nth-child(4){width:25%;}
.tbl.doc-responsibility th{word-break:normal;overflow-wrap:normal;white-space:normal;}
.tbl.doc-responsibility td{word-break:normal;overflow-wrap:break-word;line-height:1.5;}
@media(min-width:761px) and (max-width:1050px){
  .tbl.doc-responsibility{min-width:980px;}
}
@media(max-width:760px){
  .tbl.doc-responsibility{table-layout:auto;min-width:0;}
}
"""
if marker not in s:
    rgx = re.compile(r'(<script[^>]*\bid=["\']tth-staffing-style["\'][^>]*>)(.*?)(</script>)', re.S)
    m = rgx.search(s)
    if not m:
        raise SystemExit('No staffing CSS block present')
    s = s[:m.start()] + m.group(1) + m.group(2) + '\n' + style + m.group(3) + s[m.end():]

if s.count(marker) != 1 or 'docTable?' not in s:
    raise SystemExit('Staffing column patch failed integrity check')
p.write_text(s,'utf-8')
print('PASS: TTH Muc 05 document columns 40/23/12/25; no staffing figures changed')
