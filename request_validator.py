from template_structure import Template
from template_structure import Value, Param
import re
import uuid


class RequestValidator:
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
            self.validate_type(request.headers.params_dict[name].value, model.headers.params_dict[name].types)
        if model.headers.required_params - required_fields_in_request != set():
            print('missing fields', model.headers.required_params - required_fields_in_request)

    def validate_type(self, value, types: list):
        print('gothere')

        first_type_name = types[0]
        # if len(types) == 1:
        """known class"""
        for type in types:
            if type in self.type_mapping:
                if isinstance(value, self.type_mapping[type]):
                    print('valid python type')

        print(value)
        print(types)

    @staticmethod
    def validate_email(email):
        # Make a regular expression
        # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # pass the regular expression
        # and the string into the fullmatch() method
        if re.fullmatch(regex, email):
            print("Valid Email")
        else:
            print("Invalid Email")

    @staticmethod
    def is_valid_email(email):
        # Make a regular expression
        # for validating an Email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # pass the regular expression
        # and the string into the fullmatch() method
        if re.fullmatch(regex, email):
            print("Valid Email")
        else:
            print("Invalid Email")

    @staticmethod
    def is_valid_uuid(value):
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_auth_token(token):
        regex = "^[A-Za-z0-9]*$"
        if token.startswith('Bearer') and bool(re.match(regex, token)):
            return True
        return False
