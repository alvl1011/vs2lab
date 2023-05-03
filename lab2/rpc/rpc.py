import constRPC
import threading
import time

from context import lab_channel
from image import image


class DBList:
    def __init__(self, basic_list):
        self.value = list(basic_list)

    def append(self, data):
        self.value = self.value + [data]
        return self


class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.chan = lab_channel.Channel()
        self.client = self.chan.join('client')
        self.server = None
        self.chan.bind(self.client)
        self.server = self.chan.subgroup('server')
        self.queue = []
        self.callback = None

    def run(self):
        print("[Thread] Waiting for response")
        received_message = self.chan.receive_from(self.server)
        print("[Thread] Response received")
        self.callback(received_message[1])


    def stop(self):
        self.chan.leave('client')

    def ack_waiting(self):
        received_message = self.chan.receive_from(self.server)
        if received_message[1] == constRPC.OK :
            print("[Client] ACK received")
            return

    def append(self, data, db_list, callback):
        assert isinstance(db_list, DBList)
        msglst = (constRPC.APPEND, data, db_list)  # message payload
        self.chan.send_to(self.server, msglst)  # send msg to server
        self.ack_waiting()
        self.start()
        self.callback = callback


class Server:
    def __init__(self):
        self.chan = lab_channel.Channel()
        self.server = self.chan.join('server')
        self.timeout = 3

    @staticmethod
    def append(data, db_list):
        assert isinstance(db_list, DBList)  # - Make sure we have a list
        return db_list.append(data)

    @staticmethod
    def send_ack(client, chan):
        chan.send_to({client}, constRPC.OK)

    def run(self):
        self.chan.bind(self.server)
        while True:
            msgreq = self.chan.receive_from_any(self.timeout)  # wait for any request
            if msgreq is not None:
                client = msgreq[0]  # see who is the caller
                msgrpc = msgreq[1]  # fetch call & parameters
                if constRPC.APPEND == msgrpc[0]:  # check what is being requested
                    self.send_ack(client, self.chan)
                    request_processing_timer(10)
                    print("\n[Server] Request processed")
                    result = self.append(msgrpc[1], msgrpc[2])  # do local call
                    self.chan.send_to({client}, result)  # return response
                else:
                    pass  # unsupported request, simply ignore

def request_processing_timer(seconds):
    print("[Server] Request processing")
    i = 1
    while i < seconds:
        dots = '.' * i
        print("\r{}".format(dots), flush=True, end='')
        time.sleep(1)
        i += 1