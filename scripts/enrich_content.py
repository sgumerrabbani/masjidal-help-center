"""Apply article summaries, recover local screenshots, and add API documentation."""
import json, hashlib, requests, html
from pathlib import Path
from pypdf import PdfReader
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'assets/content-sources.json'
d = json.loads(p.read_text(encoding='utf-8'))
articles = d['articles']
descriptions = {
 'displaying-content-on-the-athan-clock': 'Share your masjid’s announcements and content with families on their Athan Clocks.',
 'taraweeh-timings': 'Set and display Taraweeh prayer times so your community can follow the Ramadan schedule.',
 'tv-guide': 'Choose a display device and get prayer timings and masjid content onto your television.',
 'widget': 'Add daily and monthly prayer timings to your masjid website with an embeddable widget.',
 'announcements-as-text': 'Publish announcements and keep your community informed through the Athan+ phone app.',
 'announcements': 'Create announcements and display them full screen, split screen, or as scrolling text.',
 'athan-time': 'Manage the Athan times shown to your community in the Athan+ phone app.',
 'content-by-screen-zones': 'Create zones to show different announcements and content on different masjid screens.',
 'countdown-screens': 'Enable a live countdown to Athan and Iqamah on your prayer displays.',
 'daily-dua': 'Add a daily dua to your slideshow to engage and inspire worshippers.',
 'daily-hadith': 'Automatically show a different Hadith each day on your masjid displays.',
 'daily-verse': 'Display a daily Quran verse as part of your masjid’s slideshow.',
 'days-countdown': 'Count down the days to an upcoming event on your masjid screens.',
 'default-icons': 'Customize the buttons and shortcuts available on your Al-Iqamah display.',
 'display-themes': 'Choose a prayer timing theme and customize the appearance of your display.',
 'displaying-events': 'Connect your Google Calendar and display upcoming masjid events.',
 'displaying-images': 'Upload images and schedule them in the slideshow on your masjid screens.',
 'donation-qr-code': 'Display QR codes for donation campaigns so worshippers can contribute from their phones.',
 'eid-countdown-days': 'Show the number of days remaining until Eid on your masjid displays.',
 'funeral-announcement': 'Enter funeral details and display an announcement for your community.',
 'get-started': 'Create your masjid account and begin setting up prayer timings and connected services.',
 'google-slides': 'Publish a Google Slides presentation and add it to your masjid slideshow.',
 'images-for-masajids': 'Use ready-made duas, reminders, and other images in your masjid slideshow.',
 'iqamah-change-notifications': 'Automatically notify worshippers when an upcoming Iqamah time changes.',
 'iqamah': 'Set and manage Iqamah times for your masjid and keep your community up to date.',
 'masjid-information': 'Set up your masjid’s information and presence in the Athan+ phone app.',
 'mobile-app-poster': 'Show an Athan+ app poster so your community can discover and download the app.',
 'prohibited-salah-time': 'Enable screens that show prohibited prayer periods and adjust with daily timings.',
 'push-notifications': 'Send push notifications to people following your masjid in the Athan+ app.',
 'qr-code-on-timing-screen': 'Add a QR code to supported timing screens for easy access from a phone.',
 'ramadan-countdown-days': 'Display a countdown to Ramadan on your masjid screens.',
 'ramadan-ready': 'Prepare your masjid’s prayer timings and display content for Ramadan.',
 'reminder-at-iqamah-time': 'Show a custom reminder automatically when it is time for Iqamah.',
 'salah': 'Configure Salah and Athan timings for your masjid.',
 'screen-size': 'Adjust the signage player’s screen size so your content fits the television correctly.',
 'settings': 'Customize zones, labels, colors, and special screens in Al-Iqamah.',
 'signage-player-setup-guide': 'Connect your Masjidal Signage Player to your TV and complete the initial setup.',
 'silence-screen': 'Reduce distractions during Jamaat with a black screen and a subtle silence reminder.',
 'split-screen': 'Display announcements and slideshow content alongside prayer timings.',
 'taraweeh-recitation-schedule': 'Share the Quran recitation schedule for Taraweeh prayers.',
 'time-sync': 'Configure automatic time synchronization on your Masjidal Signage Player.',
 'updating-the-app': 'Update Al-Iqamah to access the latest features and improvements.',
 'wordpress': 'Integrate Masjidal prayer timings into your WordPress website.'
}
for a in articles.values():
 for b in a['blocks']:
  if b['type'] == 'link' and b['text'] == 'View screenshot':
   url = b['url'].replace('https://mymasjidal.com/', 'https://help.masjidal.com/')
   r = requests.get(url, timeout=45); r.raise_for_status()
   assert r.headers.get('Content-Type', '').startswith('image/')
   dest = 'assets/images/official/' + hashlib.sha1(url.encode()).hexdigest()[:14] + Path(url).suffix
   (ROOT / dest).write_bytes(r.content); d['assets'][url] = dest
   b.clear(); b.update(type='image', src=dest, alt=a['title'] + ' screenshot')
 a['desc'] = descriptions.get(a['slug'], a.get('desc', ''))
 a['image'] = next((b['src'] for b in a['blocks'] if b['type'] == 'image'), next((t['image'] for t in d['topics'] if a['slug'] in t['items']), d['topics'][0]['image']))

def illustration(name, label, detail, symbol):
 path = f'assets/images/api-{name}.svg'
 (ROOT / path).write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400"><rect width="600" height="400" rx="20" fill="#eef4fc"/><rect x="64" y="52" width="472" height="296" rx="20" fill="white" stroke="#d4e0f3"/><rect x="88" y="76" width="424" height="42" rx="8" fill="#0047ab"/><circle cx="108" cy="97" r="5" fill="white"/><circle cx="126" cy="97" r="5" fill="white"/><circle cx="144" cy="97" r="5" fill="white"/><text x="300" y="212" text-anchor="middle" font-family="monospace" font-size="54" font-weight="bold" fill="#0047ab">{html.escape(symbol)}</text><text x="300" y="268" text-anchor="middle" font-family="Arial,sans-serif" font-size="24" font-weight="bold" fill="#1d1d1f">{html.escape(label)}</text><text x="300" y="302" text-anchor="middle" font-family="Arial,sans-serif" font-size="17" fill="#626269">{html.escape(detail)}</text></svg>''', encoding='utf-8')
 return path

def code(text):
 return '<pre><code>' + html.escape(text) + '</code></pre>'

def guide(slug, title, desc, body, symbol, detail):
 articles[slug] = dict(slug=slug, title=title, desc=desc, image=illustration(slug, title, detail, symbol), source='Masjidal-Server-Key-Guide.pdf', blocks=[dict(type='html', html=body)])

guide('server-key-get-started', 'Get your server key', 'Generate a server key in the portal and store it securely for your backend integration.', '''<p>A server key lets your backend retrieve your masjid’s prayer timings. It is a secret credential and belongs on your server.</p><h2>What your key can access</h2><p>A server key unlocks only <code>GET /timings</code>. Requests to any other Masjidal endpoint are rejected.</p><h2>Generate a key</h2><ol><li>Sign in to the Masjidal portal and open <strong>Integrations → API Keys</strong>.</li><li>On the <strong>Server Key</strong> card, choose <strong>Generate Server Key</strong>.</li><li>Copy the key and store it securely immediately. It starts with <code>msj_sk_</code> and is shown only once.</li></ol><p>Only masjid admins can generate, rotate, or disable a server key. If you lose it, open the ⋮ menu on the Server Key card and choose <strong>Rotate key</strong>.</p><div class="guide-note"><strong>Building a website or widget?</strong><p>Use a frontend key (<code>msj_pk_…</code>) in browser code. Frontend keys work only from the domains you allow. Never publish a server key in a page.</p></div>''', 'msj_sk_', 'Portal → Integrations → API Keys')
guide('timings-endpoint', 'Prayer timings endpoint', 'Use the required date parameters and API headers to retrieve prayer timings for a chosen period.', '<p>Retrieve prayer timings for a date range with the Timings endpoint.</p>' + code('GET https://api.masjidal.com/timings?start_date={start}&end_date={end}') + '''<h2>Query parameters</h2><div class="table-scroll"><table><thead><tr><th>Parameter</th><th>Required format</th></tr></thead><tbody><tr><td><code>start_date</code></td><td>First day of the range, as YYYY-MM-DD.</td></tr><tr><td><code>end_date</code></td><td>Last day, as YYYY-MM-DD. Must be on or after start_date.</td></tr></tbody></table></div><h2>Required headers</h2><div class="table-scroll"><table><thead><tr><th>Header</th><th>Value</th></tr></thead><tbody><tr><td><code>Accept</code></td><td><code>application/vnd.masjidal.com.v1+json</code></td></tr><tr><td><code>x-api-key</code></td><td>Your <code>msj_sk_…</code> key, with no quotes or Bearer prefix.</td></tr></tbody></table></div><p>Send the Accept header on every request to select version 1. A successful request returns JSON containing the prayer timings for each day in the requested range.</p><h2>Request only what you need</h2><p>A month at a time is usually sufficient. Cache the results instead of requesting the same days on every page load.</p>''', 'GET', '/timings · date range · JSON')
pdf = PdfReader(ROOT / 'assets/docs/Masjidal-Server-Key-Guide.pdf')
texts = [p.extract_text() for p in pdf.pages]
curl = texts[1].split('CURL\n', 1)[1].strip()
node = texts[2].split('NODE.JS\n', 1)[1].split('\nPHP\n')[0].strip()
php = texts[2].split('\nPHP\n', 1)[1].strip()
python = texts[3].split('PYTHON\n', 1)[1].split('\nA successful request')[0].strip()
guide('server-key-request-examples', 'Make an API request', 'Copy backend request examples for cURL, Node.js, PHP, and Python using an environment variable.', '''<p>Each example reads your key from the environment variable <code>MASJIDAL_SERVER_KEY</code> to keep it out of source code and version control. Configure this variable on your backend or hosting platform.</p><div class="guide-note"><strong>Server-side examples</strong><p>Run these on your backend. Never place the server key in browser JavaScript or a mobile app.</p></div>''' + ''.join('<h2>' + label + '</h2>' + code(example) for label, example in [('cURL', curl), ('Node.js', node), ('PHP', php), ('Python', python)]), '{ }', 'cURL · Node.js · PHP · Python')
guide('server-key-security', 'Keep your key safe', 'Store credentials securely and learn when to rotate or disable a server key.', '''<p>Treat your server key like a password. Anyone who has it can pull your masjid’s data. It is never shown again after generation, and Masjidal support cannot recover it.</p><h2>Store and use it securely</h2><ul><li>Keep it in an environment variable or your hosting platform’s secrets manager.</li><li>Call the API from your backend and pass the results to your pages.</li><li>Never put the key in HTML, browser JavaScript, a mobile app, or anything a visitor can view.</li><li>Never commit it to Git, paste it into a support ticket, or send it over chat or email.</li><li>Use a separate key for each masjid. Never share a key between organizations.</li></ul><h2>If a key is exposed</h2><p>Open <strong>Integrations → API Keys</strong>, then the ⋮ menu on the Server Key card.</p><h2>Rotate key</h2><p>Issues a replacement and invalidates the old key immediately. Have the new key ready to paste into your server configuration: anything using the old key stops working as soon as you rotate it.</p><h2>Disable key</h2><p>Switches the key off permanently without a replacement. Use this when retiring an integration. Disabling cannot be undone; generate a fresh key to start again.</p>''', '••••', 'Store · rotate · disable')
guide('server-key-troubleshooting', 'Troubleshoot API requests', 'Resolve authorization errors, unexpected responses, date ranges, and deployment configuration issues.', '''<h2>Request rejected as unauthorized</h2><p>Check that <code>x-api-key</code> is present and spelled correctly. Remove stray quotes or whitespace. Confirm the value starts with <code>msj_sk_</code> and has not been rotated or disabled.</p><h2>Unexpected response format</h2><p>Set <code>Accept</code> to exactly <code>application/vnd.masjidal.com.v1+json</code>. Some clients replace it with a default unless you set it explicitly.</p><h2>Fewer days than expected, or no days</h2><p>Both dates must use YYYY-MM-DD. Confirm <code>end_date</code> is not earlier than <code>start_date</code>.</p><h2>It worked yesterday and fails today</h2><p>Check whether someone rotated or disabled the key in the portal. Rotation takes effect immediately. Generate a new key if needed and update your server configuration.</p><h2>Works locally but fails after deployment</h2><p>Check that the environment variable holding your key is set in your hosting platform’s environment settings.</p><div class="guide-note"><strong>Need help?</strong><p>Contact Masjidal support from your portal account. Never include your server key in the message.</p></div>''', '?', 'Headers · dates · environment')
api_items = ['server-key-get-started', 'timings-endpoint', 'server-key-request-examples', 'server-key-security', 'server-key-troubleshooting']
api = dict(slug='api-server-guide', title='API Server Guide', desc='Connect your backend to Masjidal prayer timings. Generate a server key, make API requests, and manage your integration securely.', image=articles[api_items[0]]['image'], items=api_items, source='Masjidal-Server-Key-Guide.pdf')
d['topics'] = [t for t in d['topics'] if t['slug'] != 'api-server-guide'] + [api]
# Make the TV category a choice of devices, with the shared final setup steps.
tv = articles['tv-guide']; sections = {}; current = None; common = []
for block in tv['blocks']:
 text = BeautifulSoup(block.get('html', ''), 'html.parser').get_text(' ', strip=True)
 if text.startswith('Option '):
  current = text.split(':', 1)[0]; sections[current] = []
 elif text == 'Next Step':
  current = 'common'
 if current == 'common': common.append(block)
 elif current: sections[current].append(block)
tv_devices = [
 ('tv-signage-player', 'Masjidal Signage Player', 'Connect the dedicated signage player to your TV with HDMI and use WiFi or Ethernet for your masjid display.'),
 ('tv-amazon-fire', 'Amazon Fire TV or Firestick', 'Install Al-Iqamah from the Amazon Appstore and connect the display to your masjid.'),
 ('tv-android', 'Android TV or Chromecast', 'Install Al-Iqamah from Google Play on a compatible Android TV device and select your masjid.')
]
for i, (slug, title, desc) in enumerate(tv_devices, 1):
 blocks = sections.get('Option ' + str(i), []) + common
 image = next((b['src'] for b in blocks if b['type'] == 'image'), tv['image'])
 articles[slug] = dict(slug=slug, title=title, desc=desc, image=image, source=tv['source'], blocks=blocks)
next(t for t in d['topics'] if t['slug'] == 'tv-guide')['items'] = [x[0] for x in tv_devices]
for t in d['topics']:
 if not t['items']: t['items'] = [t['slug']]
for a in articles.values():
 for b in a['blocks']:
  if b['type'] == 'html':
   soup = BeautifulSoup(b['html'], 'html.parser')
   for link in soup.select('a[href]'):
    href = link['href']; target = href.split('?')[0].rstrip('/').split('/')[-1]
    if '/knowledge-base/' in href and target in articles: link['href'] = '../article/index.html?topic=' + target
   b['html'] = str(soup)
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
js = ROOT / 'assets/js/data.js'; old = js.read_text(encoding='utf-8-sig'); product = old[old.index('const productLinks'):]
js.write_text('const helpData = ' + json.dumps(d, ensure_ascii=False) + ';\nconst topics=helpData.topics;\n' + product, encoding='utf-8')
print('Updated', len(articles), 'guides and', len(d['topics']), 'categories.')
