from article.article import Article
import requests
from bs4 import BeautifulSoup

class NovinkyArticle(Article):

    def __init__(self, name, url, summary = ''):
        self.name = name
        self.url  = url
        self.summary = summary
        self.content = ""

    def get_content(self):
        if self.content:
            return self.content

        scraper = NovinkyScraper(self.url)

        text = ""

        for paragraph in scraper.get_next_paragraph():
            text = text + paragraph + "\n"

        self.content = text

        return text

class NovinkyArticleJson(NovinkyArticle):

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id


class NovinkyScraper():

    def __init__(self, url):
        self.url = url

    def get_next_paragraph(self):
        html = requests.get(self.url).text
        parsed = BeautifulSoup(html, 'html.parser')
        
        for paragraph in parsed.select('.d_c1:not(.d_ae)'):
            yield paragraph.get_text()