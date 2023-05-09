import pickle
import requests
import zmq
import constPipe
import re


class Splitter:  # in this Class we have to get a text, which will be split and sent to Mapper.
    def __init__(self, text):
        self.text = text
        self.context = zmq.Context()
        self.push_socket = self.context.socket(zmq.PUSH)  # create a push socket
        self.address = "tcp://" + constPipe.SRC + ":" + constPipe.PORT1  # how and where to connect
        self.push_socket.bind(self.address)  # bind socket to address
        self.count = 0

    def run(self):
        print(self.text)
        sentences = self.text.split(".")
        print("Length of sentences: {}".format(len(sentences)-1))
        for i in range(len(sentences)):  # iteration in sentences exclusive last sentence (empty)
            self.count += 1  # increment the counter to use as unique ID for each sentences as message.
            print(str(i) + ": " + sentences[i])
            self.push_socket.send(pickle.dumps((len(sentences), re.sub('[!@#$-:,."",?]', "", sentences[i]))))  # send the message to mapper


if __name__ == "__main__":
    with open("text.txt") as file:
        text = file.read()

    splitter = Splitter(text)

    input("Start Mapper and hit a button...")
    splitter.run()
