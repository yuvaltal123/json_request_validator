import json_reader
from model_structure import Param, ParamBlock, Model


class ModelsBuilder:
    """ Model Builder is responsible for building the models classes from json file"""
    @staticmethod
    def build_models_from_json(json_fname: str) -> dict[str: Model]:
        """ Adding all models from json file to the models storage dict
            the key is the model unique key and value is the model"""

        # Note: using a dict (and not a list of models) to efficiently lookup for model param when going
        # over the requests later

        models = {}
        # read models as json
        json_models = json_reader.load_from_json_file(json_fname)
        if not json_models:
            return False
        # store models - path,method use as unique key, 'headers','query_params','body' as values

        for model_dict in json_models:
            # print(model_dict)
            model = ModelsBuilder._build_model_from_dict(model_dict)
            models[model.unique_key] = model
            # print(model , '\n')
        return models

    @staticmethod
    def _build_model_from_dict(model_dict):
        params_dict, required_set = ModelsBuilder._build_params_dict_per_block(model_dict['query_params'])
        query_params = ParamBlock(params_dict, required_set)
        params_dict, required_set = ModelsBuilder._build_params_dict_per_block(model_dict['headers'])
        headers = ParamBlock(params_dict, required_set)
        params_dict, required_set = ModelsBuilder._build_params_dict_per_block(model_dict['body'])
        body = ParamBlock(params_dict, required_set)
        model = Model(model_dict['path'], model_dict['method'], query_params, headers, body)
        return model

    @staticmethod
    def _build_params_dict_per_block(list_of_param_dicts: list) -> tuple[dict[str: Param], set]:
        """ build for every block ('query_params', 'headers', 'body')
            a dictionary where key - param name, value - param
        """
        # Note: using a dict (and not a list of params for example) to efficiently lookup for param when going
        # over the request values later

        params_dict = dict()
        required_set = set()
        for param_dict in list_of_param_dicts:
            param = Param(param_dict['name'], param_dict['types'], param_dict['required'])
            params_dict[param.name] = param
            if param.required:
                required_set.add(param.name)
        return params_dict, required_set
