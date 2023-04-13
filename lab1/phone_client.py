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
        phone_data = {}
        chunks = []
        while True:
            data = self.sock.recv(4096)
            if data.decode('ascii').endswith('\x00'):
                tmp = data.decode('ascii').split('\x00')[0].encode('ascii')
                if tmp != "".encode('ascii'):
                    chunks.append(tmp)
                break
            chunks.append(data)

        for chunk in chunks:
            for k, v in json.loads(chunk.decode('ascii')).items():
                phone_data.update({k: v})
        print('\n ALL:')
        format(phone_data)
        return phone_data
    def close(self):
        self.sock.close()
        self.logger.info("Client connection is down.")


def format(data):
    for key, value in data.items():
        print("\t" + key.capitalize() + "'s" + " phone: " + value)

def fill_dict(dict, out_dict):
    for key, value in dict.items():
        out_dict.update({key: value})
    return out_dict