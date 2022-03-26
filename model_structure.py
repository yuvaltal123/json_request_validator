class Param:
    def __init__(self, name: str, types: list[str], required: bool):
        self.name = name
        self.types = types
        self.required = required

    def __str__(self):
        return str(self.__class__) + '\n' + '\n'.join(
            ('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


class ParamBlock:
    def __init__(self, params_dict: dict[str: Param], required_params: set):
        self.params_dict = params_dict
        self.required_params = required_params


class Model:
    def __init__(self, path: str, method: str, query_params: ParamBlock, headers: ParamBlock, body: ParamBlock):
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