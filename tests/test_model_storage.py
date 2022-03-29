# import sys, os
# sys.path.append('../')
import unittest
import pickle
from json_reader import load_from_json_str
import json
from template_structure import ContentBlock, Param, Template
from template_builder import TemplateBuilder, TemplateTypes


class TestModelsBuilder(unittest.TestCase):
    single_model_str = """{
        "path": "/users/info",
        "method": "GET",
        "query_params": [
            {
                "name": "with_extra_data",
                "types": ["Boolean"],
                "required": false
            },
            {
                "name": "user_id",
                "types": ["String", "UUID"],
                "required": false
            }
        ],
        "headers": [
            {
                "name": "Authorization",
                "types": ["String", "Auth-Token"],
                "required": true
            }
        ],
        "body": []
    }"""

    def setUp(self):
        self.json_fname = '../models.json'
        with open(self.json_fname) as f:
            self.json_models = json.load(f)
        self.model_builder = TemplateBuilder(TemplateTypes.MODEL)
        self.models = self.model_builder.build_models_from_json_file(self.json_fname)

    def test_build_models_from_json(self):
        """ test the number models stored is as expected"""
        self.assertEqual(len(self.models), len(self.json_models))

    def test_build_from_single_dict(self):
        """ test a single model is built as expected (from a string)"""
        # create a dict from test string
        dic = load_from_json_str(TestModelsBuilder.single_model_str)
        # create a model from the dict
        model_test = self.model_builder.build_template_from_dict(dic)
        # get first model from json
        first_model_from_json = self.models[model_test.unique_key]
        # make sure that the model contents is the same
        self.assertEqual(pickle.dumps(first_model_from_json) == pickle.dumps(model_test), True)

    def test_create_new_model_from_vals(self):
        # create a dict from test string
        dic = load_from_json_str(TestModelsBuilder.single_model_str)
        # create a model from the dict
        model_test = self.model_builder.build_template_from_dict(dic)

        path = dic['path']
        method = dic['method']
        # test unique key
        self.assertEqual(model_test.unique_key, "/users/info GET")
        # test query params
        param1 = Param("with_extra_data", ["Boolean"], False)
        param2 = Param("user_id", ["String", "UUID"], False)
        required = set()
        new_query_params = ContentBlock({"with_extra_data": param1, 'user_id': param2}, required)
        self.assertEqual(pickle.dumps(model_test.blocks['query_params']), pickle.dumps(new_query_params))
        # test headers
        param = Param("Authorization", ["String", "Auth-Token"], True)
        required = {'Authorization'}
        new_headers = ContentBlock({"Authorization": param}, required)
        self.assertEqual(pickle.dumps(model_test.blocks['headers']), pickle.dumps(new_headers))
        # test body
        required = set()
        new_body = ContentBlock({}, required)
        self.assertEqual(pickle.dumps(model_test.blocks['body']), pickle.dumps(new_body))
        first_model_from_json = self.models[model_test.unique_key]
        new_model = Template(TemplateTypes.MODEL, path, method, {'query_params': new_query_params, 'headers':  new_headers, 'body': new_body})
        print(new_model, '\n')
        print(first_model_from_json)
        self.assertEqual(pickle.dumps(new_model.method) == pickle.dumps(first_model_from_json.method), True)
        self.assertEqual(pickle.dumps(new_model.path) == pickle.dumps(first_model_from_json.path), True)
        self.assertEqual(pickle.dumps(new_model.blocks['query_params']) == pickle.dumps(first_model_from_json.blocks['query_params']), True)
        self.assertEqual(pickle.dumps(new_model.blocks['headers']) == pickle.dumps(first_model_from_json.blocks['headers']), True)
        self.assertEqual(pickle.dumps(new_model.blocks['body']) == pickle.dumps(first_model_from_json.blocks['body']), True)
        self.assertEqual(pickle.dumps(new_model.unique_key) == pickle.dumps(first_model_from_json.unique_key), True)
        # todo check
        # self.assertEqual(pickle.dumps(new_model) == pickle.dumps(first_model_from_json), True)

    def test_required_sets(self):
        """ test the required sets are as expected for the first model"""
        model_key = "/users/info GET"
        expected_query_required_params = set()
        expected_header_required_params = {'Authorization'}
        expected_body_required_params = set()
        model = self.models[model_key]

        self.assertSetEqual(model.blocks['query_params'].required_params, expected_query_required_params)
        self.assertSetEqual(model.blocks['headers'].required_params, expected_header_required_params)
        self.assertSetEqual(model.blocks['body'].required_params, expected_body_required_params)


if __name__ == '__main__':
    unittest.main()
