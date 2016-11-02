"""
use pickle?
"""
import numpy as np
from sklearn.decomposition import PCA
from socket import *
from gensim.models import word2vec
import config
from time import strftime, time
import json
import sys
import codecs

dictionary = open(config.path['dictionary'],'r')
entity_dict = dict()
for l in dictionary:
    tokens = l.split("\t")
    name = tokens[1].strip()
    entitytype = tokens[2].strip()
    entity_dict[name] = entitytype

model = word2vec.Word2Vec.load_word2vec_format(config.path['word2vec_model'], binary=True)

HOST = ''
PORT = 21567
BUFSIZ = 4096
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(30)


class numpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(numpyEncoder, self).default(obj)

def recv_all(the_socket, timeout=2):
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    print "start"
    #beginning time
    begin=time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data)

def get_data(pos_queries, neg_queries, nearTopn):
    valid_pos_queries = [v for v in pos_queries if v in model]
    valid_neg_queries = [v for v in neg_queries if v in model]
    valid_queries = valid_pos_queries + valid_neg_queries
    simTerms = []

    queryWithSim = valid_pos_queries + valid_neg_queries
    if nearTopn > 0:
        simTerms = [t[0] for t in model.most_similar(positive=valid_pos_queries, negative=valid_neg_queries, topn=nearTopn)]
        queryWithSim += simTerms
    
        print queryWithSim

    vectors = [model[v] for v in queryWithSim]
    return {"terms":queryWithSim, "vectors":vectors, "query":valid_queries, "similar_terms":simTerms}

def make_return_data(terms, vectors):
    if len(vectors) == 0: 
        return {"filepath":'null', "reduced_data":'null'}
    terms_with_space = map(lambda x:x.replace("_"," "),terms)
    vecstr = ["\t".join(map(lambda y : str(y),x)) for x in  vectors]
    vec_with_term = map(lambda x, y: x+"\t"+y, terms_with_space, vecstr)
    send_str = "\n".join(vec_with_term)

    temp_file_path = 'temp_files/' + strftime("%y_%m_%d_%H_%M_%S") + '.txt' 
    #with open('templates/' + temp_file_path, 'w') as fw:
    with codecs.open('templates/' + temp_file_path, 'w', 'utf-8-sig') as fw:
        fw.write(send_str)
    if len(vectors) == 1:
        return {"filepath":temp_file_path, "reduced_data":'null'}
    # vector_mat = np.asarray(vectors)
    # pcam = PCA(n_components=2)
    # reduced_vectors = pcam.fit_transform(vector_mat)

    types = list()
    print terms_with_space
    print vectors

    for term in terms_with_space:
        term_unicode = term.encode('ascii', 'ignore')
        if term not in entity_dict.keys():
            types.append("Not Identified")
        else:
            types.append(entity_dict[term])
    # reduced_data = map(lambda x, y, z: {"term":x, "x":y[0], "y":y[1], "type":z}, terms_with_space, reduced_vectors, types)

    # return {"filepath":temp_file_path, "terms":terms_with_space, "reduced_data":reduced_data}
    return {"filepath":temp_file_path, "terms":terms_with_space}

def make_XY(terms, vectors):
    terms_with_space = map(lambda x: x.replace("_", " "), terms)
    vector_mat = np.asarray(vectors)
    pcam = PCA(n_components=2)
    reduced_vectors = pcam.fit_transform(vector_mat)

    print vector_mat
    print reduced_vectors

    types = list()
    for term in terms_with_space:
        term_unicode = term.encode('ascii', 'ignore')
        if term not in entity_dict.keys():
            types.append("Not Identified")
        else:
            types.append(entity_dict[term])
    reduced_data = map(lambda x, y, z: {"term": x, "x": y[0], "y": y[1], "type": z}, terms_with_space, reduced_vectors,
                       types)
    return {"reduced_data":reduced_data}

while True:
#  try:
    print 'waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()
    print '...connected from:', addr
    while True:
#        input = tcpCliSock.recv(BUFSIZ)
        input = recv_all(tcpCliSock)
        if not input:
            break

        request = json.loads(input)
        command = request["command"]

        print ("command: "+command)

        if command == "get":
            pos_query = request["pos_query"]
            neg_query = request["neg_query"]
            topn = request["topn"]
            data = get_data(pos_query, neg_query, topn)
            terms = data["terms"]
            vectors = data["vectors"]

            return_data = make_return_data(terms, vectors)
            tcpCliSock.sendall(json.dumps(return_data, cls=numpyEncoder))
        elif command == "get_XY":
            filename = request["filepath"]

            terms = []
            vectors = []
            for l in open(filename):
                tokens = l.split("\t")
                if len(tokens) < 100:
                    continue
                terms.append(tokens[0])
                vectors.append(tokens[1:])
            return_data = make_XY(terms=terms, vectors=vectors)
            tcpCliSock.sendall(json.dumps(return_data, cls=numpyEncoder))

        elif command == "get_similarity":
            termA = request["termA"]
            termB = request["termB"]
            if (termA not in model) or (termB not in model):
                tcpCliSock.sendall(json.dumps({"similarity":"null"}, cls=numpyEncoder))
            else:
                tcpCliSock.sendall(json.dumps({"similarity":str(model.similarity(termA, termB))}, cls=numpyEncoder))
        else:
            pass
        break
    tcpCliSock.close()
"""
  except KeyboardInterrupt:
    tcpSerSock.close()
    sys.exit()
  except Exception as e:
    tcpCliSock.close()
    print "ERROR:%s"%e
"""
tcpSerSock.close()
