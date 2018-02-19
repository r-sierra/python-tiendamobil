import re
import unittest
import responses
import tienda_mobil

DEFAULT_URL = re.compile(r'https?://tiendamobil\.com\.ar/.*')

def readJSONFile(fname):
    import os
    import json
    cwd = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cwd, 'data', fname)) as f:
        data = json.loads(f.read())
    return data

class ApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://tiendamobil.com.ar'
        self.api = tienda_mobil.Api(base_url=self.base_url, api_key='test')

    def testSetCredentials(self):
        test_key = 'test'
        auth_header = "Token token={0}".format(test_key)
        api = tienda_mobil.Api(base_url=self.base_url, api_key=test_key)
        self.assertEqual(api._request_headers['authorization'], auth_header)

    @responses.activate
    def testGetPendingOrders(self):
        json_data = readJSONFile('pending_orders.json')
        responses.add(responses.GET, DEFAULT_URL, json=json_data, status=200)

        resp = self.api.GetPendingOrders()
        self.assertEqual(3, len(resp))
        self.assertTrue(type(resp[0]) is tienda_mobil.OrderPreview)
        self.assertTrue(type(resp[0].customer) is tienda_mobil.Customer)
