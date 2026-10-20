"""Full local UI audit. Does not send mail, dial phones, sign in, or make purchases."""
import argparse,json,re,time
from pathlib import Path
from urllib.parse import urlparse,parse_qs,unquote
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--base',default='http://localhost:4173/');parser.add_argument('--quick',action='store_true');args=parser.parse_args()
BASE=args.base.rstrip('/')+'/'
OUT=ROOT/'artifacts/full-audit';OUT.mkdir(parents=True,exist_ok=True)
D=json.loads((ROOT/'assets/content-sources.json').read_text(encoding='utf-8'))
paths=['index.html','al-iqamah/index.html','category/index.html?q=prayer']+['category/index.html?topic='+t['slug'] for t in D['topics']]+['article/index.html?topic='+s for s in D['articles']]
results=[];visited=set();hrefs=set();errors=[];bad_responses=[];started=time.monotonic()

def assert_local_link(href):
    u=urlparse(href);base=urlparse(BASE)
    if u.netloc!=base.netloc:return
    path=unquote(u.path.removeprefix(base.path))
    assert (ROOT/(path or 'index.html')).is_file(),('Missing local destination',href)
    q=parse_qs(u.query)
    if path=='article/index.html':assert q.get('topic',[''])[0] in D['articles'],('Unknown guide',href)
    if path=='category/index.html' and 'topic' in q:assert q['topic'][0] in {t['slug'] for t in D['topics']},('Unknown category',href)

def ready(page):
    page.wait_for_selector('main h1')
    page.locator('img').evaluate_all("imgs=>imgs.forEach(i=>i.loading='eager')")
    page.wait_for_function('[...document.images].every(i=>i.complete)')
    page.evaluate('document.fonts.ready')

with sync_playwright() as p:
 for engine,widths in [('chromium',[1440,1280,1024,900,768,390,320]),('firefox',[1440,390])]:
    if args.quick:widths=[390]
    browser=getattr(p,engine).launch()
    context=browser.new_context(permissions=['clipboard-read','clipboard-write'] if engine=='chromium' else [])
    page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('response',lambda r:bad_responses.append({'url':r.url,'status':r.status}) if r.status>=400 and r.url.startswith(BASE) else None)
    for width in widths:
      page.set_viewport_size({'width':width,'height':900})
      for path in paths:
        response=page.goto(BASE+path);assert response.status in [200,304],(path,response.status)
        ready(page);visited.add(path)
        facts=page.evaluate('''() => ({
            overflow:document.documentElement.scrollWidth>innerWidth,
            broken:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),
            title:document.title,
            bodyFont:getComputedStyle(document.body).fontFamily,
            fontReady:document.fonts.check('16px Poppins')&&document.fonts.check('600 23px Poppins'),
            badFonts:[...document.querySelectorAll('.article-body p,.article-body li,.article-body h2,.article-body h3,.article-body span,.topic-body p')].filter(e=>!e.closest('pre,code,kbd,samp')&&!getComputedStyle(e).fontFamily.includes('Poppins')).map(e=>e.tagName),
            badHeadings:[...document.querySelectorAll('.article-body h1,.article-body h2,.article-body h3')].filter(e=>e.textContent.trim().length>120).map(e=>e.textContent),
            links:[...document.querySelectorAll('a[href]')].map(a=>a.href)
        })''')
        assert not facts['overflow'],(engine,width,path,'horizontal overflow')
        assert not facts['broken'],(path,facts['broken'])
        assert facts['fontReady'] and 'Poppins' in facts['bodyFont'],(path,'font not loaded')
        assert not facts['badFonts'],(path,'inconsistent fonts',facts['badFonts'])
        assert not facts['badHeadings'],(path,'paragraph styled as heading',facts['badHeadings'])
        assert page.locator('main h1').count()==1,path
        assert page.locator('.article-sidebar,.source-link').count()==0,path
        for href in facts['links']:assert_local_link(href);hrefs.add(href)
        for card in page.locator('.topic-card').all():
            assert card.locator('img').count()==1,path
            assert card.locator('.topic-body p').inner_text().strip(),path
        if path=='index.html':assert page.locator('.topic-card h3').last.inner_text()=='All Other Topics'
        if 'article/' in path:
            assert page.locator('.article-body').inner_text().strip(),path
            assert page.locator('.back-to-guides').count()==1,path
            assert page.locator('.article-body script,.article-body masjidal-widget').count()==0,path
            slug=parse_qs(urlparse(page.url).query)['topic'][0]
            assert page.locator('.article-body img').count()==sum(b['type']=='image' for b in D['articles'][slug]['blocks']),path
        if engine=='chromium' and width in [1440,390]:
            key=re.sub(r'[^a-zA-Z0-9_-]','-',path)
            page.evaluate("window.scrollTo({top:0,left:0,behavior:'instant'})")
            page.screenshot(path=str(OUT/f'{width}-{key}.png'),full_page=True)
        if engine=='chromium' and width==1440 and path.startswith('article/'):
            original=page.url;page.locator('.back-to-guides').click();page.wait_for_selector('.topic-grid')
            assert '/category/' in page.url,path
            page.go_back();page.wait_for_selector('main h1');assert page.url==original,path
            page.go_forward();page.wait_for_selector('.topic-grid');assert '/category/' in page.url,path
        results.append({'engine':engine,'width':width,'path':path,'status':'pass'})
      print('Passed',engine,width,len(paths),'routes',flush=True)
    # Click every category tile and verify contextual breadcrumb/back navigation.
    page.set_viewport_size({'width':390,'height':900})
    for group in D['topics']:
        category=BASE+'category/index.html?topic='+group['slug']
        page.goto(category);page.wait_for_selector('.topic-card');count=page.locator('.topic-card').count();assert count==len(group['items'])
        print('Checking category navigation',engine,group['slug'],flush=True)
        for index,slug in enumerate(group['items']):
            page.goto(category);page.locator('.topic-card').nth(index).click();page.wait_for_selector('.article-body')
            assert parse_qs(urlparse(page.url).query)['topic'][0]==slug
            assert page.locator('.breadcrumbs a').last.inner_text()==group['title']
            page.locator('.back-to-guides').click();page.wait_for_url(category);page.wait_for_selector('.topic-grid');assert page.url==category
    # Shared controls and history.
    page.goto(BASE);page.get_by_role('button',name='Menu').click();assert page.locator('#navigation').is_visible()
    page.locator('.dropdown summary').click();assert page.locator('.dropdown').get_attribute('open') is not None
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.keyboard.press('Escape');assert not page.locator('#navigation').is_visible()
    page.locator('.search-input').fill('screen size');page.locator('.search-submit').click();page.wait_for_selector('.topic-card')
    assert 'Screen Size' in page.locator('#searchResults').inner_text()
    page.locator('.search-input').fill('zzzznoresult');assert page.locator('.empty').count()==1
    page.goto(BASE+'article/index.html?topic=not-a-guide');assert page.get_by_role('heading',name='Guide not found').is_visible()
    print('Checking all email controls',engine,flush=True)
    for path in paths:
        page.goto(BASE+path);page.wait_for_selector('main h1')
        email_links=page.locator('a[href^="mailto:"]:not([data-email-launch]):visible')
        for email_index in range(email_links.count()):
            link=email_links.nth(email_index);recipient=unquote(link.get_attribute('href')[7:].split('?')[0]);link.click()
            assert page.locator('#emailOptions').is_visible()
            assert page.locator('#emailAddress').input_value()==recipient
            assert parse_qs(urlparse(page.locator('#emailGmail').get_attribute('href')).query)['to'][0]==recipient
            assert parse_qs(urlparse(page.locator('#emailOutlook').get_attribute('href')).query)['to'][0]==recipient
            page.keyboard.press('Escape');assert not page.locator('#emailOptions').is_visible()
    browser.close()
assert not errors,errors
assert not bad_responses,bad_responses
report={'routes':len(paths),'engines':['chromium','firefox'],'page_cases':len(results),'unique_local_routes_checked':len(visited),'unique_links_checked':len(hrefs),'elapsed_seconds':round(time.monotonic()-started),'results':results,'runtime_errors':errors,'failed_http_resources':bad_responses}
(OUT/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Full browser audit passed:',len(results),'page cases;',len(hrefs),'unique links;',round(time.monotonic()-started),'seconds.')
