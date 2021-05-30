from providers.articleprovider import ArticleProvider
from article.novinkyarticle import NovinkyArticleJson
import requests
import time

class NovinkyJsonArticleProvider(ArticleProvider):

    def __init__(self, first_id):
        self.url = "https://www.novinky.cz/api/documenttimelines?service=novinky&maxItems=100&itemIds=section_5ad5a5fec25e64000bd6e838_novinky&loadingNextItems=1&sort=-dateOfUpdate,-uid&embedded=sectionsTree"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        }

        self.first_id = first_id

        self.ids = []

    def build_url(self, last_id):
        return self.url + "&lastItemId=" + str(last_id)

    def fetch_articles(self, url):
        response = requests.get(url, headers = self.headers)
        data = []

        ret = response.json()

        for document in ret['_items'][0]['documents']:
            article = NovinkyArticleJson(
                document['title'],
                "https://www.novinky.cz/clanek/" + document['slug'] + "-" + str(document['uid']),
                document['perex']
            )

            article.set_id(document['uid'])
            data.append(article)
   
        return data

    def get_next_article(self):
        articles = self.fetch_articles(
            self.build_url(self.first_id)
        )

        ids = []

        while (len(articles)):
            article = articles.pop()

            if article.get_id() not in ids:
                yield article

            ids.append(article.get_id())

            if len(articles) == 0:
                time.sleep(1.5)
                articles = self.fetch_articles(
                    self.build_url(article.get_id())
                )

            if len(articles) == 0:
                break
            

            



