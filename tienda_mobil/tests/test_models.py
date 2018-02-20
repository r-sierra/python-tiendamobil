import os
import json
import unittest
import tienda_mobil

def loadJSON(fname):
    cwd = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(cwd, 'data', 'models', fname), 'rb') as f:
        data = json.loads(f.read())
    return data

class ModelsTest(unittest.TestCase):

    ORDER_PREVIEW_SAMPLE = loadJSON('order_preview.json')
    CUSTOMER_SAMPLE = loadJSON('customer.json')
    ORDER_SAMPLE = loadJSON('order.json')

    def test_order_preview(self):
        """ Test tienda_mobil.OrderPreview object """
        preview = tienda_mobil.OrderPreview.NewFromJsonDict(
            self.ORDER_PREVIEW_SAMPLE)
        try:
            repr(preview)
        except Exception as e:
            self.fail(e)

        self.assertTrue(preview.AsJsonString())
        self.assertTrue(preview.AsDict())
        # Properties
        self.assertEqual(preview.id,
            self.ORDER_PREVIEW_SAMPLE['id'])
        self.assertEqual(preview.comment,
            self.ORDER_PREVIEW_SAMPLE['attributes']['comment'])
        self.assertEqual(preview.businessman,
            self.ORDER_PREVIEW_SAMPLE['attributes']['businessman'])
        self.assertEqual(str(preview.totalAmount),
            self.ORDER_PREVIEW_SAMPLE['attributes']['total-amount'])
        self.assertEqual(str(preview.totalQuantity),
            self.ORDER_PREVIEW_SAMPLE['attributes']['total-quantity'])
        self.assertTrue(preview.priceList in
            self.ORDER_PREVIEW_SAMPLE['attributes']['price-list'])
        self.assertIs(type(preview.customer), tienda_mobil.Customer)

    def test_customer(self):
        """ Test tienda_mobil.Customer object """
        customer = tienda_mobil.Customer.NewFromJsonDict(self.CUSTOMER_SAMPLE)
        try:
            repr(customer)
        except Exception as e:
            self.fail(e)

        self.assertTrue(customer.AsJsonString())
        self.assertTrue(customer.AsDict())
        # Properties
        self.assertEqual(customer.code, self.CUSTOMER_SAMPLE['code'])
        self.assertEqual(customer.email, self.CUSTOMER_SAMPLE['email'])
        self.assertEqual(customer.commercial_origin, self.CUSTOMER_SAMPLE['commercial_origin'])
        self.assertEqual(customer.address, self.CUSTOMER_SAMPLE['address'])
        self.assertEqual(customer.locality, self.CUSTOMER_SAMPLE['locality'])
        self.assertEqual(customer.telephone, self.CUSTOMER_SAMPLE['telephone'])
        self.assertEqual(customer.gender, self.CUSTOMER_SAMPLE['gender'])
        self.assertEqual(customer.name, self.CUSTOMER_SAMPLE['name'])
        self.assertEqual(customer.city, self.CUSTOMER_SAMPLE['city'])
        self.assertEqual(customer.province, self.CUSTOMER_SAMPLE['province'])
        self.assertEqual(customer.cellphone, self.CUSTOMER_SAMPLE['cellphone'])
        self.assertEqual(customer.businessman_code, self.CUSTOMER_SAMPLE['businessman_code'])
        self.assertEqual(customer.associate_code, self.CUSTOMER_SAMPLE['associate_code'])
        self.assertEqual(customer.zip_code, self.CUSTOMER_SAMPLE['zip_code'])
        self.assertEqual(customer.charge_date, self.CUSTOMER_SAMPLE['charge_date'])
        self.assertEqual(customer.birthdate, self.CUSTOMER_SAMPLE['birthdate'])
        self.assertEqual(customer.sex, 1)

    def test_order(self):
        """ Test tienda_mobil.Order object"""
        order = tienda_mobil.Order.NewFromJsonDict(self.ORDER_SAMPLE)
        try:
            repr(order)
        except Exception as e:
            self.fail(e)

        self.assertTrue(order.AsJsonString())
        self.assertTrue(order.AsDict())

        # Properties
        self.assertEqual(order.id, self.ORDER_SAMPLE['id'])
        self.assertEqual(order.priceList, self.ORDER_SAMPLE['attributes']['price-list'])
        self.assertEqual(order.comment, self.ORDER_SAMPLE['attributes']['comment'])
        self.assertIs(type(order.customer), tienda_mobil.Customer)
        self.assertIs(type(order.items[0]), tienda_mobil.OrderItem)
        self.assertTrue(len(order.items) == len(self.ORDER_SAMPLE['attributes']['order-items']))

    def test_order_item(self):
        """ Test tienda_mobil.OrderItem object"""

        order_item = tienda_mobil.OrderItem(code='47633002', quantity='2')
        self.assertEqual(order_item.code, '47633002')
        self.assertEqual(order_item.quantity, '2')
