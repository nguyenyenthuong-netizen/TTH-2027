#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gắn 07 kết quả cuối năm và 84 điểm kiểm soát tháng vào sổ kế hoạch Mục 05.
Không thay thế KPI gốc hoặc tự gán số nền, giờ chuẩn, ngân sách, doanh thu.
"""
import csv, json, sys
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
def main(site):
    path=site/"ke-hoach-mkt-2027"/"data.json"
    d=json.loads(path.read_text("utf-8"))
    y=json.loads((REPO/"pages-overrides/catalog/marketing-2027-outcome-contract.json").read_text("utf-8"))
    assert len(d["roles"])==26 and len(d["portfolio"]["projects"])==24
    assert len(y["outcomes"])==7 and len(y["monthlyGates"])==84
    codes=[c["code"] for c in y["outcomes"]]
    assert len(set(codes))==7
    allkpis=[k for c in y["outcomes"] for k in c["kpis"]]
    assert len(allkpis)==25 and len(set(k["id"] for k in allkpis))==25
    assert {x["month"] for x in y["monthlyGates"]}==set(range(1,13))
    assert all(sum(x["resultId"]==code for x in y["monthlyGates"])==12 for code in codes)
    assert all(k["baseline2026"] is None and k["target2027"] is None for k in allkpis)
    assert all(g["targetValue"] is None and g["plannedBudgetVND"] is None and g["plannedHours"] is None for g in y["monthlyGates"])
    assert all(c["ownerRole"] and c["projects"] and c["evidence"] and c["costBasis"] for c in y["outcomes"])
    # Các mã TD27 là tham chiếu đến PHỤ LỤC đang đối chiếu, không tự tạo mục mới.
    appendix={p["code"] for p in d["ctdaAddendum"]["programs"]}
    assert all(code in appendix for c in y["outcomes"] for code in c["projects"])
    existing=(len(d["portfolio"]["programs"]),len(d["portfolio"]["projects"]),len(d["portfolio"]["tasks"]))
    d["yearEndCommitments"]=y
    assert existing==(len(d["portfolio"]["programs"]),len(d["portfolio"]["projects"]),len(d["portfolio"]["tasks"]))
    path.write_text(json.dumps(d,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    with (site/"ke-hoach-mkt-2027/ket-qua-cuoi-nam-2027.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(["Mã kết quả","Kết quả cần nhận","Một chủ kết quả","Phạm vi","Mã chỉ số dự thảo","Công thức","Nguồn xác minh","Người kiểm","Số nền 2026","Mục tiêu 2027","Ngân sách","Giờ công","Trạng thái"])
        for c in y["outcomes"]:
            for k in c["kpis"]:
                w.writerow([c["code"],c["title"],c["ownerRole"],c["scope"],k["id"],k["formula"],k["source"],k["checker"],"Chưa xác nhận","Chưa duyệt","Chưa duyệt","Chưa chốt","CHUA_KHOA"])
    with (site/"ke-hoach-mkt-2027/kiem-soat-muc-tieu-thang-2027.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f);w.writerow(["Mã kết quả","Tháng","Cổng kiểm soát","Chỉ tiêu tháng","Ngân sách tháng","Giờ công tháng","Trạng thái"])
        for x in y["monthlyGates"]:w.writerow([x["resultId"],x["month"],x["expectedCheckpoint"],"Chưa duyệt","Chưa duyệt","Chưa chốt",x["status"]])
    (site/"ke-hoach-mkt-2027/ket-qua-cuoi-nam-2027.json").write_text(json.dumps(y,ensure_ascii=False,indent=2),encoding="utf-8")
    print("PASS outcome contract: 7 year-end results, 25 evidence metrics, 84 monthly checkpoints. 6/24/288 kept. Zero invented financial or baseline targets.")
if __name__=="__main__":
    main(Path(sys.argv[1] if len(sys.argv)>1 else "_site"))
