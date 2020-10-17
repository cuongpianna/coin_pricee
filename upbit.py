import websocket
import json
from models import db, Exchange, Action
import redis
from datetime import datetime

r = redis.Redis()

try:
    import thread
except ImportError:
    import _thread as thread
import time


def add_tick_action(ms):
    tick = Exchange.query.filter_by(name='upbit-tick-btc').first()
    action = Action(exchange_id=tick.id, low=ms['low_price'], open=ms['opening_price'], high=ms['high_price'],
                    close=ms['trade_price'], timestamp=ms['timestamp'], real_timestamp=datetime.now(),
                    created_at=datetime.now())
    db.session.add(action)
    db.session.commit()


def check_redis_exchange(ms, coin):
    flag = r.exists('upbit:{}'.format(coin))
    if flag == 0:
        r.set('upbit:{}'.format(coin), ms['timestamp'])
        add_tick_action(ms)
    else:
        ts = json.loads(r.get('upbit:{}'.format(coin)))
        if ts != ms['timestamp']:
            r.set('upbit:{}'.format(coin), ms['timestamp'])
            add_tick_action(ms)


def on_message(ws, message):
    ms = json.loads(message.decode('utf-8'))
    code = ms['code']
    if 'BTC' in code:
        check_redis_exchange(ms, 'btc')


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("close")


def on_open(ws):
    def run(*args):
        sendData = '[{"ticket":"test"},{"type":"ticker","codes":["KRW-BTC", "KRW-ETH"]}]'
        ws.send(sendData)
        time.sleep(2)

        ws.close()

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
