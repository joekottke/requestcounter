import unittest
import json
from requestcounter import app


class RequestCounterTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        await self.client().get('/reset')

    def test_get_home(self):
        resp = await self.client().get('/')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(42, data['theanswer'])

    def test_metric_increment(self):
        '''Test 100 requests'''
        for i in range(100):
            self.client().get('/')

        resp = self.client().get('/metrics')
        metrics = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(100, metrics['theanswer_count'])

    def test_metric_reset(self):
        for i in range(100):
            self.client().get('/')

        # Check that we got 100 requests first
        resp = self.client().get('/metrics')
        metrics = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(100, metrics['theanswer_count'])

        # Now reset and confirm that we go back to zero
        self.client().get('/reset')
        resp = self.client().get('/metrics')
        metrics = json.loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertEqual(0, metrics['theanswer_count'])


if __name__ == '__main__':
    unittest.main()
