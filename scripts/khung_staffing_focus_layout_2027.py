"""Open a spacious focus view for the staffing tables; preserve all content and state."""
from pathlib import Path
import re,sys
p=Path(sys.argv[1])/'khung-marketing'/'index.html'
s=p.read_text(encoding='utf-8')
mark='/* tth-staffing-focus-layout-2027 */'
css=r"""
/* tth-staffing-focus-layout-2027 */
.app{border-radius:9px}
.padded{padding:clamp(12px,1.45vw,20px)}
.nav{gap:5px 7px}
.wide-action{margin-left:auto;border:1px solid #8ca9d2!important;background:#fff!important;color:#0837a1!important;font-weight:750!important;white-space:nowrap;min-height:40px!important;padding:8px 13px!important}
.wide-action[aria-pressed="true"]{background:#f5f8ff!important}
.app.reader-wide{position:fixed;inset:8px;z-index:2147483000;margin:0;width:auto;height:calc(100dvh - 16px);min-width:0;overflow-y:auto;overflow-x:hidden;border:1px solid #a4bbda;border-radius:10px;box-shadow:0 0 0 300vmax rgba(10,24,49,.40),0 14px 48px rgba(10,24,49,.16)}
.app.reader-wide .nav{position:sticky;top:0;z-index:20;background:#f0f4fa}
.app.reader-wide .padded{padding:clamp(16px,2vw,30px)}
.app.reader-wide .tbl.doc-responsibility{min-width:1080px}
.app.reader-wide .scroll{overflow-x:auto}
.app.reader-wide .control{gap:11px 22px}
@media(max-width:760px){
  .wide-action{margin-left:0;flex:1 0 100%!important}
  .app.reader-wide{inset:3px;height:calc(100dvh - 6px)}
  .app.reader-wide .nav{position:relative}
  .app.reader-wide .padded{padding:12px}
  .app.reader-wide .tbl.doc-responsibility{min-width:0}
}
@media print{.app.reader-wide{position:static;inset:auto;height:auto;box-shadow:none;overflow:visible}}
"""
if mark not in s:
    pat=re.compile(r'(<script[^>]*id="tth-staffing-style"[^>]*>)(.*?)(</script>)',re.S)
    m=pat.search(s)
    if not m:raise SystemExit('Missing embedded staffing stylesheet')
    s=s[:m.start()]+m.group(1)+m.group(2)+'\n'+css+m.group(3)+s[m.end():]
    target='</nav><div class="padded">'
    if s.count(target)!=1:raise SystemExit('Staffing nav anchor not unique')
    s=s.replace(target,'<button type="button" class="wide-action" data-wide="toggle" aria-pressed="false" title="Mở rộng bảng, Esc để đóng">Mở rộng bảng</button>'+target,1)
    target="if(b.dataset.panel)go(b.dataset.panel);"
    if s.count(target)!=1:raise SystemExit('Event handler anchor not unique')
    s=s.replace(target,"if(b.dataset.wide){const app=root.querySelector('.app'),wide=app.classList.toggle('reader-wide');b.setAttribute('aria-pressed',String(wide));b.textContent=wide?'Thu gọn cửa sổ':'Mở rộng bảng';return;}\n "+target,1)
    target="root.addEventListener('click',ev=>{"
    if s.count(target)!=1:raise SystemExit('Click listener anchor not unique')
    s=s.replace(target,"root.addEventListener('keydown',ev=>{if(ev.key==='Escape'){const app=root.querySelector('.app');if(app.classList.contains('reader-wide')){app.classList.remove('reader-wide');const b=root.querySelector('[data-wide]');if(b){b.setAttribute('aria-pressed','false');b.textContent='Mở rộng bảng';b.focus();}}}});\n"+target,1)
if s.count(mark)!=1 or s.count('data-wide="toggle"')!=1:raise SystemExit('Focus-mode patch failed')
p.write_text(s,encoding='utf-8')
print('PASS: spacious focus view with reversible Esc, responsive table, unchanged model data')
