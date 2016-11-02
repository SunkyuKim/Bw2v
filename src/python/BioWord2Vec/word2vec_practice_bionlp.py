import os
import logging
from sunkyu_utils import *
from multiprocessing import Pool, Manager
from gensim.models import word2vec
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
res_dir = "../res/"
result_dir = "../result/"
abs_dir = "../res/pubmed_entity_found/"
kegg_sentence_dir = '/'.join([res_dir,'pathwaykgmls','pathway_text'])
pubmed_sentence_dir = '/'.join([res_dir,'pubmed_sentences'])

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for l in open(os.path.join(self.dirname, fname)):
                line_tokens = []
                temp_token_list = re.split('[,. ]', l.strip())
                for t in temp_token_list:
                    if len(t) != 0:
                        line_tokens.append(t)
                # tokens.append(line_tokens)
                yield line_tokens
                # yield line.split()

def __get_sentence_tokens(file_path):
    print file_path
    # return token list from a abstract text file
    lines = open(file_path, 'r').readlines()
    # someday we will stem a line here
    tokens = []
    for l in lines:
        line_tokens = []
        temp_token_list = re.split('[,. ]', l.strip())
        for t in temp_token_list:
            if len(t)!=0:
                line_tokens.append(t)
        tokens.append(line_tokens)
    return tokens

@time_checker
def get_sentence_tokens(sentences_dir, num_thread=4):
    # return token by sentence list from abstract text files
    file_names = os.listdir(sentences_dir)
    file_pathes = [sentences_dir + '/' + name for name in file_names]
    pool = Pool(num_thread)
    sentences_by_file = []
    for path in file_pathes:
        sentences_by_file.append(__get_sentence_tokens(path))
    # sentences_by_file = pool.map(__get_sentence_tokens, file_pathes[0:10])
    sentences_tokens = []
    for s in sentences_by_file:
        sentences_tokens += s
    return sentences_tokens

def __train_word2vec(sentence_path, model):
    pubmed_sentence_tokens = __get_sentence_tokens(pubmed_sentence_dir + '/' + sentence_path)
    # update = True is IMPORTANT!!
    # model.build_vocab(pubmed_sentence_tokens, update=True)

    model.train(pubmed_sentence_tokens)

@time_checker
def train_word2vec():
    # return word2vec trained model

    sentence = MySentences(pubmed_sentence_dir)
    model = word2vec.Word2Vec(sentences=sentence, size=300, min_count=5, workers=4)


    # kegg_sentence_tokens = get_sentence_tokens(kegg_sentence_dir)
    # model.build_vocab(kegg_sentence_tokens)
    # model.train(kegg_sentence_tokens)


    # for one_pubmed_sentence_path in os.listdir(pubmed_sentence_dir):
    #     __train_word2vec(one_pubmed_sentence_path,model)

    # __train_word2vec(pubmed_sentence_dir, model)

    return model

def __get_pubmed_abstract(path, sentence_list_100_file):
    fr = open(path, 'r')
    for l in fr:
        tokens = l.strip().split('@@@')
        title = tokens[3].strip()
        abs = tokens[5].strip()

        abs_sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', abs)

        sentence_list_100_file.append(title)
        for sentence in abs_sentences:
            if len(sentence)==0:
                continue
            sentence_list_100_file.append(sentence)
    print len(sentence_list_100_file)

@time_checker
def get_pubmed_abstract():

    fs_temp = os.listdir(abs_dir)
    fs = []
    for f in fs_temp:
        if 'txt' in f:
           fs.append(f)

    f_num = len(fs)
    count = 0
    sentence_list_100_file = list()

    for f in fs:
        __get_pubmed_abstract(abs_dir + f, sentence_list_100_file)

        count += 1
        if count%100 == 0:
            print count, '/', f_num
            with open(pubmed_sentence_dir +  '/' + 'f_'+str(count)+'.txt', 'w') as fw:
                for sentence in sentence_list_100_file:
                    if len(sentence) == 0:
                        continue
                    fw.write(sentence + '\n')
            sentence_list_100_file = []

    return sentence_list_100_file

def get_bionlp_sentence():
    bionlp_path = "../res/testing_whole_entity_named_BE_added_rels_0831.csv"
    # bionlp_path = "../res/train_data_entfeat_BE_center_0906.csv"

    import pandas as pd
    df = pd.read_csv(bionlp_path)
    sentences = list(df['tagged_sentence'])
    return_data = []
    for l in sentences:
        sentence = l
        # print sentence
        # sentence = sentence.replace('<entity1>', '<entity1> ')\
        #                     .replace('</entity1>', ' </entity1>')\
        #                     .replace('<entity2>', '<entity2> ')\
        #                     .replace('</entity2>', ' </entity2>')
        sentence = sentence.strip().replace("> ", ">").replace(">", "> ").replace(" <", "<").replace("<", " <")
        temp_token_list = re.split('[,. ]', sentence.strip())
        return_data.append(temp_token_list)
    return return_data

if __name__=='__main__':
    # import time
    sentence_set = get_bionlp_sentence()

    # model = train_word2vec()
    model = word2vec.Word2Vec(sentences=sentence_set, size=300, min_count=5, workers=4)

    # possible to resume training
    model.save(res_dir + "word2vec/temp_model_160906")

    # not possible to resume training with this model file
    model.save_word2vec_format(res_dir + "word2vec/pubmed_bionlp_train_300.bin", binary=True)
##########################################################################################
    s = time.time()
    # model = word2vec.Word2Vec.load_word2vec_format(
    #     res_dir + "word2vec/fixed_model_160629.bin", binary=True)
    # model = word2vec.Word2Vec.load_word2vec_format(
    #     res_dir + "word2vec/only_bionlp_train_300.bin", binary=True)
    # f = time.time()
    # print f - s
    #
    # sentence_set = get_bionlp_sentence()
    # model.train(sentence_set)
    # model = word2vec.Word2Vec(sentences=sentence_set, size=300, min_count=5, workers=4)

    # print list(model['chronic'])
    # print model['chronic'].tolist()
    # s = time.time()
    # model = word2vec.Word2Vec.load(
    #     res_dir + "word2vec/temp_model_160427")
    # f = time.time()
    # print f - s

    # print len(model.vocab)
    #
    # vs = ['p53', 'mTOR', 'AKT', 'EGFR', 'to', 'Wnt', 'Rb', 'it']
    # for v in vs:
    #     print v, model.similarity('apoptosis', v)
    #
    # print model.similarity("imatinib", "dasatinib")
    #
    # for v in model.most_similar(positive=["chronic_myeloid_leukemia", "drug"], negative=["imatinib"],topn=100):
    #     print v
    # for v in model.most_similar(positive=["imatinib"],topn=100):
    #     print v