import datetime
from template_structure import Template
import re
import uuid


class Validator:
    """ Verifies if a request is valid or "abnormal" based on the "learned" models """
    type_mapping = {"String": str, "Int": int, "Boolean": bool, "List": list}

    def __init__(self, models: dict[str: Template]):
        self.models = models

    def validate_request(self, request: Template):
        model = self.models[request.unique_key]

        required_fields_in_request = set()
        for name in request.headers.params_dict:
            print(name)
            if name not in model.headers.params_dict:
                print('field exist in request but not in model ', name)
                continue
            if name in model.headers.required_params:
                required_fields_in_request.add(name)
            self._validate_type(request.headers.params_dict[name].value, model.headers.params_dict[name].types)
        if model.headers.required_params - required_fields_in_request != set():
            print('missing fields', model.headers.required_params - required_fields_in_request)

    def _validate_type(self, value, types: list):
        print('gothere')
        first_type_name = types[0]
        # if len(types) == 1:
        """known class"""
        for type in types:
            if type in self.type_mapping:
                if isinstance(value, self.type_mapping[type]):
                    print('valid python type')

    @staticmethod
    def _is_valid_py_type(value, py_type):
        return isinstance(value, py_type)

    @staticmethod
    def _is_valid_email(email):
        """validate email based on regex from
            https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/"""
        # Make a regular expression
        # for validating an Email
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if re.fullmatch(regex, email):
            return True
        return False

    @staticmethod
    def _is_valid_uuid(value):
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_valid_auth_token(token):
        regex = r'^Bearer+[a-zA-Z0-9]+$'
        if re.search(regex, token):
            return True
        return False

    @staticmethod
    def _is_valid_date(date):
        try:
            datetime.datetime.strptime(date, '%d-%m-%Y')
            return True
        except ValueError:
            return False