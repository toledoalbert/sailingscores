#!flask/bin/python
from flask import Flask, jsonify, request
# from Data import Data
import json
from bs4 import BeautifulSoup
import requests
# from Regatta import Regatta
from models import *

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

@app.route('/rotations/<regatta>', methods=['GET'])
def get_rotations(regatta):
	rotations = []

	r = requests.get("http://scores.collegesailing.org/f14/" + regatta + "/rotations/")
	data = r.text
	soup = BeautifulSoup(data)

	for rotationTable in soup.find_all(class_='port'):
		raceNames = []
		head = rotationTable.find('thead')

		for raceName in head.find_all('th'):
			raceNames.append(raceName.text)
		raceNames.pop(0)
		raceNames.pop(0)

		teamNames = []

		for teamName in rotationTable.find_all(class_='teamname'):
			teamNames.append(teamName.text)
		divName = rotationTable.find('h3').text

		r = Rotation(divName)

		t = rotationTable.find('tbody')

		countTeams = 0

		for row in t.find_all('tr'):
			countRaces = 0

			rotTeam = RotationTeam(teamNames[countTeams])

			for race in row.find_all(class_='sail'):
				teamRace = Race(raceNames[countRaces], race.text)
				rotTeam.races.append(teamRace.to_json())
				if countRaces < raceNames.__len__():
					countRaces = countRaces + 1
			r.teams.append(rotTeam.to_json())

			if countTeams < teamNames.__len__():
				countTeams = countTeams + 1
		rotations.append(r.to_json())
	response = {'rotations': rotations}
	return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)