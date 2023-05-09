import sys
import time
import zmq
import hostlist
import pprint

pp = pprint.PrettyPrinter(indent=4)
context = zmq.Context()

# Bind reducers' sockets
sinker_sock = context.socket(zmq.PULL)
sinker_sock.bind("tcp://" + hostlist.HOST + ":" + hostlist.SINKER_PORT)

text = {}
rcv_words_counter = 0
words_counter = 0
while True:
    receive_data = sinker_sock.recv_string()
    if receive_data.isdigit():
        rcv_words_counter = receive_data
        print(rcv_words_counter)
    else:
        if int(words_counter) >= int(rcv_words_counter):
            text = {}
        data = eval(receive_data)
        for key, value in data.items():
            if key not in text:
                text[key] = value
            else:
                text[key] += value
            words_counter += value
        pp.pprint(text)