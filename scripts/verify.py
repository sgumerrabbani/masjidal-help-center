import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path('artifacts');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
 browser=p.chromium.launch();page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 data=json.loads(Path('assets/content-sources.json').read_text(encoding='utf-8'))
 paths=['index.html','al-iqamah/index.html','category/index.html?q=prayer']+['category/index.html?topic='+t['slug'] for t in data['topics']]+['article/index.html?topic='+s for s in data['articles']]
 for width in [1440,768,390,320]:
  page.set_viewport_size({'width':width,'height':900})
  for path in paths:
   page.goto('http://localhost:4173/'+path)
   page.locator('img').evaluate_all("imgs => imgs.forEach(i => i.loading = 'eager')")
   page.wait_for_function("[...document.images].every(i => i.complete)")
   issue=page.evaluate('({overflow:document.documentElement.scrollWidth>innerWidth,broken:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)})')
   assert not issue['overflow'],(width,path,'overflow')
   assert not issue['broken'],(width,path,issue['broken'])
   assert page.locator('.article-sidebar,.source-link').count()==0
   assert 'View screenshot' not in page.locator('main').inner_text()
   assert 'View the official setup guide and instructions.' not in page.locator('main').inner_text()
   for card in page.locator('.topic-card').all():
    assert card.locator('img').count()==1
    assert card.locator('.topic-body p').inner_text().strip()
   assert page.evaluate("[...document.images].every(i=>new URL(i.src).origin===location.origin)")
   if path=='index.html':page.screenshot(path=str(OUT/f'home-{width}.png'),full_page=True)
   if width in [1440,390] and path in ['category/index.html?topic=api-server-guide','category/index.html?topic=tv-guide','article/index.html?topic=server-key-request-examples','article/index.html?topic=prohibited-salah-time']:
    page.screenshot(path=str(OUT/(path.split('=')[-1]+f'-{width}.png')),full_page=True)
  print('Passed all pages at',width,flush=True)
 page.goto('http://localhost:4173/index.html');page.get_by_role('button',name='Menu').click();assert page.locator('#navigation').is_visible()
 page.set_viewport_size({'width':1440,'height':900});page.goto('http://localhost:4173/index.html');page.locator('.search-input').fill('iqamah');page.locator('.search-submit').click();page.locator('img').evaluate_all("imgs => imgs.forEach(i => i.loading = 'eager')");page.wait_for_load_state('networkidle');assert page.locator('.topic-card').count()>0
 page.locator('.search-input').fill('zzzzzzzz');assert page.locator('.empty').count()==1
 assert not errors,errors
 print('Menu, search, images, runtime and overflow checks passed.')
 browser.close()
