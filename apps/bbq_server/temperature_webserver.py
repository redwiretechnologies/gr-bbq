#!/usr/bin/env python3

#from flask_wtf import FlaskForm
from flask import Flask, render_template
import json
from threading import Lock
from flask_socketio import SocketIO
import zmq


async_mode = "threading"
ip = "localhost"
port = "4001"

smoker_data = []
cook_data = []
time_data = []

app = Flask(__name__,template_folder='./templates',static_folder='./static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# Socket to talk to flowgraph

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ("tcp://" + ip + ":" + port)
socket.setsockopt_string(zmq.SUBSCRIBE, "{")

# 0MQ to websocket

def background_thread():
    count = 0
    while True:
        msg = socket.recv_string()
        packet_data = json.loads(msg)
        smoker_data.append(packet_data['bbqTemp'])
        cook_data.append(packet_data['foodTemp'])
        time_data.append(len(time_data))
        packet_data['timeData'] = time_data[-1]
        socketio.emit('temperature', packet_data)

        print(packet_data)

# Home Page

@app.route("/")
def bbq_home():
    return render_template('bbq_home.html', smoker_data=smoker_data, cook_data=cook_data, time_data=time_data, async_mode=socketio.async_mode)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

if __name__ == '__main__':

    try:
        socketio.run(app, host='0.0.0.0')
    finally:
        print("The End")