from project.tests.test_config import BaseTestCase


class TestRoutes(BaseTestCase):
    fixtures = ['test_data.json']

    def test_ticks(self):
        resp_client = self.client.get('/api/')
        self.assertEqual(resp_client.status_code, 200)
