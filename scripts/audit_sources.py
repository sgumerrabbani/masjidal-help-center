"""Audit and recover all published source guides; snapshots stay in ignored tmp/."""
import json,hashlib,requests,concurrent.futures,collections,argparse
from pathlib import Path
from bs4 import BeautifulSoup
from article_extract import extract_article,tokens
from urllib.parse import urlparse, urljoin
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--refresh',action='store_true');args=parser.parse_args()
D=json.loads((ROOT/'assets/content-sources.json').read_text(encoding='utf-8'))
OUT=ROOT/'tmp/content-audit';OUT.mkdir(parents=True,exist_ok=True)
SOURCES=sorted({a['source'] for a in D['articles'].values() if a['source'].startswith('http')})
def fetch(url):
    name=hashlib.sha1(url.encode()).hexdigest()[:14]+'.html';path=OUT/name
    if args.refresh or not path.exists():
        r=requests.get(url,timeout=45);r.raise_for_status();path.write_bytes(r.content)
    return url,BeautifulSoup(path.read_bytes(),'html.parser')
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:pages=dict(pool.map(fetch,SOURCES))
# Follow linked help articles too; category-only crawling missed these guides.
while True:
    known_slugs = {a['slug'] for a in D['articles'].values()}
    new_urls = set()
    for origin, page in pages.items():
        body = page.select_one('#eckb-article-content-body')
        for link in body.select('a[href]') if body else []:
            target = urlparse(urljoin(origin, link['href']))
            slug = target.path.strip('/').split('/')[-1]
            if target.hostname in ['help.masjidal.com','mymasjidal.com','masjidal.com'] and '/knowledge-base/' in target.path and '/category/' not in target.path and slug and slug not in known_slugs and slug != 'knowledge-base':
                new_urls.add('https://help.masjidal.com' + target.path.rstrip('/') + '/')
    if not new_urls:break
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:extra=dict(pool.map(fetch,sorted(new_urls)))
    for url,page in extra.items():
        body=page.select_one('#eckb-article-content-body')
        if body is None:continue
        slug=urlparse(url).path.strip('/').split('/')[-1]
        title=page.select_one('.eckb-article-title').get_text(' ',strip=True)
        D['articles'][slug]={'slug':slug,'title':title,'desc':'','source':url,'blocks':[]}
        next(t for t in D['topics'] if t['slug']=='general')['items'].append(slug)
    if not extra:break
    pages.update(extra)
def asset(url):
    candidate=url.replace('https://mymasjidal.com/wp-content/','https://help.masjidal.com/wp-content/')
    for key in [candidate,url]:
        known=D['assets'].get(key)
        if known and (ROOT/known).exists():return known
    r=requests.get(candidate,timeout=45);r.raise_for_status()
    assert r.headers.get('content-type','').startswith('image/'),candidate
    dest='assets/images/official/'+hashlib.sha1(candidate.encode()).hexdigest()[:14]+Path(candidate.split('?')[0]).suffix
    (ROOT/dest).write_bytes(r.content);D['assets'][candidate]=dest;return dest
report=[];recovered=0
for url,soup in pages.items():
    body=soup.select_one('#eckb-article-content-body')
    assert body is not None,url
    blocks=extract_article(body,url,asset)
    expected_images=sum(bool(i.get('data-lazy-src') or i.get('data-src') or (i.get('src') and not i['src'].startswith('data:'))) for i in body.select('img'))
    assert sum(b['type']=='image' for b in blocks)==expected_images,(url,'Screenshot count differs from source',expected_images)
    for tag in list(body.select('script,style,noscript,form,input,select,textarea,button')):tag.decompose()
    source_tokens=collections.Counter(tokens(body.get_text(' ',strip=True)))
    new_text=' '.join(BeautifulSoup(b.get('html',''),'html.parser').get_text(' ',strip=True) for b in blocks)
    missing=source_tokens-collections.Counter(tokens(new_text))
    assert not missing,(url,missing)
    # The TV overview is also the source of three derived device guides.
    article=next((a for a in D['articles'].values() if a['source']==url and a['slug'] not in ['tv-signage-player','tv-amazon-fire','tv-android']),None)
    assert article,url
    old_text=' '.join(BeautifulSoup(b.get('html',''),'html.parser').get_text(' ',strip=True) for b in article['blocks'])
    omitted=source_tokens-collections.Counter(tokens(old_text));recovered+=sum(omitted.values())
    article['blocks']=blocks
    if not article.get('desc'):
        article['desc']=next((BeautifulSoup(b['html'],'html.parser').get_text(' ',strip=True) for b in blocks if b['type']=='html' and BeautifulSoup(b['html'],'html.parser').find('p')),title if 'title' in globals() else article['title'])[:190]
        article['image']=next((b['src'] for b in blocks if b['type']=='image'),D['topics'][0]['image'])
    report.append({'slug':article['slug'],'source':url,'source_word_tokens':sum(source_tokens.values()),'missing_before':sum(omitted.values()),'missing_after':0,'image_count':sum(b['type']=='image' for b in blocks)})
    print(article['slug'],'recovered word tokens',sum(omitted.values()),flush=True)
(ROOT/'assets/content-sources.json').write_text(json.dumps(D,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Source audit complete:',len(report),'sources;',recovered,'omitted word tokens recovered. Apply enrichment next.')
