from app import db, Exchange, Action

# db.create_all()


def create_exchange(name):
    e1 = Exchange(name=name)
    db.session.add(e1)
    db.session.commit()

create_exchange('huobi-tick-btc')
create_exchange('huobi-tick-eth')
create_exchange('huobi-tick-eos')
create_exchange('huobi-tick-ada')
create_exchange('huobi-tick-ltc')
create_exchange('huobi-tick-bch')
create_exchange('huobi-tick-bsv')
create_exchange('huobi-tick-xrp')
create_exchange('huobi-tick-etc')
create_exchange('huobi-tick-trx')

create_exchange('huobi-1m-btc')
create_exchange('huobi-1m-eth')
create_exchange('huobi-1m-eos')
create_exchange('huobi-1m-ada')
create_exchange('huobi-1m-ltc')
create_exchange('huobi-1m-bch')
create_exchange('huobi-1m-bsv')
create_exchange('huobi-1m-xrp')
create_exchange('huobi-1m-etc')
create_exchange('huobi-1m-trx')


create_exchange('huobi-5m-btc')
create_exchange('huobi-5m-eth')
create_exchange('huobi-5m-eos')
create_exchange('huobi-5m-ada')
create_exchange('huobi-5m-ltc')
create_exchange('huobi-5m-bch')
create_exchange('huobi-5m-bsv')
create_exchange('huobi-5m-xrp')
create_exchange('huobi-5m-etc')
create_exchange('huobi-5m-trx')


create_exchange('huobi-10m-btc')
create_exchange('huobi-10m-eth')
create_exchange('huobi-10m-eos')
create_exchange('huobi-10m-ada')
create_exchange('huobi-10m-ltc')
create_exchange('huobi-10m-bch')
create_exchange('huobi-10m-bsv')
create_exchange('huobi-10m-xrp')
create_exchange('huobi-10m-etc')
create_exchange('huobi-10m-trx')