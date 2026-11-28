import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
const root=new URL('../',import.meta.url);
const html=execFileSync('unzip',['-p',new URL('tth-healthcare-release/website.zip',root).pathname,'index.html'],{maxBuffer:70*1024*1024}).toString();
const pages=JSON.parse(/<script id="pagesData" type="application\/json">([\s\S]*?)<\/script>/.exec(html)[1]);
const entities=Object.entries(pages).filter(([p])=>/^ChuyenKhoa_(?!DanhSach)|^BacSi_HoSo_/.test(p)).map(([page,doc])=>({page,title:/<h1[^>]*>([\s\S]*?)<\/h1>/.exec(doc)[1].replace(/<[^>]*>/g,'').trim()}));
const config={page:'Main.html',title:'Trang chủ',known:Object.keys(pages),entities};
const w={__TTH_NAV_CONFIG__:config,addEventListener(){}};
const context={window:w,URLSearchParams,Map,Set,location:{search:''},document:{readyState:'loading',addEventListener(){},querySelector(){return {textContent:'Trang chủ'}},querySelectorAll(){return []}}};
vm.runInNewContext(readFileSync(new URL('tth-healthcare-release/navigation.js',root),'utf8'),context);
const link=(label,href,cardTitle='',original)=>({textContent:label,dataset:{},getAttribute:k=>k==='href'?href:k==='data-nav-original'?original??null:null,closest:()=>cardTitle?{textContent:cardTitle,querySelector:()=>({textContent:cardTitle})}:null});
let count=0;function equal(actual,expected,message){assert.deepEqual(JSON.parse(JSON.stringify(actual)),expected,message);count++;}
// All approved named details must survive links left pointing to shared templates.
for(const e of entities){const doctor=e.page.startsWith('BacSi_');
 for(const lang of ['vi','en']){
  w.__TTH_OFFLINE_ROUTE_QUERY__='lang='+lang;
  const r=w.TTHNavigation.resolve(link(doctor?'Hồ sơ bác sĩ →':e.title,doctor?'BacSi_HoSo.html':'ChuyenKhoa_TimMach.html',doctor?e.title:''));
  equal([r.to?.split('?')[0],r.language],[e.page,lang],e.title);
 }
}
for(const [label,path] of [['Mắt – mổ Phaco','ChuyenKhoa_mat.html'],['Thận nhân tạo','ChuyenKhoa_than-tiet-nieu.html'],['Chấn thương chỉnh hình','ChuyenKhoa_chan-thuong-chinh-hinh-y-hoc-the-thao.html'],['Tiêu hóa','ChuyenKhoa_tieu-hoa-than-kinh.html'],['Thần kinh','ChuyenKhoa_tieu-hoa-than-kinh.html'],['Phục hồi chức năng','ChuyenKhoa_y-hoc-co-truyen-phuc-hoi-chuc-nang.html']]){
 for(const suffix of ['', ' Mô tả đã duyệt trên thẻ'])equal(w.TTHNavigation.resolve(link(label+suffix,'ChuyenKhoa_TimMach.html')).to?.split('?')[0],path,label);
}
equal(w.TTHNavigation.resolve(link('Hồ sơ bác sĩ →','BacSi_HoSo.html','Đội ngũ bác sĩ chưa công bố')).status,'unavailable');
equal(w.TTHNavigation.resolve(link('Lão khoa','ChuyenKhoa_TimMach.html')).status,'unavailable');
const compact=link('Thận nhân tạoLọc máu định kỳ cho người bệnh suy thận.','ChuyenKhoa_TimMach.html');
compact.querySelector=()=>({textContent:'Thận nhân tạo'});
equal(w.TTHNavigation.resolve(compact).to?.split('?')[0],'ChuyenKhoa_than-tiet-nieu.html','Adjacent title/description nodes must not lose the specialty');
// The first scan may run before the old runtime contextualizes a generic link.
const item=JSON.stringify({title:'Thai sản trọn gói',kind:'service'});
const r=w.TTHNavigation.resolve(link('Xem chi tiết','Demo_ChiTiet.html?item='+encodeURIComponent(item),'Thai sản trọn gói','DichVu_ChiTiet.html'));
equal([r.to?.split('?')[0],new URLSearchParams(r.to?.split('?')[1]).get('item')],['Demo_ChiTiet.html',item]);
w.__TTH_WEBSITE_PAGE_NAME__='Microsite_TTHHaTinh.html';w.__TTH_OFFLINE_ROUTE_QUERY__='lang=en';
const facility=w.TTHNavigation.resolve(link('Sản phụ khoa','ChuyenKhoa_TimMach.html'));
equal([facility.to?.split('?')[0],new URLSearchParams(facility.to?.split('?')[1]).get('branch')],['ChuyenKhoa_san-phu-khoa.html','TTH Hà Tĩnh']);
const baseline=readFileSync(new URL('navigation-handover/healthcare-semantic-baseline.json',root),'utf8');
assert(JSON.parse(baseline).observed_heading==='Tim mạch');
console.log(`PASS ${count} Healthcare semantic identity/context assertions; ${entities.length} approved object identities`);
