import re
import unittest
import responses
import tienda_mobil

DEFAULT_URL = re.compile(r'https?://tiendamobil\.com\.ar/api/.*')

def readJSONFile(fname):
    import os
    import json
    cwd = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cwd, 'data', fname)) as f:
        data = json.loads(f.read())
    return data

class ApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://tiendamobil.com.ar/api'
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

    @responses.activate
    def testGetOrder(self):
        json_data = readJSONFile('order.json')
        order_id = json_data['data']['id']

        responses.add(
            responses.GET,
            '{0}/orders/{1}'.format(self.base_url, order_id),
            json=json_data,
            status=200)
        responses.add(
            responses.GET,
            '{0}/orders/99999999'.format(self.base_url),
            status=400)

        resp = self.api.GetOrder(order_id)
        self.assertIs(type(resp), tienda_mobil.Order)
        self.assertEqual(order_id, resp.id)

        # test raw json response
        json_resp = self.api.GetOrder(order_id, return_json=True)
        self.assertIs(type(json_resp), dict)
        self.assertEqual(order_id, json_resp['id'])

        with self.assertRaises(tienda_mobil.TiendaMobilError) as cm:
            resp = self.api.GetOrder(99999999)
        self.assertRegexpMatches(cm.exception.message, 'Bad Request')



