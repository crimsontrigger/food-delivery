from flask import Flask, render_template, request
from flask import jsonify
import ui_handler
import json
from flask_cors import CORS
import utils_nosql
from constants import *

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['POST'])
def handle_request():
    response = ""
    json_response = ""

    # Get the json from the request

    req = request.get_json()

    # Get the command from the json
    action = req.get('command')

    if action == 'a_menu':
        response = ui_handler.a_menu()
        print(response)
        json_response = jsonify(response)

    elif action == 'c_menu':
        json_response = jsonify(ui_handler.c_menu())

    elif action == 'order_dets_save':
        params = req.get('params')
        json_response = jsonify(ui_handler.order_save(params))

    elif action == 'order_dets':
        params = req.get('params')
        json_response = jsonify(ui_handler.order_dets(params))

    elif action == 'details':
        params = req.get('params')
        json_response = jsonify(ui_handler.details(params))


    return json_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>/')
def render_static(page_name):
    return render_template('%s' % page_name)


if __name__ == '__main__':
    utils_nosql.drop_col()
    params_to_be_inserted = {ORDER_ID_VAR: 0,
                             NAME_VAR: '',
                             ROOM_VAR: '',
                             PHONE_VAR: '',
                             PAYMENT_MODE_VAR: '',
                             PAYMENT_ID_VAR: '',
                             INITIAL_COST_VAR: 1,
                             FINAL_COST_VAR: 2,
                             PACKING_CHARGE_VAR: (2 * PACKING_CHARGE),
                             }
    utils_nosql.insert_into_db(params_to_be_inserted)
    app.run(host='0.0.0.0', port=80)
