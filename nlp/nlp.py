from ufal.morphodita import *

class NLP():

    def __init__(self):
        self.morpho = Morpho.load("./czech-morfflex-pdt-161115/czech-morfflex-161115.dict")
        print(self.morpho)

    def lemmatize(self, token):
        lemmas = TaggedLemmas()
        lemmas_forms = TaggedLemmasForms()

        result = self.morpho.analyze(token, self.morpho.GUESSER, lemmas)

        for lemma in lemmas:
            candidate = lemma.lemma.split('_')[0]
            candidate = candidate.split('-')[0]
            candidate = candidate.split('`')[0]

            return candidate
        
        # cannot be lemmatized?
        return token

    # returns only nouns and verbs
    def lemmatize_nv(self, token):
        lemmas = TaggedLemmas()
        lemmas_forms = TaggedLemmasForms()

        result = self.morpho.analyze(token, self.morpho.GUESSER, lemmas)

        for lemma in lemmas:

            if lemma.tag.startswith('N') or lemma.tag.startswith('V'):
                candidate = lemma.lemma.split('_')[0]
                candidate = candidate.split('-')[0]
                candidate = candidate.split('`')[0]

                return candidate
        
        # cannot be lemmatized?
        return ""