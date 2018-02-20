#encoding: utf-8

import json

class TiendaMobilModel(object):

    """ Base class from which all models will inherit. """

    def __init__(self, **kwargs):
        self.param_defaults = {}

    def __str__(self):
        """ Returns a string representation of TiendaMobilModel. By default
        this is the same as AsJsonString(). """
        return self.AsJsonString()

    def __eq__(self, other):
        return other and self.AsDict() == other.AsDict()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if hasattr(self, 'id'):
            return hash(self.id)
        else:
            raise TypeError('unhashable type: {} (no id attribute)'
                            .format(type(self)))

    def AsJsonString(self):
        """ Returns the TiendaMobilModel as a JSON string based on key/value
        pairs returned from the AsDict() method. """
        return json.dumps(self.AsDict(), sort_keys=True)

    def AsDict(self):
        """ Create a dictionary representation of the object. Please see inline
        comments on construction when dictionaries contain TiendaMobilModels. """
        data = {}

        for (key, value) in self.param_defaults.items():

            # If the value is a list, we need to create a list to hold the
            # dicts created by an object supporting the AsDict() method,
            # i.e., if it inherits from TiendaMobilModel. If the item in the list
            # doesn't support the AsDict() method, then we assign the value
            # directly.
            if isinstance(getattr(self, key, None), (list, tuple, set)):
                data[key] = list()
                for subobj in getattr(self, key, None):
                    if getattr(subobj, 'AsDict', None):
                        data[key].append(subobj.AsDict())
                    else:
                        data[key].append(subobj)

            # Not a list, *but still a subclass of TiendaMobilModel* and
            # and we can assign the data[key] directly with the AsDict()
            # method of the object.
            elif getattr(getattr(self, key, None), 'AsDict', None):
                data[key] = getattr(self, key).AsDict()

            # If the value doesn't have an AsDict() method, i.e., it's not
            # something that subclasses TiendaMobilModel, then we can use direct
            # assigment.
            elif getattr(self, key, None):
                data[key] = getattr(self, key, None)
        return data

    @classmethod
    def NewFromJsonDict(cls, data, **kwargs):
        """ Create a new instance based on a JSON dict. Any kwargs should be
        supplied by the inherited, calling class.

        Args:
            data: A JSON dict, as converted from the JSON in the API.

        """
        json_data = data.copy()
        if kwargs:
            for key, val in kwargs.items():
                json_data[key] = val

        c = cls(**json_data)
        c._json = data
        return c

    def __getattr__(self, attr):
        if hasattr(self, 'attributes') and attr in self.attributes:
            return self.attributes[attr]
        raise AttributeError(attr)

class OrderPreview(TiendaMobilModel):

    """A class representing the preview of an order. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'id': None,
            'type': None,
            'attributes': {
                'businessman': '',
                'price-list': '',
                'total-quantity': 0,
                'customer': Customer(),
                'comment': '',
                'total-amount': 0.
            }
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))
        if 'attributes' in kwargs and 'customer' in kwargs['attributes']:
            self.customer = Customer.NewFromJsonDict(kwargs['attributes']['customer'])

    def __repr__(self):
        return "OrderPreview(ID={i}, Customer='{c}', TotalAmount='{a}')".format(
            i=self.id,
            c=self.customer.code,
            a=self.totalAmount)

    @property
    def totalAmount(self):
        return float(self.attributes['total-amount'])

    @property
    def totalQuantity(self):
        return int(self.attributes['total-quantity'])

    @property
    def priceList(self):
        return self.attributes['price-list'].replace('R','')


class Order(TiendaMobilModel):
    """A class representing an order. """

    def __init__(self, **kwargs):
        self.param_defaults = {
            'id': None,
            'type': None,
            'attributes': {
                'comment': '',
                'price-list': '',
                'order-items': [],
                'customer': Customer()
            }
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))
        if 'attributes' in kwargs:
            attr = kwargs['attributes']
            if 'customer' in attr:
                self.customer = Customer.NewFromJsonDict(attr['customer'])
            if 'order-items' in attr:
                self.items = []
                for oi in attr['order-items']:
                    self.items.append(OrderItem.NewFromJsonDict(oi))

    def __repr__(self):
        return "Order(ID={i}, Customer={c})".format(
            i=self.id,
            c=self.customer.code)

    @property
    def priceList(self):
        return self.attributes['price-list']

class OrderItem(TiendaMobilModel):
    """A class representing an item of an Order, an order-item"""

    def __init__(self, **kwargs):
        self.param_defaults = {
            'code': '',
            'quantity': ''
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "OrderItem(Code='{c}', Quantity={q})".format(
          c=self.code,
          q=self.quantity)

class Customer(TiendaMobilModel):
    """A class representing a Customer."""

    def __init__(self, **kwargs):
        self.param_defaults = {
            "email": "",
            "commercial_origin": "",
            "address": "",
            "locality": "",
            "telephone": "",
            "gender": "female",
            "name": "",
            "city": "",
            "province": "",
            "cellphone": "",
            "code": "",
            "businessman_code": "",
            "associate_code": "",
            "zip_code": "",
            "charge_date": "",
            "birthdate": ""
        }

        for (param, default) in self.param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def __repr__(self):
        return "Customer(Code='{i}', Name='{c}')".format(i=self.code, c=self.name)

    @property
    def sex(self):
        return 1 if self.gender == 'female' else 0
