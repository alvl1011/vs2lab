import logging
import socket
import json

import const_cs
from phone_dictionary import phone_dictionary as phones

class PhoneServer:
    """ The phone server """
    _logger = logging.getLogger("[vs2lab.lab1.phone-server.PhoneServer]")
    _serving = False
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((const_cs.HOST, const_cs.PORT))
        self.sock.settimeout(3)  # time out in order not to block forever
        self._logger.info("Server bound to socket " + str(self.sock))
    def serve(self):
        self.sock.listen(1)
        while self._serving:
            try:
                (connection, address) = self.sock.accept()
                while True:
                    data = connection.recv(1024).decode("ascii")
                    if not data:
                        break
                    if data.startswith("GET"):
                        connection.send(search(data[3:]).encode("ascii"))
                    elif data.startswith("GETALL"):
                        connection.send(json.dumps(phones).encode("ascii"))
                    else:
                        self._logger.error("Command is not found: " + data)
                        connection.send("Command is undefined.")
                connection.close()
            except socket.timeout:
                pass
        self.close()
    def close(self):
        self.sock.close()
        self._logger.info("Server connection closed.")


def search(name="default"):
    for key, value in phones.items():
        if key == name:
            return key.capitalize() + "'s" + " phone: " + value
    return "Phone does not set for this person."


