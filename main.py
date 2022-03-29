import traceback
from flask import Flask, jsonify, request
from template_builder import TemplateBuilder
from template_structure import TemplateTypes
from validator import Validator

EXIT_CODE = -1
MODELS_FILE_PATH = "models.json"


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def processjson():
    if request.method == 'POST':
        try:
            data = request.get_json()
            user_request = request_builder.build_template_from_dict(data)
            res = request_validator.validate_request(user_request)
            return jsonify(res)
        except Exception:
            print('Exception handling request\n')
            print(traceback.format_exc())
            exit(EXIT_CODE)
    else:
        return "Hello from Requests Validator"


""" One time setups"""
try:
    model_builder = TemplateBuilder(TemplateTypes.MODEL)
    models = model_builder.build_models_from_json_file(MODELS_FILE_PATH)
    if not models:
        exit(EXIT_CODE)
    request_validator = Validator(models)
    request_builder = TemplateBuilder(TemplateTypes.REQUEST)
except Exception:
    print('Exception during setup\n')
    print(traceback.format_exc())
    exit(EXIT_CODE)


app.config['JSON_SORT_KEYS'] = False
app.run(debug=True)
