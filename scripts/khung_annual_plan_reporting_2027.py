#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bổ sung kế hoạch và báo cáo năm 2027 ngay trong mục 30.4–30.5 của Khung.
Giữ nguyên 12 phần, dữ liệu gốc, định biên, phân quyền và các luồng đã có.
"""
import re
import json
import html
import sys
from pathlib import Path


def build_outcome_fragment():
    """Kết quả cuối năm xuất phát từ cùng sổ dữ liệu nhúng vào Mục 05."""
    data=json.loads((Path(__file__).resolve().parent.parent/"pages-overrides/catalog/marketing-2027-outcome-contract.json").read_text("utf-8"))
    assert len(data["outcomes"])==7 and len(data["monthlyGates"])==84
    h=lambda x:html.escape(str(x),quote=True)
    cards=[]
    rows=[]
    for c in data["outcomes"]:
        stages="".join("<li><strong>Q"+str(i+1)+":</strong> "+h(v)+"</li>" for i,v in enumerate(c["gates"]))
        cards.append(
          '<article class="tth-outcome-card"><b class="tth-outcome-code">'+h(c["code"])+'</b>'
          '<h5>'+h(c["title"])+'</h5>'
          '<p><b>Kết quả nhận được:</b> '+h(c["result"])+'</p>'
          '<p><b>Một chủ kết quả cấp hệ thống:</b> '+h(c["ownerRole"])+'</p>'
          '<p><b>Chủ nghiệp vụ thực thi:</b> '+h(c["executionOwner"])+'</p>'
          '<p><b>Chứng từ nghiệm thu:</b> '+h(c["evidence"])+'</p>'
          '<p><b>Nguồn lực/chi phí:</b> '+h(c["costBasis"])+'</p>'
          '<p><b>Tham chiếu dự án:</b> '+h(", ".join(c["projects"]))+' (mã phụ lục, chưa tự cộng giờ)</p>'
          '<details><summary>Điều kiện và lộ trình 4 quý</summary><ol>'+stages+'</ol></details>'
          '</article>'
        )
        for k in c["kpis"]:
            rows.append('<tr><td><strong>'+h(k["id"])+'</strong><small>'+h(c["code"])+'</small></td>'
                '<td>'+h(k["name"])+'</td><td>'+h(k["formula"])+'</td>'
                '<td>'+h(k["source"])+'<small>Kiểm: '+h(k["checker"])+'</small></td>'
                '<td>Chưa xác nhận</td><td>Chờ phê duyệt</td><td>Chờ xác minh</td></tr>')
    return '''<div class="tth-outcome-contract" id="tth-year-end-commitment-2027">
<style id="tth-year-end-commitment-style-2027">
.tth-outcome-contract{margin:18px 0 26px;padding:18px 22px;background:#fff;border:1px solid #bfd0e9;border-radius:12px;font-size:16px;line-height:1.58;color:#18304c}
.tth-outcome-contract h4{font-size:23px;line-height:1.35;margin:4px 0 13px;color:#0837A1}
.tth-outcome-contract h5{font-size:18px;line-height:1.4;margin:6px 0 10px;color:#0c3474}
.tth-outcome-contract p{max-width:none;font-size:16px;line-height:1.6;margin:7px 0}
.tth-outcome-contract .tth-outcome-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:18px 0}
.tth-outcome-card{border:1px solid #d3dff0;padding:16px 18px;background:#fbfcff;border-radius:10px;min-width:0}
.tth-outcome-code{display:inline-block;color:#0837A1;font-weight:750;font-size:15px}
.tth-outcome-card details{margin-top:12px}
.tth-outcome-card summary{font-size:16px;cursor:pointer;color:#0837A1;font-weight:750}
.tth-outcome-card li{font-size:15px;line-height:1.6;margin-bottom:5px}
.tth-outcome-contract .tth-outcome-scroll{max-width:100%;overflow-x:auto;overflow-y:auto;max-height:690px;border:1px solid #dce4ee;border-radius:9px}
.tth-outcome-contract table{min-width:1340px;width:100%;border-collapse:collapse}
.tth-outcome-contract th,.tth-outcome-contract td{font-size:15.5px;line-height:1.55;padding:12px 13px;text-align:left;vertical-align:top;border-bottom:1px solid #e4ebf4;white-space:normal}
.tth-outcome-contract th{background:#edf3fd;position:sticky;top:0;font-weight:750}
.tth-outcome-contract td small{display:block;font-size:14px;line-height:1.5;margin-top:5px}
.tth-outcome-contract .tth-outcome-guard{border-left:4px solid #ED3237;padding:12px 14px;background:#f6f8fc;margin:15px 0}
@media(max-width:940px){.tth-outcome-contract .tth-outcome-grid{grid-template-columns:1fr}.tth-outcome-contract{padding:13px}}
</style>
<h4>ĐÍCH ĐẾN 31/12/2027 – 07 KẾT QUẢ TTH CẦN NHẬN ĐƯỢC</h4>
<p><strong>Đây là khung cam kết kết quả để trình, chưa phải chỉ tiêu đã được giao.</strong> Mỗi mục tiêu có chủ kết quả, sản phẩm/chứng cứ, chỉ số đo lường, các cửa kiểm soát quý và nguồn chi phí. Kế hoạch hành động, định biên và ngân sách phải chứng minh có thể tạo ra các kết quả này, không lập kế hoạch từ định biên ngược lên.</p>
<div class="tth-outcome-guard"><b>Điều kiện chặn cam kết:</b> các chỉ số dưới đây chưa có đủ số nền 2026, chỉ tiêu 2027 và xác nhận nguồn. Không tự suy diễn bằng 0 hoặc tự chia chỉ tiêu năm cho 12 tháng. Chưa đối chiếu chính thức 06 mục tiêu chiến lược, 09 chỉ số BTGĐ và bộ 23 KPI hiện hữu với các chỉ số kiểm chứng này.</div>
<div class="tth-outcome-grid">'''+ "".join(cards)+'''</div>
<details><summary style="font-size:19px;font-weight:750;color:#0837A1;cursor:pointer;padding:10px 0">Mở 25 chỉ số kiểm chứng – công thức, nguồn, số nền và chỉ tiêu</summary>
<div class="tth-outcome-scroll"><table><thead><tr><th>Mã</th><th>Chỉ số</th><th>Công thức</th><th>Nguồn và người kiểm</th><th>Nền 2026</th><th>Đích 2027</th><th>Trạng thái</th></tr></thead><tbody>'''+ "".join(rows)+'''</tbody></table></div></details>
<p><strong>Kiểm soát theo tháng:</strong> 84 dòng kiểm soát (7 kết quả × 12 tháng) nằm trong kế hoạch Mục 05; các mốc quý và tháng là lịch kiểm soát, chưa phải cam kết chỉ tiêu số lượng.</p>
<p><strong>Chuỗi nghiệm thu:</strong> Đích năm → chỉ tiêu quý và tháng có nguồn → chương trình/dự án → mã sản phẩm gốc → người/công đoạn/giờ công → nguồn ngân sách → thực tế đối soát → kết quả nghiệm thu. Giữ dự phòng phát sinh 25% trong phép tính năng lực theo người/tháng.</p>
</div>'''


root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site")
p = root / "khung-marketing" / "index.html"
src = p.read_text(encoding="utf-8")
base = Path(__file__).resolve().parent.parent / "pages-overrides"
items = [
    ("m-30-4a", "annual-marketing-2027-plan.html", "m-30-5"),
    ("m-30-5a", "annual-marketing-2027-report.html", "m-31"),
]
for new_id, filename, next_id in items:
    fragment = (base / filename).read_text(encoding="utf-8").strip()
    if new_id=="m-30-4a":
        marker='<p><strong>Đầu ra bắt buộc:</strong>'
        if fragment.count(marker)!=1:
            raise RuntimeError("Thiếu điểm chèn cam kết kết quả năm")
        fragment=fragment.replace(marker,build_outcome_fragment()+ "\n" +marker,1)

    extra_file = {
        "m-30-4a": "annual-marketing-2027-coverage.html",
        "m-30-5a": "annual-marketing-2027-performance.html",
    }[new_id]
    extra = (base / extra_file).read_text(encoding="utf-8").strip()
    extra_id = {"m-30-4a": "m-30-4a-matrix",
                "m-30-5a": "m-30-5a-scorecard"}[new_id]
    if extra.count('id="' + extra_id + '"') != 1:
        raise RuntimeError("Lỗi mã khối đo lường " + extra_file)
    if fragment.count("</section>") != 1 or not fragment.endswith("</section>"):
        raise RuntimeError("Biểu mẫu năm có cấu trúc section ngoài dự kiến: " + filename)
    fragment = fragment[:-len("</section>")] + extra + "\n</section>"
    if fragment.count('id="' + new_id + '"') != 1:
        raise RuntimeError("Trùng hoặc thiếu id trong " + filename)
    if 'id="' + new_id + '"' in src:
        if src.count('id="' + new_id + '"') != 1:
            raise RuntimeError("Đã có nhiều section " + new_id)
        if 'id="' + extra_id + '"' not in src:
            raise RuntimeError("Cấu trúc kế hoạch năm cũ không có ma trận hiệu suất: " + new_id)
        continue
    pattern = r'(<section\s+class="doc-sec(?:\s+sub)?"[^>]*\bid="' + re.escape(next_id) + r'")'
    if len(re.findall(pattern, src)) != 1:
        raise RuntimeError("Không tìm thấy đúng một điểm chèn trước " + next_id)
    src = re.sub(pattern, lambda match: fragment + "\n" + match.group(1), src, count=1)
    print("Bổ sung", new_id, "trước", next_id)

# Tạo liên kết từ tiêu đề hai mục gốc mà không sửa quy tắc báo cáo hiện hành.
for origin_id, target_id, label in [
    ("m-30-4", "m-30-4a", "Kế hoạch năm đầy đủ"),
    ("m-30-5", "m-30-5a", "Báo cáo tổng kết năm đầy đủ"),
]:
    rx = (r'(<section class="doc-sec sub"[^>]*\bid="' + origin_id +
          r'"><h3 class="sec-h">[\s\S]*?</h3>)')
    marker = '<p><strong>Biểu mẫu bổ sung:</strong> <a href="#' + target_id + '">' + label + '</a>.</p>'
    if marker not in src:
        src, count = re.subn(rx, lambda m: m.group(1) + marker, src, count=1)
        if count != 1:
            raise RuntimeError("Không liên kết được từ " + origin_id)

for required in ('id="tth-year-end-commitment-2027"', 'id="m-30-4a-matrix"', 'id="m-30-5a-scorecard"',
                 "Phát sinh ngoài kế hoạch", "Tổ chuyên môn TCT"):
    if required not in src:
        raise RuntimeError("Thiếu phạm vi hoặc hiệu suất bắt buộc: " + required)
for marker in ("m-30-4", "m-30-4a", "m-30-5", "m-30-5a", "m-31"):
    if src.count('id="' + marker + '"') != 1:
        raise RuntimeError("Lỗi cấu trúc mục " + marker)
if len(re.findall(r'<section class="view"[^>]*\bdata-view=', src)) != 12:
    raise RuntimeError("Không được thay đổi số lượng 12 phần của Khung")
assert "36 suất" in src and "26" in src, "Mất cơ sở dữ liệu định biên"
p.write_text(src, encoding="utf-8")
print("Đã chèn kế hoạch/báo cáo năm vào Khung, giữ nguyên 12 phần.")
