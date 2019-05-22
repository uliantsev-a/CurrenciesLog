"""

Factories classes for fixtures of first bootstrap and testing
"""

import factory

from project.models.auth import User
from project.models.trades import Currency, Rate


class UserFactory(factory.Factory):
    class Meta:
        model = User


class CurrencyFactory(factory.Factory):
    class Meta:
        model = Currency


class RateFactory(factory.Factory):
    class Meta:
        model = Rate

    currency_id = factory.SelfAttribute('currency.id')
