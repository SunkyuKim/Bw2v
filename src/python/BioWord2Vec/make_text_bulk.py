from gensim.models import word2vec
from multiprocessing import Pool
import codecs


model = word2vec.Word2Vec.load_word2vec_format(
    "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/fixed_model_160629.bin", binary=True)

w_file = "/media/sunkyu/327680A376806985/word2vec_bulk/bulk_300d.txt"

with codecs.open(w_file, 'w', 'utf-8-sig') as fw:
    for v in model.vocab:
        str_vectors = [str(val) for val in model[v]]
        fw.write('\t'.join([v] + str_vectors))
        fw.write('\n')
