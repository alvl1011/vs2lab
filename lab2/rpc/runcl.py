import rpc
import logging
import time
from image import image

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)

def print_result(result):
    print("Result: {}".format(result.value))

cl = rpc.Client()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, print_result)

time.sleep(1)
print("[Client] Here client does something")
time.sleep(1)
print("[Client] Here is a simulation of work")
time.sleep(1)
print("[Client] Are you boring?")
time.sleep(1)
print("[Client] I can show something to you")
time.sleep(1)
print("[Client] Ready?")
time.sleep(1)
print("[Client] Don't be so shy")
time.sleep(1)
print(image)
time.sleep(3)

cl.stop()
