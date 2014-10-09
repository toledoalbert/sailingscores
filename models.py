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


