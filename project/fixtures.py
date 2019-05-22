from datetime import datetime
from project import factories, db
from project.models.trades import Currency, Rate
from sqlalchemy import orm
Session = orm.scoped_session(orm.sessionmaker())

def make_test_user():
    user = factories.UserFactory(
        username='test',
        password='test',
        firstname='Test',
    )
    db.session.add(user)
    db.session.commit()


def make_default_currency():
    currencies = (
        factories.CurrencyFactory.build(name='BTC'),
        factories.CurrencyFactory.build(name='ETH'),
        factories.CurrencyFactory.build(name='XRP'),
        factories.CurrencyFactory.build(name='XCH'),
        factories.CurrencyFactory.build(name='EUS'),
    )
    db.session.bulk_save_objects(currencies)
    db.session.commit()


def make_test_rates():
    d_19_5_17 = datetime.fromtimestamp(1558051200)
    d_19_5_5 = datetime.fromtimestamp(1557051200)
    btc = Currency.query.filter(Currency.name == 'BTC').first()
    eus = Currency.query.filter(Currency.name == 'EUS').first()

    factories.RateFactory(currency=btc, date=d_19_5_17, rate=0.3788, volume=6611.3)
    factories.RateFactory(currency=eus, date=d_19_5_5, rate=0.4022, volume=16611.7)
