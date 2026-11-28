import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const config={page:'BacSi_HoSo_bs-test.html',title:'BS.CKI Bác sĩ mẫu – Hồ sơ minh họa TTH Healthcare',known:['Main.html','EN_TrangChu.html','BacSi_HoSo_bs-test.html','MS_TTHHaTinh_DichVu.html','HuongDan_DatLich.html','HuongDan_LienHe.html','DatLich_Offline.html']};
const w={__TTH_NAV_CONFIG__:config,__TTH_WEBSITE_PAGE_NAME__:config.page,__TTH_OFFLINE_ROUTE_QUERY__:'',addEventListener(){}};
const context={window:w,URLSearchParams,Map,Set,location:{search:''},document:{readyState:'loading',addEventListener(){},querySelector(){return {textContent:config.title}},querySelectorAll(){return []}}};
vm.runInNewContext(readFileSync(new URL('../tth-healthcare-release/navigation.js',import.meta.url),'utf8'),context);
const el=(text,href)=>({textContent:text,dataset:{},getAttribute:k=>k==='href'?href:null,closest:()=>null});
let count=0;const check=(v,e)=>{assert.deepEqual(JSON.parse(JSON.stringify(v)),e);count++;};
for(const label of ['Đặt lịch khám','Đặt lịch','đặt lịch khám','Book an appointment','Book appointment','Book now']){
 const r=w.TTHNavigation.resolve(el(label,'HuongDan_DatLich.html'));const [path,q]=r.to.split('?');const p=new URLSearchParams(q);
 check([r.action,path,p.get('doctor'),p.get('nav_from')],['booking','DatLich_Offline.html','BS.CKI Bác sĩ mẫu',config.page]);
}
w.__TTH_WEBSITE_PAGE_NAME__='MS_TTHHaTinh_DichVu.html';config.title='Dịch vụ & Gói khám';
let r=w.TTHNavigation.resolve(el('Đặt lịch khám','HuongDan_DatLich.html'));let p=new URLSearchParams(r.to.split('?')[1]);check([p.get('branch'),p.get('nav_from')],['TTH Hà Tĩnh','MS_TTHHaTinh_DichVu.html']);
w.__TTH_OFFLINE_ROUTE_QUERY__='branch=TTH+H%C3%A0+T%C4%A9nh&nav_object=service-3';
r=w.TTHNavigation.resolve(el('EN','EN_TrangChu.html'));p=new URLSearchParams(r.to.split('?')[1]);check([r.to.split('?')[0],p.get('lang'),p.get('nav_object')],['MS_TTHHaTinh_DichVu.html','en','service-3']);
r=w.TTHNavigation.resolve(el('Kết nối hợp tác','VeTTH_TrangCon.html'));p=new URLSearchParams(r.to.split('?')[1]);check([r.action,r.to.split('?')[0],p.get('nav_intent'),p.get('branch')],['contact','HuongDan_LienHe.html','partner','TTH Hà Tĩnh']);
r=w.TTHNavigation.resolve(el('Hotline','tel:0948956622'));check([r.action,r.external,r.unit],['hotline','tel:0948956622','TTH Hà Tĩnh']);
r=w.TTHNavigation.resolve(el('VI | EN','EN_TrangChu.html'));p=new URLSearchParams(r.to.split('?')[1]);check([r.action,r.to.split('?')[0],p.get('lang'),p.get('branch')],['language','MS_TTHHaTinh_DichVu.html','en','TTH Hà Tĩnh']);
w.__TTH_OFFLINE_ROUTE_QUERY__='lang=en&branch=TTH+H%C3%A0+T%C4%A9nh&nav_object=service-3';r=w.TTHNavigation.resolve(el('VI | EN','EN_TrangChu.html'));p=new URLSearchParams(r.to.split('?')[1]);check([p.get('lang'),p.get('nav_object')],['vi','service-3']);
w.__TTH_WEBSITE_PAGE_NAME__='EN_TrangChu.html';w.__TTH_OFFLINE_ROUTE_QUERY__='';r=w.TTHNavigation.resolve(el('Doctors','BacSi_HoSo_bs-test.html'));check(new URLSearchParams(r.to.split('?')[1]).get('lang'),'en');
w.__TTH_WEBSITE_PAGE_NAME__='MS_TTHHaTinh_DichVu.html';w.__TTH_OFFLINE_ROUTE_QUERY__='branch=TTH+H%C3%A0+T%C4%A9nh&nav_object=service-3';r=w.TTHNavigation.resolve(el('Liên hệ','HuongDan_LienHe.html'));p=new URLSearchParams(r.to.split('?')[1]);check([p.get('branch'),p.get('nav_object'),p.get('nav_from')],['TTH Hà Tĩnh','service-3','MS_TTHHaTinh_DichVu.html']);
r=w.TTHNavigation.resolve(el('Gửi góp ý','#g-i-g-p'));check([r.action,r.status],['unavailable','unavailable']);
console.log(`PASS ${count} Healthcare business assertions, including uppercase Vietnamese and English booking`);
