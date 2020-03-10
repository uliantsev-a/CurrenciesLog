from base64 import b64encode

from project.tests.test_config import BaseTestCase


class TestRoutes(BaseTestCase):
    fixtures = ['test_data.json']

    def test_ticks(self):
        auth_data = b64encode(b'test:test').decode('utf-8')
        resp_client = self.client.get('/api/currencies',
                                      data={'perPage': 0},
                                      headers={
                                          'Authorization': f"Basic {auth_data}"
                                      })
        self.assertEqual(resp_client.status_code, 200)
