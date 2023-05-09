import pickle
import zmq
import constPipe
import sys


class Mapper:
    def __init__(self, mapper_id):
        self.mapper_id = mapper_id
        self.context = zmq.Context()
        self.pull_socket = self.context.socket(zmq.PULL)  # create a pull socket
        address1 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT1  # how and where to connect
        self.pull_socket.connect(address1)  # bind socket to address
        # Reducer 1:
        address2 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT2
        self.reducer1_socket = self.context.socket(zmq.PUSH)
        self.reducer1_socket.connect(address2)
        # Reducer 2:
        address3 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT3
        self.reducer2_socket = self.context.socket(zmq.PUSH)
        self.reducer2_socket.connect(address3)

    def run(self):
        print("Mapper {}: waiting for the sentence".format(self.mapper_id))
        while True:
            data = pickle.loads(self.pull_socket.recv())
            sentence = data[1]
            sentences_amount = data[0]
            words = sentence.split()
            print("Mapper {}: sentence is split to {}".format(self.mapper_id, words))
            for word in words:
                word = word.lower()
                socket = self.reducer1_socket if 97 <= ord(word[0][0]) < 109 else self.reducer2_socket
                socket.send(pickle.dumps((sentences_amount, word)))
            self.reducer1_socket.send(pickle.dumps((sentences_amount, 'EOF')))
            self.reducer2_socket.send(pickle.dumps((sentences_amount, 'EOF')))
                #  By using a hash function, the words can be distributed evenly between the two reducers.


if __name__ == "__main__":
    mapper = Mapper(str(sys.argv[1]))
    mapper.run()
