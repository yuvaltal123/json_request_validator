import json
import unittest
from flask import Flask, jsonify, request

from template_builder import TemplateBuilder
from template_structure import TemplateTypes
from validator import RequestValidator


class TestValidator(unittest.TestCase):

    single_request_str = """{
	"path": "/users/info",
	"method": "GET",
	"query_params": [
		{
			"name": "with_extra_data",
			"value": false
		}
	],
	"headers": [
		{
			"name": "Authorization",
			"value": "Bearerebb3cbbe938c4776bd22a4ec2ea8b2ca"
		}
		
	],
	"body": []
}"""

    request_str_2 = """{
	"path": "/orders/update",
	"method": "PATCH",
	"query_params": [],
	"headers": [
		{
			"name": "Authorization",
			"value": "Bearerebb3cbbe938c4776bd22a4ec2ea8b2cas!"
		}
	],
	"body": [
		{
			"name": "order_id",
			"value": "46da6390-7c78-4a1c-9efa-7c0396067ce4@"
		},
		{
			"name": "address",
			"value": "Very New Test Road"
		},
		{
			"name": "order_type",
			"value": 8
		},
		{
			"name": "items",
			"value": [
				{
					"id": "a3",
					"amount": 3
				},
				{
					"id": "a5",
					"amount": 4
				}
			]
		}
	]
}"""

    def setUp(self):
        self.json_fname = '../models.json'
        with open(self.json_fname) as f:
            self.json_models = json.load(f)
        self.request_builder = TemplateBuilder(TemplateTypes.REQUEST)
        self.models_builder = TemplateBuilder(TemplateTypes.MODEL)
        self.models = self.models_builder.build_models_from_json_file(self.json_fname)

    def test_build_from_single_dict(self):
        """ test a single request is built as expected (from a string)"""
        # create a request from json string
        request = self.request_builder.build_template_from_json_str(self.request_str_2)
        self.assertNotEqual(False, request)
        request_validator = RequestValidator(self.models)
        res = request_validator.validate_request(request)
        a = json.dumps(res)
        print(res)