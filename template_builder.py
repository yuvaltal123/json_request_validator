import json_reader
from template_structure import Param, ContentBlock, Template, Value, TemplateTypes


TEMPLATE_CONTENT_TYPES = {TemplateTypes.MODEL: Param, TemplateTypes.REQUEST: Value}


class TemplateBuilder:
    """ Responsible for building the template object from json file/string/dict"""

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
            model = self.build_template_from_dict(model_dict)
            models[model.unique_key] = model
        return models

    def build_template_from_json_str(self, json_str: str) -> Template:
        """ Adding all templates from json file to the models storage dict
            the key is the template unique key and value is the template"""
        template_dict = json_reader.load_from_json_str(json_str)
        if not template_dict:
            return False
        return self.build_template_from_dict(template_dict)

    def build_template_from_dict(self, template_dict: dict) -> Template:
        """ Build a template from a dictionary representing it"""
        blocks = dict()
        for block_name in Template.block_names:
            params_dict, required_set = self._build_params_dict_per_block(template_dict[block_name])
            block = ContentBlock(params_dict, required_set)
            blocks[block_name] = block
        return Template(self.template_type, template_dict[Template.path_name], template_dict[Template.method_name], blocks)

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

