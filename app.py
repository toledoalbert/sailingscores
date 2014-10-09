#!flask/bin/python
from flask import Flask, jsonify, request
# from Data import Data
import json
from bs4 import BeautifulSoup
import requests
# from Regatta import Regatta
from models import Moment

app = Flask(__name__)

# url = "http://scores.collegesailing.org"

@app.route('/')
def index():
    return "This is the root for sailing scores API"

@app.route('/regattas', methods=['GET'])
def get_regattas():
	m = Moment()
	# print m.to_json()
	return jsonify(m.to_json())

# @app.route('/rotations', methods=['GET'])
# def get_rotations():
	

if __name__ == '__main__':
    app.run(debug=True)