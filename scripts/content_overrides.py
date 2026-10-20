"""Maintain authored guides when refreshing imported legacy content."""
from pathlib import Path
from bs4 import BeautifulSoup

def apply_content_overrides(data, root):
    import re
    from urllib.parse import urlparse, parse_qs
    for article in data['articles'].values():
        for block in article['blocks']:
            if block['type'] != 'html':
                continue
            fragment = BeautifulSoup(block['html'], 'html.parser')
            for link in fragment.select('a[href]'):
                if link['href'].rstrip('/') in ['https://portal.masjidal.com/login','https://portal.masjidal.com/registration','https://portal.masjidal.com/site/signup']:
                    link['href'] = 'https://portal.masjidal.com/'
                url = urlparse(link['href'])
                slug = url.path.strip('/').split('/')[-1]
                if url.hostname in ['help.masjidal.com', 'mymasjidal.com', 'masjidal.com']:
                    if any(key in parse_qs(url.query) for key in ['add_to_cart', 'add-to-cart']):
                        link['href'] = 'https://mymasjidal.ca/pages/pricing-plan'
                        link.string = 'View plans and trial availability'
                    elif '/knowledge-base/' in url.path and '/category/' not in url.path and slug in data['articles']:
                        link['href'] = '../article/index.html?topic=' + slug
                    elif '/knowledge-base/category/' in url.path and any(t['slug'] == slug for t in data['topics']):
                        link['href'] = '../category/index.html?topic=' + slug
                    elif url.path.rstrip('/') == '/in-masjid-displays':
                        link['href'] = '../category/index.html?topic=in-masjid-displays'
                    elif url.path.rstrip('/') == '/app_masjid':
                        link['href'] = '../category/index.html?topic=athan-phone-app'
                if link['href'] in ['http://masjidal.com/site/login', 'https://masjidal.com/site/login']:
                    link['href'] = 'https://portal.masjidal.com/'
                if link['href'] in ['http://masjidal.com/site/signup', 'https://masjidal.com/site/signup']:
                    link['href'] = 'https://portal.masjidal.com/'
            if article['slug'] == 'displaying-content-on-the-athan-clock':
                for paragraph in list(fragment.find_all('p')):
                    if paragraph.get_text(' ', strip=True).upper() == 'COMING SOON': paragraph.decompose()
            if article['slug'] == 'updating-the-app':
                for paragraph in fragment.find_all('p'):
                    version = re.fullmatch(r'CURRENT VERSION[ :]*(\d+)', paragraph.get_text(' ', strip=True), re.IGNORECASE)
                    if version:
                        paragraph.clear(); paragraph['class'] = 'guide-note'
                        paragraph.append('Example version: ' + version[1] + '. Check the update available for your device rather than treating a version number in this guide or its screenshots as the latest release.')
            for heading in fragment.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = heading.get_text(' ', strip=True)
                if len(text) > 120:
                    heading.name = 'p'
                if text == 'Fine Tuning':
                    heading.name = 'p'; heading['class'] = 'article-kicker'
            for paragraph in list(fragment.find_all('p')):
                text = paragraph.get_text(' ', strip=True)
                if len(text) < 85 and (re.match(r'^(?:STEP|Step|Option) [1-9]', text) or text in ['Quick Setup Guide', 'Next Step', 'IQAMAH TIME MANAGEMENT', 'ATHAN TIME (Exception Cases)', 'CONFIGURING WORDPRESS PLUGIN', 'Editing/Deleting Times']):
                    paragraph.name = 'h2'
                first = paragraph.find(['b', 'strong'])
                if first and paragraph.name == 'p' and paragraph.get_text(strip=True).startswith(first.get_text(strip=True)) and re.match(r'^Step [1-9]', first.get_text()):
                    heading = fragment.new_tag('h2'); heading.string = first.get_text(' ', strip=True)
                    paragraph.insert_before(heading); first.decompose()
            block['html'] = str(fragment)
    for slug, description in {
        'slideshow': 'Choose, schedule, and organize slideshow content on your masjid screens.',
        'sponsor-an-iftar-campaign': 'Set up an iftar sponsorship campaign and manage sponsorships for your community.',
        'zakat-ul-fitr-campaign': 'Create and manage a Zakat ul-Fitr collection campaign for your masjid.'
    }.items():
        if slug in data['articles']: data['articles'][slug]['desc'] = description
    screen = data['articles']['screen-size']
    screenshots = [b for b in screen['blocks'] if b['type'] == 'image']
    if len(screenshots) == 5:
        instructions = [
            ('Open Settings', 'Click the Settings icon on the screen.'),
            ('Choose Display', 'Click the DISPLAY option.'),
            ('Choose HDMI', 'Click the HDMI option.'),
            ('Open Screen Zoom', 'Click the SCREEN ZOOM option.'),
            ('Fit the picture to your TV', 'Click the arrows to adjust the screen size. A red border should be visible at the top, bottom, left, and right edges.')
        ]
        screen['blocks'] = [{'type':'html', 'html':'<p>If the top, bottom, left, or right of your masjid TV display is cut off, adjust the signage player screen size to fit the TV.</p>'}]
        for i, ((title, text), image) in enumerate(zip(instructions, screenshots), 1):
            screen['blocks'].extend([{'type':'html', 'html':f'<h2>{i}. {title}</h2><p>{text}</p>'}, image])
    legacy = data['articles']['wordpress']
    legacy['title'] = 'WordPress Plugin (Legacy)'
    legacy['desc'] = 'Reference for the older Masjidal WordPress plugin and its shortcodes. For new installations, use Website Widgets.'
    note = {'type':'html', 'html':'<div class="guide-note"><strong>Using the current widget system?</strong><p>This guide describes the older WordPress plugin, Masjid ID settings, and shortcodes. For new installations, follow the <a href="../article/index.html?topic=widget">Website Widgets guide</a>, which uses Integrations &rarr; Widgets and a frontend key. The plugin instructions below are retained for existing installations.</p></div>'}
    if not any('This guide describes the older WordPress plugin' in b.get('html','') for b in legacy['blocks']):
        legacy['blocks'].insert(0, note)
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
    from PIL import Image
    for guide in data['articles'].values():
        for block in guide['blocks']:
            if block['type'] == 'image':
                with Image.open(root / block['src']) as image:
                    block['width'], block['height'] = image.size

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
    from stamp_assets import stamp_assets
    stamp_assets(root)
    print('Updated authored widget guide and category metadata.')
