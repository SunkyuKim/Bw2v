from matplotlib import pyplot as plt

import numpy as np
from gensim.models import word2vec
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# dictionary = open("/home/sunkyu/workspace/PathwayMaker/res/WordNetChecked_bossNewDic_2016-04-25.txt",'r')
# entity_dict = dict()
# for l in dictionary:
#     tokens = l.split("\t")
#     name = tokens[1].strip()
#     type = tokens[2].strip()
#     if type not in entity_dict.keys():
#         entity_dict[type] = list()
#     entity_dict[type].append(name)
#
# print entity_dict.keys()

# model = word2vec.Word2Vec.load_word2vec_format(
#     "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/fixed_model_160526.bin", binary=True)



# def get_vector(key):
#     names = entity_dict[key]
#     names_one_token = []
#     for n in names:
#         if len(n.split()) > 1:
#             names_one_token.append(n.replace(" ","_"))
#
#     names_vec = []
#     for n in names_one_token:
#         if n in model:
#             names_vec.append(model[n])
#
#     return random.sample(names_vec,100)

# disease_vec = get_vector('Disease')
# drug_vec = get_vector('Drug')
# cellline_vec = get_vector('CellLine')
# gene_vec = get_vector('Gene')

# disease_vec = [model['chronic_myeloid_leukemia'], model['breast_cancer']]
# drug_vec = [model['imatinib'], model['busulfan'], model['nilotinib'], model['dasatinib'], model['bosutinib'], model['docetaxel'], model['letrozole'], model['pertuzumab']]
# X = np.asarray(disease_vec + drug_vec + cellline_vec + gene_vec)
# X = np.asarray(disease_vec + drug_vec)

# Y = (
#     ['blue'] * len(disease_vec)
#     + ['red'] * len(drug_vec)
#     # + ['green'] * len(cellline_vec)
#     )

print "model loading.."
# model = word2vec.Word2Vec.load_word2vec_format(
#     "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/PubMed-w2v.bin", binary=True)

model = word2vec.Word2Vec.load_word2vec_format(
    "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/fixed_model_160629.bin", binary=True)
mode = "pub2vec"
print mode
print "end"

def __get_model_vec(name):
    # HOST = 'localhost'
    # PORT = 21567
    # BUFSIZ = 4096
    # ADDR = (HOST, PORT)
    #
    # tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    # tcpCliSocket.connect(ADDR)
    #
    # input = "vec#"+name
    # tcpCliSocket.send(input)
    # vector_str = tcpCliSocket.recv(BUFSIZ)
    # if "no vec" in vector_str:
    #     result = None
    # else:
    #     result = [float(v) for v in vector_str.split('\t')]

    name = name.split('_')
    # result = sum([model[n] for n in name]) / float(len(name))
    result = sum([model[n] for n in name])
    # result = model[name]
    return result

def get_model_vec(name_list):
    return [__get_model_vec(v) for v in name_list]

if False:
    cml_list = ['chronic_myeloid_leukemia','imatinib', 'dasatinib', 'bosutinib']
    breast_list = ['breast_cancer', 'docetaxel', 'letrozole', 'pertuzumab']
    melan_list = ['melanoma', 'dabrafenib', 'trametinib', 'nivolumab']
    lung_list = ['lung_cancer', 'ceritinib', 'gefitinib', 'paciltaxel']
    lung_list = []
    prostate_list = ['prostate_cancer', 'enzalutamide', 'flutamide', 'lupron']
    pancreatic_list = ['pancreatic_cancer', 'abraxane', 'everolimus', 'sunitinib']
    bladder_list = ['bladder_cancer', 'atezolizumab', 'cisplatin', 'thiotepa']
    bladder_list = []
    cervical_list = ['cervical_cancer', 'avastin', 'bevacizumab', 'topotecan_hydrochloride']
    ovarian_list = ['ovarian_cancer', 'avastin', 'paciltaxel', 'cyclophosphamide']

    txt_list = (breast_list + melan_list + lung_list + prostate_list + pancreatic_list + bladder_list + cervical_list + ovarian_list)
    X = np.asarray(get_model_vec(txt_list))

    # colors = (
    #     ['red'] * len(breast_list)
    #     + ['green'] * len(melan_list)
    #     + ['blue'] * len(lung_list)
    #     + ['black'] * len(prostate_list)
    #     + ['purple'] * len(pancreatic_list)
    #     + ['orange'] * len(bladder_list)
    #     )

    colors = (
        ['red'] * len(breast_list)
        + ['blue'] * len(melan_list)
        + ['blue'] * len(lung_list)
        + ['red'] * len(prostate_list)
        + ['blue'] * len(pancreatic_list)
        + ['blue'] * len(bladder_list)
        + ['red'] * len(cervical_list)
        + ['red'] * len(ovarian_list)
    )

    # m = TSNE(n_components=2, random_state=0)
    # m = TSNE(n_components=2)
    m = PCA(n_components=2)

    plt.figure(1)
    # ax = plt.subplot(111)
    # ax.set_title("Cancer - Drug")
    plt.title("Cancer - Drug")
    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    color_index = ['red', 'blue', 'green', 'yellow']
    cm = KMeans(n_clusters=4)
    # cm = DBSCAN(eps=0.05)
    print cm.fit_predict(points)
    # colors = [color_index[v] for v in cm.fit_predict(points)]

    plt.scatter(vis_x, vis_y, c=colors, s=50)
    for i,txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
    for j in range(0,len(vis_x),4):
        for k in range(4):
            plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], "r--", c=colors[j+k])
    plt.savefig("../res/screenshots/%s_Cancer - Drug" % mode)
    plt.show()


    # m = PCA(n_components=3)
    #
    # fig = plt.figure(1)
    # ax = fig.add_subplot(111, projection='3d')
    # # ax = plt.subplot(111)
    # # ax.set_title("Cancer - Drug")
    # plt.title("Cancer - Drug_3D")
    # points = m.fit_transform(X)
    # vis_x = points[:, 0]
    # vis_y = points[:, 1]
    # vis_z = points[:, 2]
    #
    # # color_index = ['red', 'blue', 'green', 'yellow']
    # cm = KMeans(n_clusters=3)
    # # cm = DBSCAN()
    # print cm.fit_predict(points)
    # colors = [color_index[v] for v in cm.fit_predict(points)]
    # ax.scatter(xs=vis_x, ys=vis_y, zs=vis_z, c=colors, s=50)
    # # plt.scatter(vis_x, vis_y, c=colors, s=50)
    # # for i, txt in enumerate(txt_list):
    # #     ax.annotate(txt, (vis_x[i], vis_y[i], vis_z[i]))
    # for j in range(0,len(vis_x),4):
    #     for k in range(4):
    #         plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], [vis_z[j],vis_z[j+k]], "r--", c=colors[j+k])
    # plt.show()

if True:
    # ax = plt.subplot(222)
    # ax.set_title("Protein - Protein_receptor")
    plt.figure(1)
    plt.title("Protein - Protein_receptor")
    txt_list = ['FGF', 'FGFR', 'EGF', 'EGFR', 'EPO', 'EpoR', 'IGF-1', 'IGF-1_receptor', 'HGF', 'HGFR']

    X = np.asarray(get_model_vec(txt_list))

    m = PCA(n_components=2)
    print X
    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    plt.scatter(vis_x, vis_y, s=50)
    for i,txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
    for j in range(0,len(vis_x),2):
        for k in range(2):
            plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], "r--")
    plt.savefig("../res/screenshots/%s_Protein - Protein_receptor" % mode)
    plt.show()

if False:
    # ax = plt.subplot(223)
    # ax.set_title("Drug-Target")
    plt.figure(1)
    plt.title("Drug-Target")
    # txt_list = ['imatinib', 'KIT', 'dasatinib', 'ABL1', 'ceritinib', 'ALK', 'gefitinib', 'EGFR']
    txt_list = ['pertuzumab', 'ERBB2', 'dasatinib', 'ABL1', 'ceritinib', 'ALK', 'gefitinib', 'EGFR']

    X = np.asarray(get_model_vec(txt_list))
    m = PCA(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    plt.scatter(vis_x, vis_y, s=50)
    for i,txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
    for j in range(0,len(vis_x),2):
        for k in range(2):
            plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], "r--")
    plt.savefig("../res/screenshots/%s_Drug-Target" % mode)
    plt.show()

if True:
    # ax = plt.subplot(224)
    # ax.set_title("Gene-Mutation")
    plt.figure(1)
    plt.title("Disease-Gene-Mutation")
    # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
    # txt_list = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D', 'breast_cancer', 'BRCA', '185delAG']
    txt_list = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D']
    X = np.asarray(get_model_vec(txt_list))
    m = PCA(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    plt.scatter(vis_x, vis_y, s=50)
    for i,txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
    for j in range(0,len(vis_x),3):
        plt.plot([vis_x[j],vis_x[j+1]], [vis_y[j],vis_y[j+1]], "r--")
        plt.plot([vis_x[j+1],vis_x[j+2]], [vis_y[j+1],vis_y[j+2]], "r--")
    plt.savefig("../res/screenshots/%s_Disease-Gene-Mutation" % mode)
    plt.show()

if False:
    plt.figure(1)
    plt.title("Enzymes-Substrates")
    # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
    txt_list = ['starch','amylase','maltose','maltase','sucrose','sucrase','lactose','lactase']

    X = np.asarray(get_model_vec(txt_list))
    m = PCA(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    plt.scatter(vis_x, vis_y, s=50)
    for i,txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
    for j in range(0,len(vis_x),2):
        for k in range(2):
            plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], "r--")
    plt.show()

if True:
    # ax = plt.subplot(224)
    # ax.set_title("Gene-Mutation")
    plt.figure(1)
    plt.title("Disease cluster")
    # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
    cancers = ['breast_cancer', 'pulmonary_cancer', 'pancreatic_cancer', 'lung_cancer', 'bronchial_carcinoma', 'brain_cancer', 'kidney_cancer']
    inflammations = ['pulmonary_inflammation', 'lung_inflammation', 'brain_inflammation', 'alveolitis']

    txt_list = cancers+inflammations

    colors = (
        ['red'] * len(cancers) +
        ['blue'] * len(inflammations)
    )
    X = np.asarray(get_model_vec(txt_list))
    m = PCA(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    plt.scatter(vis_x, vis_y, s=50, c=colors)
    for i, txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
        plt.savefig("../res/screenshots/%s_Disease cluster" % mode)
    plt.show()

    # plt.figure(1)
    # plt.title("Disease cluster_TSNE")
    # m = TSNE(n_components=2)
    #
    # points = m.fit_transform(X)
    # vis_x = points[:, 0]
    # vis_y = points[:, 1]
    #
    # plt.scatter(vis_x, vis_y, s=50, c=colors)
    # for i, txt in enumerate(txt_list):
    #     plt.annotate(txt, (vis_x[i], vis_y[i]))
    #
    # plt.show()

if True:
    # ax = plt.subplot(224)
    # ax.set_title("Gene-Mutation")
    plt.figure(1)
    plt.title("Disease-Gene-Mutation-Drug_BRONCO")
    # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
    # txt_list = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D', 'breast_cancer', 'BRCA', '185delAG']
    # txt_list = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D',
    #             'melanoma', 'MEK1', 'F129L']
    import load_bronco
    txt_list, color_list = load_bronco.bronco_full()

    vec_list = get_model_vec(txt_list)
    new_txt_list = []
    new_vec_list = []
    new_color_list = []
    for i in range(len(vec_list)):
        if vec_list[i] == None:
            continue
        new_txt_list.append(txt_list[i])
        new_vec_list.append(vec_list[i])
        new_color_list.append(color_list[i])

    X = np.asarray(new_vec_list)
    m = PCA(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    plt.scatter(vis_x, vis_y, s=50, c=new_color_list)

    # for i, txt in enumerate(txt_list):
    #     plt.annotate(txt, (vis_x[i], vis_y[i]))
    # for j in range(0, len(vis_x), 3):
    #     plt.plot([vis_x[j], vis_x[j + 1]], [vis_y[j], vis_y[j + 1]], "r--")
    #     plt.plot([vis_x[j + 1], vis_x[j + 2]], [vis_y[j + 1], vis_y[j + 2]], "r--")
    plt.savefig("../res/screenshots/%s_Disease-Gene-Mutation-Drug_BRONCO" % mode)
    plt.show()

    # 3D!!
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # m = PCA(n_components=3)
    #
    # points = m.fit_transform(X)
    # vis_x = points[:, 0]
    # vis_y = points[:, 1]
    # vis_z = points[:, 2]
    #
    # ax.scatter(xs=vis_x, ys=vis_y, zs=vis_z, s=50, c=new_color_list)
    # plt.show()

if False:
    # ax = plt.subplot(224)
    # ax.set_title("Gene-Mutation")
    plt.figure(1)
    plt.title("Disease-Gene-Mutation_BRONCO")
    # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
    # txt_list = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D', 'breast_cancer', 'BRCA', '185delAG']
    # txt_list = ['melanoma', 'BRAF', 'V600E', 'lung_cancer', 'EGFR', 'T790M', 'pancreatic_cancer', 'KRAS', 'G12D',
    #             'melanoma', 'MEK1', 'F129L']
    import load_bronco

    txt_list, color_list = load_bronco.bronco_full()
    vec_list = get_model_vec(txt_list)
    new_txt_list = []
    new_vec_list = []
    new_color_list = []
    for i in range(len(vec_list)):
        if vec_list[i] == None:
            continue
        new_txt_list.append(txt_list[i])
        new_vec_list.append(vec_list[i])
        new_color_list.append(color_list[i])

    X = np.asarray(new_vec_list)

    m = TSNE(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    color_index = ['red', 'blue', 'green', 'yellow']
    cm = KMeans(n_clusters=4)
    # cm = DBSCAN(eps=0.05)
    colors = [color_index[v] for v in cm.fit_predict(points)]

    plt.scatter(vis_x, vis_y, s=50, c=new_color_list)
    # for i, txt in enumerate(txt_list):
    #     plt.annotate(txt, (vis_x[i], vis_y[i]))
    # for j in range(0, len(vis_x), 3):
    #     plt.plot([vis_x[j], vis_x[j + 1]], [vis_y[j], vis_y[j + 1]], "r--")
    #     plt.plot([vis_x[j + 1], vis_x[j + 2]], [vis_y[j + 1], vis_y[j + 2]], "r--")
    plt.show()

if False:
    plt.figure(1)
    plt.title("O")
    # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
    txt_list = ['starch', 'amylase', 'maltose', 'maltase', 'sucrose', 'sucrase', 'lactose', 'lactase']

    X = np.asarray(get_model_vec(txt_list))
    m = PCA(n_components=2)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]


    for i, txt in enumerate(txt_list):
        plt.annotate(txt, (vis_x[i], vis_y[i]))
    for j in range(0, len(vis_x), 2):
        for k in range(2):
            plt.plot([vis_x[j], vis_x[j + k]], [vis_y[j], vis_y[j + k]], "r--")
    plt.show()


# plt.figure(1)
# plt.title("CellLines")
# # txt_list = ['BRAF', 'V600E', 'BRAF', 'Val600Glu']
# txt_list = [v.strip() for v in open('/home/sunkyu/workspace/BioWord2Vec/res/cell_line_list.txt')]
# X = np.asarray(get_model_vec(txt_list))
# # m = PCA(n_components=2)
# m = TSNE(n_components=2)
#
# points = m.fit_transform(X)
# vis_x = points[:, 0]
# vis_y = points[:, 1]
#
# plt.scatter(vis_x, vis_y, s=50)
# for i,txt in enumerate(txt_list):
#     plt.annotate(txt, (vis_x[i], vis_y[i]))
# # for j in range(0,len(vis_x),2):
# #     for k in range(2):
# #         plt.plot([vis_x[j],vis_x[j+k]], [vis_y[j],vis_y[j+k]], "r--")
# plt.show()
