#!/usr/bin/env python3
"""Remove the superseded 7-step transfer table from the assembled Marketing frame.

Do not hide with CSS: physically remove the table and its orphan intro.
Preserve the rest of section 19 and all other sections.
"""
from pathlib import Path
import sys

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
file=root/"khung-marketing"/"index.html"
s=file.read_text(encoding="utf-8")
section=s.find('id="m-19"')
if section < 0:
    raise SystemExit("FAIL: section m-19 missing")

needle='<div class="tbl"><table class="t"><thead><tr><th>Bước</th><th>Nội dung</th></tr></thead><tbody>'
a=s.find(needle,section)
next_section=s.find('</section>',section)
if a < 0 or (next_section >= 0 and a > next_section):
    raise SystemExit("FAIL: expected steps table missing from section m-19")
b=s.find('</table></div>',a)
if b<0 or (next_section>=0 and b>next_section):
    raise SystemExit("FAIL: table close missing in section m-19")
b+=len('</table></div>')
fragment=s[a:b]
if fragment.count('<tr>')!=8 or 'Chuyển tiếp: đến hết Giai đoạn 1' not in fragment:
    raise SystemExit("FAIL: refusing to delete unrelated table")

# Remove the caption paragraph too; it describes only the removed 7-step table.
heading='<p><strong>Nguyên tắc xếp người</strong>'
c=s.rfind(heading,section,a)
if c<0 or '</p>' not in s[c:a] or s[c:a].strip()[-4:]!='</p>':
    raise SystemExit("FAIL: personnel-table caption structure changed")
s=s[:c]+s[b:]
assert needle not in s
assert 'id="m-19"' in s
assert '<th>Bệnh viện</th><th>Hiện có</th>' in s
file.write_text(s,encoding="utf-8")
print("PASS: removed section 19 seven-step table and its caption",len(fragment),"characters")
