# Example of a PUB server using ZeroMQ taken from
#   https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html
#
# 17 Feb 2023

import zmq
import random
import time
import json

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://localhost:4001")

time_data = 11

while True:
    messagedata = {"smokerData": random.randrange(1,215) - 80, "cookData": random.randrange(1,215) - 80, "timeData": time_data}
    print(messagedata)
    msg = json.dumps(messagedata)
    # socket.send_json(messagedata)
    socket.send_string(msg)
    # socket.send(mdp)
    time_data += 1
    time.sleep(1)