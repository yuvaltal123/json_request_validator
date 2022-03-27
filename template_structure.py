from enum import Enum


class TemplateTypes(Enum):
    MODEL = 1
    REQUEST = 2


class Content:
    def __init__(self, name: str):
        self.name = name


class Param(Content):
    def __init__(self, name: str, types: list[str], required: bool):
        super().__init__(name)
        self.types = types
        self.required = required


class Value(Content):
    def __init__(self, name: str, value):
        super().__init__(name)
        self.value = value


class ContentBlock:
    def __init__(self, params_dict: dict[str: Content], required_params: set):
        self.params_dict = params_dict
        self.required_params = required_params


class Template:
    def __init__(self, template_type: TemplateTypes, path: str, method: str, query_params: ContentBlock, headers: ContentBlock, body: ContentBlock):
        self.template_type = template_type
        self.path = path
        self.method = method
        self.query_params = query_params
        self.headers = headers
        self.body = body

    @property
    def unique_key(self):
        return self.path + ' ' + self.method

    def __str__(self):
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))
