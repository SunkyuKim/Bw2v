import os
from socket import *
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import numpy as np

# wsd_res_dir = "../res/ncbi wsd 2013/all/"
wsd_res_dir = "../res/ncbi wsd 2013/wsd2013_ner/"
around_num = 3

def __get_model_vec(name, port):
    HOST = 'localhost'
    # PORT = 21567
    PORT = port
    BUFSIZ = 4096
    ADDR = (HOST, PORT)

    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)

    input = "vec#"+name
    tcpCliSocket.send(input)
    vector_str = tcpCliSocket.recv(BUFSIZ)
    if "no vec" in vector_str:
        result = None
    else:
        result = [float(v) for v in vector_str.split('\t')]
    tcpCliSocket.close()
    return result

def get_model_vec(name_list, port):
    return [__get_model_vec(v, port) for v in name_list]

def test(f, port):
    windows = dict()
    notinwindows = list()

    for l in open(wsd_res_dir+f):
        tokens = l.split('\t')
        if tokens[2] not in windows:
            windows[tokens[2]] = list()
        windows[tokens[2]] += get_windows(tokens[0], tokens[1])

    concat_vector_list = list()
    colors = list()
    color_index = ['red','blue','green','yellow']
    for i in range(len(windows.keys())):
        key = windows.keys()[i]
        for window in windows[key]:
            concat_vector = []
            len_vector = 0
            for vector in get_model_vec(window, port):
                if vector == None:
                    continue
                concat_vector.extend(vector)
                len_vector = len(vector)

            if len(concat_vector) == (2*around_num+1)*len_vector:
                concat_vector_list.append(concat_vector)
                colors.append(color_index[i])
            else:
                notinwindows.append(window)
    print f, len(concat_vector_list)
    if len(concat_vector_list) == 0:
        return notinwindows
    make_plot(concat_vector_list, colors, f)
    return notinwindows

def make_plot(X, colors, title):
    # print X
    m = PCA(n_components=2)
    # m = TSNE(n_components=2)

    plt.figure()
    plt.title(title)

    points = m.fit_transform(X)
    vis_x = points[:, 0]
    vis_y = points[:, 1]

    color_index = ['red', 'blue', 'green', 'yellow']
    # cm = KMeans(n_clusters=4)
    # cm = DBSCAN(eps=0.05)
    # print cm.fit_predict(points)
    # colors = [color_index[v] for v in cm.fit_predict(points)]

    plt.scatter(vis_x, vis_y, c=colors, s=50)

    plt.savefig("../res/ncbi wsd 2013/w2v300_ner/%s" % title.replace('.', '_'))
    plt.show()

def get_windows(sentence, entity):
    result_list = []
    tokens_unprocessed = sentence.replace('<e>', '').replace('</e>', '').split()
    tokens = []
    for t in tokens_unprocessed:
        if len(t) == 0:
            continue
        if t[len(t)-1] == '.':
            t = t.replace('.', '')
        if len(t) == 0:
            continue
        if t[len(t) - 1] == ';':
            t = t.replace(';', '')
        tokens.append(t)
        # print t

    for i in range(len(tokens)):
        if tokens[i] == entity:
            start = max(0,i-around_num)
            end = min(i+around_num+1,len(tokens))
            result_list.append(tokens[start:end])
    return result_list


def do_wsd():
    import time
    fnames = os.listdir(wsd_res_dir)
    err_file= open("../res/ncbi wsd 2013/w2v300_ner/error_log.txt",'w')
    for f in fnames:
        d1 = test(f, 21568)
        # d2 = test(f, 21568)

        # print "**onlyd1**"
        # onlyd1 = [v for v in d1 if v in d2]
        # for l in onlyd1:
        #     print l
        #
        # print "**onlyd2**"
        # onlyd2 = [v for v in d2 if v not in d1]
        # for l in onlyd2:
        #     print l
        time.sleep(3)
        # break
        # try:
        #     test(f)
        #     time.sleep(3)
        # except:
        #     err_file.write(f)
        #     err_file.write('\n')
    err_file.close()


if __name__ == '__main__':
    do_wsd()
    # print get_model_vec(['plants.'], 21568)
