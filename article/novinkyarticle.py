from article.article import Article
import requests
from bs4 import BeautifulSoup

class NovinkyArticle(Article):

    def get_content(self):
        scraper = NovinkyScaper(self.url)

        text = ""

        for paragraph in scraper.get_next_paragraph():
            text = text + paragraph + "\n"

        return text


class NovinkyScaper():

    def __init__(self, url):
        self.url = url

    def get_next_paragraph(self):
        html = requests.get(self.url).text
        parsed = BeautifulSoup(html, 'html.parser')
        
        for paragraph in parsed.select('.d_c1:not(.d_ae)'):
            yield paragraph.get_text()