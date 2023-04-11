from phone_server import PhoneServer
from phone_dictionary import phone_dictionary

server = PhoneServer(phone_dictionary)

server.serve()