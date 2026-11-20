#!/usr/bin/env python3
"""Repair only unambiguous dead App links to verified existing screens.
Do not substitute unrelated screens for actions needing HIS, medical data, consent or payments.
"""
import re,html,json,sys,collections
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
p=root/"healthcare-app"/"index.html";raw=p.read_text("utf8")
m=re.search(r'(<script\b[^>]*\bid=["\']pageData["\'][^>]*>)(.*?)(</script>)',raw,re.S|re.I)
if not m:raise SystemExit("Missing app catalog")
pages=json.loads(m.group(2))
if len(pages)!=102:raise SystemExit("App page count changed")
rules={
 "Web_DangNhap.html":{
  "Đặt lịch không cần tài khoản":"Web_DatLich.html",
 },
 "Web_HoSo.html":{
  "Đơn thuốc":"Web_DonThuoc.html",
  "Lịch sử khám":"Web_LichSu.html",
  "Khám ở nơi khác":"HoSo_KhamNoiKhac.html",
  "Kết quả sàng lọc":"SangLoc_CauHoi.html",
  "Ai được xem hồ sơ của bạn":"HoSo_QuyenNguoiThan.html",
 },
 "Web_Toi.html":{
  "Cài đặt liên hệ, thông báo":"LienHe_CaiDat.html",
  "Bảo mật và dữ liệu":"Toi_BaoMatDuLieu.html",
  "Mã ưu đãi":"UuDai_MaCuaToi.html",
  "Chi phí, hóa đơn":"Web_ChiPhi.html",
  "Bảng giá, BHYT":"BangGia_ChiPhi.html",
  "Trợ lý TTH":"Web_TroLy.html",
  "Chat với tư vấn viên":"HoTro_ChatTuVan.html",
  "Phản ánh của tôi":"PhanHoi_Ticket.html",
  "Đăng xuất":"Web_DangNhap.html",
 },
 "Web_ThongBao.html":{
  "Cài đặt liên hệ":"LienHe_CaiDat.html",
 },
 "Web_GoiKham.html":{
  "Hỏi tư vấn viên":"HoTro_ChatTuVan.html",
 },
 "Web_TrangChu.html":{
  "Khai báo":"TruocKham_KhaiBao.html",
  "Thư viện kiến thức":"KienThuc_DanhSach.html",
  "Chỉ đường":"CoSo_DuongDi.html",
 },
 "Web_TrangChu_HomNay.html":{
  "Chỉ đường trong viện":"CoSo_DuongDi.html",
  "Chỉ đường":"CoSo_DuongDi.html",
 },
 "Web_TrangChu_KhachMoi.html":{
  "Cơ sở gần bạn":"CoSo_DanhSach.html",
  "Tất cả dịch vụ":"TatCa_DichVu.html",
  "Khám sức khỏe định kỳ":"GoiKham_DanhSach.html",
  "Nguy cơ đột quỵ":"SangLoc_CauHoi.html",
 },
 "Web_TrangChu_SauKham.html":{
  "Đánh giá":"PhanHoi_Ticket.html",
  "Thư viện kiến thức":"KienThuc_DanhSach.html",
 },
 "Web_LichSu.html":{
  "Khám ở nơi khác":"HoSo_KhamNoiKhac.html",
  "Đánh giá":"PhanHoi_Ticket.html",
 },
 "Web_LichHen.html":{
  "Đổi lịch":"GianDoan_HuyLich.html",
  "Hủy lịch":"GianDoan_HuyLich.html",
  "Chỉ đường":"CoSo_DuongDi.html",
 },
 "Web_DatLich.html":{
  "Cấp cứu gần nhất":"HoTro_KhanCap.html",
 },
 "Web_TroLy.html":{
  "Gặp tư vấn viên":"HoTro_ChatTuVan.html",
 }
}
for data in rules.values():
 for dest in data.values():
  if dest not in pages:raise SystemExit("Missing mapped target "+dest)
link_rx=re.compile(r'(<a\b[^>]*\bhref=["\'])(#)(["\'][^>]*>)(.*?)(</a>)',re.I|re.S)
fixed=collections.Counter();unresolved=collections.Counter()
def norm(src):
 return " ".join(html.unescape(re.sub(r'<[^>]+>',' ',src)).split())
updated={}
for name,doc in pages.items():
 def replace(m):
  text=norm(m.group(4))
  target=None
  if name.startswith("Web_") and text in ("tthhealthcare.com","← Về tthhealthcare.com"):
   target="https://tthhealthcare.com/"
  elif name.startswith("Web_") and text in ("Cấp cứu","Cấp cứu gần nhất","Cổng cấp cứu ↗"):
   target="HoTro_KhanCap.html"
  else:
   for label,dest in rules.get(name,{}).items():
    if text==label or (len(label)>=10 and text.startswith(label)):
     target=dest;break
  if target:
   fixed[(name,target)]+=1
   return m.group(1)+target+m.group(3)+m.group(4)+m.group(5)
  unresolved[name]+=1
  return m.group(0)
 updated[name]=link_rx.sub(replace,doc)
encoded=json.dumps(updated,ensure_ascii=False,separators=(',',':')).replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026")
p.write_text(raw[:m.start(2)]+encoded+raw[m.end(2):],"utf8")
print("APP_LINK_ROUTING_FIX",json.dumps({"new_valid_routes":sum(fixed.values()),"screens_mapped":len(fixed),"still_placeholder":sum(unresolved.values()),"per_destination":dict(collections.Counter({k[1]:v for k,v in fixed.items()}))},ensure_ascii=False))
