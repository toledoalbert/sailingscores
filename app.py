#!flask/bin/python
from flask import Flask, jsonify, request
from Data import Data
import json
from bs4 import BeautifulSoup
import requests
from Regatta import Regatta

app = Flask(__name__)

# url = "http://scores.collegesailing.org"

@app.route('/')
def index():
    return "This is the root for sailing scores API"

@app.route('/regattas', methods=['GET'])
def get_regattas():
	url = "http://scores.collegesailing.org"
	regattas = []

	#Get the response sending a request to the url
	r  = requests.get(url)

	#Get the html into a string
	data = r.text

	#get the soup object
	soup = BeautifulSoup(data)

	#Go through the table regatta variable as each row
	for regatta in soup.find_all('tr'):

		#Variables to hold regatta information
		order = 0
		name = ""
		host = ""
		link = ""

		#go through each column to get host and name
		for info in regatta.find_all('td'):
			if order == 0:
			      name = info.text
			      link = url + info.find('a').get("href")
			elif order == 1:
			      host = info.text
			else:
			      break
			order += 1

		#Make a new regatta object
		regatta = Regatta(name, host, link)

		#Append the new regatta object to the list
		regattas.append(regatta)

		#Pop the first object since that was the titles for the columns
		regattas.pop(0)

		#array to return
		reponse = []

		#Print the objects collected from the site as json
		for regatta in regattas:
	    		response.append(regatta.to_JSON())
	return response

if __name__ == '__main__':
    app.run(debug=True)