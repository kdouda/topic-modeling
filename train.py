from pymongo import MongoClient
from nlp.stopword import StopwordsRemover
from gensim import corpora
from gensim.models import LdaModel
from gensim.test.utils import datapath
from gensim.models.coherencemodel import CoherenceModel

client = MongoClient("mongodb+srv://lda-nlp:9rJrKvf9Z5wSLdMq@cluster0.pbtmt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['topicmodeling']
collection = db['novinky']
cursor = collection.find({})

dictionary = {}

stopwords = StopwordsRemover()

docs = []

for document in cursor:
    doc = []

    for term in document["terms"]:
        if not stopwords.is_stopword(term):
            doc.append(term)

    docs.append(doc)

dictionary = corpora.Dictionary(
    docs
)

corpus = [dictionary.doc2bow(text) for text in docs]

num_topics = 5
chunksize = 2000
passes = 10
iterations = 50
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

model.save("./models/model2/model")

cm = CoherenceModel(model=model, corpus=corpus, coherence='u_mass')
coherence = cm.get_coherence() 

print(coherence)