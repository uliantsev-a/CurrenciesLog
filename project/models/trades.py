from datetime import datetime, timedelta
from project import db
from sqlalchemy.sql import func
from sqlalchemy.schema import UniqueConstraint


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    rates = db.relationship('Rate', backref='currency', lazy=True)

    def average_from_period(self, days=10):
        today = datetime.now().date()
        delta = today - timedelta(days=days)
        rates = (Rate.query.with_entities(func.avg(Rate.volume).label('average')).
                 filter(Currency.id == self.id, Rate.date >= delta).one())

        return rates[0]


class Rate(db.Model):
    __table_args__ = (
        UniqueConstraint('currency_id', 'date', name='_ticker__date'),
    )

    id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, server_default=func.current_date())
    rate = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    volume = db.Column(db.Float(decimal_return_scale=2), nullable=False)
