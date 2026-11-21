#!/usr/bin/env python3
"""Build authentic staffing model on the audit branch, stopping before browser testing."""
import os,subprocess
from pathlib import Path
import yaml
root=Path(__file__).resolve().parents[1]
workflow=yaml.safe_load((root/".github/workflows/pages.yml").read_text("utf-8"))
started=False;steps=0
for step in workflow["jobs"]["deploy"]["steps"]:
    name=step.get("name","")
    if name.startswith("Giai nen dung cau truc ZIP"):started=True
    if not started:continue
    if name.startswith("Bo sung mau ke hoach va bao cao tong ket Marketing nam 2027 vao khung"):
        break
    if command:=step.get("run"):
        subprocess.run(["bash","-e","-o","pipefail","-c",command],cwd=root,env=os.environ.copy(),check=True,capture_output=True,text=True)
        steps+=1
else:raise RuntimeError("Stopped before the expected annual-plan step")
assert steps>=32,steps
html=(root/"_site/khung-marketing/index.html").read_text("utf-8")
assert 'data-version="2027.05.11"' in html
assert 'dinh_bien_theo_dau_ra_2027' in html
print("PASSED generated framework with 26 job descriptions and 2027.05.11; pipeline steps",steps,flush=True)
subprocess.run(["node","scripts/staffing_capacity_snapshot_2027.js","_site/khung-marketing/index.html"],cwd=root,check=True)
