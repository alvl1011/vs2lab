import pickle
import zmq
import constPipe
import sys


class Reducer:
    def __init__(self, reducer_id):
        self.reducer_id = reducer_id
        self.context = zmq.Context()
        port = constPipe.PORT2 if self.reducer_id == "1" else constPipe.PORT3

        address1 = "tcp://" + constPipe.SRC + ":" + port  # how and where to connect
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind(address1)

        address2 = "tcp://" + constPipe.SRC + ":" + constPipe.PORT4  # Counter
        self.counter_socker = self.context.socket(zmq.PUSH)
        self.counter_socker.connect(address2)

        self.word_dict = {}
        self.eof_counter = 0

    def run(self):
        while True:
            data = pickle.loads(self.pull_socket.recv())

            if data[1] not in self.word_dict:
                self.word_dict[data[1]] = 1
            else:
                self.word_dict[data[1]] += 1
            print(self.word_dict)
            self.counter_socker.send(pickle.dumps((data[0], self.word_dict)))

            if 'EOF' in self.word_dict:
                if self.word_dict['EOF'] == data[0]:
                    self.word_dict = {}




if __name__ == "__main__":
    reducer = Reducer(str(sys.argv[1]))
    reducer.run()
