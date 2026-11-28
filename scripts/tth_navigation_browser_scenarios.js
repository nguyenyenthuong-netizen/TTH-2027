/* Local acceptance runner; append to a compiled page only, never to production. */
(function(){
const run=document.createElement('button');run.id='run-scenarios';run.textContent='Run navigation scenarios';document.body.prepend(run);
const wait=()=>new Promise(r=>setTimeout(r,200));
run.onclick=async()=>{
 const report={at:new Date().toISOString(),cases:[]};
 const check=(name,expected,actual)=>report.cases.push({name,expected,actual,result:JSON.stringify(expected)===JSON.stringify(actual)?'PASS':'FAIL'});
 const reset=async(site,route,lang='vi')=>{tthRestoreState({site,route:'#'+route,lang});await wait();};
 const click=async(selector)=>{const e=document.querySelector(selector);if(!e)throw Error('Missing '+selector);e.click();await wait();};
 try{
  await reset('group','home');await click('header .tth-menu-primary[data-nav-raw="#about"]');check('Click parent menu','about',currentHash.slice(1));
  for(const route of ['topic-0','topic-1','topic-2','topic-3','partner-projects']){
   await reset('group',route);const b=[...document.querySelectorAll('#app a,#app button')].find(e=>/^Kết nối hợp tác/.test(e.textContent.trim()));
   if(b){b.click();await wait();const q=new URL(location.href).searchParams;check('Partnership '+route,['contact','partner',route],[q.get('page'),q.get('nav_intent'),q.get('nav_from')]);}
  }
  await reset('group','media');await click('#app a[data-nav-raw="#contact"],#app a[href="#contact"]');check('Media intent','press',new URL(location.href).searchParams.get('nav_intent'));
  clinicalLang('en');await wait();check('Language keeps contact context',['contact','en','media'],['page','lang','nav_from'].map(k=>new URL(location.href).searchParams.get(k)));
  tthRestoreURL();await wait();check('Restore media select',1,document.querySelector('#app .corp-form select').selectedIndex);
  for(const site of ['tri','chau','thao','phuc','tam','tth','bach'])for(const lang of ['vi','en']){
   for(const type of ['doctor','service','package','facility'])for(let index=0;index<NORMALIZED[site][type==='facility'?'facilities':type==='package'?'packages':type+'s'].length;index++){
    const route='med-'+type+'-'+index;await reset(site,route,lang);
    const b=[...document.querySelectorAll('#app a,#app button')].find(e=>window.TTHNavigation.resolve(e)?.action==='booking');
    if(!b){check(site+'/'+lang+'/'+type+'/'+index+' CTA exists',true,false);continue;}
    b.click();await wait();const q=new URL(location.href).searchParams;
    check(site+'/'+lang+'/'+type+'/'+index+' route',[site,'med-book',route,lang],['site','page','nav_object','lang'].map(k=>q.get(k)));
    const f=document.querySelector('#demo-book-form form');const vals=()=>({facility:f?.elements.facility?.value,service:f?.elements.service?.value,doctor:f?.elements.doctor?.value});
    const before=vals();tthRestoreURL();await wait();const f2=document.querySelector('#demo-book-form form');const after={facility:f2?.elements.facility?.value,service:f2?.elements.service?.value,doctor:f2?.elements.doctor?.value};check(site+'/'+lang+'/'+type+'/'+index+' restore preference',before,after);
    if(type==='doctor')check(site+'/'+lang+' correct doctor',String(index+1),f2?.elements.doctor?.value);
    if(type==='facility')check(site+'/'+lang+' correct facility',String(index),f2?.elements.facility?.value);
    if(type==='package'&&before.service!=='')check(site+'/'+lang+' correct package',String(NORMALIZED[site].services.length+index),before.service);
   }
  }
  for(const site of ['tri','chau','thao','phuc','tam','tth','bach']){await reset(site,'clinical-0');const b=[...document.querySelectorAll('#app a,#app button')].find(e=>window.TTHNavigation.resolve(e)?.action==='booking');if(b){b.click();await wait();check(site+' specialty context',String(NORMALIZED[site].services[0].spec[0]),new URL(location.href).searchParams.get('nav_specialty'));}}
  await reset('group','home');check('Hotline actual number','tel:19002675',window.TTHNavigation.resolve(document.querySelector('#tth-contact-dock a')).external);
  await reset('architecture','home');
  const views=[...document.querySelectorAll('.view[id]')].map(e=>e.id).filter(id=>id!=='home');
  for(const id of views){const a=document.querySelector('a[href="#'+id+'"]');if(a){a.click();await wait();check('Architecture '+id,[id,false],[new URL(location.href).searchParams.get('page'),document.getElementById(id).hidden]);}}
 }catch(e){report.cases.push({name:'Runner exception',result:'FAIL',error:String(e)})}
 report.failed=report.cases.filter(c=>c.result==='FAIL').length;
 const out=document.createElement('script');out.id='scenario-results';out.type='application/json';out.textContent=JSON.stringify(report);document.body.append(out);
 const status=document.createElement('pre');status.id='scenario-summary';status.textContent=JSON.stringify({cases:report.cases.length,failed:report.failed});document.body.prepend(status);document.body.dataset.done='true';
};
})();
