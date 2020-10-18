from app import db, Exchange, Action

# db.create_all()


def create_exchange(name):
    e1 = Exchange(name=name)
    db.session.add(e1)
    db.session.commit()

create_exchange('upbit-tick-btc')
create_exchange('upbit-tick-eth')
create_exchange('upbit-tick-eos')
create_exchange('upbit-tick-ada')
create_exchange('upbit-tick-ltc')
create_exchange('upbit-tick-bch')
create_exchange('upbit-tick-bsv')
create_exchange('upbit-tick-xrp')
create_exchange('upbit-tick-etc')
create_exchange('upbit-tick-trx')

create_exchange('upbit-1m-btc')
create_exchange('upbit-1m-eth')
create_exchange('upbit-1m-eos')
create_exchange('upbit-1m-ada')
create_exchange('upbit-1m-ltc')
create_exchange('upbit-1m-bch')
create_exchange('upbit-1m-bsv')
create_exchange('upbit-1m-xrp')
create_exchange('upbit-1m-etc')
create_exchange('upbit-1m-trx')


create_exchange('upbit-5m-btc')
create_exchange('upbit-5m-eth')
create_exchange('upbit-5m-eos')
create_exchange('upbit-5m-ada')
create_exchange('upbit-5m-ltc')
create_exchange('upbit-5m-bch')
create_exchange('upbit-5m-bsv')
create_exchange('upbit-5m-xrp')
create_exchange('upbit-5m-etc')
create_exchange('upbit-5m-trx')


create_exchange('upbit-10m-btc')
create_exchange('upbit-10m-eth')
create_exchange('upbit-10m-eos')
create_exchange('upbit-10m-ada')
create_exchange('upbit-10m-ltc')
create_exchange('upbit-10m-bch')
create_exchange('upbit-10m-bsv')
create_exchange('upbit-10m-xrp')
create_exchange('upbit-10m-etc')
create_exchange('upbit-10m-trx')