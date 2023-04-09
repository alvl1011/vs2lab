"""

Phone client server UNIT tests

"""

import logging
import threading
import unittest

import phone_server
import phone_client
from context import lab_logging

from phone_dictionary import phone_dictionary

lab_logging.setup(stream_level=logging.INFO)

class TestPhoneServer(unittest.TestCase):
    _server = phone_server.PhoneServer(phone_dictionary)  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running serve
    names = ['vladi', 'shoaib', 'nico', 'default']
    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = phone_client.PhoneClient()  # create new client for each test

    # def test_receive_getall(self):
    #     msg = self.client.getall()
    #     self.assertEqual(msg, phone_dictionary)
    #
    # def test_receive_get(self):
    #     for name in self.names:
    #         msg = self.client.get(name)
    #         self.assertEqual(msg.split('\'')[0].lower(), name)

    def test_getall_500(self):
        phone_dict = {}
        for i in range(1, 500):
            phone_dict["Testuser" + str(i)] = str(i)
        print(phone_dict)
        self._server.phones_dict = phone_dict
        msg = self.client.getall()
        self.assertEqual(msg, phone_dict)

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate

if __name__ == '__main__':
    unittest.main()
