#!/usr/bin/python3
""" flask api """
from os import getenv
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r'/*': {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_context(exception):
    """closes on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Response in JSON if error 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=api_host, port=api_port, threaded=True)
