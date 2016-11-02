import os

dir = "/media/sunkyu/327680A376806985/workspace/pubmed_sentences/"
filenames = os.listdir(dir)

with open("../res/GloVe-1.2/onefile.txt", "w") as fw:
    for name in filenames:
        for l in open(dir + name):
            fw.write(l)