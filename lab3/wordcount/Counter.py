import pickle
import zmq
import constPipe


class Counter:
    def __init__(self):
        self.context = zmq.Context()
        address = "tcp://" + constPipe.SRC + ":" + constPipe.PORT4  # how and where to connect
        self.pull_socket = self.context.socket(zmq.PULL)
        self.pull_socket.bind(address)

        self.text = {}
        self.recv_counter = 0

    def run(self):
        while True:
            data = pickle.loads(self.pull_socket.recv())
            recv_text = data[1]
            self.text.update(data[1])
            for key, value in recv_text.items():
                if key == 'EOF':
                    if value == data[0]:
                        self.recv_counter += 1
            if self.recv_counter == 2:
                break
        self.text = {k: v for k, v in self.text.items() if k != 'EOF'}
        print(self.text)



if __name__ == "__main__":
    counter = Counter()
    counter.run()
