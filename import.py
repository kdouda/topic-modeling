from pymongo import MongoClient
from providers.novinkyjsonarticleprovider import NovinkyJsonArticleProvider
from nlp.nlp import NLP
from nlp.sentencesplitter import SentenceSplitter
from nlp.tokenizer import SentenceTokenizer
from nlp.stopword import StopwordsRemover
import datetime
import time

client = MongoClient("mongodb+srv://lda-nlp:9rJrKvf9Z5wSLdMq@cluster0.pbtmt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['topicmodeling']
collection = db['novinky']

nlp = NLP()

tokenizer = SentenceTokenizer()
splitter = SentenceSplitter()
stopwords = StopwordsRemover()

provider = NovinkyJsonArticleProvider(40348699)
i = 0

for article in provider.get_next_article():

    if collection.find_one({"_id": article.get_id()}):
        continue

    content = article.get_content()
    sentences = splitter.split(content)
    doc = []

    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        tokens = stopwords.remove_stopwords(tokens)

        for token in tokens:
            tok = token.strip()

            if tok == '' or len(tok) < 3:
                continue

            lemma = nlp.lemmatize_nv(tok)
            if not stopwords.is_stopword(lemma):
                if lemma != '' and len(lemma) > 3:
                    doc.append(lemma)

    i = i + 1

    post = {
        "_id": article.get_id(), # ID článku
        "title": article.get_name(), # titulek článku
        "summary": article.get_summary(), # perex článku - využitý jako "sumarizace" při výpisu
        "url": article.get_url(), # URL článku
        "terms": doc, # pole termů
        "date": datetime.datetime.utcnow() # čas vytvoření záznamu
    }

    collection.insert_one(post)
    time.sleep(1.00)