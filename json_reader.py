import json

const_titles = {'headers', 'query_params', 'body'}
request_titles = {'name', 'value'}
model_titles = {'name', 'types', 'required'}


# code to validate fields exist:
# required_fields = {'field'}
# allowed_fields = required_fields | {'group', 'function'}
#
# d = {'field': 12,'bound': 123,'bddsund': 123, 'boufnd': 123}  # Set any value here
#
# if required_fields <= d.keys() <= allowed_fields:
#     print("Yes!")
# else:
#     print("No!")


def load_from_json_file(json_fname):
    """ load json to file"""
    try:
        with open(json_fname) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {json_fname} not found.  Aborting")
    except OSError:
        print(f"OS error occurred trying to open {json_fname}")
    except Exception as err:
        print(f"Unexpected error opening {json_fname} is", repr(err))
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
    return False


def load_from_json_str(json_str):
    try:
        return json.loads(json_str)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
