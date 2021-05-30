from pymongo import MongoClient
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nlp.stopword import StopwordsRemover

client = MongoClient("mongodb+srv://lda-nlp:9rJrKvf9Z5wSLdMq@cluster0.pbtmt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['topicmodeling']
collection = db['novinky']
cursor = collection.find({})

dictionary = {}

stopwords = StopwordsRemover()

for document in cursor:
    for term in document["terms"]:
        if not stopwords.is_stopword(term):
            if term not in dictionary:
                dictionary[term] = 0

            dictionary[term] = dictionary[term] + 1

print(dictionary)

wordcloud = WordCloud(
    background_color="white",
    width=1920,
    height=1080,
    max_words=200,
    normalize_plurals=False
).generate_from_frequencies(dictionary)

wordcloud.to_file('wordcloud.png')