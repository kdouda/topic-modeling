# naive implementation of a sentence-based tokenizer
# it does not require sentences per se, but it makes it a little easier to work with
import re

class SentenceTokenizer():

    def __init__(self):
        self.punctuation = [" ", ".", ",", "!", "?", "…", "–", "„", "“", "”", ":", ";", '\n', "\r", "(", ")", "<", ">"]

    def tokenize(self, sentence):

        for punc in self.punctuation:
            sentence = sentence.replace(punc, " ")

        return re.split('\s+', sentence)
