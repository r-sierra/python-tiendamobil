import re
import unittest
import responses
import tienda_mobil
from tienda_mobil import TiendaMobilError

DEFAULT_URL = re.compile(r'https?://tiendamobil.com.ar/api/.*')


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
    def testBadGateway(self):
        # Server Error
        responses.add(GET, DEFAULT_URL, status=502)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Gateway'):
            resp = self.api.GetPendingOrders()

        # try:
        #     resp = self.api.GetPendingOrders()
        # except tienda_mobil.TiendaMobilError as e:
        #     print e.message
        #     self.assertEqual(e.message, "Bad Gateway")

    @responses.activate
    def testUnauthorized(self):
        # Application Error
        responses.add(GET, DEFAULT_URL, status=401)
        with self.assertRaisesRegexp(TiendaMobilError, 'Not authorized'):
            resp = self.api.GetPendingOrders()

        # try:
        #     resp = self.api.GetPendingOrders()
        # except tienda_mobil.TiendaMobilError as e:
        #     print e.message
        #     self.assertEqual(e.message, "Not authorized.")

    @responses.activate
    def testBadRequest(self):
        # Application Error
        responses.add(GET, DEFAULT_URL, status=400)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            resp = self.api.GetPendingOrders()

        # try:
        #     resp = self.api.GetPendingOrders()
        # except tienda_mobil.TiendaMobilError as e:
        #     print e.message
        #     self.assertEqual(e.message, "Bad Request")

    @responses.activate
    def testUnprocessableEntity(self):
        # Application Error
        responses.add(GET, DEFAULT_URL, status=422)
        with self.assertRaisesRegexp(TiendaMobilError, 'Unprocessable Entity'):
            resp = self.api.GetPendingOrders()

        # try:
        #     resp = self.api.GetPendingOrders()
        # except tienda_mobil.TiendaMobilError as e:
        #     print e.message
        #     self.assertEqual(e.message, "Unprocessable Entity")

    @responses.activate
    def testGetPendingOrders(self):
        with open('testdata/get_trends_current.json') as f:
            resp_data = f.read()

        url = '{0}/orders'.format(self.base_url)
        responses.add(responses.GET, url, json=resp_data, status=200)

        resp = self.api.GetPendingOrders()
        self.assertTrue(type(resp[0]) is tienda_mobil.OrderPreview)
