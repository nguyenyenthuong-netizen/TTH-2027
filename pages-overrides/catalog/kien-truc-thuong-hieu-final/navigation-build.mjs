import {readFileSync} from 'node:fs';
export function assertStableRouting(data,registry){for(const [site,types] of Object.entries(registry))for(const [type,records]of Object.entries(types))for(const [i,expected]of records.entries()){const actual=data[site]?.[type]?.[i];if(!actual||(actual.id||actual.route||actual.name)!==expected.id||actual.name!==expected.name)throw Error('Stable navigation identity changed: '+site+'/'+type+'/'+i+'; migrate the route registry and profile together');}}
// Register newly added service records in both content and legacy route titles.
// Existing templates, photographs, styles and brand hierarchy remain byte-identical.
export function prepareNavigationContent(html) {
  const dataMarker='const DATA=', dataStart=html.indexOf(dataMarker)+dataMarker.length;
  const dataEnd=html.indexOf(';\nfor(const item',dataStart);
  const marker='const NORMALIZED=', start=html.indexOf(marker)+marker.length;
  const end=html.indexOf(';\n',start);
  if(dataStart<dataMarker.length||dataEnd<0||start<marker.length||end<0)throw Error('Navigation source markers changed');
  const sites=JSON.parse(html.slice(dataStart,dataEnd));
  const normalized=JSON.parse(html.slice(start,end));
  const registry=JSON.parse(readFileSync(new URL('./navigation-registry.json',import.meta.url),'utf8'));
  assertStableRouting(normalized,registry);
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const specialties=['Tai Mũi Họng','Mắt','Răng Hàm Mặt','Y học cổ truyền','Thẩm mỹ'];
  const visualSource=['tri','chau','thao','phuc','tam'];
  let taggedHeadings=0;
  sites.group.body=sites.group.body.replace(/(<template id="tpl-([^"]+)">)([\s\S]*?)(<\/template>)/g,(all,open,page,body,close)=>open+body.replace(/<h([1-4])([^>]*)>([\s\S]*?)<\/h\1>/g,(tag,level,attrs,text)=>{if(attrs.includes('data-nav-object-id'))return tag;const slug=text.replace(/<[^>]*>/g,' ').replace(/&amp;/g,'and').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[đĐ]/g,'d').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,Math.max(1,94-page.length));if(!slug)return tag;taggedHeadings++;return '<h'+level+attrs+' data-nav-object-id="'+page+'--'+slug+'">'+text+'</h'+level+'>';})+close);
  const additions=[];
  for(const [site,d]of Object.entries(normalized))for(const [index,r]of d.services.entries()){
    const route='med-service-'+index;
    if(sites[site].body.includes('id="tpl-'+route+'"'))continue;
    const facilities=r.facilities.map(i=>({i,f:d.facilities[i]}));
    if(!r.name||facilities.some(x=>!x.f)||!r.spec.length)throw Error('Incomplete service route: '+site+'/'+route);
    const figure=/<template id="tpl-med-service-0">[\s\S]*?(<figure>[\s\S]*?<\/figure>)/.exec(sites[visualSource[r.spec[0]]]?.body||'')?.[1]||'';
    const photo=figure.replace(/alt="[^"]*"/,`alt="${esc(r.name)} – hình ảnh minh họa"`);
    const units=facilities.map(({i,f})=>`<a href="#${esc(f.route||'med-facility-'+i)}">${esc(f.name)}</a>`).join(' · ');
    const body=`<div class="med-wrap"><div class="med-disclaimer">Thông tin minh họa; không phải hồ sơ hoặc dịch vụ đã được xác nhận.</div><div class="med-lead"><div><span class="med-kicker">Chăm sóc chuyên sâu</span><h2>${esc(r.name)}</h2><p>Thông tin dịch vụ theo phạm vi chuyên khoa và cơ sở trong danh mục minh họa.</p><a class="med-button" href="#med-book" onclick="demoAppointment('service',${index});return false">Đặt lịch khám</a></div>${photo}</div><table class="med-table"><tr><th>Dịch vụ</th><td>${esc(r.name)}</td></tr><tr><th>Chuyên khoa</th><td>${r.spec.map(i=>esc(specialties[i])).join(' · ')}</td></tr><tr><th>Đơn vị thực hiện</th><td>${units} (minh họa)</td></tr></table><div class="med-links"><a href="#treatment">Danh mục dịch vụ</a><a href="#facilities">Cơ sở</a></div></div>`;
    sites[site].body+=`<template id="tpl-${route}">${body}</template>`;
    additions.push({site,route,title:r.name});
  }
  if(!additions.length&&!taggedHeadings)return html;
  let output=html.slice(0,dataStart)+JSON.stringify(sites).replaceAll('</script','<\\/script')+html.slice(dataEnd);
  for(const {site,route,title}of additions){
    const prefix=`const ID="${site}",TITLE={`;
    if(output.split(prefix).length!==2)throw Error('Route-title registration is not unique: '+site);
    output=output.replace(prefix,prefix+JSON.stringify(route)+':'+JSON.stringify(title)+',');
  }
  console.log('Registered normalized service routes: '+additions.map(x=>x.site+'/'+x.route).join(', '));
  return output;
}
