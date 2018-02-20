import re
import unittest
import responses
import tienda_mobil
from tienda_mobil import TiendaMobilError

DEFAULT_URL = re.compile(r'https?://tiendamobil\.com\.ar/api/.*')


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://tiendamobil.com.ar/api'
        self.api = tienda_mobil.Api(base_url=self.base_url, api_key='test')

    @responses.activate
    def testBadGateway(self):
        responses.add(responses.GET, DEFAULT_URL, status=502)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Gateway'):
            self.api.GetPendingOrders()

        responses.add(responses.GET, DEFAULT_URL, status=502)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Gateway'):
            self.api.GetOrder(99999)

        responses.add(responses.PATCH, DEFAULT_URL, status=502)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Gateway'):
            self.api.UpdateResource('orders', 99999, {})

        responses.add(responses.POST, DEFAULT_URL, status=502)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Gateway'):
            self.api.CreateResource('orders', {})

    @responses.activate
    def testUnauthorized(self):
        responses.add(responses.GET, DEFAULT_URL, status=401)
        with self.assertRaisesRegexp(TiendaMobilError, 'Unauthorized for url'):
            resp = self.api.GetPendingOrders()

        responses.add(responses.GET, DEFAULT_URL, status=401)
        with self.assertRaisesRegexp(TiendaMobilError, 'Unauthorized for url'):
            self.api.GetOrder(99999)

        responses.add(responses.PATCH, DEFAULT_URL, status=401)
        with self.assertRaisesRegexp(TiendaMobilError, 'Unauthorized for url'):
            self.api.UpdateResource('orders', 99999, {})

        responses.add(responses.POST, DEFAULT_URL, status=401)
        with self.assertRaisesRegexp(TiendaMobilError, 'Unauthorized for url'):
            self.api.CreateResource('orders', {})

    @responses.activate
    def testBadRequest(self):
        responses.add(responses.GET, DEFAULT_URL, status=400)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            resp = self.api.GetPendingOrders()

        responses.add(responses.GET, DEFAULT_URL, status=400)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            self.api.GetOrder(99999)

        responses.add(responses.PATCH, DEFAULT_URL, status=400)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            self.api.UpdateResource('orders', 99999, {})

        responses.add(responses.POST, DEFAULT_URL, status=400)
        with self.assertRaisesRegexp(TiendaMobilError, 'Bad Request'):
            self.api.CreateResource('orders', {})

    @responses.activate
    def testUnprocessableEntity(self):
        responses.add(responses.PATCH, DEFAULT_URL, status=422,
            json={'error': 'Customer cannot be empty'})
        with self.assertRaisesRegexp(TiendaMobilError, 'cannot be empty'):
            self.api.UpdateResource('orders', 99999, {})

        responses.add(responses.POST, DEFAULT_URL, status=422,
            json={'error': 'Customer cannot be empty'})
        with self.assertRaisesRegexp(TiendaMobilError, 'cannot be empty'):
            self.api.CreateResource('orders', {})
