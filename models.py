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
      tmp = link.split("/")
      self.label = tmp[tmp.__len__()-2]

      r = requests.get(link) #+ "rotations")

      data = r.text

      soup = BeautifulSoup(data)

      table = soup.find_all('tbody')

      if table:
         for t in table:
            for d in row.find_all("tr"):
               info = d.find_all("td")
               # self.teams.append({'name': col.text, 'rotation':[], 'scores':[]})
               self.teams.append({'name': info[3] })
      else:
         self.teams.append("Teams not available")



   def to_json(self):
      return {
         'name': self.name,
         'label': self.label,
         # 'host': self.host,
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


