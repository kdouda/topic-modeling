from providers.novinkyjsonarticleprovider import NovinkyJsonArticleProvider
from nlp.nlp import NLP
from nlp.sentencesplitter import SentenceSplitter
from nlp.tokenizer import SentenceTokenizer
from wordcloud import WordCloud
from nlp.stopword import StopwordsRemover
from gensim import corpora
from gensim.models import LdaModel
import time

nlp = NLP()

tokenizer = SentenceTokenizer()
splitter = SentenceSplitter()
stopwords = StopwordsRemover()

provider = NovinkyJsonArticleProvider()

for article in provider.get_next_article():
    print(article)

quit()

i = 0

docs = []

articleurls = []

for article in provider.get_next_article():
    time.sleep(0.07)
    print(article)
    print(article.get_content())

    content = article.get_content()

    sentences = splitter.split(content)

    doc = []
    tf = {}

    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        tokens = stopwords.remove_stopwords(tokens)

        for token in tokens:
            tok = token.strip()

            if tok == '' or len(tok) < 3:
                continue

            lemma = nlp.lemmatize_nv(tok)
            if not stopwords.is_stopword(lemma):
                if lemma not in tf:
                    tf[lemma] = 0
                
                tf[lemma] = tf[lemma] + 1
                
                if lemma != '' and len(lemma) > 3:
                    doc.append(lemma)

    docs.append(doc)
    articleurls.append(article.get_url())

    i = i + 1

dictionary = corpora.Dictionary(
    docs
)

corpus = [dictionary.doc2bow(text) for text in docs]

num_topics = 10
chunksize = 2000
passes = 100
iterations = 1000
eval_every = None 

temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

print("Corpus size: " + str(len(docs)))

model = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha='auto',
    eta='auto',
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every
)

print(model.print_topics())

for i in range(len(articleurls)):
    print("----")
    print(articleurls[i])
    topics = model.get_document_topics(corpus[i])

    for topic in topics:
        print("Topic:" + str(topic[0]))
        print(model.print_topic(topic[0]))
        print(topic[1])

    print("----")

#wordcloud = WordCloud(
#    background_color="white",
#    max_words=5000,
#    contour_width=3,
#    contour_color='steelblue',
#    width=1600,
#    height=800
#)
#
#wordcloud.generate_from_text(complete)
#wordcloud.to_file('wordcloud.png')