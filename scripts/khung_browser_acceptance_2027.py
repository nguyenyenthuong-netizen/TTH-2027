#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E2E trình duyệt thật: giao diện & 8 tình huống vận hành, desktop/mobile.

Không kiểm thử chỉ bằng chuỗi HTML: Chromium thực thi JS, mở trang chi tiết,
nhấn các bảng đầu ra, đo tràn lề, ảnh chụp và lỗi console.
"""
import json,os,sys,base64
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(sys.argv[1]) if len(sys.argv)>1 else Path("_site")
url=(root/"khung-marketing"/"index.html").resolve().as_uri()
out=Path("artifacts/khung-e2e")
out.mkdir(parents=True,exist_ok=True)

flows=[
 ("hang-muc",11,"Hạng mục trọng điểm – người yêu cầu, sản xuất, duyệt"),
 ("tin-trong-ngay",None,"Tin V1 – phát hành tại cơ sở"),
 ("hang-muc-toan-he-thong",None,"Hạng mục hai nhóm thương hiệu"),
 ("phat-thanh-man-hinh",None,"Phát thanh, màn hình và cơ sở hai người"),
 ("crm",None,"Bàn giao nghiệp vụ Contact Center"),
 ("danh-gia",None,"Phản ánh tiêu cực, khủng hoảng"),
 ("nguoi-benh-nuoc-ngoai",None,"Nội dung nhiều ngôn ngữ"),
 ("quang-cao-tra-phi",None,"Quảng cáo và ngân sách"),
]
issues=[]
results=[]
with sync_playwright() as p:
    try:
        browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    except Exception as e:
        raise RuntimeError("Không mở được Chrome trên runner: "+str(e))
    for form,(width,height) in (("desktop",(1440,900)),("mobile",(390,844))):
        context=browser.new_context(viewport={"width":width,"height":height},device_scale_factor=1,locale="vi-VN")
        page=context.new_page()
        page_errors=[]
        page.on("pageerror",lambda exc:page_errors.append(str(exc)))
        page.goto(url+"#vh-qt-hang-muc",wait_until="domcontentloaded",timeout=30000)
        page.wait_for_timeout(900)
        try:
            page.wait_for_selector("#vh-qt-hang-muc .ops-output-audit",timeout=8000)
        except Exception as e:
            issues.append(form+": Không dựng được VH.5/đầu ra: "+str(e))
            context.close()
            continue
        count=page.locator(".ops-output-audit").count()
        if count!=407:issues.append(form+": số bảng đầu ra hiển thị "+str(count)+"/407")
        root_box=page.locator("#ops-root")
        if root_box.count()!=1:issues.append(form+": thiếu phần luồng vận hành")
        page.locator("#vh-qt-hang-muc").scroll_into_view_if_needed()
        audited=page.locator("#vh-qt-hang-muc .ops-output-audit")
        if audited.count()!=11:issues.append(form+": hạng mục phải có 11 bảng đầu ra, thấy "+str(audited.count()))
        # Bước 6 gồm Biên tập + Thiết kế + Media = 3 đầu ra riêng.
        sixth=audited.nth(5)
        before=sixth.evaluate("(e)=>e.open")
        sixth.locator("summary").click(timeout=8000)
        after=sixth.evaluate("(e)=>e.open")
        if before==after:issues.append(form+": nhấn chuột không đổi trạng thái bảng đầu ra")
        if not after:sixth.locator("summary").click(timeout=8000)
        if not sixth.evaluate("(e)=>e.open"):issues.append(form+": không mở được bảng đầu ra sản xuất")
        row_count=sixth.locator(".ops-output-card").count()
        if row_count!=3:issues.append(form+": bước 6 cần 3 đầu ra, thấy "+str(row_count))
        vals=sixth.locator(".ops-output-card").all_text_contents()
        if not (any("biên tập" in x.lower() for x in vals)
                and any("thiết kế" in x.lower() for x in vals)
                and any("media" in x.lower() for x in vals)):
            issues.append(form+": ba đầu ra chưa đủ Biên tập/Thiết kế/Media")
        if form=="mobile":
            card_dims=sixth.locator(".ops-output-card").first.evaluate(
                "(e)=>({scroll:e.scrollWidth,client:e.clientWidth,rect:e.getBoundingClientRect().width})"
            )
            if card_dims["scroll"]>card_dims["client"]+3:
                issues.append("mobile: thẻ đầu ra vượt chiều rộng: "+str(card_dims))

        # Tình huống thực tế: xem đủ luồng và mở ra được bằng nhấn thật.
        for flow,expected,label in flows:
            section=page.locator("#vh-qt-"+flow)
            if section.count()!=1:
                issues.append(form+": thiếu luồng "+flow)
                continue
            n=section.locator(".ops-output-audit").count()
            if expected is not None and n!=expected:issues.append(form+": "+flow+" thiếu bước")
            assert n>0,form+" "+flow+" không có đối soát đầu ra"
            details=section.locator(".ops-output-audit").first
            details.scroll_into_view_if_needed(timeout=8000)
            was_open=details.evaluate("(e)=>e.open")
            details.locator("summary").click(timeout=8000)
            now_open=details.evaluate("(e)=>e.open")
            if was_open==now_open:
                issues.append(form+": nhấn không đổi trạng thái "+flow)
            if not now_open:details.locator("summary").click(timeout=8000)
            if not details.evaluate("(e)=>e.open"):
                issues.append(form+": không thao tác được bảng đầu ra "+flow)
            if details.locator(".ops-output-card").count()<1:
                issues.append(form+": không có dòng trách nhiệm trong "+flow)
            results.append({"giao_dien":form,"luong":flow,"so_buoc":n,"thao_tac":"Mở bảng đầu ra"})
        # Cân lề trên cả trang: các bảng có cuộn riêng, trang không tràn ngang.
        dims=page.evaluate("""() => ({
            vp: window.innerWidth,
            document: document.documentElement.scrollWidth,
            body: document.body.scrollWidth,
            pageErrors: document.querySelectorAll('.ops-output-audit').length
        })""")
        if dims["document"]>width+18:
            issues.append(form+": tràn ngang trang "+str(dims))
        if page_errors:
            issues.append(form+": lỗi JS: "+";".join(page_errors[:3])[:500])
        # Điều hướng đến phần CNNV, mở được chứ không rơi vào tab ẩn.
        page.goto(url+"#m-4-3",wait_until="domcontentloaded",timeout=30000)
        page.wait_for_timeout(650)
        panel=page.locator("#tth-output-contracts-2027")
        if panel.count()!=1:issues.append(form+": thiếu bảng tổng hợp 568 hợp đồng đầu ra")
        elif not panel.is_visible():
            issues.append(form+": bảng 568 đầu ra đang bị ẩn khi vào mục 4.3")
        # Kiểm tra 14 ví dụ trên trình duyệt, không chỉ kiểm tra mã HTML.
        examples=page.locator("#tth-cvt-worked-examples-2027 .cvt-case")
        if examples.count()!=14:
            issues.append(form+": thiếu ví dụ hai tuyến, thấy "+str(examples.count())+"/14")
        else:
            for pos in (0,6,13):
                card=examples.nth(pos)
                card.scroll_into_view_if_needed(timeout=8000)
                old=card.evaluate("(e)=>e.open")
                card.locator("summary").click(timeout=8000)
                new=card.evaluate("(e)=>e.open")
                if old==new:
                    issues.append(form+": ví dụ "+str(pos+1)+" không mở/thu được")
                if not new:
                    card.locator("summary").click(timeout=8000)
                link=card.locator('a[href^="#vh-qt-"]')
                if link.count()!=1:
                    issues.append(form+": ví dụ "+str(pos+1)+" thiếu liên kết quy trình")
                else:
                    target=link.get_attribute("href")[1:]
                    if page.locator("[id='"+target+"']").count()!=1:
                        issues.append(form+": liên kết ví dụ sai ID "+target)
            panel_width=page.locator("#tth-cvt-worked-examples-2027").evaluate(
                "(e)=>({client:e.clientWidth,scroll:e.scrollWidth})")
            if panel_width["scroll"]>panel_width["client"]+3:
                issues.append(form+": ví dụ tràn ngang "+str(panel_width))
        contract=page.evaluate("""() => {
            const el=document.getElementById('csdl');
            if (!el) return {problem:'missing-csdl'};
            const d=JSON.parse(el.textContent);
            const arr=d.quy_trinh.flatMap(q=>q.buoc.flatMap(b=>b.doi_soat_tung_dau_ra_2027||[]));
            const mkt=arr.filter(x=>(x.ma_chu_tri_theo_nhom||{}).can_phan_giai==='mkt-tct');
            return {total:arr.length,blocked:arr.filter(x=>x.trang_thai_nghiem_thu_2027==='CHƯA NGHIỆM THU HỒ SƠ THỰC TẾ').length,
              unresolvedTct:mkt.length,unsafeTct:mkt.filter(x=>x.chu_tri_01.indexOf('Trưởng phòng chỉ')<0).length,
              gate:!!d.kiem_toan_chong_cheo_chot_2027}
        }""")
        if (contract.get("total")!=568 or contract.get("blocked")!=568
                or contract.get("unsafeTct",0)>0 or not contract.get("gate")):
            issues.append(form+": dữ liệu 568 đầu ra chưa nhất quán "+str(contract))
        latest_dims=page.evaluate("() => document.documentElement.scrollWidth")
        if latest_dims>width+18:
            issues.append(form+": tràn trang sau khi mở 14 ví dụ: "+str(latest_dims))
        page.goto(url+"#vh-qt-hang-muc",wait_until="domcontentloaded",timeout=30000)
        page.wait_for_timeout(700)
        shot_details=page.locator("#vh-qt-hang-muc .ops-output-audit").nth(5)
        if not shot_details.evaluate("(e)=>e.open"):
            shot_details.locator("summary").click()
        assert shot_details.evaluate("(e)=>e.open")
        screenshot=out/("khung_"+form+"_dau_ra.jpg")
        page.locator("#vh-qt-hang-muc .ops-output-audit").nth(5).screenshot(
            path=str(screenshot),type="jpeg",quality=48,animations="disabled",timeout=20000
        )
        # Thu nhỏ ảnh để có thể quan sát từ nhật ký, ngoài file ảnh gốc.
        from PIL import Image
        im=Image.open(screenshot)
        im.thumbnail((950,720))
        thumb=out/("thu_nho_"+form+".jpg")
        im.convert("RGB").save(thumb,quality=42,optimize=True)
        b64=base64.b64encode(thumb.read_bytes()).decode("ascii")
        print("SHOT_START:"+form)
        for i in range(0,len(b64),3000):print("SHOT_PART:"+b64[i:i+3000])
        print("SHOT_END:"+form)
        print("E2E",form,"407 bảng,",len(flows),"luồng,",row_count,"đầu ra sản xuất, kích thước",dims)
        context.close()
    browser.close()
report={"test":"Trình duyệt Chromium thực tế","screenshot_files":[x.name for x in out.glob("*.jpg")],
        "flows":results,"problems":issues}
(out/"ket_qua_kiem_thu.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
assert not issues,"E2E FAIL: "+json.dumps(issues,ensure_ascii=False)
assert len(results)==len(flows)*2
print("PASS BROWSER E2E: 8 luồng x desktop/mobile; bảng 3 đầu ra; CNNV; không có lỗi JavaScript/tràn trang")
