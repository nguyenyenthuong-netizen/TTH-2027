import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
const base=dirname(fileURLToPath(import.meta.url));
const source=execFileSync('unzip',['-p',join(base,'website.zip'),'index.html'],{maxBuffer:70*1024*1024}).toString('utf8');
const match=/<script id="pagesData" type="application\/json">([\s\S]*?)<\/script>/.exec(source);
if(!match)throw Error('Missing authoritative pagesData');
const pages=JSON.parse(match[1]),known=Object.keys(pages),adapter=readFileSync(join(base,'navigation.js'),'utf8');
// Read identities from the approved detail pages, rather than routing unrelated
// cards to the old shared Tim mạch/doctor templates.
const entities=Object.entries(pages).filter(([page])=>/^ChuyenKhoa_(?!DanhSach)|^BacSi_HoSo_/.test(page)).map(([page,doc])=>({
 page,title:(/<h1[^>]*>([\s\S]*?)<\/h1>/.exec(doc)?.[1]||'').replace(/<[^>]*>/g,'').trim()
}));
if(entities.some(x=>!x.title))throw Error('Missing approved entity identity');
for(const [page,doc]of Object.entries(pages)){
 if(doc.includes('id="tth-central-navigation"'))throw Error('Duplicate navigation adapter');
 const title=/<title>([\s\S]*?)<\/title>/.exec(doc)?.[1]||page;
 const config=JSON.stringify({page,title,known,entities}).replaceAll('</','<\\/');
 const injection='<script id="tth-central-navigation">window.__TTH_NAV_CONFIG__='+config+';'+adapter+'</script>';
 pages[page]=doc.replace('</head>',injection+'</head>');
}
const json=JSON.stringify(pages).replaceAll('<','\\u003c').replaceAll('>','\\u003e');
let output=source.slice(0,match.index)+match[0].replace(match[1],()=>json)+source.slice(match.index+match[0].length);
const bridge=`<script id="tth-contact-protocol-bridge">(function(){const frame=document.getElementById('frame');window.addEventListener('message',e=>{if(e.source!==frame?.contentWindow)return;if(e.data?.type==='TTH_NAV_BACK'){history.back();return;}if(e.data?.type!=='TTH_NAV_EXTERNAL')return;const href=e.data.href;if(typeof href==='string'&&(/^(tel:[+0-9 -]{5,20})$/.test(href)||(/^mailto:/.test(href)&&!/[<>\\r\\n]/.test(href))))location.href=href;});})();<\/script>`;
const bodyEnd=output.lastIndexOf('</body>');if(bodyEnd<0)throw Error('Missing outer body');
output=output.slice(0,bodyEnd)+bridge+output.slice(bodyEnd);
const destination=process.argv[2]||join(base,'public');mkdirSync(destination,{recursive:true});writeFileSync(join(destination,'index.html'),output);
console.log(`PASS: ${known.length} Healthcare pages; additive navigation adapter; ${Buffer.byteLength(output)} bytes`);
