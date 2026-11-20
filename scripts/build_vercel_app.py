#!/usr/bin/env python3
"""Build the Healthcare App from the same source bundle used by GitHub Pages.
Only publishes healthcare-app output. No Khung/source changes.
"""
from pathlib import Path
import shutil,subprocess,zipfile
root=Path.cwd()
site=root/'_site'
bundle=root/'TTH_5_Giao_Dien_GitLab_Pages_Free.zip'
if not bundle.exists():raise SystemExit('Missing TTH source archive')
with zipfile.ZipFile(bundle) as z:
 names=set(z.namelist())
 if 'public/healthcare-app/index.html' not in names:
  raise SystemExit('Bundle lacks Healthcare App')
 z.extractall(root/'_vercel_source')
shutil.copytree(root/'_vercel_source'/'public',site,dirs_exist_ok=True)
# The post-assembly repair expects the canonical 27-slide source as in Pages CI.
shutil.copytree(root/'pages-overrides'/'trinh-chieu-marketing',site/'trinh-chieu-marketing',dirs_exist_ok=True)
def run(script):
 subprocess.run(['python3',str(root/'scripts'/script),str(site)],check=True)
run('layout_fix.py')
run('remove_extra_navigation.py')
run('slide_web_app_fix_2027.py')
run('tth_five_asset_logic_fix_2027.py')
run('app_all_pages_scroll_2027.py')
app=site/'healthcare-app'/'index.html'
out=app.read_text('utf-8')
for required in ('id="pageData"','tth-app-all-pages-scroll-2027','tth-app-catalog-full-2027','tth-embedded-vietnamese-font-2027'):
 if required not in out:raise SystemExit('Missing App release marker '+required)
print('VERCEL_APP_BUILD_OK bytes='+str(app.stat().st_size))
