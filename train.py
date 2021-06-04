# this "hack" is necessary  for c_v algorithm to work right 
if __name__ == '__main__':
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

    dictionary.save('./models/model4/dictionary.id2word')

    corpus = [dictionary.doc2bow(text) for text in docs]

    num_topics = 20
    chunksize = 2000
    passes = 1
    iterations = 50
    eval_every = None 

    temp = dictionary[0]
    id2word = dictionary.id2token

    print("Corpus size: " + str(len(docs)))

    for num_topics in [14]:
        model = LdaModel(
            corpus=corpus,
            id2word=id2word,
            chunksize=chunksize,
            alpha='auto',
            eta='auto',
            iterations=iterations,
            num_topics=num_topics,
            passes=passes,
            eval_every=eval_every,
            random_state=31052021
        )

        model.save("models/model4/model")

        print(model.print_topics())

        measures = ['u_mass', 'c_v']

        for measure in measures:
            cm = CoherenceModel(model=model, corpus=corpus, coherence=measure, texts=docs, dictionary=dictionary)
            coherence = cm.get_coherence() 

            print("---")
            print(num_topics)
            print(measure)
            print(coherence)
            print("---")