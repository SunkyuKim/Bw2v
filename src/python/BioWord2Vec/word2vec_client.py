"""
use pickle?
"""
from socket import *

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSocket = socket(AF_INET, SOCK_STREAM)
tcpCliSocket.connect(ADDR)

input = ""
tcpCliSocket.send(input)
vector_str = tcpCliSocket.recv(BUFSIZ)
result = [float(v) for v in vector_str.split('\t')]

print result
