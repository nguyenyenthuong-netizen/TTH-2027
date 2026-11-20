#!/usr/bin/env python3
"""Show honest, accessible feedback for unresolved App mockup anchors.
Does not claim to connect HIS/CRM, fabricate data, or reroute to unrelated screens.
Existing functional click handlers get first opportunity to handle the action.
"""
import re,json,sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else "_site")
p=root/"healthcare-app"/"index.html"
raw=p.read_text("utf-8")
m=re.search(r'(<script\b[^>]*\bid=["\x27]pageData["\x27][^>]*>)(.*?)(</script>)',raw,re.I|re.S)
if not m:raise SystemExit("App catalog missing")
pages=json.loads(m.group(2))
if len(pages)!=102:raise SystemExit("App screens changed")
script=r'''<script id="tth-app-unresolved-actions-2027">
(function(){
 "use strict";
 function notify(message){
  let box=document.getElementById("tth-app-action-notice");
  if(!box){
   box=document.createElement("div");
   box.id="tth-app-action-notice";
   box.setAttribute("role","status");box.setAttribute("aria-live","polite");
   box.style.cssText="position:fixed;z-index:2147483000;left:12px;right:12px;bottom:16px;max-width:520px;margin:auto;padding:13px 42px 13px 15px;border-radius:10px;background:#fff;color:#12376d;border:1px solid #b9c9e3;box-shadow:0 8px 26px #092b5a35;font:500 15px/1.5 Arial,sans-serif";
   const close=document.createElement("button");close.type="button";close.textContent="×";
   close.setAttribute("aria-label","Đóng thông báo");
   close.style.cssText="position:absolute;right:10px;top:7px;border:0;background:transparent;color:#12376d;font-size:25px;cursor:pointer";
   close.addEventListener("click",()=>box.hidden=true);
   box.append(close);document.body.append(box);
  }
  let msg=box.querySelector("[data-message]");
  if(!msg){msg=document.createElement("span");msg.dataset.message="1";box.prepend(msg);}
  msg.textContent=message;box.hidden=false;
 }
 document.addEventListener("click",function(ev){
  const a=ev.target.closest?.('a[href="#"]');
  if(!a||ev.defaultPrevented)return;
  if(a.hasAttribute("onclick")||a.hasAttribute("data-route")||a.hasAttribute("data-href"))return;
  // Do not invent a destination or trigger a real backend action.
  ev.preventDefault();
  const label=(a.innerText||a.textContent||"").trim();
  const legal=/điều khoản|quyền riêng tư|chính sách|pháp lý/i.test(label);
  const sensitive=/tải|pdf|in đơn|bệnh án|hóa đơn|vneid|xóa tài khoản|thanh toán|chia sẻ|lịch hẹn|đặt lịch|đăng ký|nhắc tôi/i.test(label);
  notify(legal
    ?"Tài liệu pháp lý này chưa được tích hợp trong bản mô phỏng. Không sử dụng nội dung thay thế chưa được phê duyệt."
    :sensitive
    ?"Chức năng này chỉ đang được minh họa; chưa kết nối dữ liệu hoặc dịch vụ thực tế. Không có giao dịch, lịch hẹn hay tệp nào được tạo."
    :"Mục này chưa có màn hình đích hoặc thao tác được xác minh trong bản mô phỏng. Không có thay đổi dữ liệu.");
 },false);
})();
</script>'''
changed=0
for name,doc in list(pages.items()):
 if 'id="tth-app-unresolved-actions-2027"' in doc:continue
 if "</body>" not in doc:raise SystemExit("Missing body "+name)
 pages[name]=doc.replace("</body>",script+"</body>",1)
 changed+=1
encoded=json.dumps(pages,ensure_ascii=False,separators=(",",":")).replace("<",r"\u003c").replace(">",r"\u003e").replace("&",r"\u0026")
p.write_text(raw[:m.start(2)]+encoded+raw[m.end(2):],"utf-8")
unresolved=sum(len(re.findall(r'<a\b[^>]*\bhref=["\x27]#["\x27]',doc,re.I)) for doc in pages.values())
print("APP_UNRESOLVED_FEEDBACK",json.dumps({"screens":len(pages),"injected":changed,"unresolved_links_remain":unresolved,"claim":"fallback notice only, not functioning link"}))
