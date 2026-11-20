#!/usr/bin/env python3
"""Exercise each of the 102 App catalog routes in a real browser.
Does not mistake form-state buttons or backend actions for navigation links.
"""
import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else "https://nguyenyenthuong-netizen.github.io/TTH-2027/healthcare-app/?demo=1"
output=Path("artifacts/app-102-qa.json")
output.parent.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch(channel='chrome',headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
 page=browser.new_page(viewport={"width":390,"height":844},locale="vi-VN")
 page.set_default_timeout(180000)
 errors=[]
 page.on("pageerror",lambda exc:errors.append(str(exc)[:160]))
 page.goto(url,wait_until="domcontentloaded",timeout=60000)
 page.locator("#screen").wait_for()
 report=page.evaluate(r'''async () => {
   const catalog=document.getElementById('catalog'),find=document.getElementById('find');
   const list=document.getElementById('pages'),frame=document.getElementById('screen');
   const pages=JSON.parse(document.getElementById('pageData').textContent);
   const results=[];
   for(const name of Object.keys(pages)){
     try {
       if(document.getElementById('drawer').hidden)catalog.click();
       find.value=name.replace(/\.html$/,'');find.dispatchEvent(new Event('input',{bubbles:true}));
       const label=name.replace(/\.html$/,'').replaceAll('_',' · ');
       const btn=[...list.querySelectorAll('button')].find(x=>x.textContent.trim()===label);
       if(!btn){results.push({name,error:'missing catalog button'});continue;}
       const loaded=await new Promise(resolve=>{
         let finished=false;
         const complete=state=>{if(finished)return;finished=true;clearTimeout(t);resolve(state);};
         const t=setTimeout(()=>complete('timeout'),2300);
         frame.addEventListener('load',()=>complete('load'),{once:true});
         btn.click();
       });
       const actual=decodeURIComponent(location.hash.slice(1));
       let contentLength=0;
       try{contentLength=frame.contentDocument?.body?.innerText?.trim().length||0;}catch(e){}
       results.push({name,actual,loaded,contentLength,error:actual!==name?'wrong destination':contentLength<25?'empty screen':''});
     }catch(e){results.push({name,error:String(e).slice(0,160)});}
   }
   const refs={internal:0,broken:0,placeholder:0,external:0};
   const missing={};
   for(const [name,doc] of Object.entries(pages)){
     const rx=/<a\b[^>]*\bhref=["']([^"']+)["']/ig;let m;
     while((m=rx.exec(doc))){
       const href=m[1].trim(),target=href.split(/[?#]/)[0].split('/').pop();
       if(href==='#'){refs.placeholder++;continue;}
       if(!target.endsWith('.html')){refs.external++;continue;}
       if(pages[target])refs.internal++;
       else{refs.broken++;missing[target]=(missing[target]||0)+1;}
     }
   }
   return {screens:Object.keys(pages).length,results,refs,missing};
 }''')
 failures=[x for x in report["results"] if x.get("error")]
 report["browserErrors"]=errors[:25]
 report["failures"]=failures
 output.write_text(json.dumps(report,ensure_ascii=False,indent=2),"utf-8")
 print("APP_102_ROUTE_QA",json.dumps({"screens":report["screens"],"passed":len(report["results"])-len(failures),"failed":len(failures),"broken_document_links":report["refs"]["broken"],"placeholders":report["refs"]["placeholder"],"browserErrors":len(errors)},ensure_ascii=False))
 for failure in failures[:30]:print("APP_ROUTE_FAILURE",json.dumps(failure,ensure_ascii=False))
 browser.close()
if failures:raise SystemExit(2)
