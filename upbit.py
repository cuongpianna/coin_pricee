import websocket
from websocket import create_connection
import json
from app import db, Exchange, Action
import redis
from datetime import datetime

r = redis.Redis(host='178.128.26.135', port=6379)

try:
    import thread
except ImportError:
    import _thread as thread
import time


def add_tick_action(ms, coin):
    try:
        r.set('upbit:data:{}'.format(coin), json.dumps(ms))
        ts = datetime.fromtimestamp(ms['timestamp'] / 1e3)
        tick = Exchange.query.filter_by(name='upbit-tick-{}'.format(coin)).first()
        if tick:
            action = Action(exchange_id=tick.id, low=ms['low_price'], open=ms['opening_price'], high=ms['high_price'],
                            close=ms['trade_price'], timestamp=ms['timestamp'], real_timestamp=datetime.now(),
                            created_at=datetime.now())
            db.session.add(action)
            db.session.commit()

        coin_compare_ts = datetime.fromtimestamp(int(r.get('upbit:btc').decode('utf-8')) / 1e3)
        print(ts.minute)
        print(coin_compare_ts.minute)
        if ts.minute != coin_compare_ts.minute:
            print('cuong')
            tick = Exchange.query.filter_by(name='upbit-1m-{}'.format(coin)).first()
            if tick:
                action = Action(exchange_id=tick.id, low=ms['low_price'], open=ms['opening_price'],
                                high=ms['high_price'],
                                close=ms['trade_price'], timestamp=ms['timestamp'], real_timestamp=datetime.now(),
                                created_at=datetime.now())
                db.session.add(action)
                db.session.commit()

        if coin_compare_ts.minute % 5 == 0 and ts.minute != coin_compare_ts.minute:
            tick = Exchange.query.filter_by(name='upbit-5m-{}'.format(coin)).first()
            if tick:
                action = Action(exchange_id=tick.id, low=ms['low_price'], open=ms['opening_price'],
                                high=ms['high_price'],
                                close=ms['trade_price'], timestamp=ms['timestamp'], real_timestamp=datetime.now(),
                                created_at=datetime.now())
                db.session.add(action)
                db.session.commit()

        if coin_compare_ts.minute % 10 == 0 and ts.minute != coin_compare_ts.minute:
            tick = Exchange.query.filter_by(name='upbit-10m-{}'.format(coin)).first()
            if tick:
                action = Action(exchange_id=tick.id, low=ms['low_price'], open=ms['opening_price'],
                                high=ms['high_price'],
                                close=ms['trade_price'], timestamp=ms['timestamp'], real_timestamp=datetime.now(),
                                created_at=datetime.now())
                db.session.add(action)
                db.session.commit()

    except:
        pass


def check_redis_exchange(ms, coin):
    flag = r.exists('upbit:{}'.format(coin))
    if flag == 0:
        r.set('upbit:{}'.format(coin), ms['timestamp'])
        add_tick_action(ms, coin)
    else:
        ts = json.loads(r.get('upbit:{}'.format(coin)))
        if ts != ms['timestamp']:
            add_tick_action(ms, coin)
            r.set('upbit:{}'.format(coin), ms['timestamp'])


def on_message(ws, message):
    ms = json.loads(message.decode('utf-8'))
    code = ms['code']
    if 'BTC' in code:
        check_redis_exchange(ms, 'btc')
    if 'ETH' in code:
        check_redis_exchange(ms, 'eth')
    if 'EOS' in code:
        check_redis_exchange(ms, 'eos')
    if 'ADA' in code:
        check_redis_exchange(ms, 'ada')
    if 'LTC' in code:
        check_redis_exchange(ms, 'ltc')
    if 'BCH' in code:
        check_redis_exchange(ms, 'bch')
    if 'BSV' in code:
        check_redis_exchange(ms, 'bsv')
    if 'XRP' in code:
        check_redis_exchange(ms, 'xrp')
    if 'ETC' in code:
        check_redis_exchange(ms, 'etc')
    if 'TRX' in code:
        check_redis_exchange(ms, 'trx')


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("close")


def on_open(ws):
    def run(*args):
        sendData = '[{"ticket":"test"},{"type":"ticker","codes":["KRW-BTC", "KRW-ETH", "KRW-EOS", "KRW-ADA", "KRW-LTC", "KRW-BCH", "KRW-BSV", "KRW-XRP", "KRW-ETC", "KRW-TRX"]}]'
        ws.send(sendData)
        time.sleep(2)

        ws.close()

    thread.start_new_thread(run, ())


def run():
    try:
        ws = create_connection("wss://api.upbit.com/websocket/v1")
        ws.send('[{"ticket":"test"},{"type":"ticker","codes":["KRW-BTC"]}]')
        # print("Sent")
        # print("Receiving...")
        result = ws.recv()
        print("Received '%s'" % result)

        ms = json.loads(result.decode('utf-8'))
        code = ms['code']
        if 'BTC' in code:
            check_redis_exchange(ms, 'btc')
        ws.close()
    except:
        pass


if __name__ == "__main__":
    while True:
        ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.on_open = on_open
        ws.run_forever()
        time.sleep(0.1)
        # run()
        # time.sleep(.1)
