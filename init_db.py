from app import db
from models import Exchange, Action

db.create_all()


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