/* Central navigation contract. No styling, brand content or patient data is changed. */
(function () {
  'use strict';
  const VERSION = '2026-11-28.1';
  const contextKeys = ['intent', 'from', 'object', 'facility', 'specialty', 'field', 'topic'];
  const medical = new Set(['bach','tri','chau','thao','phuc','tam','tth']);
  const state = { context: {}, errors: [], records: new Map() };
  const page = () => String(currentHash || '#home').slice(1);
  const locale = () => tthLocale === 'en' ? 'en' : 'vi';
  const tr = (vi,en) => locale() === 'en' ? en : vi;
  const validKey = x => /^[a-z0-9-]{1,100}$/.test(x || '');
  const formPage = p => ['contact','guide','med-book','med-program-register','apply'].includes(p);
  const parseContext = () => {
    const q = new URL(location.href).searchParams, c = {};
    for (const k of contextKeys) { const v = q.get('nav_'+k); if (validKey(v)) c[k] = v; }
    return c;
  };
  function url(site, dest, ctx = {}, lang = locale()) {
    const u = new URL(location.href); u.hash = '';
    for (const k of contextKeys) u.searchParams.delete('nav_'+k);
    if (site === 'catalog') for (const k of ['site','page','lang']) u.searchParams.delete(k);
    else { u.searchParams.set('site',site);u.searchParams.set('page',dest);u.searchParams.set('lang',lang); }
    if (formPage(dest)) for (const k of contextKeys) if (validKey(ctx[k])) u.searchParams.set('nav_'+k,ctx[k]);
    return u.href;
  }
  function field(p) {
    if (/media|news|press|article|gallery|video/.test(p)) return 'media';
    if (/career|job|apply|recruit|benefit/.test(p)) return 'careers';
    if (/esg|community|sustainab/.test(p)) return 'community';
    if (/field-|member-|partner|investment/.test(p)) return p;
    return p;
  }
  function objectContext(p) {
    const c = {from:p,object:p,field:field(p)};
    const m=/^med-(doctor|service|package|program)-(\d+)$/.exec(p), d=NORMALIZED[active];
    if(m&&d){
      const r=d[m[1]==='package'?'packages':m[1]+'s']?.[Number(m[2])];
      if(r){const f=m[1]==='doctor'?r.facility:r.facilities?.length===1?r.facilities[0]:undefined;
        if(Number.isInteger(f))c.facility=String(f);
        if(r.spec?.length===1)c.specialty=String(r.spec[0]);}
    }
    const clinical=/^clinical-(\d+)$/.exec(p);
    if(clinical&&d){const i=+clinical[1];const sp=active==='bach'?i:active==='tth'?(i<=4?2:i<=6?4:undefined):d.services[0]?.spec[0];if(Number.isInteger(sp))c.specialty=String(sp);}
    const i=d?.facilities.findIndex(x=>x.route===p);
    if(i>=0)c.facility=String(i);
    return c;
  }
  function contract(el) {
    const raw=el.getAttribute('data-nav-raw') ?? el.getAttribute('href') ?? '';
    const inline=el.getAttribute('onclick') || '';
    const text=(el.textContent || el.getAttribute('aria-label') || '').trim().replace(/\s+/g,' ');
    const origin=page(); let site=el.dataset.site||active, dest=null, action='page', ctx={};
    const data=NORMALIZED[active];
    if(el.id==='nav-recent')return {action:'back',status:history.length>1?'configured':'unavailable'};
    if(el.id==='nav-up'||el.id==='nav-down')return {action:el.id==='nav-up'?'top':'bottom',status:'configured'};
    const language=/^clinicalLang\(['"](vi|en)['"]\)/.exec(inline);
    if(language)return {site:active,to:origin,action:'language',context:{...state.context},language:language[1],object:state.context.object||origin,status:'configured'};
    if(/^closeSite\(/.test(inline))return {site:'catalog',to:'home',action:'catalog',context:{},status:'configured'};
    if(/^(?:openAdvancedSearch|search)\(/.test(inline))return {action:'search',scope:active,status:'configured'};
    if(el.tagName==='FORM')return {action:'submit',status:medical.has(active)&&origin==='guide'?'configured':'illustrative'};
    if (el.matches('[data-tth-contact]')) {dest=medical.has(active)?'guide':'contact';action='contact';}
    else if(/(?:tthContact|medContact|elContact)\(['"]call/.test(inline) || (el.closest('#elder-cta-dock')&&/Hotline/i.test(text))){
      const hotline=DATA[active].contact?.hotline;
      return {action:'hotline',external:hotline?'tel:'+hotline.replace(/[^+\d]/g,''):null,status:hotline?'configured':'unavailable'};
    }
    else if(/(?:tthContact|medContact)\(['"]zalo/.test(inline)||el.dataset.elderSupport==='zalo'){return {action:'zalo',unit:active,status:'unavailable'};}
    else if(/(?:tthContact|medContact)\(['"]chat/.test(inline)||el.dataset.elderSupport==='assistant'){return {action:'assistant',unit:active,status:'illustrative'};}
    else if (/^(tel:|mailto:)/i.test(raw)) return {action:raw.startsWith('tel:')?'hotline':'email',external:raw,status:/X|undefined|null/.test(raw)?'unavailable':'configured'};
    else {
      let m;
      if ((m=/demoAppointment\(['"](service|package|doctor)['"]\s*,\s*(\d+)\)/.exec(inline))) {
        dest='med-book';action='booking';ctx=objectContext('med-'+m[1]+'-'+m[2]);ctx.from=origin;
      } else if((m=/demoProgram\((\d+)\)/.exec(inline))){dest='med-program-register';action='programme';ctx=objectContext('med-program-'+m[1]);ctx.from=origin;}
      else if((m=/(?:geoBook|nbBook)\((\d+)\)/.exec(inline))){dest='med-book';action='booking';ctx={...objectContext('med-facility-'+m[1]),from:origin};}
      else if((m=/qc110Book\((\d+)\s*,\s*(\d+)\)/.exec(inline))){dest='med-book';action='booking';ctx={...objectContext(origin),facility:m[1],specialty:m[2]};}
      else if(/^request\s*\(/.test(inline)){
        dest=active==='group'?'contact':medical.has(active)?'med-book':'contact';action=medical.has(active)?'booking':'contact';
      }else if(raw.startsWith('#') && raw.length>1)dest=raw.slice(1);
      else if(raw){try{const u=new URL(raw,location.href);if(u.origin===location.origin&&u.searchParams.has('site')){site=u.searchParams.get('site');dest=u.searchParams.get('page')||'home';}}
        catch{} }
    }
    if(!dest)return null;
    if(dest==='med-facility')dest='facilities';
    // Intent is determined by the action on the card, independently of its editorial field.
    if(/^(Kết nối hợp tác|Connect for partnerships|Partnership enquiries|Liên hệ hợp tác)/i.test(text)){
      dest=medical.has(active)?'guide':'contact';action='partnership';ctx={...objectContext(origin),...ctx,intent:'partner'};
    }else if(dest==='contact'||(dest==='guide'&&action==='contact')){
      action='contact';ctx={...objectContext(origin),...ctx,intent:/truyền thông|báo chí|press|media/i.test(text)?'press':/cộng đồng|community/i.test(text)?'community':/hợp tác|đầu tư|partner|investment/i.test(text)?'partner':'info'};
    }else if(dest==='med-book'){
      action='booking';ctx={...objectContext(origin),...ctx};
    }else if(dest==='med-program-register'){
      action='programme';ctx={...objectContext(origin),...ctx};
    }
    if(active==='group'&&['contact','partnership'].includes(action)){
      const card=el.closest('article,.card,.tile,.premium-tile');const heading=card?.querySelector('h2,h3,h4');
      const id=card?.dataset.navObjectId||heading?.dataset.navObjectId;
      if(validKey(id)){ctx.object=id;ctx.topic=id;if(/truyen-thong|bao-chi|media/.test(id))ctx.field='media';}
    }
    return {brand:site,unit:site,site,page:origin,object:ctx.object||dest,action,from:origin,to:dest,context:ctx,language:locale(),status:'configured',back:'browser-history'};
  }
  function resolve(el){const r=contract(el);return r?{brand:active,unit:active,site:active,page:page(),object:page(),from:page(),to:null,context:{},language:locale(),status:'configured',back:'browser-history',...r}:null;}
  function preferences(c) {
    const pref={}, m=/^med-(doctor|service|package|program)-(\d+)$/.exec(c.object||'');
    const d=NORMALIZED[active];
    if(m&&d){const list=d[m[1]==='package'?'packages':m[1]+'s'];if(list?.[+m[2]]){pref.type=m[1];pref.index=+m[2];}}
    if(c.facility!==undefined&&d?.facilities[+c.facility]){pref.facility=+c.facility;if(!pref.type){pref.type='facility';pref.index=+c.facility;}geoSelected[active]=+c.facility;}
    if(c.specialty!==undefined&&/^\d+$/.test(c.specialty))pref.specialty=+c.specialty;
    return pref;
  }
  function navigate(r) {
    const c=r.context||{}, lang=r.language||locale();
    // Use the existing URL lifecycle atomically; no intermediate brand-home entry.
    const destURL=url(r.site,r.to,c,lang);
    history.pushState({tth:TTH_HISTORY_MARKER,depth:tthHistoryDepth()+1,site:r.site,route:'#'+r.to,lang},'',destURL);
    state.context=c;
    tthRestoreState({site:r.site,route:'#'+r.to,lang});
    hydrate();schedule();
  }
  function displayUnavailable(title,body) {
    document.getElementById('tth-navigation-notice')?.remove();
    const dlg=document.createElement('dialog');dlg.id='tth-navigation-notice';
    const h=document.createElement('h2');h.textContent=title;const p=document.createElement('p');p.textContent=body;
    const b=document.createElement('button');b.textContent=tr('Đóng','Close');b.onclick=()=>dlg.close();
    dlg.append(h,p,b);document.body.append(dlg);dlg.showModal();
  }
  function hydrate() {
    if(!formPage(page()))return;
    const c=state.context;
    if(medical.has(active)&&page()==='med-book'){
      const form=document.querySelector('#demo-book-form form');
      if(form&&!form.dataset.navPreferenceBound){form.dataset.navPreferenceBound='1';const pref=preferences(c);
        const apply=()=>{const spec=form.elements.specialty,svc=form.elements.service;
          if(spec&&c.specialty!==undefined&&[...spec.options].some(x=>x.value===c.specialty)&&spec.value!==c.specialty){spec.value=c.specialty;spec.dispatchEvent(new Event('change',{bubbles:true}));}
          const desired=pref.type==='package'?NORMALIZED[active].services.length+pref.index:pref.type==='service'?pref.index:null;
          if(svc&&desired!==null&&[...svc.options].some(x=>x.value===String(desired))&&svc.value!==String(desired)){svc.value=String(desired);svc.dispatchEvent(new Event('change',{bubbles:true}));}
        };
        form.elements.facility?.addEventListener('change',apply);apply();
      }
    }
    if(active==='group'&&page()==='contact'){
      const f=document.querySelector('#app .corp-form');if(!f)return;
      const select=f.querySelector('select');const index={partner:0,press:1,recruitment:2,info:3,community:4}[c.intent];
      if(select&&index!==undefined&&select.options[index]&&f.dataset.navContext!==JSON.stringify(c)){select.selectedIndex=index;f.dataset.navContext=JSON.stringify(c);}
      // Keep source context in the form without exposing technical identifiers to visitors.
      for(const [key,value] of Object.entries({brand:active,unit:active,language:locale(),...c})){
        let input=f.querySelector('[name="nav_'+key+'"]');if(!input){input=document.createElement('input');input.type='hidden';input.name='nav_'+key;f.append(input);}input.value=value;
      }
    }
  }
  function scan() {
    pending=false;
    if(typeof DATA==='undefined'||!DATA[active])return;
    for(const el of document.querySelectorAll('a,button')){
      if(el.closest('template'))continue;
      const r=resolve(el);if(!r)continue;
      if(el.tagName==='A'&&!el.hasAttribute('data-nav-raw'))el.dataset.navRaw=el.getAttribute('href')||'';
      let href=r.external;
      if(r.to){el.dataset.navUrl=url(r.site,r.to,r.context);if(formPage(r.to))href=el.dataset.navUrl;}
      if(href&&el.tagName==='A'&&el.getAttribute('href')!==href)el.setAttribute('href',href);
      const key=JSON.stringify([active,page(),r.action,r.object,r.to,locale()]);
      el.dataset.navAction=r.action;el.dataset.navStatus=r.status;el.dataset.navUnit=active;
      if(r.action==='hotline'&&r.status==='unavailable'&&el.closest('#elder-cta-dock')){const label=el.querySelector('span');const text='Hotline – '+tr('Chưa công bố','Not published');if(label&&label.textContent!==text)label.textContent=text;}
      state.records.set(key,r);
    }
    hydrate();
  }
  let pending=false;
  function schedule(){if(!pending){pending=true;requestAnimationFrame(scan);}}
  // Registered before legacy handlers. Each recognized action executes exactly once.
  window.addEventListener('click',e=>{
    const el=e.target.closest?.('a,button');if(!el||typeof DATA==='undefined'||!DATA[active])return;
    const r=resolve(el);if(!r)return;
    if(e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    if(r.status==='unavailable'){e.preventDefault();e.stopImmediatePropagation();displayUnavailable(r.action==='zalo'?'Zalo OA':'Hotline',tr('Đơn vị chưa công bố kênh liên hệ này. Vui lòng sử dụng thông tin email tại mục Liên hệ.','This contact channel has not been published by this organisation. Please use the email listed under Contact.'));return;}
    if(r.action==='hotline'&&r.external){
      if(el.tagName==='A')el.setAttribute('href',r.external);else{e.preventDefault();location.href=r.external;}
      // A real tel: anchor is left to the operating system; suppress old popup handlers.
      e.stopImmediatePropagation();return;
    }
    if(!r.to)return;
    const targetSite=r.site||active;
    if(targetSite===active&&!document.getElementById('tpl-'+r.to)&&r.to!=='home'){
      if(active==='architecture')return;
      const anchor=document.getElementById(r.to);
      if(anchor&&anchor.tagName!=='TEMPLATE'){e.preventDefault();e.stopImmediatePropagation();anchor.scrollIntoView({behavior:'smooth'});return;}
      // Architecture has its own views. Let its existing router handle these.
      if(active==='architecture')return;
      state.errors.push({...r,error:'missing-target'});e.preventDefault();e.stopImmediatePropagation();
      displayUnavailable(tr('Nội dung chưa có','Content unavailable'),tr('Nội dung này chưa được cung cấp. Vui lòng chọn một mục khác.','This content is not yet available. Please choose another section.'));return;
    }
    if(!DATA[targetSite]||targetSite==='healthcare')return;
    e.preventDefault();e.stopImmediatePropagation();navigate(r);
  },true);
  function start(){
    state.context=parseContext();
    // Resolve native fragment links opened in a new tab against their source-page URL.
    const fragment=location.hash.slice(1);
    if(validKey(fragment)&&document.getElementById('tpl-'+fragment)){
      const c=formPage(fragment)?{...objectContext(page()),...state.context}:{};
      history.replaceState(history.state,'',url(active,fragment,c));state.context=c;
      if(NORMALIZED[active])demoPref=preferences(c);tthRestoreState({site:active,route:'#'+fragment,lang:locale()});
    }
    // Restore object context before booking forms are mounted, including reload/back/forward.
    const restore=tthRestoreState;
    tthRestoreState=function(x){state.context=parseContext();if(NORMALIZED[x.site])demoPref=preferencesFor(x.site,state.context);return restore(x);};
    function preferencesFor(site,c){const previous=active;/* preferences() reads active; restore before first mount is handled below */
      if(site===previous)return preferences(c);
      const d=NORMALIZED[site],pref={},m=/^med-(doctor|service|package|program)-(\d+)$/.exec(c.object||'');
      if(m&&d?.[m[1]==='package'?'packages':m[1]+'s']?.[+m[2]]){pref.type=m[1];pref.index=+m[2];}
      if(c.facility!==undefined&&d?.facilities[+c.facility]){pref.facility=+c.facility;if(!pref.type){pref.type='facility';pref.index=+c.facility;}geoSelected[site]=+c.facility;}
      if(/^\d+$/.test(c.specialty||''))pref.specialty=+c.specialty;return pref;
    }
    const controls=updateNavControls;
    updateNavControls=function(){controls();const b=document.getElementById('nav-recent');if(b){b.disabled=history.length<=1;b.title=tr('Quay lại trang trước','Back to the previous page');}};
    navBack=function(){if(history.length>1)history.back();};
    const write=tthWriteURL;
    tthWriteURL=function(replace=false){
      if(!formPage(page())){state.context={};const u=new URL(location.href);let changed=false;for(const k of contextKeys){if(u.searchParams.has('nav_'+k)){u.searchParams.delete('nav_'+k);changed=true;}}if(changed)history.replaceState(history.state,'',u.href);}
      const result=write(replace);schedule();return result;
    };
    const lang=clinicalLang;
    clinicalLang=function(l){const ctx=state.context;const result=lang(l);state.context=ctx;hydrate();schedule();return result;};
    new MutationObserver(schedule).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:['href','onclick']});
    if(formPage(page())&&Object.keys(state.context).length)tthRestoreState(tthURLState());
    updateNavControls();schedule();
  }
  window.TTHNavigation={version:VERSION,url,resolve,records:()=>[...state.records.values()],errors:()=>state.errors.slice(),context:()=>({...state.context})};
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
