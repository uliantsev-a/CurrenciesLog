from datetime import datetime
from project.tests.test_config import BaseTestCase
from sqlalchemy.sql import exists
from project.models.trades import Currency, Rate
from project.loader import saving_response_rates, MS_TO_MICROSEC
from project.fixtures import make_default_currency


class TestLoaderRates(BaseTestCase):
    def setUp(self):
        super().setUp()
        make_default_currency()

        self.data_rates = [
            # [timeshtamp, open, close, high, low, volume]
            [1558483200000, 0.41371, 0.4184, 0.42111, 0.41347, 369297.66665151],
            [1558396800000, 0.40848, 0.41352, 0.42732, 0.39968, 6194982.38647951]
        ]

    def test_saving_response_rates(self):
        curr = Currency.query.filter(Currency.name == 'BTC').first()
        date_first_rate = datetime.fromtimestamp(self.data_rates[0][0] / MS_TO_MICROSEC).date()

        # Tests before saving
        first_rate_exists = self.db.session.query(exists().where(Rate.date == date_first_rate)).scalar()
        self.assertFalse(first_rate_exists)

        query_rates = Rate.query.join(Rate.currency).filter(Currency.name == curr.name)
        self.assertEqual(0, query_rates.count())

        saving_response_rates(curr, self.data_rates)

        # Tests after saving
        first_rate_exists = self.db.session.query(exists().where(Rate.date == date_first_rate)).scalar()
        self.assertTrue(first_rate_exists)

        query_rates = Rate.query.join(Rate.currency).filter(Currency.name == curr.name)
        self.assertEqual(len(self.data_rates), query_rates.count())

    # TODO: test for get_hist and main_crawl_and_save from loader.py
