from gensim.models import word2vec
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import random
from socket import *

dictionary = open("/home/sunkyu/workspace/PathwayMaker/res/WordNetChecked_bossNewDic_2016-04-25.txt",'r')
entity_dict = dict()
for l in dictionary:
    tokens = l.split("\t")
    name = tokens[1].strip()
    type = tokens[2].strip()
    if type not in entity_dict.keys():
        entity_dict[type] = list()
    entity_dict[type].append(name)

print entity_dict.keys()
def __get_model_vec(name):
    HOST = 'localhost'
    PORT = 21567
    BUFSIZ = 4096
    ADDR = (HOST, PORT)

    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)

    input = name
    tcpCliSocket.send(input)
    vector_str = tcpCliSocket.recv(BUFSIZ)
    result = [float(v) for v in vector_str.split('\t')]
    return result

def get_model_vec(name_list):
    return [__get_model_vec(v) for v in name_list]

plt.figure(1)

txt_list = ['AML', 'acute_myeloid_leukemia', 'CML', 'chronic_myeloid_leukemia', 'imatinib', 'imatinib_mesylate', 'oncogene', 'target']

X = np.asarray(get_model_vec(txt_list))
m = PCA(n_components=2)
# m = TSNE(n_components=2)

points = m.fit_transform(X)
vis_x = points[:, 0]
vis_y = points[:, 1]

plt.scatter(vis_x, vis_y, s=50)
for i,txt in enumerate(txt_list):
    plt.annotate(txt, (vis_x[i], vis_y[i]))
# for j in range(0,len(vis_x),2):
#     for k in range(2):
#         plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], "r--")
plt.show()
