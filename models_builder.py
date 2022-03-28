from enum import Enum

import json_reader
from template_structure import Param, ContentBlock, Template, Value, TemplateTypes


TEMPLATE_CONTENT_TYPES = {TemplateTypes.MODEL: Param, TemplateTypes.REQUEST: Value}


class TemplateBuilder:
    """ Responsible for building the template object from json file/string"""

    def __init__(self, template_type: TemplateTypes):
        self.template_type = template_type

    @property
    def content_cls(self):
        return TEMPLATE_CONTENT_TYPES[self.template_type]

    def build_models_from_json_file(self, json_fname: str) -> dict[str: Template]:
        """ Adding all templates from json file to the models storage dict
            the key is the template unique key and value is the template"""

        # Note: using a dict (and not a list of models) to efficiently lookup for model param when going
        # over the requests later

        models = {}
        # read models as json
        json_models = json_reader.load_from_json_file(json_fname)
        if not json_models:
            return False
        # store models - path,method use as unique key, 'headers','query_params','body' as values

        for model_dict in json_models:
            model = self._build_model_from_dict(model_dict)
            models[model.unique_key] = model
        return models

    def build_template_from_json_str(self, json_str: str) -> [Template]:
        """ Adding all templates from json file to the models storage dict
            the key is the template unique key and value is the template"""

        template_dict = json_reader.load_from_json_str(json_str)
        if not template_dict:
            return False
        template = self._build_model_from_dict(template_dict)
        return template

    def _build_model_from_dict(self, model_dict):
        params_dict, required_set = self._build_params_dict_per_block(model_dict['query_params'])
        query_params = ContentBlock(params_dict, required_set)
        params_dict, required_set = self._build_params_dict_per_block(model_dict['headers'])
        headers = ContentBlock(params_dict, required_set)
        params_dict, required_set = self._build_params_dict_per_block(model_dict['body'])
        body = ContentBlock(params_dict, required_set)
        template = Template(self.template_type, model_dict['path'], model_dict['method'], query_params, headers, body)
        return template

    def _build_params_dict_per_block(self, list_of_param_dicts: list) -> tuple[dict[str: Param], set]:
        """ build for every block ('query_params', 'headers', 'body')
            a dictionary where key - param name, value - param
        """
        # Note: using a dict (and not a list of params for example) to efficiently lookup for param when going
        # over the request values later

        params_dict = dict()
        required_set = set()
        for param_dict in list_of_param_dicts:
            param = self.content_cls(**param_dict)
            params_dict[param.name] = param
            if self.content_cls == Param and param.required:
                required_set.add(param.name)
        return params_dict, required_set

    # @staticmethod
    # def _build_request_from_dict(model_dict):
    #     params_dict, required_set = TemplateBuilder._build_values_dict_per_block(model_dict['query_params'])
    #     query_params = ContentBlock(params_dict, required_set)
    #     params_dict, required_set = TemplateBuilder._build_values_dict_per_block(model_dict['headers'])
    #     headers = ContentBlock(params_dict, required_set)
    #     params_dict, required_set = TemplateBuilder._build_values_dict_per_block(model_dict['body'])
    #     body = ContentBlock(params_dict, required_set)
    #     model = Template(model_dict['path'], model_dict['method'], query_params, headers, body)
    #     return model
    #
    # @staticmethod
    # def _build_values_dict_per_block(list_of_param_dicts: list) -> tuple[dict[str: Value], set]:
    #     """ build for every block ('query_params', 'headers', 'body')
    #         a dictionary where key - param name, value - param
    #     """
    #     # Note: using a dict (and not a list of params for example) to efficiently lookup for param when going
    #     # over the request values later
    #
    #     params_dict = dict()
    #     required_set = set()
    #     for param_dict in list_of_param_dicts:
    #         param = Value(param_dict['name'], param_dict['value'])
    #         params_dict[param.name] = param
    #     return params_dict, required_set
