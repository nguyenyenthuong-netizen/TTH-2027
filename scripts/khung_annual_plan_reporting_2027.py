#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bổ sung kế hoạch và báo cáo năm 2027 ngay trong mục 30.4–30.5 của Khung.
Giữ nguyên 12 phần, dữ liệu gốc, định biên, phân quyền và các luồng đã có.
"""
import re
import sys
from pathlib import Path

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
    if fragment.count('id="' + new_id + '"') != 1:
        raise RuntimeError("Trùng hoặc thiếu id trong " + filename)
    if 'id="' + new_id + '"' in src:
        if src.count('id="' + new_id + '"') != 1:
            raise RuntimeError("Đã có nhiều section " + new_id)
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

for marker in ("m-30-4", "m-30-4a", "m-30-5", "m-30-5a", "m-31"):
    if src.count('id="' + marker + '"') != 1:
        raise RuntimeError("Lỗi cấu trúc mục " + marker)
if len(re.findall(r'<section class="view"[^>]*\bdata-view=', src)) != 12:
    raise RuntimeError("Không được thay đổi số lượng 12 phần của Khung")
assert "36 suất" in src and "26" in src, "Mất cơ sở dữ liệu định biên"
p.write_text(src, encoding="utf-8")
print("Đã chèn kế hoạch/báo cáo năm vào Khung, giữ nguyên 12 phần.")
