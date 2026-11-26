#!/usr/bin/env python3
"""Validate and stage V8 preview without replacing the existing catalog or production item 06."""
from pathlib import Path
from zipfile import ZipFile
from hashlib import sha256
import json, re, sys, threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from urllib.parse import urlsplit, parse_qs
from playwright.sync_api import sync_playwright

archive = Path("pages-overrides/catalog/TTH-2027-V8-preview.zip")
root = Path(sys.argv[1] if len(sys.argv)>1 else "_site").resolve()
target = root/"kien-truc-thuong-hieu-v8"
if not archive.exists():
    print("V8 preview archive not uploaded; existing Pages content unchanged")
    sys.exit(0)
assert sha256(archive.read_bytes()).hexdigest() == "fc44868aa5e678709dbc6f34da835ea543ce10afb9bd10f4f0966309fa27bd72", "Unexpected V8 release checksum"
before = {p:sha256(p.read_bytes()).hexdigest() for p in (root/"index.html",root/"kien-truc-thuong-hieu/index.html")}
assert not target.exists(), "Unexpected existing preview destination"
with ZipFile(archive) as z:
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))==145, "Unexpected ZIP contents"
    manifest=json.loads(z.read("asset-manifest.json"))
    assert len(manifest)==143
    assert set(names)==set(manifest)|{"index.html","asset-manifest.json"}
    html=z.read("index.html")
    assert len(html)==3127715 and b"noindex" in html
    for name,meta in manifest.items():
        assert re.fullmatch(r"assets/[a-f0-9]{24}\.(?:webp|png|jpg|jpeg|gif|svg|mp4|webm|avif)",name), name
        data=z.read(name)
        assert len(data)==meta["bytes"] and sha256(data).hexdigest()==meta["sha256"], name
    for name in ["index.html",*manifest]:
        p=target/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(z.read(name))
assert all(sha256(p.read_bytes()).hexdigest()==v for p,v in before.items())
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f"http://127.0.0.1:{server.server_port}/kien-truc-thuong-hieu-v8/"
report=[]
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(channel="chrome",headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
        for width,height in [(1440,900),(390,844)]:
            page=browser.new_page(viewport={"width":width,"height":height})
            errors=[];bad=[]
            page.on("pageerror",lambda e:errors.append(str(e)))
            page.on("response",lambda r:bad.append((r.status,r.url)) if r.url.startswith(base) and r.status>=400 else None)
            for brand in ["group","bach","tri","chau","thao","phuc","tam","tth","elder"]:
                for lang in ["vi","en"]:
                    response=page.goto(base+f"?site={brand}&page=home&lang={lang}",wait_until="domcontentloaded",timeout=30000)
                    assert response.status==200
                    page.wait_for_function("document.readyState==='complete'",timeout=30000)
                    state=page.evaluate("({site:active,route:currentHash,lang:document.documentElement.lang,overflow:document.documentElement.scrollWidth>innerWidth+2,images:[...document.images].filter(x=>x.complete&&x.naturalWidth===0&&x.getAttribute('src')).map(x=>x.src),loaded:[...document.images].filter(x=>x.complete&&x.naturalWidth>0).length})")
                    assert state["site"]==brand and state["route"]=="#home" and state["lang"]==lang and not state["overflow"] and not state["images"] and state["loaded"]>0,state
                    report.append({"brand":brand,"lang":lang,"viewport":[width,height],"state":state})
            page.goto(base+"?site=tam&page=home&lang=en",wait_until="load")
            page.evaluate("currentHash='#about';window.navRoute()")
            page.wait_for_function("new URL(location.href).searchParams.get('page')==='about'")
            page.reload(wait_until="load")
            assert page.evaluate("active==='tam'&&currentHash==='#about'&&document.documentElement.lang==='en'")
            page.evaluate("currentHash='#services';window.navRoute()")
            page.wait_for_function("new URL(location.href).searchParams.get('page')==='services'")
            page.go_back(wait_until="commit")
            page.wait_for_function("currentHash==='#about'")
            page.go_forward(wait_until="commit")
            page.wait_for_function("currentHash==='#services'")
            assert not errors and not bad, {"errors":errors,"bad_responses":bad}
            report.append({"viewport":[width,height],"reload":True,"back":True,"forward":True})
            page.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
assert all(sha256(p.read_bytes()).hexdigest()==v for p,v in before.items())
print("V8_PREVIEW_HTTP_QA",json.dumps(report,ensure_ascii=False))
