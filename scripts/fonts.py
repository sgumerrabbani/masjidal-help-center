import requests,re
from pathlib import Path
css=requests.get('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&display=swap',headers={'User-Agent':'Mozilla/5.0'}).text
for weight in [400,500,700]:
 blocks=[b for b in css.split('}') if f'font-weight: {weight};' in b]
 block=blocks[-1];url=re.search(r'url\((.*?)\)',block)[1];ext='.woff2' if 'woff2' in block else '.ttf';dest=f'assets/fonts/poppins-{weight}{ext}';Path(dest).write_bytes(requests.get(url).content)
 with open('assets/css/styles.css','a',encoding='utf-8') as f:f.write(f'\n@font-face{{font-family:Poppins;src:url(../fonts/poppins-{weight}{ext});font-weight:{weight};font-style:normal;font-display:swap}}')
