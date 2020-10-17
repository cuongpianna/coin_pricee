from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from threading import Thread, Event
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))

try:
    import thread
except ImportError:
    import _thread as thread
import time

import requests
import json
import websocket
from websocket import create_connection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/getData/*": {"origins": "http://localhost:8080/"}})
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:8080")

thread1 = Thread()
thread2 = Thread()


@app.route('/')
def index():
    res = requests.get('https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=60').text
    return render_template('index.html', res=res)


def run_upbit():
    while True:
        ws = create_connection("wss://api.upbit.com/websocket/v1")
        print('ssss')
        ws.send('[{"ticket":"test"},{"format":"SIMPLE"},{"type":"ticker","codes":["KRW-BTC"]}]')
        print("Sent")
        print("Receiving...")
        result = ws.recv()
        print("Received '%s'" % result)
        ws.close()
        socketio.emit('test', {'number': 'cuong'})
        time.sleep(.5)


def hello():
    while True:
        time.sleep(0.5)
        print('helo')


@socketio.on('getData')
def handle_my_custom_event(json):
    run_upbit()
    return 'one', 2


@socketio.on('connect')
def connect():
    print('Client connected')
    global thread1
    thread1 = socketio.start_background_task(run_upbit)
    thread2 = socketio.start_background_task(hello)


@socketio.on('disconnect')
def test_check_disconnect():
    print('Client disconnected!!!!!!!')


if __name__ == '__main__':
    socketio.run(app)
    # app.run()
