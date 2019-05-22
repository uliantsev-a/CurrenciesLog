from datetime import datetime
from project import factories, db


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
        factories.CurrencyFactory(name='BTC'),
        factories.CurrencyFactory(name='ETH'),
        factories.CurrencyFactory(name='XRP'),
        factories.CurrencyFactory(name='XCH'),
        factories.CurrencyFactory(name='EUS'),
    )
    db.session.bulk_save_objects(currencies)
    db.session.commit()


def make_test_rates():
    d_19_5_17 = datetime.fromtimestamp(1558051200)
    d_19_5_5 = datetime.fromtimestamp(1557051200)
    rates = (
        factories.RateFactory(currency__name='BTC', date=d_19_5_17, rate=0.3788, volume=6611.3),
        factories.RateFactory(currency__name='EUS', date=d_19_5_5, rate=0.4022, volume=16611.7),
    )
    db.session.bulk_save_objects(rates)
    db.session.commit()
