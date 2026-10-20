import unittest
from bs4 import BeautifulSoup
from article_extract import extract_article

class ArticleExtractionTests(unittest.TestCase):
    def test_bare_instruction_text_and_wrapped_images_survive(self):
        page=BeautifulSoup('<html><body><article><div class="et_pb_text_inner">Install the library in &lt;head&gt; and <a href="/setup">continue setup</a>.</div><div class="et_pb_image"><span><a href="/shot.png"><img src="/shot.png" alt="Setup screen"></a></span></div><h1>'+('Explanatory paragraph. '*10)+'</h1></article></body></html>','html.parser')
        blocks=extract_article(page.article,'https://example.com/guide',lambda url:'assets/screenshot.png')
        text=' '.join(BeautifulSoup(b.get('html',''),'html.parser').get_text(' ',strip=True) for b in blocks)
        self.assertIn('Install the library in <head>',text)
        self.assertIn('continue setup',text)
        self.assertEqual(sum(b['type']=='image' for b in blocks),1)
        self.assertFalse(any(BeautifulSoup(b.get('html',''),'html.parser').find('h1') for b in blocks))
        self.assertIn('https://example.com/setup',''.join(b.get('html','') for b in blocks))

    def test_divi_out_of_line_button_becomes_a_real_link(self):
        page=BeautifulSoup('<html><body><article><div class="et_pb_text_3"><div class="et_pb_text_inner"><p>LEARN MORE</p></div></div></article><script>var et_link_options_data = [{"class":"et_pb_text_3","url":"/timings/","target":"_self"}];</script></body></html>','html.parser')
        blocks=extract_article(page.article,'https://example.com/guide',lambda url:url)
        html=''.join(b.get('html','') for b in blocks)
        link=BeautifulSoup(html,'html.parser').find('a')
        self.assertEqual(link['href'],'https://example.com/timings/')
        self.assertEqual(link.get_text(),'LEARN MORE')

if __name__=='__main__':unittest.main()
