/* Healthcare adapter for the same navigation contract as the Group catalogue. */
(function(){'use strict';
const config=window.__TTH_NAV_CONFIG__, records=new Map();
const fold=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[đĐ]/g,'d').toLowerCase().replace(/\s+/g,' ').trim();
const clean=s=>String(s||'').replace(/\s+/g,' ').trim();
const query=()=>new URLSearchParams(window.__TTH_OFFLINE_ROUTE_QUERY__||location.search);
const source=()=>window.__TTH_WEBSITE_PAGE_NAME__||config.page;
const locale=()=>query().get('lang')||(source()==='EN_TrangChu.html'?'en':'vi');
function branch(){const p=source();return /TTHHaTinh/.test(p)?'TTH Hà Tĩnh':/TTHQuangBinh/.test(p)?'TTH Quảng Bình':/TTHVinh/.test(p)?'TTH Vinh':/TTHKheTre/.test(p)?'TTH Khe Tre':/TTHALuoi/.test(p)?'TTH A Lưới':/TTHHue/.test(p)?'TTH Huế':query().get('branch')||'';}
function subject(el){
 const card=el.closest('article,.card');let title=clean(card?.querySelector('h2,h3,h4,strong')?.textContent);
 if(!title||/^(đặt lịch|xem thêm|xem chi tiết|liên hệ|danh mục)/i.test(title))title=clean(document.querySelector('main h1,main h2,#app h1')?.textContent);
 if(source()==='Demo_ChiTiet.html')try{title=JSON.parse(query().get('item'))?.title||title;}catch{}
 return title?.slice(0,180)||config.title;
}
function contract(el){
 const raw=el.getAttribute('data-nav-original')??el.getAttribute('href')??el.dataset.href??el.dataset.route??'';
 const text=fold(el.textContent||el.getAttribute('aria-label'));
 if(/^(?:←\s*|‹\s*)?(quay lai|back)$/.test(text))return {action:'back',status:'configured'};
 if(/^(gui gop y|gui yeu cau( tu van| ho tro)?|send feedback|send request|submit feedback|submit request)$/.test(text))return {action:'unavailable',status:'unavailable',object:'unconnected-enquiry'};
 if(/Web_TroLy\.html/.test(raw)||/^hoi tro ly|tro ly tth|information assistant/.test(text))return {action:'assistant',status:'illustrative',unit:branch()||'healthcare'};
 let target=raw;const q=query(),ctx=new URLSearchParams();
 const combined=/^(?:vi|vn)\s*[|/]\s*en$/i.test(clean(el.textContent))||el.getAttribute('aria-label')==='Chuyển ngôn ngữ';
 const isLanguage=combined||/^(vn|vi|en|english|tiếng việt)$/.test(clean(el.textContent).toLowerCase())||raw.split('?')[0]==='EN_TrangChu.html';
 if(isLanguage){const lang=combined?(locale()==='en'?'vi':'en'):/^(vn|vi|tiếng việt)$/.test(clean(el.textContent).toLowerCase())?'vi':'en';
  const p=source()==='EN_TrangChu.html'?'Main.html':source();
  const dest=p==='Main.html'&&lang==='en'?'EN_TrangChu.html':p;
  q.set('lang',lang);return {brand:'healthcare',unit:branch()||'healthcare',from:source(),to:dest+'?'+q,object:q.get('nav_object')||source(),action:'language',language:lang,status:lang==='en'&&dest!=='EN_TrangChu.html'?'partial-translation':'configured',back:'browser-history'};
 }
 const partnership=/^(ket noi hop tac|lien he hop tac|partnership|partner with|connect for partnership)/.test(text);
 if(partnership){ctx.set('nav_intent','partner');ctx.set('nav_from',source());ctx.set('nav_object',source());if(branch())ctx.set('branch',branch());target='HuongDan_LienHe.html?'+ctx;}
 const booking=/^(dat lich( kham)?|tiep tuc dat lich|chon lich|dat hen|book( an?)? appointment|book now|book a visit|make an appointment|appointment$)/.test(text)&&!/(huong dan|nhu the nao)/.test(text);
 if(booking){
  const existing=new URLSearchParams(raw.includes('?')?raw.split('?')[1]:'');
  for(const [k,v]of existing)ctx.set(k,v);
  const unit=branch();if(unit&&!ctx.has('branch'))ctx.set('branch',unit);
  if(/^BacSi_HoSo_/.test(source())&&!ctx.has('doctor')){ctx.set('doctor',config.title.split(' – ')[0]);
   const explicit=[...document.querySelectorAll('a[href*="DatLich_Offline.html?doctor="]')][0];if(explicit){for(const[k,v]of new URLSearchParams(explicit.getAttribute('href').split('?')[1]))ctx.set(k,v);}}
  if(/^ChuyenKhoa_/.test(source())&&!/DanhSach/.test(source())&&!ctx.has('specialty'))ctx.set('specialty',config.title.replace(/ – TTH Healthcare$/,'').replace(/^Chuyên khoa /,''));
  ctx.set('nav_subject',subject(el));ctx.set('nav_from',source());ctx.set('nav_object',q.get('nav_object')||source());target='DatLich_Offline.html?'+ctx;
 }
 if(/^(tel:|mailto:)/i.test(target))return {action:target.startsWith('tel:')?'hotline':'email',external:target,status:'configured'};
 if(target==='#chua-co-trang'&&text==='chuyen khoa')target='ChuyenKhoa_DanhSach.html';
 if(target.startsWith('#')){
  if(target==='#top')return {action:'top',anchor:'top',status:'configured'};
  const anchor=document.getElementById(target.slice(1));if(anchor)return {action:'anchor',anchor:target.slice(1),status:'configured'};
  return {action:'unavailable',status:'unavailable',from:source(),object:target};
 }
 if(/^(https?:|\/\/|javascript:|data:|blob:)/i.test(target))return null;
 const path=target.split(/[?#]/)[0].split('/').pop();if(!config.known.includes(path))return null;
 const params=new URLSearchParams(target.includes('?')?target.split('?')[1].split('#')[0]:'');
 if(!params.has('lang'))params.set('lang',locale());
 if(path==='HuongDan_LienHe.html'){if(branch()&&!params.has('branch'))params.set('branch',branch());params.set('nav_from',source());if(!params.has('nav_object'))params.set('nav_object',q.get('nav_object')||source());}
 const dest=path+(params.size?'?'+params:'');
 return {brand:'healthcare',unit:branch()||'healthcare',facility:branch(),from:source(),to:dest,object:params.get('nav_object')||path,action:booking?'booking':/lien he|hop tac|contact/.test(text)?'contact':'page',context:Object.fromEntries(params),language:params.get('lang'),status:booking?'illustrative':'configured',back:'browser-history'};
}
function resolve(el){const r=contract(el);return r?{brand:'healthcare',unit:branch()||'healthcare',facility:branch(),page:source(),from:source(),object:source(),to:null,context:{},language:locale(),status:'configured',back:'browser-history',...r}:null;}
function go(r){if(window.parent!==window)window.parent.postMessage({type:'TTH_WEBSITE_OFFLINE_NAV',target:r.to},'*');else location.href=r.to;}
window.addEventListener('click',e=>{
 if(e.button!==0||e.ctrlKey||e.metaKey||e.altKey||e.shiftKey)return;
 const el=e.target.closest('a[href],[data-nav-original],button[data-href],button[data-route]');if(!el||el.hasAttribute('download'))return;
 const r=resolve(el);if(!r)return;
 if(r.action==='assistant'){e.preventDefault();e.stopImmediatePropagation();assistant();return;}
 if(r.action==='back'){e.preventDefault();e.stopImmediatePropagation();if(window.parent!==window)window.parent.postMessage({type:'TTH_NAV_BACK'},'*');else history.back();return;}
 if(r.status==='unavailable'){e.preventDefault();e.stopImmediatePropagation();notice();return;}
 if(r.action==='hotline'||r.action==='email'){if(window.parent!==window){e.preventDefault();window.parent.postMessage({type:'TTH_NAV_EXTERNAL',href:r.external},'*');}e.stopImmediatePropagation();return;}
 if(r.action==='top'){e.preventDefault();e.stopImmediatePropagation();scrollTo({top:0,behavior:'smooth'});return;}
 if(r.action==='anchor')return;
 if(!r.to)return;
 e.preventDefault();e.stopImmediatePropagation();go(r);
},true);
function assistant(){document.getElementById('tth-nav-assistant')?.remove();const dlg=document.createElement('dialog');dlg.id='tth-nav-assistant';const h=document.createElement('h2');h.textContent='Tra cứu TTH Healthcare';const p=document.createElement('p');p.textContent='Công cụ tra cứu minh họa trong phạm vi TTH Healthcare; chưa kết nối trợ lý AI trực tuyến.';dlg.append(h,p);for(const [to,label]of [['BacSi_DanhSach.html','Bác sĩ'],['DichVu_DanhSach.html','Dịch vụ và gói khám'],['HeThongYTe.html','Cơ sở'],['HuongDan_LienHe.html','Liên hệ']]){const a=document.createElement('a');a.textContent=label;a.href=to+'?lang='+(locale())+'&branch='+encodeURIComponent(branch());a.style.display='block';dlg.append(a);}const b=document.createElement('button');b.textContent='Đóng';b.onclick=()=>dlg.close();dlg.append(b);document.body.append(dlg);dlg.showModal();}
function notice(){document.getElementById('tth-nav-unavailable')?.remove();const dlg=document.createElement('dialog');dlg.id='tth-nav-unavailable';const p=document.createElement('p');p.textContent=query().get('lang')==='en'?'This function has not been connected. Please use the Contact section.':'Chức năng này chưa được kết nối. Vui lòng sử dụng mục Liên hệ.';const b=document.createElement('button');b.textContent=query().get('lang')==='en'?'Close':'Đóng';b.onclick=()=>dlg.close();dlg.append(p,b);document.body.append(dlg);dlg.showModal();}
function scan(){
 for(const el of document.querySelectorAll('a[href],[data-nav-original],button[data-href],button[data-route]')){
  const r=resolve(el);if(!r)continue;
  if(el.tagName==='A'&&!el.hasAttribute('data-nav-original'))el.dataset.navOriginal=el.getAttribute('href');
  if(el.tagName==='A'&&['booking','language'].includes(r.action)&&r.to&&el.getAttribute('href')!==r.to)el.setAttribute('href',r.to);
  if(r.status==='unavailable'&&el.hasAttribute('href')){el.removeAttribute('href');el.setAttribute('role','button');el.tabIndex=0;el.setAttribute('aria-disabled','true');el.title=query().get('lang')==='en'?'Not connected':'Chưa kết nối';}
  if(r.status==='partial-translation')el.title='English navigation; full English content is not yet available for this page.';
  el.dataset.navAction=r.action;el.dataset.navStatus=r.status;el.dataset.navUnit=r.unit||branch()||'healthcare';
  records.set(JSON.stringify([r.from,r.action,r.object,r.to]),r);
 }
 if(source()==='HuongDan_LienHe.html'&&branch()){
  for(const select of document.querySelectorAll('main select')){if(select.dataset.navUnitPrefilled)continue;const o=[...select.options].find(o=>fold(o.textContent).includes(fold(branch())));if(o){select.value=o.value;select.dataset.navUnitPrefilled='1';}}
 }
 for(const strong of document.querySelectorAll('[role=status] strong'))if(/^Sau khi gửi:/.test(strong.textContent)){strong.textContent='Biểu mẫu minh họa, chưa kết nối tiếp nhận. Chưa gửi hoặc xác nhận yêu cầu.';const next=strong.nextElementSibling;if(next?.tagName==='SPAN')next.textContent='Vui lòng liên hệ tổng đài để được hỗ trợ. Lịch khám cần được cơ sở xác nhận.';}
 const f=document.getElementById('tth-website-booking-form');if(f&&!f.dataset.navContext){
  f.dataset.navContext='1';const q=query();const text=q.get('nav_subject');
  if(text){const label=document.createElement('label');label.textContent=q.get('lang')==='en'?'Subject of interest':'Nội dung quan tâm';const input=document.createElement('input');input.name='nav_subject';input.readOnly=true;input.value=text;label.append(input);f.prepend(label);}
  for(const key of ['nav_from','nav_object','lang']){const input=document.createElement('input');input.type='hidden';input.name=key;input.value=q.get(key)||'';f.append(input);}
 }
}
let pending=false;function schedule(){if(!pending){pending=true;requestAnimationFrame(()=>{pending=false;scan()})}}
window.TTHNavigation={version:'2026-11-28.1',resolve,records:()=>[...records.values()]};
document.addEventListener('keydown',e=>{const el=e.target.closest('[data-nav-status=unavailable]');if(el&&['Enter',' '].includes(e.key)){e.preventDefault();el.click();}});
function init(){scan();new MutationObserver(schedule).observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['href']});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
