"""
Simple client server unit test for phone dictionary
"""

import logging
import threading
import unittest

from phone_server import PhoneServer
from phone_client import PhoneClient
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestPhoneDictionary1(unittest.TestCase): # test if the server give the right result for dictionary search with "nico"
    """Test to search in the dictonary"""
    _server = PhoneServer()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = PhoneClient()  # create new client for each test

    def test_srv_getNico(self):  # each test_* function is a test
        """Test simple get nico"""
        msg = self.client.get("nico")
        self.assertEqual(msg, "Nico's phone: 555-52145")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


class TestPhoneDictionary2(unittest.TestCase): # test if the server give the right result for dictionary search with "shoaib"
    """Test to search in the dictonary"""
    _server = PhoneServer()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = PhoneClient()  # create new client for each test

    def test_srv_getShoaib(self):  # each test_* function is a test
        """Test simple get shoaib"""
        msg = self.client.get("shoaib")
        self.assertEqual(msg, "Shoaib's phone: 555-58954")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate

class TestPhoneDictionary3(unittest.TestCase): # test if the server give the right result for dictionary search with "get all"
    """The test to get all entries from the dictionary"""
    _server = PhoneServer()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = PhoneClient()  # create new client for each test

    def test_srv_getAll(self):  # each test_* function is a test
        """Test simple get all"""
        msg = self.client.getall()
        self.assertEqual(msg, "{\"default\": \"555-default\", \"vladi\": \"+49 1517 5489401\", \"shoaib\": \"555-58954\", \"nico\": \"555-52145\"}")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate

class TestPhoneDictionary4(unittest.TestCase): # test if the server give the right result for dictionary search with a name which is not in the dictionary
    """The test checks if it come the expected result if there is a input which is not in the dictionary """
    _server = PhoneServer()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.serve)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = PhoneClient()  # create new client for each test

    def test_srv_get(self):  # each test_* function is a test
        """Test simple get all"""
        msg = self.client.get("no")
        self.assertEqual(msg, "Phone does not set for this person.")

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate



if __name__ == '__main__':
    unittest.main()
