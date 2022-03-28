import unittest
from validator import Validator


class TestModelsBuilder(unittest.TestCase):

    def test_valid_emails(self):
        valid_emails_examples = {"yuvaltal123@gmail.com", "yuvaltal123@walla.com", "yuvaltal123@walla.co.il", "abc@gmail.com",
                        "example@yahoo.com"}
        valid_email_prefixes = {"abc.def@mail.com", "abc@mail.com", "abc_def@mail.com"}
        valid_email_domains = {"abc.def@mail.cc", "abc.def@mail-archive.com", "abc.def@mail.org", "abc.def@mail.com"}
        valid_emails = valid_email_prefixes | valid_email_domains | valid_emails_examples
        for valid_email in valid_emails:
            validator_result = Validator._is_valid_email(valid_email)
            self.assertEqual(True, validator_result)

    def test_invalid_emails(self):
        invalid_email_prefixes = {"abc#def@mail.com", ".abc@mail.com", "abc..def@mail.com", "abc-@mail.com"}
        invalid_email_domains = {"abc.def@mail.c", "abc.def@mail#archive.com", "abc.def@mail", "abc.def@mail..com"}
        invalid_emails_examples = {"yuvaltal123gmail.com", "", "bb@com", "com", "yuval@walla"}
        invalid_emails = invalid_email_prefixes | invalid_email_domains | invalid_emails_examples
        for invalid_email in invalid_emails:
            validator_result = Validator._is_valid_email(invalid_email)
            self.assertEqual(False, validator_result)

    def test_valid_uuids(self):
        valid_uuids = {"46da6390-7c78-4a1c-9efa-7c0396067ce4"}
        for uuid in valid_uuids:
            validator_result = Validator._is_valid_uuid(uuid)
            self.assertEqual(True, validator_result)

    def test_invalid_uuids(self):
        invalid_uuids = {"46da6390-7c78-4a1c-9efa-7c0396067ce46", "123", "46da63907c78-4a1c-9efa-7c0396067ce46",
                       "46da6390-07c78-4a1c-9efa-7c0396067ce46", "46da6390-7c784a1c-9efa-7c0396067ce46"}
        for uuid in invalid_uuids:
            validator_result = Validator._is_valid_uuid(uuid)
            self.assertEqual(False, validator_result)

    def test_valid_auth_tokens(self):
        valid_auth_tokens = {"Bearerebb3cbbe938c4776bd22a4ec2ea8b2ca", "BearerAB", "Bearerab"}
        for token in valid_auth_tokens:
            validator_result = Validator._is_valid_auth_token(token)
            self.assertEqual(True, validator_result)

    def test_invalid_auth_tokens(self):
        invalid_auth_tokens = {"aBearerebb3cbbe938c4776bd22a4ec2ea8b2ca", "aearerebb3cbbe938c4776bd22a4ec2ea8b2ca", " ",
                               "Bearerebb3cbbe938c4776bd22a4ec2ea8b2c@", "Bearerebb3cbbe938c4776bd22a4ec2ea8b2c.",
                               "Bearer"}
        for token in invalid_auth_tokens:
            validator_result = Validator._is_valid_auth_token(token)
            self.assertEqual(False, validator_result)

    def test_valid_dates(self):
        valid_dates = {"04-05-1994", "04-05-2005", "30-12-2015"}
        for date in valid_dates:
            validator_result = Validator._is_valid_date(date)
            self.assertEqual(True, validator_result)

    def test_invalid_dates(self):
        invalid_dates = {"04-31-1994", "99-05-2005", "30-12-11"}
        for date in invalid_dates:
            validator_result = Validator._is_valid_date(date)
            self.assertEqual(False, validator_result)

    def test_valid_py_types(self):
        py_types = [str, bool, int, list]
        vals = ["abc", True, 3, []]
        for val, py_type in zip(vals, py_types):
            validator_result = Validator._is_valid_py_type(val, py_type)
            self.assertEqual(True, validator_result)

    def test_invalid_py_types(self):
        py_types = [str, bool, int, list]
        vals = [3, 'true', "a", {}]
        for val, py_type in zip(vals, py_types):
            validator_result = Validator._is_valid_py_type(val, py_type)
            self.assertEqual(False, validator_result)