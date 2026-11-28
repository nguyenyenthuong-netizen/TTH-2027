
const f={src:location.href},status=document.createElement('pre');let report;const run=document.createElement('button');run.id='run';run.textContent='Run complete route audit';document.body.prepend(run);
const tick=()=>new Promise(r=>setTimeout(r,80));
document.getElementById('run').onclick=async()=>{
 report={at:new Date().toISOString(),url:f.src,pages:[],links:[],errors:[]};window.report=report;
 const w=window,d=document;
 for(const site of ['group','tri','chau','thao','phuc','tth','tam','bach','elder']){
  w.render(site);await tick();const routes=[...d.querySelectorAll('template[id^="tpl-"]')].map(x=>x.id.slice(4));
  for(const lang of ['vi','en']){
   w.clinicalLang(lang);
   for(const route of routes){
    try{tthRestoringURL=true;currentHash='#'+route;w.navRoute();tthRestoringURL=false;await tick();
    const actual=currentHash.slice(1);
    const links=[...d.querySelectorAll('a,button,form,input,select,textarea,[role=button]')].filter(e=>e.getClientRects().length);
    const row={site,lang,route,actual,heading:d.querySelector('#app h1,#app h2')?.textContent,actions:links.length};report.pages.push(row);document.documentElement.dataset.qaProgress=site+'/'+lang+'/'+route+' '+report.pages.length;
    if(actual!==route)report.errors.push({type:'route-fallback',...row});
    for(const a of links){const href=a.getAttribute('href'),onclick=a.getAttribute('onclick');let to=null;
     if(href?.startsWith('#'))to=href.slice(1);else if(href){try{const u=new URL(href,w.location.href);if(u.origin===w.location.origin)to=u.searchParams.get('page')}catch{}}
     const resolved=window.TTHNavigation?.resolve(a)||null;
     const link={site,lang,from:route,tag:a.tagName,id:a.id||null,component:a.closest('header')?'header':a.closest('footer')?'footer':a.closest('#app')?'content':a.closest('dialog')?'dialog':'fixed-controls',contract:resolved,label:(a.textContent||a.getAttribute('aria-label')||'').trim().replace(/\s+/g,' ').slice(0,160),href,onclick,to};
     if(to&&to!=='home'&&!d.getElementById('tpl-'+to)&&!d.getElementById(to))report.errors.push({type:'missing-target',...link});
     if(href==='#'||href==='javascript:void(0)')report.errors.push({type:'empty-link',...link});
     report.links.push(link);
    }
    status.textContent=`${site}/${lang}/${route}\n${report.pages.length} pages, ${report.links.length} actions, ${report.errors.length} structural errors`;
    }catch(e){report.errors.push({site,lang,route,type:'exception',error:String(e)});}
   }
  }
 }
 status.textContent='DONE '+JSON.stringify({pages:report.pages.length,links:report.links.length,errors:report.errors.length});
 document.body.dataset.done='true';document.body.prepend(status);const out=document.createElement('script');out.id='qa-results';out.type='application/json';out.textContent=JSON.stringify(report);document.body.append(out);
};
