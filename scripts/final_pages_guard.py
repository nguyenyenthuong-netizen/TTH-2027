#!/usr/bin/env python3
"""Final non-destructive presentation guard. Runs AFTER latest overrides are copied.
No changes to business content, approval rights or operational rules.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
targets = {
    "khung-marketing": """
/* Khung: permit wide tables to scroll instead of clipping their cells. */
html,body{max-width:100%;overflow-x:hidden}
main,section,article,.view,.card,.doc-sec{min-width:0}
table{max-width:100%}
table th,table td{overflow-wrap:anywhere;word-break:normal;vertical-align:top}
img,svg,video,iframe{max-width:100%}
:where(button,a,input,select,textarea):focus-visible{outline:2px solid #0837A1;outline-offset:2px}
""",
    "trinh-chieu-marketing": """
/* Slide: protect titles and text from clipping; retain the native arrows. */
html,body{max-width:100%}
.slide{box-sizing:border-box}
.slide h1,.slide h2,.slide h3,.slide p,.slide li{overflow-wrap:break-word}
.slide img,.slide svg,.slide video{max-width:100%}
:where(button,a):focus-visible{outline:2px solid #0837A1;outline-offset:2px}
"""
}
for page, css in targets.items():
    p = root / page / "index.html"
    s = p.read_text(encoding="utf-8")
    start = '<style id="tth-final-pages-guard">'
    if start in s:
        a=s.index(start)
        b=s.index("</style>",a)+len("</style>")
        s=s[:a]+s[b:]
    if "</head>" not in s:
        raise ValueError(f"{page}: missing head tag")
    s=s.replace("</head>",start+css+"</style></head>",1)
    if page == "khung-marketing":
        for term in ("Chuyên viên trưởng Nội dung", "KB-DV12", "tth-line-audit"):
            if term not in s:
                raise ValueError(f"{page}: critical baseline not found: {term}")
    else:
        if s.count('<section class="slide') != 27:
            raise ValueError("Slide count changed; expected 27")
    p.write_text(s,encoding="utf-8")
    print(f"PASS final QA: {page}, {len(s)} chars")
