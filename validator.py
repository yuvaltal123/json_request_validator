import datetime
from template_structure import Template
import re
import uuid


class RequestValidator:
    """ Verifies if a request is valid or "abnormal" based on the "learned" models """

    def __init__(self, models: dict[str: Template]):
        self.models = models
        self.type_validator = TypeValidator()

    def validate_request(self, request: Template) -> dict:
        """ validates a single request according to the corresponding model and return the validation result"""
        is_valid = True
        validation_results = dict()
        validation_results["result"] = "normal"
        model = self.models[request.unique_key]
        for (block_name, content_block), (_, model_block) in zip(request.blocks.items(), model.blocks.items()):
            is_valid_block, block_validations_results = self._validate_single_block(content_block, model_block)
            is_valid &= is_valid_block
            validation_results[block_name] = block_validations_results
        validation_results["result"] = "normal" if is_valid else "abnormal"
        return validation_results

    def _validate_single_block(self, content_block, model_block):
        is_valid = True
        block_validations_results = list()
        required_fields_in_request = set()
        """ validate type mismatch or field that's not allowed in model"""
        for name in content_block.params_dict:
            if name not in model_block.params_dict:
                block_validations_results.append({name: 'field does not appear in model'})
                continue
            if name in model_block.required_params:
                required_fields_in_request.add(name)
            field_value, expected_types = content_block.params_dict[name].value, model_block.params_dict[name].types
            if not self.type_validator.validate_type(field_value, expected_types):
                block_validations_results.append({name: 'type mismatch'})
        """ validate required fields"""
        required_fields_missing = model_block.required_params - required_fields_in_request
        if required_fields_missing:
            for missing_param in required_fields_missing:
                block_validations_results.append({missing_param: 'missing required parameter'})
        """ determine result per block"""
        if len(block_validations_results) != 0:
            is_valid = False
        return is_valid, block_validations_results


class TypeValidator:
    """ Validates a value is in required type"""
    def __init__(self):
        self._type_mapping = {"String": str, "Int": int, "Boolean": bool, "List": list}
        self._custom_type_mapping = {"UUID": self._is_valid_uuid, "Auth-Token": self._is_valid_auth_token,
                            "Email": self._is_valid_email, "Date": self._is_valid_date}

    def validate_type(self, value, types: list) -> bool:
        for type_name in types:
            result = True
            if type_name in self._type_mapping:
                result &= self._is_valid_py_type(value, self._type_mapping[type_name])
            elif type_name in self._custom_type_mapping:
                result &= self._custom_type_mapping[type_name](value)
            else:
                print(f'Unsupported type: {type_name}')
                return False
        return result

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
        regex = r'^Bearer +[a-zA-Z0-9]{32}$'
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



