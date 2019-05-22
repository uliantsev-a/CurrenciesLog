from project.tests.test_config import BaseTestCase
from project.models.auth import User
from project.models.trades import Currency, Rate
from project.fixtures import make_default_currency, make_test_rates


class TestUserModel(BaseTestCase):

    def test_create_user(self):
        test_pass = 'test_password'
        user = User(username='test_name', password=test_pass, firstname='f_name')
        self.assertIn('pbkdf2:sha256', user.password)
        self.assertTrue(user.check_password(test_pass))
        self.assertFalse(user.check_password(test_pass+'asd'))
        self.assertFalse(user.check_password(''))


class TestTradesRelationship(BaseTestCase):

    def setUp(self):
        super().setUp()
        make_default_currency()
        make_test_rates()

    def test_relationship(self):
        curr = Currency.query.filter(Currency.name == 'BTC').first()
        rate = Rate.query.join(Rate.currency).filter(Currency.name == 'BTC').first()
        self.assertIn(rate, curr.rates)
