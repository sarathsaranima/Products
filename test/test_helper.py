import json
import logging
import sys
import unittest
from unittest import TestCase

import requests

base_url = 'http://127.0.0.1:5000/api/Product'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


class TestProductRead(TestCase):

    def setUp(self):
        """
        setUp method for the test case.
        :return: None
        """
        json_input = {
            'name': 'test product',
            'description': 'test product description',
            'brand': 'test brand',
            'product_code': 'test product code',
            'price': 1}

        response = requests.post(base_url, data=json.dumps(json_input))
        response_data = response.json()
        self.create_id = response_data['data']['id']
        self.created_name = response_data['data']['name']
        logging.debug('Test item created setUp : status {}'.format(response.status_code))
        self.created_item = response_data['data']

    def test_read_all(self):
        """
        Test case for testing the read operation of all products.
        :return:
        """
        response = requests.get(base_url)
        self.assertEqual(response.status_code, 200)

    def test_read_by_name(self):
        """
        Test case for testing the read operation by name.
        :return:
        """
        url = base_url+"?name="+str(self.created_name)
        response = requests.get(url)
        response_json = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(self.created_item, response_json['data'])

    def test_read_by_name_failure(self):
        """
        Test case for testing negative scenarios in the read operation by passing invalid name.
        :return:
        """
        url = base_url + "?name=XXXXXXXXX12121"
        response = requests.get(url)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """
        tearDown method for the test case.
        :return: None
        """
        delete_url = base_url+"?id="+str(self.create_id)
        response = requests.delete(delete_url)
        logging.debug('Test item deleted tearDown : status {}'.format(response.status_code))


class TestProductCreate(TestCase):

    def test_create_item_success(self):
        """
        Test case for testing the creation of product.
        :return:
        """
        self.create_id = None
        json_input = {
            'name': 'test product',
            'description': 'test product description',
            'brand': 'test brand',
            'product_code': 'test product code',
            'price': 1}

        response = requests.post(base_url, data=json.dumps(json_input))
        response_data = response.json()
        self.create_id = response_data['data']['id']
        logging.debug('Test item created : status {}'.format(response.status_code))
        self.created_item = response_data['data']
        self.assertEqual(response.status_code, 201)
        json_input['id'] = self.create_id
        self.assertDictEqual(json_input, response_data['data'])

    def test_create_item_failure(self):
        """
        Test case for testing failure in the creation of product for invalid input data.
        :return:
        """
        self.create_id = None
        json_input = {
            'nameabcd': 'test product',
            'descriptiondi': 'test product description',
            'brandab': 'test brand',
            'product_codecd': 'test product code',
            'pricedf': 1}

        response = requests.post(base_url, data=json.dumps(json_input))
        self.assertEqual(response.status_code, 500)

    def test_create_already_exist(self):
        """
        Test case for testing failure in creation of product, for an already existing product.
        :return:
        """
        self.create_id = None
        json_input = {
            'name': 'test product',
            'description': 'test product description',
            'brand': 'test brand',
            'product_code': 'test product code',
            'price': 1}
        response = requests.post(base_url, data=json.dumps(json_input))
        response_data = response.json()
        self.create_id = response_data['data']['id']
        logging.debug('Test item created : status {}'.format(response.status_code))
        response = requests.post(base_url, data=json.dumps(json_input))
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """
        tearDown method for the test case.
        :return: None
        """
        if self.create_id:
            delete_url = base_url + "?id=" + str(self.create_id)
            response = requests.delete(delete_url)
            logging.debug('Test item deleted tearDown : status {}'.format(response.status_code))


class TestProductUpdate(TestCase):
    def setUp(self):
        """
        setUp method for the test case.
        :return: None
        """
        json_input = {
            'name': 'test product',
            'description': 'test product description',
            'brand': 'test brand',
            'product_code': 'test product code',
            'price': 1}

        response = requests.post(base_url, data=json.dumps(json_input))
        response_data = response.json()
        self.create_id = response_data['data']['id']
        logging.debug('Test item created setUp : status {}'.format(response.status_code))

    def test_update_success(self):
        """
        Test case for testing update operation on a product.
        :return:
        """
        json_input = {
            'id': self.create_id,
            'name': 'test product update',
            'description': 'test product description update',
            'brand': 'test brand update',
            'product_code': 'test product code update',
            'price': 2}

        response = requests.put(base_url, data=json.dumps(json_input))
        response_data = response.json()
        logging.debug('Test item updated : status {}'.format(response.status_code))
        self.assertDictEqual(json_input, response_data['data'])
        self.assertEqual(response.status_code, 200)

    def test_update_failure(self):
        """
        Test case for testing failure on updation of a product for invalid input.
        :return:
        """
        json_input = {
            'id2': self.create_id,
            'name2': 'test product update',
            'description2': 'test product description update',
            'brand2': 'test brand update',
            'product_code2': 'test product code update',
            'price2': 2}
        response = requests.put(base_url, data=json.dumps(json_input))
        logging.debug('Test item update : status {}'.format(response.status_code))
        self.assertEqual(response.status_code, 500)

    def tearDown(self):
        """
        tearDown method for the test case.
        :return: None
        """
        if self.create_id:
            delete_url = base_url + "?id=" + str(self.create_id)
            response = requests.delete(delete_url)
            logging.debug('Test item deleted tearDown : status {}'.format(response.status_code))


class TestProductDelete(TestCase):
    def setUp(self):
        """
        setUp method for the test case.
        :return: None
        """
        json_input = {
            'name': 'test product',
            'description': 'test product description',
            'brand': 'test brand',
            'product_code': 'test product code',
            'price': 1}
        response = requests.post(base_url, data=json.dumps(json_input))
        response_data = response.json()
        self.create_id = response_data['data']['id']
        logging.debug('Test item created : status {}'.format(response.status_code))

    def test_delete_success(self):
        """
        Test case for testing successful delete operation of a product.
        :return:
        """
        self.is_deleted = False
        delete_url = base_url + "?id=" + str(self.create_id)
        response = requests.delete(delete_url)
        self.is_deleted = True
        self.assertEqual(response.status_code, 200)

    def test_delete_failure(self):
        """
        Test case for testing delete failure for invalid input.
        :return:
        """
        self.is_deleted = False
        delete_url = base_url + "?id=test"
        response = requests.delete(delete_url)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """
        tearDown method for the test case.
        :return: None
        """
        if not self.is_deleted:
            delete_url = base_url + "?id=" + str(self.create_id)
            response = requests.delete(delete_url)
            logging.debug('Test item deleted tearDown : status {}'.format(response.status_code))


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=1), exit=False)
