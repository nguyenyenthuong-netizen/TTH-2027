#!/usr/bin/env python3
"""Guard the exact TTH CRM three-stage decision slide after every publication build.
This verifies the finished CRM HTML, never edits the Marketing framework.
"""
import sys,re,html
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"crm-da-kenh"/"index.html"
s=p.read_text("utf-8")
parts=re.search(r'<div class="roadmap">(?P<body>.*?)</div>\s*<div class="decisionGrid">',s,re.I|re.S)
if not parts:raise SystemExit("CRM_PHASE_GATE: missing roadmap or decision panel")
road=parts.group('body')
cards=re.findall(r'<div class="phase">\s*<div class="phase-index">(\d+)</div>\s*<div class="eyebrow">(.*?)</div>\s*<b>(.*?)</b>\s*<small>(.*?)</small>\s*</div>',road,re.I|re.S)
if len(cards)!=3:raise SystemExit(f"CRM_PHASE_GATE: expected 3 stages, found {len(cards)}")
def norm(s):
 s=re.sub(r'<br\s*/?>',' + ',s,flags=re.I)
 s=re.sub(r'<[^>]+>',' ',s)
 return ' '.join(html.unescape(s).split()).replace(' + + ',' + ')
one,two,three=cards
if one[0]!="01" or norm(one[2])!="CRM + Call Center + HIS":
 raise SystemExit("CRM_PHASE_GATE: wrong phase 1 "+repr(one))
if two[0]!="02" or norm(two[2])!="Đa kênh":
 raise SystemExit("CRM_PHASE_GATE: phase 2 must be ONLY multichannel "+repr(two))
if three[0]!="03" or norm(three[2])!="Đo lường + AI":
 raise SystemExit("CRM_PHASE_GATE: phase 3 was changed "+repr(three))
if not all(("CRM" in one[3],"Call Center" in one[3],"HIS" in one[3])):
 raise SystemExit("CRM_PHASE_GATE: missing responsibility explanation in phase 1")
if "HIS" in two[3]:
 raise SystemExit("CRM_PHASE_GATE: phase 2 explanation still includes HIS as a new workstream")
if not all(("Zalo" in two[3],"Fanpage" in two[3],"Website" in two[3])):
 raise SystemExit("CRM_PHASE_GATE: multichannel scope incompletely explained")
print("CRM_PHASE_GATE_OK stage1=",norm(one[2]),"stage2=",norm(two[2]),"stage3=",norm(three[2]),"phase1_detail=",norm(one[3]),"phase2_detail=",norm(two[3]))
