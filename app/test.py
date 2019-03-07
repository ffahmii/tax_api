import unittest
import json
from model import db
from run import create_app


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client

        with self.app.app_context():
            db.create_all()
            db.init_app(self.app)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_create_tax_success(self):
        """ test create tax """
        tax = {'name': 'Big Mac', 'tax_code': 1, 'price': 1000}
        res = self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax))
        json_data = json.loads(res.data)

        self.assertEqual('Big Mac', json_data.get('name'))
        self.assertEqual(1, json_data.get('tax_code'))
        self.assertEqual(1000, json_data.get('price'))

    def test_create_tax_missing_name_attribute_error_thrown(self):
        """ test create tax with missing name attribute, so it will throw error """
        tax = {'tax_code': 1, 'price': 1000}
        res = self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax))
        json_data = json.loads(res.data)

        self.assertEqual('Missing data for required field.', json_data.get('name')[0])

    def test_create_tax_missing_price_attribute_error_thrown(self):
        """ test create tax with missing price attribute, so it will throw error """
        tax = {'name': 'Big Mac', 'tax_code': 1}
        res = self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax))
        json_data = json.loads(res.data)

        self.assertEqual('Missing data for required field.', json_data.get('price')[0])

    def test_create_tax_missing_tax_code_attribute_error_thrown(self):
        """ test create tax with missing tax_code attribute, so it will throw error """
        tax = {'name': 'Big Mac', 'price': 1000}
        res = self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax))
        json_data = json.loads(res.data)

        self.assertEqual('Missing data for required field.', json_data.get('tax_code')[0])

    def test_create_tax_invalid_tax_code_value_error_thrown(self):
        """ test create tax with invalid tax_code value, so it will throw error """
        tax = {'name': 'Big Mac', 'price': 1000, 'tax_code': 4}
        res = self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax))
        json_data = json.loads(res.data)

        self.assertEqual('Tax code is invalid. Tax code should be 1, 2, or 3', json_data.get('tax_code')[0])

    def test_get_bill_success(self):
        """ test get bill """
        tax1 = {'name': 'Lucky Stretch', 'tax_code': 2, 'price': 1000}
        tax2 = {'name': 'Big Mac', 'tax_code': 1, 'price': 1000}
        tax3 = {'name': 'Movie', 'tax_code': 3, 'price': 150}
        self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax1))
        self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax2))
        self.client().post('/api/tax', headers={'Content-Type': 'application/json'}, data=json.dumps(tax3))

        res = self.client().get('/api/bill', headers={'Content-Type': 'application/json'})
        json_data = json.loads(res.data)

        self.assertEqual(2150, json_data.get('price_sub_total'))
        self.assertEqual(130.5, json_data.get('tax_sub_total'))
        self.assertEqual(2280.5, json_data.get('grand_total'))

        for detail in json_data.get('detail'):
            if detail.get('name') == 'Lucky Stretch':
                self.assertEqual(1000, detail.get('price'))
                self.assertEqual(2, detail.get('tax_code'))
                self.assertEqual('Tobacco', detail.get('tax_type'))
                self.assertEqual(30, detail.get('tax'))
                self.assertEqual('No', detail.get('is_refundable'))
                self.assertEqual(1030, detail.get('amount'))
            elif detail.get('name') == 'Big Mac':
                self.assertEqual(1000, detail.get('price'))
                self.assertEqual(1, detail.get('tax_code'))
                self.assertEqual('Food & Beverage', detail.get('tax_type'))
                self.assertEqual(100, detail.get('tax'))
                self.assertEqual('Yes', detail.get('is_refundable'))
                self.assertEqual(1100, detail.get('amount'))
            elif detail.get('name') == 'Movie':
                self.assertEqual(150, detail.get('price'))
                self.assertEqual(3, detail.get('tax_code'))
                self.assertEqual('Entertainment', detail.get('tax_type'))
                self.assertEqual(0.5, detail.get('tax'))
                self.assertEqual('No', detail.get('is_refundable'))
                self.assertEqual(150.5, detail.get('amount'))

    def test_get_bill_with_empty_result(self):
        """ test get bill with empty result"""
        res = self.client().get('/api/bill', headers={'Content-Type': 'application/json'})
        json_data = json.loads(res.data)

        self.assertEqual(0, json_data.get('price_sub_total'))
        self.assertEqual(0, json_data.get('tax_sub_total'))
        self.assertEqual(0, json_data.get('grand_total'))


if __name__ == '__main__':
    unittest.main()
