#!flask/bin/python
from flask import Flask, jsonify, request
import json
from bs4 import BeautifulSoup
import requests

class Regatta():
   'Class that represents a Regatta'

   def __init__(self, name, host, link):
      self.name = name
      self.host = host
      self.link = link
      self.teams = []

      r = requests.get(link + "rotations")

      data = r.text

      soup = BeautifulSoup(data)

      table = soup.find_all('tbody')

      if table:
         for row in table:
            for col in row.find_all("td", {"class" : "teamname"}):
               self.teams.append({'name': col.text, 'rotation':[], 'scores':[]})
      else:
         self.teams.append("Teams not available")



   def to_json(self):
      return {
         'name': self.name,
         'host': self.host,
         'link': self.link,
         'teams': self.teams
      }



class Rotation():
   'Class that represents the rotation of a team in a Regatta'

   def __init__(self, divName):
      self.divName = divName
      self.teams = []

   def to_json(self):
      return {
         'division': self.divName,
         'teams': self.teams
      }



class RotationTeam():
   'Class that represents a rotation for a single team in a regatta'

   def __init__(self, teamName):
      self.teamName = teamName
      self.races = []

   def to_json(self):
      return {
         'name': self.teamName,
         'races': self.races
      }



class Race():
   'Class that represents a race for a rotation or score table'

   def __init__(self, name, value):
      self.name = name
      self.value = value

   def to_json(self):
      return {
         'name': self.name,
         'value': self.value
      }




class Moment():
   'Class that represent any given moment'

   def __init__(self):
      self.url = "http://scores.collegesailing.org"
      self.regattas = []

      r = requests.get(self.url)

      data = r.text

      soup = BeautifulSoup(data)

      for regatta in soup.find_all('tr'):
         name = ""
         host = ""
         link = ""
         order = 0

         for info in regatta.find_all('td'):
            if order == 0:
               name = info.text
               link = self.url + info.find('a').get("href")
            elif order == 1:
               host = info.text
            else:
               break
            order += 1

         if order > 0:
            reg = Regatta(name, host, link)

            self.regattas.append(reg.to_json())

   def to_json(self):
      return {
         'url': self.url,
         'regattas': self.regattas
      }


r = requests.get("http://scores.collegesailing.org/f14/tom-curtis/rotations/")
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
      # print countTeams
      countRaces = 0
      # print countTeams
      rotTeam = RotationTeam(teamNames[countTeams])
      for race in  row.find_all(class_='sail'):
         teamRace = Race(raceNames[countRaces], race.text)
         rotTeam.races.append(teamRace.to_json())
         if countRaces < raceNames.__len__():
            countRaces = countRaces + 1
      r.teams.append(rotTeam.to_json())
      # print rotTeam.to_json()
      if countTeams < teamNames.__len__():
         countTeams = countTeams + 1

   print r.to_json()
   # print raceNames
   # print teamNames

