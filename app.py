import os
import json
import time

basedir = os.path.abspath(os.path.dirname(__file__))

import requests
import redis
from flask import Flask, render_template, request, jsonify
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

r = redis.Redis(host='178.128.26.135', port=6379)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

db = SQLAlchemy(app)
cors = CORS(app, resources={r"/getData/*": {"origins": "http://localhost:8080/"}})
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

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

    upbit_btc = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-btc').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_eth = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-eth').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_eos = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-eos').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_ada = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-ada').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_ltc = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-ltc').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_bch = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-bch').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_bsv = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-bsv').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_xrp = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-xrp').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_etc = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-etc').first().id).order_by(
        Action.timestamp.desc()).first()
    upbit_trx = Action.query.filter_by(exchange_id=Exchange.query.filter_by(name='upbit-tick-trx').first().id).order_by(
        Action.timestamp.desc()).first()
    prices = [upbit_btc.close, upbit_eth.close, upbit_eos.close, upbit_ada.close, upbit_ltc.close, upbit_bch.close,
              upbit_bsv.close, upbit_xrp.close, upbit_etc.close, upbit_trx.close]
    return render_template('index.html', res=res, upbits=json.dumps(result_upbits), prices=prices)


@app.route('/change_currency/', methods=['GET', 'POST'])
def change_currency():
    exchange_upbit = Exchange.query.filter_by(name='upbit-1m-{}'.format(request.form['data'])).first()

    upbits = Action.query.filter_by(exchange_id=exchange_upbit.id).order_by(Action.timestamp.desc()).limit(50).all()
    result = []
    for item in upbits:
        result.append({
            'timestamp': item.timestamp,
            'open': item.open,
            'close': item.close,
            'high': item.high,
            'low': item.low
        })
    return jsonify({
        'result': result
    })


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


@socketio.on('connect')
def connect():
    # print('Client connected')
    global thread1
    thread1 = socketio.start_background_task(run_upbit)
    # thread2 = socketio.start_background_task(hello)


@socketio.on('currency')
def currency(message):
    value = message['value']
    r.set('current', value)


@socketio.on('disconnect')
def test_check_disconnect():
    print('Client disconnected!!!!!!!')


if __name__ == '__main__':
    socketio.run(app, debug=True, port=7777, host='0.0.0.0')
    # app.run()
