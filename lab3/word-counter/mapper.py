import zmq
import sys
import hostlist
import array

context = zmq.Context()

# identify mappers' ports from argument 1 of terminal input
map_identifier = str(sys.argv[1])
port = ''

if map_identifier == '1':
    port = hostlist.MAPPER_PORT1
elif map_identifier == '2':
    port = hostlist.MAPPER_PORT2
elif map_identifier == '3':
    port = hostlist.MAPPER_PORT3

# bind splitter's socket
splitter_sock = context.socket(zmq.PULL)
splitter_sock.bind("tcp://" + hostlist.HOST + ":" + port)
print("Mapper " + map_identifier + " connected to the port: " + port)

# Connect reducers
reducer_1 = context.socket(zmq.PUSH)
reducer_1.connect("tcp://" + hostlist.HOST + ":" + hostlist.REDUCER_PORT1)

reducer_2 = context.socket(zmq.PUSH)
reducer_2.connect("tcp://" + hostlist.HOST + ":" + hostlist.REDUCER_PORT2)

# Process tasks
print("Mapper started, await for data")
send_to_reducer_1 = 0
send_to_reducer_2 = 0

while True:
    data = splitter_sock.recv_string()
    if data.isdigit():
        reducer_1.send_string(data)
        reducer_2.send_string(data)
    data_arr = data.split()
    # send all odd numbers to reducer 2, all even to reducer 1
    for word in data_arr:
        if 97 <= ord(word[0][0]) < 109:
            reducer_1.send_string(word)
            send_to_reducer_1 += 1
        else:
            reducer_2.send_string(word)
            send_to_reducer_2 += 1

        sys.stdout.write("Send to Reducer 1: %d | Send to Reducer 2: %d   \r" % (send_to_reducer_1, send_to_reducer_2))
        sys.stdout.flush()