import sys
sys.path.append("../scheduler")

import os
from flask import Flask, render_template, send_from_directory, request, jsonify, make_response, current_app
from functools import wraps
from constants import SINGLE_VALUE_KEY, DEBUG
from scheduler import main as main_scheduler
backend_path = "/API"

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")

def json_route(function):
    '''Makes functions take a data parameter that will be a dict and then when they return a dict, it will be encoded into JSON'''
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = request.get_json(force=True)
        if "data" not in kwargs:
            kwargs["data"] = data
        else:
            raise RuntimeError("The key 'data' should be reserved for the JSON, but it is not")
        non_json_ans = function(*args, **kwargs)
        ans = jsonify(non_json_ans)
        return ans
    return wrapper

@app.route("/")
def index():
    return render_template("schedule.html")

@app.route(backend_path + "/schedule", methods=["POST"])
@json_route
def schedule(data):
    # note that index is a string, not a number
    info = data[SINGLE_VALUE_KEY]
    response = main_scheduler(info)
    return {SINGLE_VALUE_KEY: response}

if __name__ == "__main__":
    if DEBUG:
        app.run(debug=False, port=5001)
