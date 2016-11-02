from socket import *
from gensim.models import word2vec

HOST = 'localhost'
PORT = 21567
BUFSIZ = 4096
ADDR = (HOST, PORT)

model = word2vec.Word2Vec.load_word2vec_format(
    "/home/sunkyu/workspace/BioWord2Vec/res/word2vec/fixed_model_160526.bin", binary=True)

def go(query):
    # if query in model.vocab:
    #     rs = model.most_similar(positive=[query])
    input = "vec#" + query
    tcpCliSocket = socket(AF_INET, SOCK_STREAM)
    tcpCliSocket.connect(ADDR)
    tcpCliSocket.send(input)
    vector_str = tcpCliSocket.recv(BUFSIZ)
    result = [v for v in vector_str.split('\t')]
    tcpCliSocket.close()
    return result
    # return [float(v.replace('[','').replace(']','')) for v in result[0].split()]

# with open("../res/verbListFromBRONCO_noTab_vector_100dim.txt", "w") as fw:
#     for l in open("../res/verbListFromBRONCO_noTab.txt"):
#         word = l.strip()
#         vec = go(word)
#         vec_str = "\t".join([str(v) for v in vec])
#         if len(vec) != 100:
#             vec_str = ""
#         fw.write(word + "\t" + vec_str + "\n")
#
# with open("../res/verbListFromEMU_noTab_vector_100dim.txt", "w") as fw:
#     for l in open("../res/verbListFromEMU_noTab.txt"):
#         word = l.strip()
#         vec = go(word)
#         vec_str = "\t".join([str(v) for v in vec])
#         if len(vec) != 100:
#             vec_str = ""
#         fw.write(word + "\t" + vec_str + "\n")

with open('../res/Four_words.txt' , 'w') as fw:

    fw.write('\t'.join(['proved'] + [str(v) for v in model['proved']]))
    fw.write('\n')
    fw.write('\t'.join(['prove'] + [str(v) for v in model['prove']]))
    fw.write('\n')
    fw.write('\t'.join(['exhibit'] + [str(v) for v in model['exhibit']]))
    fw.write('\n')
    fw.write('\t'.join(['exhibits'] + [str(v) for v in model['exhibits']]))
