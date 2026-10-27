"""Check published WordPress KB coverage independently of directory navigation."""
import json
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree
import requests

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'assets/content-sources.json').read_text(encoding='utf-8'))
response = requests.get('https://help.masjidal.com/wp-sitemap-posts-epkb_post_type_1-1.xml', timeout=45)
response.raise_for_status()
urls = [node.text for node in ElementTree.fromstring(response.content).iter() if node.tag.endswith('}loc')]
assert urls, 'Published article sitemap is empty'
missing = [url for url in urls if urlparse(url).path.strip('/').split('/')[-1] not in data['articles']]
assigned = {slug for topic in data['topics'] for slug in topic['items']}
unlisted = sorted(set(data['articles']) - assigned)
assert not missing, ('Published articles missing from the site', missing)
assert not unlisted, ('Articles inaccessible through categories', unlisted)
print(f"Inventory passed: all {len(urls)} published WordPress articles represented; all {len(data['articles'])} local guides assigned to categories.")
