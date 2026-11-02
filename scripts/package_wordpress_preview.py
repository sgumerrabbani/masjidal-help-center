"""Wrap the verified static package for WordPress Admin > Plugins > Upload Plugin.

No WordPress files, database, hosting settings, or remote sites are changed.
"""
from pathlib import Path
import runpy
import zipfile

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / 'scripts/package_site.py'), run_name='__main__')
prefix = 'masjidal-help-center-preview/'
target = ROOT / 'artifacts/masjidal-help-center-wordpress-preview.zip'
with zipfile.ZipFile(ROOT / 'artifacts/masjidal-help-center-upload.zip') as source:
    assert source.testzip() is None
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as output:
        output.write(ROOT / 'wordpress/masjidal-help-center-preview.php', prefix + 'masjidal-help-center-preview.php')
        for entry in source.infolist():
            path = Path(entry.filename)
            assert not path.is_absolute() and '..' not in path.parts
            output.writestr(prefix + 'site/' + entry.filename, source.read(entry.filename))
with zipfile.ZipFile(target) as packaged:
    assert packaged.testzip() is None
    assert prefix + 'site/index.html' in packaged.namelist()
print('WordPress preview plugin:', target, 'bytes:', target.stat().st_size)
