"""Extract complete help copy without retaining source typography or dropping bare text."""
from bs4 import BeautifulSoup, Tag, NavigableString, Comment
from urllib.parse import urljoin
import re,json,html
BLOCKS={'p','h1','h2','h3','h4','h5','h6','ul','ol','pre','table','blockquote'}
CONTAINERS={'div','section','article','figure','figcaption','details','summary','center'}
IGNORE={'script','style','noscript','form','input','select','textarea','button'}

def extract_article(body, source, download):
    # Divi sometimes stores button destinations outside the article markup.
    document = body.find_parent('html')
    match = re.search(r'et_link_options_data\s*=\s*(\[.*?\]);', str(document)) if document else None
    for option in json.loads(match[1]) if match else []:
        module = body.select_one('.' + option['class'])
        if module is None: continue
        label = module.select_one('.et_pb_text_inner') or module
        if label.find('a'): continue
        paragraph = label.find('p', recursive=False)
        target = paragraph if paragraph is not None else label
        link = BeautifulSoup('', 'html.parser').new_tag('a', href=urljoin(source, option['url']))
        for child in list(target.contents): link.append(child.extract())
        target.append(link)
    blocks=[]
    def image(node):
        src=node.get('data-lazy-src') or node.get('data-src') or node.get('src')
        if src and not src.startswith('data:'):
            blocks.append({'type':'image','src':download(urljoin(source,src)),'alt':node.get('alt') or node.get('title') or 'Guide screenshot'})
    def clean(fragment):
        s=BeautifulSoup(str(fragment),'html.parser')
        for tag in list(s.find_all(IGNORE)):
            tag.decompose()
        for tag in s.find_all():
            for attr in list(tag.attrs):
                if attr not in ['href','rowspan','colspan','start']:del tag[attr]
            if tag.name=='a' and tag.get('href'):
                tag['href']=urljoin(source,tag['href'])
        for tag in list(s.find_all(['span','font'])):tag.unwrap()
        return s
    def emit(node):
        # Keep images in paragraphs as real images in their original position.
        if node.find(['img','iframe','video']):
            for child in node.children:walk(child)
            return
        fragment=clean(node)
        root=fragment.find()
        if not root or not root.get_text(' ',strip=True):return
        if root.name.startswith('h') and len(root.name)==2:
            text=root.get_text(' ',strip=True)
            root.name='p' if len(text)>120 else ('h2' if root.name in ['h1','h2'] else 'h3')
        blocks.append({'type':'html','html':str(fragment)})
    def flush(run):
        if run:
            fragment=clean('<p>'+''.join(str(n) if isinstance(n,Tag) else html.escape(str(n)) for n in run)+'</p>')
            if fragment.get_text(' ',strip=True):blocks.append({'type':'html','html':str(fragment)})
            run.clear()
    def walk(node):
        if isinstance(node,Comment):return
        if isinstance(node,NavigableString):
            if str(node).strip():blocks.append({'type':'html','html':str(clean('<p>'+html.escape(str(node))+'</p>'))})
            return
        if not isinstance(node,Tag) or node.name in IGNORE:return
        if node.name=='img':image(node);return
        if node.name in ['iframe','video']:
            url=node.get('data-src') or node.get('src')
            if url:blocks.append({'type':'link','url':urljoin(source,url),'text':'Open the video or interactive example'})
            return
        if node.name in BLOCKS:emit(node);return
        run=[]
        for child in node.children:
            if isinstance(child,Comment):continue
            if isinstance(child,Tag) and (child.name in CONTAINERS|BLOCKS|IGNORE|{'img','iframe','video'} or child.find(['img','iframe','video'])):
                flush(run);walk(child)
            else:run.append(child)
        flush(run)
    walk(body)
    return blocks

def tokens(text):
    return re.findall(r'[\w]+',text.lower().replace('\u00a0',' '))
