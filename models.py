from app import db
from datetime import datetime


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
