from providers.novinkyarticleprovider import NovinkyArticleProvider

provider = NovinkyArticleProvider()

for article in provider.get_next_article():
    print(article)
    print(article.get_content())
    break
