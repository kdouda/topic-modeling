from pymongo import MongoClient
from gensim import corpora
from gensim.models import LdaModel
from gensim.test.utils import datapath
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
from nlp.nlp import NLP
from nlp.sentencesplitter import SentenceSplitter
from nlp.tokenizer import SentenceTokenizer
from wordcloud import WordCloud
from nlp.stopword import StopwordsRemover
import fileinput
from os import listdir
from os.path import isfile, join

lda = LdaModel.load("./models/model3/model")
dictionary = Dictionary.load('./models/model4/dictionary.id2word')
tokenizer = SentenceTokenizer()
splitter = SentenceSplitter()
stopwords = StopwordsRemover()
nlp = NLP()

text = ""

directory = "./test/"

def classify_document(text):
    sentences = splitter.split(text)

    doc = [] #bow

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

    bow = dictionary.doc2bow(doc)
    return lda[bow]

files = [f for f in listdir(directory) if isfile(join(directory, f))]

for f in files:
    with open(directory + f, 'r', encoding="utf-8") as doc:
        text = doc.read()
        print(f)
        topics = classify_document(text)
        print(topics)