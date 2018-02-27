import re
import unittest
import responses
import tienda_mobil
from tienda_mobil import TiendaMobilError

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

    def testSetUserAgent(self):
        new = 'foo/bar'
        old = self.api._request_headers['User-Agent']
        self.assertNotEqual(new, old)
        self.api.SetUserAgent(new)
        self.assertEqual(new, self.api._request_headers['User-Agent'])

    @responses.activate
    def testGetPendingOrders(self):
        json_data = readJSONFile('pending_orders.json')
        responses.add(responses.GET, DEFAULT_URL, json=json_data, status=200)
        responses.add(responses.GET, DEFAULT_URL, json={}, status=200)

        resp = self.api.GetPendingOrders()
        self.assertEqual(3, len(resp))
        self.assertIs(type(resp), list)
        self.assertIs(type(resp[0]), tienda_mobil.OrderPreview)

        # empty response
        resp = self.api.GetPendingOrders()
        self.assertIs(type(resp), list)
        self.assertEqual(0, len(resp))

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

        # invalid order number
        with self.assertRaises(TiendaMobilError) as cm:
            resp = self.api.GetOrder(99999999)
        self.assertRegexpMatches(cm.exception.message, 'Bad Request')

    @responses.activate
    def testUpdateOrderStatus(self):
        responses.add(responses.PATCH, DEFAULT_URL, status=200)
        responses.add(responses.PATCH, DEFAULT_URL, status=400)
        responses.add(responses.PATCH, DEFAULT_URL, status=422,
            json={'errors': 'some error'})

        self.assertTrue(self.api.UpdateOrderStatus(123456))

        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            self.api.UpdateOrderStatus(123456)

        with self.assertRaisesRegexp(TiendaMobilError, 'some error'):
            self.api.UpdateOrderStatus(123456)

    @responses.activate
    def testUpdateResource(self):
        responses.add(responses.PATCH, DEFAULT_URL, status=200)
        responses.add(responses.PATCH, DEFAULT_URL, status=400)
        responses.add(responses.PATCH, DEFAULT_URL, status=404)
        responses.add(responses.PATCH, DEFAULT_URL, status=422,
            json={'error': 'Order cannot be empty'})
        responses.add(responses.PATCH, DEFAULT_URL, status=422,
            json={'errors': ['Order cannot be empty','Items cannot be empty']})

        self.assertTrue(self.api.UpdateResource('orders', 1, {}))

        # invalid resource id
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            self.api.UpdateResource('orders', 1, {})

        # invalid resource name
        with self.assertRaisesRegexp(TiendaMobilError, 'Not Found for url'):
            self.api.UpdateResource('invalid-resource', 1, {})

        # validation error
        with self.assertRaisesRegexp(TiendaMobilError, 'Error: '):
            self.api.UpdateResource('orders', 1, {})

        # validation errors
        with self.assertRaisesRegexp(TiendaMobilError, 'Errors: '):
            self.api.UpdateResource('orders', 1, {})

    @responses.activate
    def testCreateResource(self):
        responses.add(responses.POST, DEFAULT_URL, status=200)
        responses.add(responses.POST, DEFAULT_URL, status=400)
        responses.add(responses.POST, DEFAULT_URL, status=404)
        responses.add(responses.POST, DEFAULT_URL, status=422,
            json={'error': 'Order cannot be empty'})
        responses.add(responses.POST, DEFAULT_URL, status=422,
            json={'errors': ['Order cannot be empty','Items cannot be empty']})

        self.assertTrue(self.api.CreateResource('orders', {}))

        # duplicated resource
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            self.api.CreateResource('orders', {})

        # invalid resource name
        with self.assertRaisesRegexp(TiendaMobilError, 'Not Found for url'):
            self.api.CreateResource('invalid-resource', {})

        # validation error
        with self.assertRaisesRegexp(TiendaMobilError, 'Error: '):
            self.api.CreateResource('orders', {})

        # validation errors
        with self.assertRaisesRegexp(TiendaMobilError, 'Errors: '):
            self.api.CreateResource('orders', {})

