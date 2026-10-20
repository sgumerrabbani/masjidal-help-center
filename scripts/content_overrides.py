"""Maintain authored guides when refreshing imported legacy content."""
from pathlib import Path
from bs4 import BeautifulSoup

def apply_content_overrides(data, root):
    data['topics'].sort(key=lambda topic: topic['slug'] == 'general')
    source = root / 'assets/content/widget.html'
    soup = BeautifulSoup(source.read_text(encoding='utf-8-sig'), 'html.parser')
    blocks = []
    for element in soup.contents:
        if not getattr(element, 'name', None):
            continue
        image = element.find('img') if element.name == 'figure' else None
        if image:
            blocks.append({'type': 'image', 'src': image['src'].removeprefix('../'), 'alt': image['alt']})
        else:
            blocks.append({'type': 'html', 'html': str(element)})
    article = data['articles']['widget']
    article.update(title='Website Widgets', desc='Customize, publish, and embed prayer times and announcements from Integrations → Widgets in the Masjidal portal.', image='assets/images/widgets/editor-overview.png', blocks=blocks, updated='2026-10-20', source='Masjidal portal widget editor and installation guide, supplied screenshots')
    for topic in data['topics']:
        if topic['slug'] == 'widget':
            topic['desc'] = 'Add prayer times and announcements to your website using customizable Masjidal widgets.'
            topic['image'] = article['image']

if __name__ == '__main__':
    import json
    root = Path(__file__).resolve().parents[1]
    manifest = root / 'assets/content-sources.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    apply_content_overrides(data, root)
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    target = root / 'assets/js/data.js'
    old = target.read_text(encoding='utf-8-sig')
    products = old[old.index('const productLinks'):]
    target.write_text('const helpData = ' + json.dumps(data, ensure_ascii=False) + ';\nconst topics=helpData.topics;\n' + products, encoding='utf-8')
    print('Updated authored widget guide and category metadata.')
