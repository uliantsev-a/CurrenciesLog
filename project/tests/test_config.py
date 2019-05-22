from unittest import TestCase
from project import app, config, db


class BaseTestCase(TestCase):

    def setUp(self):

        app.config.from_object(config.TestingConfig)

        self.client = app.test_client()
        self.db = db
        self.db.init_app(app)
        self.db.create_all()

    def tearDown(self):
        self.db.session.rollback()
        self.db.drop_all()
        super().tearDown()
