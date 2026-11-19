#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kiểm thử độc lập tất cả mã vai trò sau khi xuất bản cấu trúc."""
import json, re, sys, tempfile, subprocess
from pathlib import Path
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
src=(root/"khung-marketing"/"index.html").read_text("utf-8")
m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',src)
assert m, "Missing embedded data"
D=json.loads(m.group(1))
roles={x["id"] for x in D["vi_tri"]}
registry=roles|{x["id"] for x in D["chuc_danh"]}|{x["id"] for x in D["vai_tro"]}|{x["id"] for x in D["don_vi"]}
assert len(roles)==26 and len(D["quy_trinh"])==60 and len(D["danh_muc_van_ban"])==83
steps=[(q["id"],i,b) for q in D["quy_trinh"] for i,b in enumerate(q["buoc"],1)]
assert len(steps)==407
bad_leads=[(qid,i,k) for qid,i,b in steps for k in [str(b["chu_tri_chinh"]).split("|",1)[0]] if k not in registry]
assert not bad_leads, "Mã chủ trì không có trong danh mục: "+repr(bad_leads[:12])
MAP=D["ma_tran_chu_tri_theo_nhom_2027"]
generic=set(MAP)
amb=[(qid,i,b) for qid,i,b in steps if str(b["chu_tri_chinh"]).split("|",1)[0] in generic]
assert len(amb)==95
for qid,i,b in amb:
 code=str(b["chu_tri_chinh"]).split("|",1)[0]
 assert b["ma_vi_tri_nhom_1_2027"]==MAP[code]["nhom_1"], (qid,i)
 assert b["ma_vi_tri_nhom_2_2027"]==MAP[code]["nhom_2"], (qid,i)
 assert b.get("phan_cong_thuc_thi_2027") and b.get("dieu_kien_giao_viec_2027"),(qid,i)
 assert b["ma_vi_tri_nhom_1_2027"] in roles and b["ma_vi_tri_nhom_2_2027"] in roles
selfs=[(qid,i,b) for qid,i,b in steps if str(b["chu_tri_chinh"]).split("|",1)[0] in [str(x).split("|",1)[0] for x in b.get("phoi_hop",[])]]
assert len(selfs)==14
assert all(b.get("chan_trung_nguoi_2027") is True and "hai cá nhân" in b.get("kiem_soat_khong_tu_kiem_2027","") for _,_,b in selfs)
chief={x["id"]:x for x in D["vi_tri"]}
assert "chưa được bàn giao" in chief["cvt"]["muc_dich"]
assert "Không có tuyến báo cáo" in chief["qlth-bc"]["bao_cao_cho"]
assert "Không tự đánh giá" in chief["qlsps"]["bao_cao_cho"]
assert "không cộng trùng" in D["kiem_soat_nguoi_ky_kiem_2027"]["bao_cao"]
assert 'id="tth-operations-integrity-2027"' in src
assert "ops-resolved-owner" in src

# JS không được hỏng cú pháp sau khi chèn nhãn vào luồng. Chạy node --check,
# không truy cập mạng, không thực thi thao tác trình duyệt.
script_pattern=re.compile(r'<script\b([^>]*)>([\s\S]*?)</script>',re.I)
checked=0
for i,(attrs,js) in enumerate(script_pattern.findall(src)):
 if not js.strip():continue
 t=re.search(r'\btype\s*=\s*["\']([^"\']+)["\']',attrs,re.I)
 if t and not any(z in t.group(1).lower() for z in ("javascript","ecmascript","module")):continue
 mode=t and "module" in t.group(1).lower()
 args=["node","--check"]
 if mode:args+=["--input-type=module"]
 args+=["-"]
 try:
  r=subprocess.run(args,input=js,text=True,capture_output=True,timeout=20)
 except FileNotFoundError:
  raise RuntimeError("Runner thiếu Node để kiểm tra mã JS")
 if r.returncode!=0:
  raise AssertionError("JavaScript khung lỗi tại script "+str(i)+": "+r.stderr[:1000])
 checked+=1
assert checked>=1
print("PASS RUNTIME-GUARD: 26 roles, 60 flows, 407 steps, 95 mapped roles, 14 independent checks, "
      +str(checked)+" JS blocks syntactically valid.")
