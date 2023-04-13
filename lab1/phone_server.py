import logging
from context import lab_logging
import socket
import json

from itertools import islice

import const_cs

lab_logging.setup(stream_level=logging.INFO)  # init loging channels for the lab

class PhoneServer:
    """ The phone server """
    _logger = logging.getLogger("vs2lab.lab1.phone_server.PhoneServer")
    _serving = False
    phones_dict = {}

    def __init__(self, phones = {}):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
        self._serving = True
        self.phones_dict = phones

    def serve(self):
        self.sock.listen(1)
        while self._serving:
            try:
                (connection, address) = self.sock.accept()
                while True:
                    data = connection.recv(4096).decode("ascii")
                    if not data:
                        break
                    if data.startswith("GETALL"):
                        for chunk in chunks(self.phones_dict):
                            connection.send(json.dumps(chunk).encode("ascii"))
                        connection.sendall('\x00'.encode('ascii'))
                    elif data.startswith("GET"):
                        connection.send(search(data[3:], self.phones_dict).encode("ascii"))
                    else:
                        self._logger.info("Command is not found: " + data)
                        connection.send("Command is undefined.")
                connection.close()
            except socket.timeout:
                pass
        self.close()


    def close(self):
        self.sock.close()
        self._logger.info("Server connection closed.")


def search(name="default", phones_dict = {}):
    for key, value in phones_dict.items():
        if key == name:
            return key.capitalize() + "'s" + " phone: " + value
    return "Phone does not set for this person."

def chunks(data, size=150):
   it = iter(data)
   for i in range(0, len(data), size):
      yield {k:data[k] for k in islice(it, size)}