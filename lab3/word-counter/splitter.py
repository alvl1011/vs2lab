import hostlist
import time
import zmq
import random
import sys
import re

try:
    raw_input
except NameError:
    # Python 3
    raw_input = input

context = zmq.Context()

# Connect mappers
map1 = context.socket(zmq.PUSH)
map1.connect("tcp://" + hostlist.HOST + ":" + hostlist.MAPPER_PORT1)

map2 = context.socket(zmq.PUSH)
map2.connect("tcp://" + hostlist.HOST + ":" + hostlist.MAPPER_PORT2)

map3 = context.socket(zmq.PUSH)
map3.connect("tcp://" + hostlist.HOST + ":" + hostlist.MAPPER_PORT3)

print("Mappers bound")

sinker_sock = context.socket(zmq.PUSH)
sinker_sock.connect("tcp://" + hostlist.HOST + ":" + hostlist.SINKER_PORT)

# Initialize random number generator
random.seed()

# Read text from file
with open("text.txt") as file:
    content = file.readlines()
    content = [c.strip() for c in content]

counter = 0
send_to_map_1 = 0
send_to_map_2 = 0
send_to_map_3 = 0

print("Press Enter when the workers are ready: ")

words_counter = 0
while True:
    _ = raw_input()
    #count all words
    for l in content:
        l = re.sub('[!@#$-:,."",?]', "", l.lower())
        words_counter += len(l.split())
    map1.send_string(str(words_counter))
    map2.send_string(str(words_counter))
    map3.send_string(str(words_counter))
    words_counter = 0

    #send to mapper
    for l in content:
        l = re.sub('[!@#$-:,."",?]', "", l.lower())
        if counter % 3 == 0:
            map3.send_string(l)
            send_to_map_3 += 1
        elif counter % 3 == 1:
            map1.send_string(l)
            send_to_map_1 += 1
        elif counter % 3 == 2:
            map2.send_string(l)
            send_to_map_2 += 1

        sys.stdout.write("Send to Map 1: %d | Send to Map 2: %d | Send to Map 3: %d  \r" % (send_to_map_1, send_to_map_2, send_to_map_3))
        sys.stdout.flush()
        counter += 1
        # Give 0MQ time to deliver
        time.sleep(1)
