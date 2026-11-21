#!/usr/bin/env python3
"""Build a reviewed, software-import-ready Marketing 2027 plan package.

The project plan, 26-role monthly plan, issued-artifact ledger and the original
Muc 05 staffing model are separate sources of truth.  Their records are linked,
not added together as if they were extra working hours.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"pages-overrides/catalog"
FIELD_TASKS=[
 "module","programId","projectId","parentId","taskId","deliverableId","name","deliverable",
 "startDate","dueDate","month","stageId","stageCode","stageName","stageExitGate","gateStatus","ownerRoleId","executorRoleId","reviewerRoleId",
 "approver","brandGroup","units","channel","activationGate","status","dependencies",
 "kpiIds","completionEvidence","workloadLedgerId","approvedBudgetVND","approvedKpi",
 "proposedPersonId","actualDoneDate","actualHours"
]
FIELD_STAGES=[
 "programId","projectId","stageId","stageCode","stageName","stageOrder",
 "plannedStartMonth","plannedEndMonth","plannedStartDate","plannedEndDate",
 "ownerRoleId","reviewerRoleId","entryGate","exitGate","acceptanceEvidence",
 "dependencies","milestoneCount","stageProducts","stageStatus","conditionalActivation",
 "plannedHours","actualHours","approvedAt","reviewDate","isApproved"
]
FIELD_ARTIFACTS=[
 "artifactId","code","title","category","source","reported","proposalOnly",
 "parentCode","ownerRoleId","writerRoleId","reviewerRoleId","scope",
 "plannedDeadline","baselineApproval","baselineVersion","currentVersion",
 "status","issuanceEvidence","sourceTaskId","sourceWorkModule"
]
FIELD_EVENTS=[
 "eventId","artifactId","eventType","version","decisionNumber","eventDate",
 "effectiveFrom","workSource","projectId","taskId","approvedBy","evidenceUrl","isVerified"
]
PERMITTED_EVENT_TYPES={
 "BAN_HANH_MOI","BAN_HANH_SUA_DOI","THAY_THE","THU_HOI","HET_HIEU_LUC","TAI_HIEU_LUC"
}
RELEASE_EVENTS={"BAN_HANH_MOI","BAN_HANH_SUA_DOI","THAY_THE","TAI_HIEU_LUC"}
WITHDRAW_EVENTS={"THU_HOI","HET_HIEU_LUC"}

def write_csv(path, columns, rows):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns,extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out={}
            for col in columns:
                v=row.get(col)
                if isinstance(v,(list,dict)):
                    v=json.dumps(v,ensure_ascii=False,separators=(",",":"))
                if v is None:
                    v=""
                if isinstance(v,str) and v[:1] in ("=","+","-","@"):
                    v="'"+v
                out[col]=v
            writer.writerow(out)

def valid_event(e,known_ids):
    required=FIELD_EVENTS
    if e.get("isVerified") is not True or e.get("eventType") not in PERMITTED_EVENT_TYPES:
        return False
    if e.get("artifactId") not in known_ids:
        return False
    if any(e.get(k) in (None,"") for k in required if k not in {"projectId"}):
        return False
    try:
        date.fromisoformat(e["eventDate"])
        date.fromisoformat(e["effectiveFrom"])
    except (ValueError,TypeError):
        return False
    return True

def summarize_issuance(registry):
    catalog=registry["catalog"]
    ids={a["artifactId"]:a for a in catalog if a["reported"]}
    all_events=registry["events"]
    ids_events=[e["eventId"] for e in all_events]
    assert len(ids_events)==len(set(ids_events)),"Trung ma su kien ban hanh"
    valid=[e for e in all_events if valid_event(e,set(ids))]
    invalid=[e.get("eventId","?") for e in all_events if not valid_event(e,set(ids))]
    seen_versions=set()
    dedup=[]
    for e in sorted(valid,key=lambda x:(x["eventDate"],x["eventId"])):
        key=(e["artifactId"],e["eventType"],e["version"])
        if key in seen_versions:
            invalid.append(e["eventId"]+" / trung phien ban-su kien")
            continue
        seen_versions.add(key)
        dedup.append(e)
    periods=[]
    for month in range(1,13):
        cutoff=date(2027,month,1)
        start=cutoff.isoformat()
        end=date(2027 if month<12 else 2028,month+1 if month<12 else 1,1).isoformat()
        in_month=[e for e in dedup if start<=e["eventDate"]<end]
        # Effective state is evaluated at the period end. Baseline 2026 is
        # unknown until entered and verified, so this is never presented as the
        # full number of active documents.
        state={}
        for e in dedup:
            if e["effectiveFrom"]>=end or e["eventDate"]>=end:
                continue
            if e["eventType"] in RELEASE_EVENTS:
                state[e["artifactId"]]="HIEU_LUC"
            elif e["eventType"] in WITHDRAW_EVENTS:
                state[e["artifactId"]]="THU_HOI"
        released=[e for e in in_month if e["eventType"] in RELEASE_EVENTS]
        categories=defaultdict(lambda:{"new":set(),"revised":set(),"anyRelease":set(),"withdrawn":set()})
        sources=defaultdict(set)
        for e in in_month:
            c=categories[ids[e["artifactId"]]["category"]]
            if e["eventType"]=="BAN_HANH_MOI":
                c["new"].add(e["artifactId"])
            if e["eventType"] in {"BAN_HANH_SUA_DOI","THAY_THE"}:
                c["revised"].add((e["artifactId"],e["version"]))
            if e["eventType"] in RELEASE_EVENTS:
                c["anyRelease"].add(e["artifactId"])
                sources[e["workSource"]].add(e["artifactId"])
            if e["eventType"] in WITHDRAW_EVENTS:
                c["withdrawn"].add(e["artifactId"])
        periods.append({
            "month":month,"start":start,"endExclusive":end,
            "newCount":len(set(e["artifactId"] for e in in_month if e["eventType"]=="BAN_HANH_MOI")),
            "revisedVersionCount":len(set((e["artifactId"],e["version"]) for e in in_month if e["eventType"] in {"BAN_HANH_SUA_DOI","THAY_THE"})),
            "uniqueReleasedCount":len(set(e["artifactId"] for e in released)),
            "withdrawnCount":len(set(e["artifactId"] for e in in_month if e["eventType"] in WITHDRAW_EVENTS)),
            "activeAtEndWithVerified2027EventsOnly":sum(x=="HIEU_LUC" for x in state.values()),
            "byCategory":{k:{m:len(v) for m,v in vals.items()} for k,vals in categories.items()},
            "bySource":{k:len(v) for k,v in sources.items()},
            "dataStatus":"DA_CO_CHUNG_TU" if dedup else "CHUA_CO_SU_KIEN_BAN_HANH_DUOC_XAC_MINH"
        })
    def period_result(label,start,end):
        events=[e for e in dedup if start<=e["eventDate"]<end]
        published=[e for e in events if e["eventType"] in RELEASE_EVENTS]
        revised=[e for e in events if e["eventType"] in {"BAN_HANH_SUA_DOI","THAY_THE"}]
        withdrawn=[e for e in events if e["eventType"] in WITHDRAW_EVENTS]
        out=defaultdict(lambda:{"new":set(),"revisedVersions":set(),"distinctPublished":set(),"withdrawn":set()})
        by_source=defaultdict(lambda:{"new":set(),"revisedVersions":set(),"distinctPublished":set()})
        for e in events:
            row=out[ids[e["artifactId"]]["category"]]
            source=by_source[e["workSource"]]
            if e["eventType"]=="BAN_HANH_MOI":
                row["new"].add(e["artifactId"])
                source["new"].add(e["artifactId"])
            if e["eventType"] in {"BAN_HANH_SUA_DOI","THAY_THE"}:
                row["revisedVersions"].add((e["artifactId"],e["version"]))
                source["revisedVersions"].add((e["artifactId"],e["version"]))
            if e["eventType"] in RELEASE_EVENTS:
                row["distinctPublished"].add(e["artifactId"])
                source["distinctPublished"].add(e["artifactId"])
            if e["eventType"] in WITHDRAW_EVENTS:
                row["withdrawn"].add(e["artifactId"])
        known_state={}
        for e in dedup:
            if e["eventDate"]>=end or e["effectiveFrom"]>=end:
                continue
            if e["eventType"] in RELEASE_EVENTS:
                known_state[e["artifactId"]]="HIEU_LUC"
            if e["eventType"] in WITHDRAW_EVENTS:
                known_state[e["artifactId"]]="KHONG_HIEU_LUC"
        return {
            "period":label,"start":start,"endExclusive":end,
            "banHanhMoi":len({e["artifactId"] for e in events if e["eventType"]=="BAN_HANH_MOI"}),
            "suaDoi":len({(e["artifactId"],e["version"]) for e in revised}),
            "maBanHanhKhongTrung":len({e["artifactId"] for e in published}),
            "thuHoi":len({e["artifactId"] for e in withdrawn}),
            "dangHieuLucCoChungTuTrongSo":sum(v=="HIEU_LUC" for v in known_state.values()),
            "byCategory":{k:{metric:len(group) for metric,group in state.items()} for k,state in out.items()},
            "byWorkSource":{k:{metric:len(group) for metric,group in state.items()} for k,state in by_source.items()},
            "missingSourceOrEvidence":len(invalid),
            "baselineCoverageVerified":False,
            "status":"CHUA_CO_SU_KIEN_DUOC_XAC_MINH" if not dedup else "CHI_TINH_TREN_SU_KIEN_CO_CHUNG_TU",
            "interpretation":"So dang hieu luc chua phai tong day du neu chua du ban goc da ban hanh truoc 2027. Gop theo phan he can bao toan ma goc de khong trung."
        }
    quarters=[
        period_result("Quy %s"%q,"2027-%02d-01"%(3*q-2),"2027-%02d-01"%(3*q+1) if q<4 else "2028-01-01")
        for q in range(1,5)
    ]
    year=period_result("Nam 2027","2027-01-01","2028-01-01")
    new_year={e["artifactId"] for e in dedup if e["eventDate"][:4]=="2027" and e["eventType"]=="BAN_HANH_MOI"}
    updated_year={(e["artifactId"],e["version"]) for e in dedup if e["eventDate"][:4]=="2027" and e["eventType"] in {"BAN_HANH_SUA_DOI","THAY_THE"}}
    return {
        "dataStatus":"CHUA_XAC_NHAN_THUC_TE" if not dedup else "CHI_TINH_BAN_HANH_CO_CHUNG_TU_DA_NHAP",
        "notCountedCatalogRows":len(catalog), "validEvents":len(dedup),
        "invalidEvents":invalid,
        "newDistinctArtifacts2027":len(new_year), "revisedDistinctVersions2027":len(updated_year),
        "monthly":periods,
        "quarterly":quarters,
        "annual":year,
        "note":"Chua co du lieu duoc xac minh thi KHONG duoc suy dien 0 la ket qua thuc. Khong tu cong so ma danh muc thanh so da ban hanh."
    }

def prepare(site):
    cat=json.loads((SOURCE/"ke-hoach-mkt-2027-data.json").read_text("utf-8"))
    portfolio=json.loads((SOURCE/"marketing-2027-portfolio.json").read_text("utf-8"))
    issuance=json.loads((SOURCE/"marketing-2027-issuance-register.json").read_text("utf-8"))
    roles={r["id"] for r in cat["roles"]}
    programs={p["programId"] for p in portfolio["programs"]}
    projects={p["projectId"] for p in portfolio["projects"]}
    priority=portfolio["tasks"]
    assert len(roles)==26 and len(cat["monthlyActions"])>=624
    assert len(programs)==6 and len(projects)==24 and len(priority)==288
    assert len(portfolio["kpis"])==23 and len(issuance["catalog"])==325
    assert len(portfolio["stageRegister"])==64 and len(portfolio["namedTwoPhaseInitiatives"])==2
    stage_ids={x["stageId"] for x in portfolio["stageRegister"]}
    assert len(stage_ids)==64 and all(t.get("stageId") in stage_ids for t in priority)
    for p in portfolio["projects"]:
        pieces=sorted((x for x in portfolio["stageRegister"] if x["projectId"]==p["projectId"]),key=lambda x:x["plannedStartMonth"])
        assert [m for stage in pieces for m in range(stage["plannedStartMonth"],stage["plannedEndMonth"]+1)]==list(range(1,13)), p["projectId"]
    for phase in portfolio["stageRegister"]:
        assert phase["stageProducts"] and phase["exitGate"] and phase["acceptanceEvidence"]
        assert all(t["stageId"]==phase["stageId"] for t in priority if t["taskId"] in {o["taskId"] for o in phase["stageProducts"]})
    assert all(p["programId"] in programs for p in portfolio["projects"])
    assert all(t["projectId"] in projects and t["ownerRoleId"] in roles for t in priority)
    assert len(set(t["taskId"] for t in priority))==len(priority)
    assert all(set(t["month"] for t in priority if t["projectId"]==p)==set(range(1,13)) for p in projects)
    assert len(set(a["artifactId"] for a in issuance["catalog"]))==len(issuance["catalog"])

    # The recurring register comes from the SAME W ledger used by Muc 05;
    # it is not a second list of work hours or production commitments.
    site_html=(site/"khung-marketing/index.html").read_text("utf-8")
    m=re.search(r'<script id="csdl" type="application/json">([\s\S]*?)</script>',site_html)
    assert m,"Khung staffing JSON missing"
    model=json.loads(m[1])["dinh_bien_theo_dau_ra_2027"]
    operations=[]
    for work in model["work"]:
        role=work["role"]
        locs=[s for s in model["sites"] if role in ({"dmpk"} if s["group"]=="clinic" else {"tn-a","mdcs-a","qhcs"} if s["group"]=="g1" else {"tn-b","mdcs-b"})] if model["roles"][role]["to"]=="coso" else [None]
        for loc in locs:
            sid=loc["id"] if loc else "tct"
            operations.append({
                "taskId":"MKT27-R-"+re.sub(r"[^A-Za-z0-9_-]","_",work["id"])+"-"+sid,
                "module":"Hoạt động thường xuyên",
                "workloadLedgerId":work["id"]+("@"+sid if loc else ""),
                "name":work["name"],"ownerRoleId":role,"executorRoleId":role,
                "locationId":sid,"locationName":loc["name"] if loc else "Tổng công ty",
                "quantityRule":work["q"],"frequency":work["period"],
                "minutesByStage":work["t"],"unitMinutes":sum(work["t"]),
                "sourceRefs":work["ref"],"kind":work["kind"],
                "loadSource":"Mục 05 - sổ W đã hạch toán",
                "isNewBillableWork":False,
                "status":"Chưa giao thực tế" if work["kind"]!="G" else "Chưa kích hoạt",
                "personId":None,"evidenceId":None,"approvedActualHours":None,
                "softwareTaskType":"RecurringTemplate", "year":2027
            })
    ids=[o["taskId"] for o in operations]
    assert len(ids)==len(set(ids))

    issuance["summary"]=summarize_issuance(issuance)
    portfolio["operations"]=operations
    portfolio["issuanceArtifactCount"]=len(issuance["catalog"])
    portfolio["softwareImportStatus"]="DRAFT_ONLY – chờ đối chiếu API/bảng nhập của phần mềm đang sử dụng"
    portfolio["assignmentMeasurementRules"]={
        "taskStatus":["Chưa giao","Chờ đầu vào","Được giao","Đang thực hiện","Chờ kiểm","Trả sửa","Chờ phê duyệt","Nghiệm thu","Đóng"],
        "measuredBy":"Output ID, unit, actual quantity, actual time per person-stage, measured KPI and source; no double-count with Muc 05.",
        "releaseCounting":"artifactId + version + verified event, regardless of originating work module",
        "zeroPolicy":"Missing approved target, actual, baseline, effort or release proof is null/unknown, never zero",
        "noWorkloadDuplication":"Priority tasks and monthly summaries are views; W or versioned document/stage ledger is the only time-accounting source"
    }
    cat["portfolio"]=portfolio
    cat["issuance"]=issuance
    target=site/"ke-hoach-mkt-2027"
    target.mkdir(parents=True,exist_ok=True)
    (target/"data.json").write_text(json.dumps(cat,ensure_ascii=False,separators=(",",":")).replace("</","<\\/"),"utf-8")
    (target/"phan-tich-ban-hanh.json").write_text(json.dumps(issuance["summary"],ensure_ascii=False,indent=2),"utf-8")
    (target/"phan-he-phan-mem.json").write_text(json.dumps(portfolio["importContract"],ensure_ascii=False,indent=2),"utf-8")
    write_csv(target/"nhap-phan-mem-du-an-trong-diem.csv",FIELD_TASKS,priority)
    write_csv(target/"giai-doan-hang-muc-trong-diem.csv",FIELD_STAGES,portfolio["stageRegister"])
    (target/"lo-trinh-hai-giai-doan.json").write_text(json.dumps(portfolio["namedTwoPhaseInitiatives"],ensure_ascii=False,indent=2),"utf-8")
    write_csv(target/"nhap-phan-mem-cong-viec-thuong-xuyen.csv",[
        "taskId","module","workloadLedgerId","name","ownerRoleId","executorRoleId",
        "locationId","locationName","quantityRule","frequency","minutesByStage",
        "unitMinutes","sourceRefs","kind","loadSource","isNewBillableWork","status",
        "personId","evidenceId","approvedActualHours"
    ],operations)
    write_csv(target/"so-tai-lieu-va-mau-goc.csv",FIELD_ARTIFACTS,issuance["catalog"])
    write_csv(target/"su-kien-ban-hanh-co-chung-tu.csv",FIELD_EVENTS,issuance["events"])
    write_csv(target/"danh-muc-kpi.csv",[
        "id","name","formula","dataSource","ownerRoleId","checkerRoleId",
        "cadence","base2026","plan2027","actual","collectionGate"
    ],portfolio["kpis"])
    write_csv(target/"cong-viec-theo-chuc-danh-12-thang.csv",[
        "id","role","month","kind","start","due","job","product","owner",
        "executor","collaborators","checker","status","hours","quantity",
        "source","includeInStaffing","actingRole"
    ],cat["monthlyActions"])
    print("PASS Marketing 2027 bundle:",
          len(portfolio["programs"]),"programs,",
          len(projects),"projects,",
          len(priority),"priority tasks,",len(portfolio["stageRegister"]),"project stages,",
          len(operations),"operational time-ledger references,",
          len(issuance["catalog"]),"artifact codes,",
          len(issuance["events"]),"verified release events,",
          len(portfolio["kpis"]),"KPIs",flush=True)

if __name__=="__main__":
    prepare(Path(sys.argv[1] if len(sys.argv)>1 else "_site"))
