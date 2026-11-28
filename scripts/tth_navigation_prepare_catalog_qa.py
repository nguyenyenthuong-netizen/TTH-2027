from pathlib import Path
import sys
root=Path(__file__).resolve().parent
source=Path(sys.argv[1]).read_text();out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
end=source.rindex('</body>')
for filename,script in [('qa-after.html','tth_navigation_browser_inventory.js'),('scenarios.html','tth_navigation_browser_scenarios.js'),('programs.html','tth_navigation_program_scenarios.js')]:
 (out/filename).write_text(source[:end]+'<script>'+ (root/script).read_text()+'</script>'+source[end:])
(out/'after.html').write_text(source)
