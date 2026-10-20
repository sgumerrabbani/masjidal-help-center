import json,re,requests,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
D=json.loads(Path('assets/content-sources.json').read_text(encoding='utf-8'));urls=set()
for a in D['articles'].values():
 for b in a['blocks']:
  if b['type']=='link':urls.add(b['url'])
  for x in BeautifulSoup(b.get('html',''),'html.parser').select('a[href]'):
   if x['href'].startswith('http'):urls.add(x['href'])
for name in ['site.js','data.js']:
 s=Path('assets/js',name).read_text(encoding='utf-8');
 if name=='data.js':s=s[s.index('const productLinks'):]
 urls.update(re.findall(r'https?://[^\s\"\'<>]+',s))
urls={u for u in urls if not any(w in u for w in ['YOUR_','widgets.masjidal.com','outlook.live.com','mail.google.com'])}
def check(url):
 try:
  if any(part in url.lower() for part in ['add_to_cart','add-to-cart','logout','delete','unsubscribe']):return dict(url=url,status='not-executed-state-changing-link')
  r=requests.get(url,timeout=25,stream=True,allow_redirects=True);row=dict(url=url,status=r.status_code,final_url=r.url);r.close();return row
 except Exception as e:return dict(url=url,status='unverified',error=str(e)[:200])
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as p:results=list(p.map(check,sorted(urls)))
Path('tmp/content-audit/external-links.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for row in results:print(row['status'],row['url'],('-> '+row['final_url']) if row.get('final_url')!=row['url'] else '')
print('TOTAL',len(results))
