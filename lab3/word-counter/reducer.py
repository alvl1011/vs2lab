import sys
import time
import zmq
import hostlist
import json

context = zmq.Context()

reducer_identifier = str(sys.argv[1])
port = ''

if reducer_identifier == '1':
    port = hostlist.REDUCER_PORT1
elif reducer_identifier == '2':
    port = hostlist.REDUCER_PORT2

# Bind mapper's socket
mapper_sock = context.socket(zmq.PULL)
mapper_sock.bind("tcp://" + hostlist.HOST + ":" + port)
print("Reducer " + reducer_identifier + " connected to the port: " + port)

sinker_sock = context.socket(zmq.PUSH)
sinker_sock.connect("tcp://" + hostlist.HOST + ":" + hostlist.SINKER_PORT)

text = {}
word_amount = 0
counter = 0
while True:
    data = mapper_sock.recv_string()
    if data.isdigit():
        word_amount = data
        sinker_sock.send_string(str(word_amount))
        if int(counter) >= int(word_amount):
            text = {}
            word_amount = 0
    elif data not in text:
        text[data] = 1
    else:
        text[data] += 1
    counter += 1
    print(text)
    sinker_sock.send_string(json.dumps(text))