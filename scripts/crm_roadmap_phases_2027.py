#!/usr/bin/env python3
"""TTH CRM roadmap: stage 1 CRM + Call Center + HIS; stage 2 multichannel only.
Patch only CRM presentation. Reject ambiguous/missing source rather than silently publish.
"""
import sys,re,html
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
p=root/"crm-da-kenh"/"index.html"
src=p.read_text("utf-8")
def locate(s,t):
 m=re.search(re.escape(t),s,re.I)
 return -1 if m is None else m.start()
for marker in ["GIAI ĐOẠN 1","CRM lõi","Cuộc gọi","GIAI ĐOẠN 2","Đa kênh","+ HIS","1900/hotline","liên kết mã bệnh nhân"]:
 k=locate(src,marker)
 print("CRM_ROADMAP_SOURCE",marker,"found",k>=0,"at",k,repr(src[max(0,k-160):k+380]) if k>=0 else "")
p1=locate(src,"GIAI ĐOẠN 1")
p2=locate(src,"GIAI ĐOẠN 2")
p3=locate(src,"GIAI ĐOẠN 3")
if not (0<=p1<p2<p3):
 raise SystemExit("CRM_ROADMAP: Cannot find ordered stage labels, source not changed.")
parts=[src[:p1],src[p1:p2],src[p2:p3],src[p3:]]
phase1,phase2=parts[1],parts[2]
if "CRM lõi" not in phase1 or "Cuộc gọi" not in phase1:
 raise SystemExit("CRM_ROADMAP: Stage 1 labels absent. Source unchanged.")
if "Đa kênh" not in phase2 or "HIS" not in phase2:
 raise SystemExit("CRM_ROADMAP: Stage 2 labels absent. Source unchanged.")
phase1=phase1.replace("CRM lõi","CRM",1)
phase1=phase1.replace("Cuộc gọi","Call Center + HIS",1)
# Keep realistic scope: a planned integration, not an assertion that live HIS is connected.
before1="Hồ sơ, nhu cầu, ticket, người phụ trách; 1900/hotline được kết nối phù hợp."
after1="CRM quản lý thông tin liên hệ, nhu cầu và ticket; Call Center tiếp nhận, lưu vết cuộc gọi 1900; HIS xác nhận lịch khám và nghiệp vụ theo phân quyền. Không chuyển toàn bộ bệnh án vào CRM."
if before1 in phase1: phase1=phase1.replace(before1,after1,1)
else:print("CRM_ROADMAP_WARN stage1_description_not_exact")
# Preserve line breaks/title styling while eliminating misleading second-stage HIS.
before2="Zalo, Fanpage, Email, Form, App/Website; liên kết mã bệnh nhân và lịch được HIS xác nhận."
after2="Kết nối Zalo, Fanpage, Email, Form, Website và App vào CRM; hợp nhất lịch sử tương tác, nguồn khách và tuyến xử lý trên nền tảng Giai đoạn 1."
if before2 in phase2:phase2=phase2.replace(before2,after2,1)
else:print("CRM_ROADMAP_WARN stage2_description_not_exact")
# The original stage-2 title is written with a line break then "+ HIS".
title_pos=phase2.index("Đa kênh")
title_area=phase2[title_pos:title_pos+300]
# Remove only HIS suffix immediately after the stage-2 title, not legitimate
# elsewhere in its explanatory text.
suffix=re.search(r'(?:(?:<br\s*/?>)|(?:\\n)|\s)*\+\s*HIS\b',title_area,re.I)
if not suffix:
 raise SystemExit("CRM_ROADMAP: Cannot locate + HIS in stage 2 title. Source unchanged.")
phase2=phase2[:title_pos+suffix.start()]+phase2[title_pos+suffix.end():]
out="".join([parts[0],phase1,phase2,parts[3]])
old_subtitle="Đi từ nền tảng dữ liệu đến liên thông HIS và tự động hóa; không đầu tư dàn trải."
new_subtitle="Giai đoạn 1 xây CRM + Call Center + HIS; Giai đoạn 2 mở rộng đa kênh; Giai đoạn 3 đo lường và AI theo nghiệm thu."
if old_subtitle in out:
 out=out.replace(old_subtitle,new_subtitle,1)
else:
 print("CRM_ROADMAP_WARN subtitle_not_exact")
if out==src:raise SystemExit("CRM_ROADMAP: Nothing changed.")
if "Call Center + HIS" not in phase1:raise SystemExit("CRM_ROADMAP: Stage1 update absent")
if re.search(r'Đa kênh.{0,120}\+\s*HIS',phase2,re.I|re.S):raise SystemExit("CRM_ROADMAP: Stage2 still includes HIS")
p.write_text(out,"utf-8")
print("CRM_ROADMAP_OK stage1=CRM + Call Center + HIS stage2=Da kenh stage3=unchanged bytes",len(out))
