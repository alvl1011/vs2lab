import json
import logging
import socket

import const_cs
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

class PhoneClient:

    logger = logging.getLogger("vs2lab.lab1.phone_client.PhoneClient")
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((const_cs.HOST, const_cs.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))


    def get(self, name="default"):
        self.sock.send(("GET" + name).encode('ascii'))
        data = self.sock.recv(1024)
        phone_data = data.decode('ascii')
        print(phone_data)
        return phone_data
    def getall(self):
        self.sock.send("GETALL".encode('ascii'))
        data = self.sock.recv(1024)
        phone_data = data.decode('ascii')
        print('\n ALL:')
        format(json.loads(phone_data))
        return json.loads(phone_data)
    def close(self):
        self.sock.close()
        self.logger.info("Client connection is down.")


def format(data):
    for key, value in data.items():
        print("\t" + key.capitalize() + "'s" + " phone: " + value)