"""Protect approved design and validate both single-file builds before publication."""
from pathlib import Path
import sys,json,re,zipfile,hashlib,subprocess,tempfile
root=Path(__file__).resolve().parent.parent
main=Path(sys.argv[1]).read_text();hc=Path(sys.argv[2]).read_text()
assert main.count('id="tth-central-navigation"')==1
assert 'tth-image-frame-limit-v2' in main
assert 'not([class*=hero i] *' in main
m=re.search(r'<script id="pagesData" type="application/json">(.*?)</script>',hc,re.S);assert m
assert '<' not in m[1], 'Embedded page JSON must be HTML-safe'
pages=json.loads(m[1]);original=zipfile.ZipFile(root/'tth-healthcare-release/website.zip').read('index.html').decode()
before=json.loads(re.search(r'<script id="pagesData" type="application/json">(.*?)</script>',original,re.S)[1]);assert pages.keys()==before.keys()
for name,doc in pages.items():
 restored,n=re.subn(r'<script id="tth-central-navigation">.*?</script>','',doc,flags=re.S)
 assert n==1 and restored==before[name],f'Approved Healthcare design changed: {name}'
 assert '</head>' in doc and '</body>' in doc
assert re.search(r'<script id="imagesData" type="application/json">(.*?)</script>',hc,re.S)[1]==re.search(r'<script id="imagesData" type="application/json">(.*?)</script>',original,re.S)[1], 'Image assets changed'
# Check every compiled executable script including generated adapters and protocol bridge.
count=0
with tempfile.TemporaryDirectory() as tmp:
 for label,doc in [('catalog',main),('healthcare',hc),('healthcare-page',next(iter(pages.values())))]:
  for attrs,script in re.findall(r'<script([^>]*)>(.*?)</script>',doc,re.S):
   if 'application/json' in attrs or not script.strip():continue
   p=Path(tmp)/'check.js';p.write_text(script)
   result=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
   assert result.returncode==0,label+': '+result.stderr[:1000]
   count+=1
report={'result':'PASS','healthcare_pages_preserved':len(pages),'image_payload_unchanged':True,'executable_scripts_checked':count,'sha256':{'catalog':hashlib.sha256(main.encode()).hexdigest(),'healthcare':hashlib.sha256(hc.encode()).hexdigest()}}
print(json.dumps(report,indent=2))
