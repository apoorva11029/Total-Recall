#!venv/bin/python

import requests
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/search/<string:query>', methods=['GET'])
def search(query):
	return make_response(jsonify({'name': query+"shit"}))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)

