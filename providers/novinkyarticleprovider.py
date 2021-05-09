from providers.articleprovider import ArticleProvider
from article.novinkyarticle import NovinkyArticle

import feedparser


class NovinkyArticleProvider(ArticleProvider):

    def __init__(self):
        self.url = "https://www.novinky.cz/rss"

    def get_next_article(self):
        feed = feedparser.parse(self.url)
        
        for entry in feed.entries:
            title   = entry.title
            link    = entry.link
            summary = entry.summary

            article = NovinkyArticle(title, link, summary)

            yield article

