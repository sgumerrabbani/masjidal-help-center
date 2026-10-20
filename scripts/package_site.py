"""Build a static-only hosting ZIP and a proposed exact-URL redirect map."""
from pathlib import Path
import json,csv,zipfile
from urllib.parse import urlparse
from stamp_assets import stamp_assets
ROOT=Path(__file__).resolve().parents[1]
stamp_assets(ROOT)
out=ROOT/'artifacts';out.mkdir(exist_ok=True)
package=out/'masjidal-help-center-upload.zip'
files=[ROOT/'index.html']
for folder in ['assets','category','article','al-iqamah']:
    files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file())
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):z.write(p,p.relative_to(ROOT).as_posix())
D=json.loads((ROOT/'assets/content-sources.json').read_text(encoding='utf-8'))
rows={'/help/':'/help-v2/'}
for t in D['topics']:
    source=t.get('source','')
    if source.startswith('https://help.masjidal.com/'):
        path=urlparse(source).path
        target=('article' if t['items']==[t['slug']] else 'category')+'/index.html?topic='+t['slug']
        rows[path]='/help-v2/'+target
for a in D['articles'].values():
    source=a.get('source','')
    if source.startswith('https://help.masjidal.com/') and a['slug'] not in ['tv-signage-player','tv-amazon-fire','tv-android']:
        rows[urlparse(source).path]='/help-v2/article/index.html?topic='+a['slug']
rows['/knowledge-base/widget/']='/help-v2/article/index.html?topic=widget'
with (ROOT/'docs/redirect-map.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f);writer.writerow(['old_path','new_path','initial_status','note'])
    for path,target in sorted(rows.items()):writer.writerow([path,target,'302','Proposed only. Review before configuring; do not redirect the site root.'])
print('Package:',package,'files:',len(files),'bytes:',package.stat().st_size)
print('Proposed exact redirects:',len(rows))
