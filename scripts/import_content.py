"""Import official Masjidal help copy and assets. Run: python scripts/import_content.py"""
import requests,re,json,hashlib,concurrent.futures
from pathlib import Path
from urllib.parse import urljoin,urlparse
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; BASE='https://help.masjidal.com'
def fetch(u):
 r=requests.get(u,timeout=45);r.raise_for_status();return BeautifulSoup(r.content,'html.parser')
def options(s):
 m=re.search(r'et_link_options_data = (.*?);',str(s));return json.loads(m[1]) if m else []
def slug(u):return urlparse(u).path.strip('/').split('/')[-1]
assets={}
def asset(u):
 u=urljoin(BASE,u)
 if u in assets:return assets[u]
 ext=Path(urlparse(u).path).suffix or '.png'; dest='assets/images/official/'+hashlib.sha1(u.encode()).hexdigest()[:14]+ext
 p=ROOT/dest;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():
  r=requests.get(u,timeout=45);r.raise_for_status();p.write_bytes(r.content)
 assets[u]=dest;return dest
home=fetch(BASE+'/help/'); groups=[]; queue=set()
for op in options(home):
 c=home.select_one('.'+op['class']); h=c.find('h4'); u=urljoin(BASE,op['url'])
 groups.append(dict(slug=slug(u),title=h.get_text(' ',strip=True),desc=c.select_one('.et_pb_blurb_description').get_text(' ',strip=True).replace('\ufffd','’'),image=asset(c.find('img')['src']),source=u,items=[]));queue.add(u)
articles={}; seen=set()
while queue:
 batch=sorted(queue-seen);queue=set()
 if not batch:break
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  results=list(pool.map(lambda u:(u,fetch(u)),batch))
 for u,s in results:
  seen.add(u); body=s.select_one('#eckb-article-content-body')
  if body:
   title=s.select_one('.eckb-article-title').get_text(' ',strip=True); blocks=[]
   for el in body.select('h1,h2,h3,h4,h5,p,ul,ol,img,iframe'):
    if el.find_parent(['p','ul','ol']) or el.find(['input','select','textarea','button']):continue
    if el.name=='img':
     src=el.get('data-lazy-src') or el.get('src');
     if src and not src.startswith('data:'):
      try: blocks.append({'type':'image','src':asset(src),'alt':el.get('alt') or title})
      except Exception: blocks.append({'type':'link','url':urljoin(u,src),'text':'View screenshot'})
    elif el.name=='iframe':blocks.append({'type':'link','url':urljoin(u,el.get('data-src') or el.get('src','')),'text':'Watch the official video or open embedded content'})
    elif el.get_text(' ',strip=True):
     for a in el.select('a[href]'):a['href']=urljoin(u,a['href'])
     for tag in [el,*el.find_all()]:
      for attr in list(tag.attrs):
       if attr not in ['href','title']:del tag[attr]
     if el.name.startswith('h'):el.name='h2'
     blocks.append({'type':'html','html':str(el)})
   if slug(u)=='widget':blocks=blocks[:6]+[{'type':'link','url':u,'text':'Open the official widget generator to customize and generate embed code'}]
   articles[slug(u)]=dict(slug=slug(u),title=title,source=u,blocks=blocks)
  else:
   links=[urljoin(u,x['url']) for x in options(s)]
   links += [urljoin(u,a['href']) for a in s.select('a[href]') if '/knowledge-base/' in a['href'] and '/category/' not in a['href']]
   links=[x.rstrip('/')+'/' for x in links if urlparse(x).hostname=='help.masjidal.com' and '/knowledge-base/' in x and slug(x)!='knowledge-base']
   queue.update(links)
   for g in groups:
    if g['source']==u:g['items']=list(dict.fromkeys(slug(x) for x in links))
 print('Imported',len(articles),'articles; pending',len(queue-seen),flush=True)
brand=fetch('https://mymasjidal.ca/')
logo=brand.select_one('.header__heading-logo'); asset('https:'+logo['src'].replace('_60x','_300x'))
logo_path=assets['https:'+logo['src'].replace('_60x','_300x')]
font=re.search(r'//mymasjidal.ca/cdn/fonts/poppins/[^"\s)]+\.woff2',str(brand))[0]
p=ROOT/'assets/fonts/poppins-600.woff2';p.parent.mkdir(exist_ok=True);p.write_bytes(requests.get('https:'+font).content)
# Preserve brand product navigation from the starter.
old=(ROOT/'assets/js/data.js').read_text(encoding='utf-8');products=old[old.index('const productLinks'):]
data={'topics':groups,'articles':articles,'logo':logo_path,'imported':'2026-10-07','assets':assets}
(ROOT/'assets/js/data.js').write_text('const helpData = '+json.dumps(data,ensure_ascii=False)+';\nconst topics=helpData.topics;\n'+products,encoding='utf-8')
(ROOT/'assets/content-sources.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
import runpy
runpy.run_path(str(ROOT/'scripts/enrich_content.py'),run_name='__main__')
