from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
from create_stack_dash import run_using_ui, stop_tests_using_ui, Config
from waitress import serve
from database_ops import retrieve_test_results

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv'}
NUMBER_OF_ROWS_TO_GET = 10

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=["POST", "GET"])
def parse_request():
    if request.method == 'POST':
        button_pressed = request.form.get('button')
        print('Request Type: {0}'.format(button_pressed))

        if button_pressed == 'generate_load':
            data = json.loads(request.form.get('form'))
            print('Data sent from UI: {0}'.format(data))
            returned_url = run_using_ui(data)
            prefix = data['prefix']
            if returned_url:
                return make_response(jsonify(url=returned_url, stack_name=prefix), 201)
            else:
                return make_response("Error", 500)
        elif button_pressed == 'stop_individual_test':
            prefix = request.form.get('stack')
            stop_tests_using_ui(prefix=prefix)
            return make_response(jsonify("Test {0} terminated".format(prefix)), 201)

    if request.method == 'GET':
        test_results = retrieve_test_results(NUMBER_OF_ROWS_TO_GET)
        grafana_url = Config.grafana_url
        return make_response(jsonify(test_results, grafana_url), 201)


CORS(app)
serve(app, host='0.0.0.0', port=5000)
