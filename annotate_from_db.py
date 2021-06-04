from pymongo import MongoClient
from gensim import corpora
from gensim.models import LdaModel
from gensim.test.utils import datapath
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
import csv

lda = LdaModel.load("./models/model3/model")
dictionary = Dictionary.load('./models/model4/dictionary.id2word')

client = MongoClient("mongodb+srv://lda-nlp:9rJrKvf9Z5wSLdMq@cluster0.pbtmt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['topicmodeling']
collection = db['novinky']
cursor = collection.find({})
docs = []

with open('annotated_original.csv', 'w', newline='', encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')

    firstrow = ["id", "url", "title", "perex"]
    num_topics = len(lda.get_topics())
    for i in range(num_topics):
        firstrow.append('topic_' + str(i))

    csvwriter.writerow(
        firstrow
    )

    for document in cursor:
        bow = dictionary.doc2bow(document['terms'])
        topics = lda[bow]

        row = [document['_id'], document['url'], document['title'], document['summary']]

        topic_array = []

        for i in range(num_topics):
            topic_array.append(0)

        for topic in topics:
            topic_array[topic[0]] = topic[1]
        
        row.extend(topic_array)

        csvwriter.writerow(
            row
        )