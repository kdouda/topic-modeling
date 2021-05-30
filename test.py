from pymongo import MongoClient
from nlp.stopword import StopwordsRemover
from gensim import corpora
from gensim.models import LdaModel

lda = LdaModel.load("model")
print(lda.print_topics())