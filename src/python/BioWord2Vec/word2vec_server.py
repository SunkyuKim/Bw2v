"""
use pickle?
"""
import numpy as np
from sklearn.decomposition import PCA
from socket import *
from gensim.models import word2vec
from load_bronco import bronco_full


HOST = ''
PORT = 21568
BUFSIZ = 4096
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(20)


# dictionary = open("/home/sunkyu/workspace/PathwayMaker/res/WordNetChecked_bossNewDic_2016-04-25.txt",'r')
# entity_dict = dict()
# for l in dictionary:
#     tokens = l.split("\t")
#     name = tokens[1].strip()
#     type = tokens[2].strip()
#     entity_dict[name] = type

# model = word2vec.Word2Vec.load_word2vec_format(
#     "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/PubMed-w2v.bin", binary=True)
model = word2vec.Word2Vec.load_word2vec_format(
    "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/fixed_model_160629.bin", binary=True)

cml_list = ['chronic_myeloid_leukemia', 'imatinib', 'dasatinib', 'bosutinib']
breast_list = ['breast_cancer', 'docetaxel', 'letrozole', 'pertuzumab']
melan_list = ['melanoma', 'dabrafenib', 'trametinib', 'nivolumab']
lung_list = ['lung_cancer', 'ceritinib', 'gefitinib', 'paciltaxel']
# lung_list = []
prostate_list = ['prostate_cancer', 'enzalutamide', 'flutamide', 'lupron']
pancreatic_list = ['pancreatic_cancer', 'abraxane', 'everolimus', 'sunitinib']
bladder_list = ['bladder_cancer', 'atezolizumab', 'cisplatin', 'thiotepa']
# bladder_list = []
cervical_list = ['cervical_cancer', 'avastin', 'bevacizumab', 'topotecan_hydrochloride']
ovarian_list = ['ovarian_cancer', 'avastin', 'paciltaxel', 'cyclophosphamide']
l1 = ['FGF', 'FGFR', 'EGF', 'EGFR', 'EPO', 'EpoR', 'IGF-1', 'IGF-1_receptor', 'HGF', 'HGFR']
l2 = ['pertuzumab', 'ERBB2', 'dasatinib', 'ABL1', 'ceritinib', 'ALK', 'gefitinib', 'EGFR']
l3 = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D']
cancers = ['breast_cancer', 'pulmonary_cancer', 'pancreatic_cancer', 'lung_cancer', 'bronchial_carcinoma', 'brain_cancer', 'kidney_cancer']
inflammations = ['pulmonary_inflammation', 'lung_inflammation', 'brain_inflammation', 'alveolitis']
fl,cl = bronco_full()

txt_list = (
breast_list + melan_list + lung_list + prostate_list + pancreatic_list + bladder_list + cervical_list + ovarian_list + fl + l1 + l2 + l3 + cancers + inflammations)

# model = dict()
# for l in open("/media/sunkyu/327680A376806985/GloVe-1.2/vectors_300.txt"):
#     tokens = l.split()
#     if tokens[0] in txt_list:
#         model[tokens[0]] = tokens[1:]



while True:
    print 'waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from:', addr

    while True:
        input = tcpCliSock.recv(BUFSIZ)
        if not input:
            break

        tokens = input.split("#")

        command = tokens[0]
        content = [t.replace(" ","_") for t in tokens[1].split("$")]

        if command == "vec":
            if content[0] not in model:
                tcpCliSock.send("no " + input)
                continue
            temp_str_list = [str(v) for v in model[content[0]]]

            send_str = '\t'.join(temp_str_list)
            tcpCliSock.send(send_str)
        elif command == "sim":
            pass
        elif command == "nearest":
            if content[0] not in model:
                tcpCliSock.send("no " + input)
                continue
            result_tup = model.most_similar(positive=content[0], topn=30)
            names = [str(t[0]) for t in result_tup]
            names.append(content[0])
            X = np.asarray([model[name] for name in names])
            m = PCA(n_components=2)

            types = list()
            for name in names:
                name = name.replace("_", " ")
                if name not in entity_dict.keys():
                    types.append("Not Bio Entity")
                else:
                    types.append(entity_dict[name])
            points = m.fit_transform(X)
            vis_x = points[:, 0]
            vis_y = points[:, 1]

            point_str_list = []
            for index in range(len(names)):
                point_str_list.append(
                    "$".join([names[index], str(vis_x[index]), str(vis_y[index]), types[index]]))
            send_str = '\t'.join(point_str_list)
            tcpCliSock.send(send_str)

    tcpCliSock.close()
 tcpSerSock.close()