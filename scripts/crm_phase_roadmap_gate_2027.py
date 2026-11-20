#!/usr/bin/env python3
"""Prevent CRM 2-stage / seven-slide scope regressions in each production build."""
from pathlib import Path
import sys,re,html
s=(Path(sys.argv[1] if len(sys.argv)>1 else "_site")/"crm-da-kenh"/"index.html").read_text("utf-8")
m=re.search(r'<div class="roadmap">(.*?)</div>\s*<div class="decisionGrid">',s,re.I|re.S)
if not m:raise SystemExit("CRM_2PHASE_GATE: roadmap missing")
road=m.group(1)
cards=re.findall(r'<div class="phase">\s*<div class="phase-index">(\d+)</div>\s*<div class="eyebrow">(.*?)</div>\s*<b>(.*?)</b>\s*<small>(.*?)</small>\s*</div>',road,re.I|re.S)
if len(cards)!=2:raise SystemExit(f"CRM_2PHASE_GATE: expected exactly 2 stages, found {len(cards)}")
def norm(s):
 s=re.sub(r'<br\s*/?>',' + ',s,flags=re.I)
 return " ".join(html.unescape(re.sub(r'<[^>]+>',' ',s)).split())
one,two=cards
if (one[0],norm(one[2]))!=("01","CRM + Call Center + HIS"):
 raise SystemExit("CRM_2PHASE_GATE: incorrect first stage "+repr(one[:3]))
if (two[0],norm(two[2]))!=("02","AI"):
 raise SystemExit("CRM_2PHASE_GATE: incorrect second stage "+repr(two[:3]))
for term in ["Chat","Fanpage","Zalo","TikTok","Call","Ads","Web","HIS","chatbot","kịch bản"]:
 if term.lower() not in one[3].lower():raise SystemExit("CRM_2PHASE_GATE: stage 1 missing "+term)
for term in ["ticket hỗ trợ từ cuộc gọi","AI Call","AI Chat","ticket hỗ trợ từ Chat"]:
 if term.lower() not in two[3].lower():raise SystemExit("CRM_2PHASE_GATE: stage 2 missing "+term)
if "GIAI ĐOẠN 3" in road:raise SystemExit("CRM_2PHASE_GATE: residual third stage")
for n in range(1,8):
 if len(re.findall(r'<section class="slide(?: active)?" id="s'+str(n)+'">',s))!=1:
  raise SystemExit("CRM_2PHASE_GATE: missing or duplicate slide "+str(n))
for term in ["Bizfly CRM","Bizfly Chat","Bizfly Call Center","Bizfly Ticket","Bizfly Email MKT","ZBS/SMS"]:
 if term not in s:raise SystemExit("CRM_2PHASE_GATE: internal input row absent "+term)
if len(re.findall(r'<tr><td data-label="STT">',s))!=6:
 raise SystemExit("CRM_2PHASE_GATE: internal table needs six service rows")
for term in ["Thông tin nội bộ cần chốt","active===slides.length-1","Math.min(slides.length-1,i)","01 / 07","7 màn quyết định"]:
 if term not in s:raise SystemExit("CRM_2PHASE_GATE: CRM navigation regression "+term)
if "tth-crm-final-two-phases-and-internal-2027" not in s:
 raise SystemExit("CRM_2PHASE_GATE: responsive styling missing")
print("CRM_2PHASE_GATE_OK stages:",norm(one[2]),"/",norm(two[2]),"slides:7 internal_service_rows:6")
