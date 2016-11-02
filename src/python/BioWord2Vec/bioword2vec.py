
from gensim.models import word2vec


class bioword2vec():
    def __init__(self):
        print "loading bioword2vec pre-trained model.."

        self.model = word2vec.Word2Vec.load_word2vec_format(
            # "../res/word2vec/fixed_model_160526.bin", binary=True)
            "../res/GloVe-1.2/vectors.bin", binary = True)

    def __preprocess(self, word):
        tokens = word.split()
        return '_'.join(tokens)

    def get(self, word):
        fixed_word = self.__preprocess(word)
        return self.model[fixed_word]

    def get_similarity(self, word1, word2):
        fixed_word1 = self.__preprocess(word1)
        fixed_word2 = self.__preprocess(word2)
        return self.model.similarity(fixed_word1, fixed_word2)

    def get_most_similar(self, positive=[], negative=[], topn=10, restrict_vocab=None):
        if len(positive + negative) == 0:
            return ''
        fixed_positive = [self.__preprocess(w) for w in positive]
        fixed_negative = [self.__preprocess(w) for w in negative]
        most_similar_list = self.model.most_similar(positive=fixed_positive,
                                       negative=fixed_negative,
                                       topn=topn,
                                       restrict_vocab=restrict_vocab)
        fixed_most_similar = []
        for tup in most_similar_list:
            word = tup[0]
            score = tup[1]
            tokens = word.split('_')
            word = ' '.join(tokens)
            fixed_most_similar.append((word, score))
        return fixed_most_similar

if __name__ == '__main__':
    m = bioword2vec()
    print m.get_most_similar(positive=["the"])
