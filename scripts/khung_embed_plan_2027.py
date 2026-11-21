#!/usr/bin/env python3
"""Embed all 2027 Marketing action-plan content directly inside Khung Muc 05.

The source-of-truth for the action register remains in pages-overrides/catalog.
Deployment creates a self-contained srcdoc iframe: no external fetch, separate
page navigation, or network dependency is needed to read the integrated plan.
The iframe isolates plan CSS/JS from the existing Khung UI and calculation code.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ANCHOR = '<section class="view" data-view="staffing" id="v-staffing">'
OLD_LINK = re.compile(r'<p id="tth-plan-2027-link"[^>]*>.*?</p>', re.S)


def integrate(site: Path):
    parent = Path(__file__).resolve().parents[1]
    source = parent / "pages-overrides/catalog"
    d = json.loads((site / "ke-hoach-mkt-2027/data.json").read_text("utf-8"))
    assert len(d["portfolio"]["programs"])==6 and len(d["portfolio"]["projects"])==24
    assert len(d["portfolio"]["tasks"])==288 and len(d["issuance"]["catalog"])==325
    assert len(d["roles"]) == 26, "Required roles absent"
    assert len(d["yearEndCommitments"]["outcomes"])==7, "Missing 7 executive year-end outcomes"
    assert len(d["yearEndCommitments"]["monthlyGates"])==84, "Missing 84 monthly outcome checkpoints"
    assert d["ctdaAddendum"]["counts"] == {"programs":13,"launchFacilities":7,"outputs":132,"steps":660,"mktStepsMissingHour":528,"unclassifiedHourSteps":132}, "CTDA addendum incomplete"
    assert len({o["code"] for o in d["ctdaAddendum"]["operations"]}) == 660, "Duplicate CTDA operation"
    assert len(d["monthlyActions"]) >= 624, "Missing monthly assignments"
    assert {x["month"] for x in d["monthlyActions"]} == set(range(1, 13))
    assert len(d["actions"]) >= 146 and len(d["themes"]) >= 157
    assert len(d["docs"]) == 74 and len(d["overlapAudits"]) >= 119
    assert sum(map(len, d["mtcv"].values())) >= 496
    ids = [x["id"] for x in d["monthlyActions"]]
    assert len(ids) == len(set(ids)), "Duplicate monthly assignment IDs"
    for r in d["roles"]:
        for m in range(1, 13):
            assert any(x["role"] == r["id"] and x["month"] == m for x in d["monthlyActions"]), (r["id"], m)

    plan_html = (source / "ke-hoach-mkt-2027.html").read_text("utf-8")
    assert plan_html.count('fetch("./data.json",{cache:"no-store"})') == 1
    data = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
    # Keep the JSON script content safe even if a future brief contains HTML.
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    inline_data = '<script type="application/json" id="tth-plan-2027-data">' + data + '</script>'
    bootstrap = 'Promise.resolve({ok:true,json:function(){return Promise.resolve(JSON.parse(document.getElementById("tth-plan-2027-data").textContent))}})'
    plan_html = plan_html.replace('fetch("./data.json",{cache:"no-store"})', bootstrap, 1)
    plan_html = plan_html.replace("<script>", inline_data + "<script>", 1)
    plan_html = plan_html.replace(
        '<a class="btn" href="../khung-marketing/#dinh-bien-2027">Về Mục 05 – Định biên</a>',
        '<span class="btn" aria-label="Đã tích hợp trong Khung Mục 05">Đang xem trong Mục 05</span>',
        1,
    )
    assert 'fetch("./data.json"' not in plan_html
    assert '<script type="application/json" id="tth-plan-2027-data">' in plan_html

    srcdoc = html.escape(plan_html, quote=True)
    embed = (
        '\n<div id="tth-mkt-2027-in-khung" style="margin:16px 18px 22px;'
        'border:1px solid #c9d7eb;border-radius:10px;background:#fff;'
        'box-shadow:0 1px 8px rgba(8,55,161,.07);overflow:hidden">\n'
        '<details open style="margin:0">\n'
        '<summary style="background:#0837A1;color:#fff;padding:16px 20px;'
        'font-weight:750;font-size:17px;cursor:pointer;line-height:1.5">'
        'KẾT QUẢ 2027: 7 ĐÍCH ĐẾN · 6 CHƯƠNG TRÌNH · 24 DỰ ÁN · 12 THÁNG · 26 CHỨC DANH'
        '<span style="display:block;font-size:12px;font-weight:450;color:#e6efff">'
        'Nằm trong Mục 05 – Định biên; nhấn để thu gọn/mở rộng nội dung'
        '</span></summary>\n'
        '<div style="padding:10px;background:#f4f7fd">'
        '<div style="padding:8px 10px 12px;color:#244466;font-size:13px;line-height:1.6">'
        '<strong>Đích đến năm 2027:</strong> 7 kết quả cấp hệ thống, 25 chỉ số cần đối chiếu bộ KPI gốc; 84 cổng tháng chưa có số giao. 132 đầu ra phụ lục và 660 bước cần đối chiếu sổ giờ; '
        '325 mã mẫu/tài liệu/quy trình cần đối chiếu; 23 KPI, 496 đầu ra MTCV. '
        'Người thực nhận, quỹ giờ và quyền phê duyệt phải xác nhận trước khi giao chính thức.'
        '</div>'
        '<iframe id="tth-mkt-2027-workframe" title="Toàn bộ kế hoạch hành động Marketing 2027 trong Khung" '
        'sandbox="allow-scripts allow-downloads" referrerpolicy="no-referrer" loading="eager" '
        'style="display:block;width:100%;height:950px;min-height:650px;'
        'border:1px solid #dce4ee;border-radius:8px;background:#fff" '
        'srcdoc="' + srcdoc + '"></iframe>'
        '</div></details></div>\n'
    )

    p = site / "khung-marketing/index.html"
    index = p.read_text("utf-8")
    index = OLD_LINK.sub("", index)
    assert ANCHOR in index, "Cannot find Khung Muc 05"
    assert 'id="tth-mkt-2027-in-khung"' not in index, "Duplicate embedded plan"
    index = index.replace(ANCHOR, ANCHOR + embed, 1)
    assert index.count('id="tth-mkt-2027-in-khung"') == 1
    assert index.count('id="tth-mkt-2027-workframe"') == 1
    assert index.count('srcdoc="') >= 1
    p.write_text(index, "utf-8")
    print(
        "PASS: embedded inside Khung Muc 05, no outside fetch:",
        len(d["roles"]), "roles,", len(d["monthlyActions"]), "monthly rows,",
        len(d["actions"]), "year milestones,", len(d["themes"]), "templates,",
        len(d["overlapAudits"]), "overlap audits;",
        len(plan_html.encode("utf-8")), "inlined bytes",
    )


if __name__ == "__main__":
    integrate(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
