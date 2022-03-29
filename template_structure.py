from enum import Enum


class TemplateTypes(Enum):
    MODEL = 1
    REQUEST = 2


class Content:
    def __init__(self, name: str):
        self.name = name


class Param(Content):
    """ Represents model param field"""
    def __init__(self, name: str, types: list[str], required: bool):
        super().__init__(name)
        self.types = types
        self.required = required


class Value(Content):
    """ Represents request value field"""
    def __init__(self, name: str, value):
        super().__init__(name)
        self.value = value


class ContentBlock:
    """ Represents an object in the json template (query params, headers, body)"""
    def __init__(self, params_dict: dict[str: Content], required_params: set):
        self.params_dict = params_dict
        self.required_params = required_params


class Template:
    """ Represent a template - can be request or model"""
    # Note: these fields should correspond to jsons values
    block_names = {"query_params", "headers", "body"}
    path_name = "path"
    method_name = "method"

    def __init__(self, template_type: TemplateTypes, path: str, method: str, blocks: dict[str:ContentBlock]):
        self.template_type = template_type
        self.path = path
        self.method = method
        self.blocks = blocks

    @property
    def unique_key(self):
        return self.path + ' ' + self.method

    def __str__(self):
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
