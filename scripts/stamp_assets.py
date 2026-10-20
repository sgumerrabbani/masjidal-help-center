"""Keep all entry pages on the same asset revision after a content or style change."""
from pathlib import Path
import hashlib,re
ROOT=Path(__file__).resolve().parents[1]
def stamp_assets(root=ROOT):
    assets=[root/'assets/css/styles.css',*sorted((root/'assets/js').glob('*.js'))]
    digest=hashlib.sha256(b''.join(p.read_bytes() for p in assets)).hexdigest()[:12]
    for name in ['index.html','article/index.html','category/index.html','al-iqamah/index.html']:
        p=root/name;s=p.read_text(encoding='utf-8-sig')
        s=re.sub(r'(assets/(?:css/styles\.css|js/(?:data|site|pages)\.js))(?:\?v=[a-zA-Z0-9_-]+)?',lambda m:m[1]+'?v='+digest,s)
        p.write_text(s,encoding='utf-8')
    return digest
if __name__=='__main__':print('Asset revision:',stamp_assets())
