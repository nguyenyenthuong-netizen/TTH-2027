#!/usr/bin/env python3
"""Rebuild the live framework with exactly the same upstream actions as Pages, but do not deploy.
Stop after the real desktop/mobile browser acceptance test. Never touch main.
"""
import os,subprocess,sys
from pathlib import Path
import yaml
root=Path(__file__).resolve().parents[1]
workflow=yaml.safe_load((root/".github/workflows/pages.yml").read_text(encoding="utf-8"))
steps=workflow["jobs"]["deploy"]["steps"]
started=False;count=0
for step in steps:
 name=step.get("name","")
 if name.startswith("Giai nen dung cau truc ZIP"):started=True
 if not started:continue
 command=step.get("run")
 if command:
  print("RUN",name,flush=True)
  subprocess.run(["bash","-e","-o","pipefail","-c",command],cwd=root,check=True,env=os.environ.copy())
  count+=1
 if name.startswith("Thu 8 luong thuc te tren desktop va mobile"):
  break
else:
 raise RuntimeError("Không tìm thấy bước kiểm thử trình duyệt chính")
assert count>=35,count
html=(root/"_site/khung-marketing/index.html").read_text(encoding="utf-8")
for marker in ('data-version="2027.05.11"','id="dinh-bien-2027"','Kiem tra' if False else 'CMS website/App'):
 assert marker in html,marker
print("PASS dựng Khung 12 phần, định biên 2027.05.11 và Chrome desktop/mobile, bước chạy:",count,flush=True)
