import os
import json
import time
basedir = os.path.abspath(os.path.dirname(__file__))

import requests
import redis
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from threading import Thread
from flask_sqlalchemy import SQLAlchemy
from websocket import create_connection
from utils import get_current_code

try:
    import thread
except ImportError:
    import _thread as thread

r = redis.Redis()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
cors = CORS(app, resources={r"/getData/*": {"origins": "http://localhost:8080/"}})
socketio = SocketIO(app, cors_allowed_origins="http://127.0.0.1:8080")

thread1 = Thread()
thread2 = Thread()

class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    actions = db.relationship('Action', backref='exchange', lazy=True)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    low = db.Column(db.Float)
    high = db.Column(db.Float)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    timestamp = db.Column(db.Integer)
    real_timestamp = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange.id'),
                            nullable=False)


@app.route('/')
def index():
    code = get_current_code()
    print(code)
    res = requests.get('https://api.upbit.com/v1/candles/minutes/1?market=KRW-BTC&count=60').text
    exchange_upbit = Exchange.query.filter_by(name='upbit-1m-btc').first()
    upbits = Action.query.filter_by(exchange_id=exchange_upbit.id).order_by(Action.timestamp.desc()).limit(50).all()
    result_upbits = []
    for item in upbits:
        result_upbits.append({
            'timestamp': item.timestamp,
            'open': item.open,
            'close': item.close,
            'high': item.high,
            'low': item.low
        })
    return render_template('index.html', res=res, upbits=json.dumps(result_upbits))


def run_upbit():
    while True:
        if r.exists('current') == 0:
            r.set('current', 'btc')

        if r.exists('bar') == 0:
            r.set('bar', '60')

        current = r.get('current').decode('utf-8')
        bar = int(r.get('bar').decode('utf-8'))
        upbit = r.get('upbit:data:{}'.format(current)).decode('utf-8')
        rp = {
            "upbit": upbit
        }
        socketio.emit('coin', {"ms": rp})
        time.sleep(bar)

    # while True:
    #     ws = create_connection("wss://api.upbit.com/websocket/v1")
    #     print('ssss')
    #     ws.send('[{"ticket":"test"},{"format":"SIMPLE"},{"type":"ticker","codes":["KRW-BTC"]}]')
    #     print("Sent")
    #     print("Receiving...")
    #     result = ws.recv()
    #     print("Received '%s'" % result)
    #     ws.close()
    #     socketio.emit('test', {'number': 'cuong'})
    #     time.sleep(.5)


@socketio.on('getData')
def handle_my_custom_event(json):
    run_upbit()
    return 'one', 2


@socketio.on('connect')
def connect():
    print('Client connected')
    global thread1
    thread1 = socketio.start_background_task(run_upbit)
    # thread2 = socketio.start_background_task(hello)


@socketio.on('disconnect')
def test_check_disconnect():
    print('Client disconnected!!!!!!!')


if __name__ == '__main__':
    socketio.run(app)
    # app.run()
