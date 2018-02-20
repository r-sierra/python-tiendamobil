#!/usr/bin/env python
# encoding: utf8

#
#
# Copyright 2018 Roberto Sierra
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from error import TiendaMobilError
from models import (
    Order,
    OrderPreview
)

class Api(object):
    """A python interface into the Tienda Mobil API"""

    def __init__(self, base_url, api_key):
        """Instantiate a new tienda_mobil.Api object.

        Args:
          api_key (str):
            Your Tienda Mobil user's api_key.
          base_url (str):
            The base URL to use to contact the Tienda Mobil API.
        """

        self.base_url = str(base_url)

        self._InitializeRequestHeaders()
        self._InitializeUserAgent()
        self._InitializeDefaultParameters()
        self._SetCredentials(api_key)

        # self.rate_limit = RateLimit()

    def _InitializeRequestHeaders(self):
        self._request_headers = {
            'accept': 'application/json',
            'accept': 'application/vnd.api.v1',
        }

    def _InitializeUserAgent(self):
        self._request_headers['user-agent'] = 'OpenOrange API Sync 0.1'

    def _InitializeDefaultParameters(self):
        self._default_params = {}

    def _SetCredentials(self, api_key):
        self._request_headers['authorization'] = "Token token={0}".format(api_key)

    def GetPendingOrders(self, return_json=False):
        """Returns a list of pending orders.

        Args:
            return_json (bool, optional):
                If True JSON data will be returned, instead of
                tienda_mobil.OrderPreview

        Returns:
          A tienda_mobil.OrderPreview list representing all pending orders
        """
        url = '%s/orders/' % self.base_url
        resp = self._RequestUrl(url, 'GET')
        self._RaiseForHeaderStatus(resp)
        data = self._ParseAndCheck(resp)

        if return_json:
            return data
        else:
            return [OrderPreview.NewFromJsonDict(x) for x in data]

    def GetOrder(self, order_id, return_json=False):
        """Returns a single order.

        Args:
            order_id(int, str):
                The id we want to retrieve.
            return_json (bool, optional):
                If True JSON data will be returned, instead of tienda_mobil.Order

        Returns:
          A tienda_mobil.Order instance representing that order
        """

        url = '%s/orders/%s' % (self.base_url, order_id)
        resp = self._RequestUrl(url, 'GET')
        self._RaiseForHeaderStatus(resp)
        data = self._ParseAndCheck(resp)

        if return_json:
            return data
        else:
            return Order.NewFromJsonDict(data)

    def UpdateOrderStatus(self, order_id):
        """Updates de requested order status

        Args:
            order_id(int, str):
                The order id we want to update.

        Returns:
          (True): if order was successfully updated

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message
        """
        payload = {'order': {'processed': True}}
        return self.UpdateResource('orders', order_id, payload)

    def UpdateResource(self, resource_name, resource_id, data):
        """Returns True or False if the record was updated

        Args:
            resource_name(str):
                The resource name we wish to update

            resource_id(int, str):
                The resource id we want to update.

            data:
                A dict of (str, unicode) key/value pairs, conforming to the
                JSON:API spec 1.0

        Returns:
          (True): If the update was successfull

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message
        """

        url = '{0}/{1}/{2}'.format(self.base_url, resource_name, resource_id)
        response = self._RequestUrl(url, 'PATCH', data)

        if response.status_code == requests.codes.unprocessable:
            # look for JSON error description
            self._ParseAndCheck(response)
        elif response.status_code != requests.codes.ok:
            self._RaiseForHeaderStatus(response)
        return True

    def CreateResource(self, resource_name, data):
        """Returns True or False if the record was created

        Args:
            resource_name(str):
                The resource name we wish to create

            data:
                A dict of (str, unicode) key/value pairs, conforming to the
                JSON:API spec 1.0

        Returns:
          True: If the resource creation was successfull

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message
        """

        url = '{0}/{1}'.format(self.base_url, resource_name)
        response = self._RequestUrl(url, 'POST', data)

        if response.status_code == requests.codes.unprocessable:
            # look for JSON error description
            self._ParseAndCheck(response)
        elif response.status_code != requests.codes.ok:
            self._RaiseForHeaderStatus(response)
        return True

    def _RaiseForHeaderStatus(self, response):
        """Raises an exception if an HTTP error ocurred or status code between
        400 <= x < 600, and status code is not 422

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message
        """
        # # If status code is `unprocessable` do not raise exception
        # # as the response body needs to be processed for error details
        # if response.status_code != requests.codes.unprocessable_entity:
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException, e:
            raise TiendaMobilError(e.message)

    def _RequestUrl(self, url, verb, data=None):
        """Request a url.

        Args:
            url:
                The web location we want to retrieve.
            verb:
                Either POST or GET.
            data:
                A dict of (str, unicode) key/value pairs.

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message

        Returns:
            A requests.response object.
        """
        if not data:
            data = {}

        resp = 0

        try:
            if verb == 'GET':
                resp = requests.get(url, headers=self._request_headers)
            elif verb in ('PATCH', 'PUT'):
                resp = requests.patch(url, json=data, headers=self._request_headers)
            elif verb == 'POST':
                resp = requests.post(url, json=data, headers=self._request_headers)
            else:
                raise TiendaMobilError('Unknown REST Verb: {0}'.format(verb))
        except requests.exceptions.ConnectionError as e:
            raise TiendaMobilError(u"Error de conexión: {0}".format(e.message))

        return resp

    def _ParseAndCheck(self, response):
        """Try and parse the JSON returned and return
        an empty dictionary if there is any error.

        This is a purely defensive check because during some
        network outages it will return an HTML fail page.

        Args:
            response (requests.models <Response> class):
                A response object created from the response content

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message
        """
        try:
            data = response.json()
        except ValueError, e:
            raise TiendaMobilError('JSON parse error: {0}'.format(e.message))
        self._CheckForError(data)
        return data.get('data', {})

    def _CheckForError(self, data):
        """Raises a TiendaMobilError if data has an error message.

        Args:
            data (dict):
                A python dict created from the json response

        Raises:
            (tiendaMobil.TiendaMobilError): TiendaMobilError wrapping the error
            message if one exists.
        """
        # Errors are relatively unlikely, so it is faster
        # to check first, rather than try and catch the exception
        if 'error' in data:
            raise TiendaMobilError('Error: {0}'.format(data['error']))
        if 'errors' in data:
            errors = data['errors']
            if type(errors) == list:
                errors = ', '.join(errors)
            raise TiendaMobilError('Errors: {0}'.format(data['errors']))
