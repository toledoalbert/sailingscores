from bs4 import BeautifulSoup

import requests
import json
from Regatta import Regatta

class Data:
   "This class gathers and parses the data from college sailing website and stores in objects"

   def __init__(self):
      self.url = "http://scores.collegesailing.org"
      self.regattas = []
   

   "This function loads all the basic regatta information from the website and store into the regattas list"
   def getRegattas(self):

      #Get the response sending a request to the url
      r  = requests.get(self.url)

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
                  link = self.url + info.find('a').get("href")
            elif order == 1:
                  host = info.text
            else:
                  break
            order += 1

         #Make a new regatta object
         regatta = Regatta(name, host, link)

         #Append the new regatta object to the list
         self.regattas.append(regatta)

      #Pop the first object since that was the titles for the columns
      self.regattas.pop(0)

      #array to return
      regattas = []

      #Print the objects collected from the site as json
      for regatta in self.regattas:
         regattas.append(regatta.to_JSON())
      return regattas


   def getTeams(self, regattaUrl):

      #Get the response from the url
      r = requests.get(regattaUrl)

      #Get the html into a string
      data = r.text

      #create the soup object
      soup = BeautifulSoup(data)

      #teams array
      teams = []

      #Get the first table possible
      table = soup.find('tbody')
      if table:
         for team in table.find_all("td", {"class" : "teamname"}):
            teams.append(team.text)

         return teams
      else:
         return "Teams not available"

   


   # def loadRotations(self, regattaUrl):
   #    #Get the response sending a request to the url
   #    r  = requests.get(regattaUrl)

   #    #Get the html into a string
   #    data = r.text

   #    #get the soup object
   #    soup = BeautifulSoup(data)

   #    #Go through the table regatta variable as each row
   #    # for regatta in soup.find_all('tr'):
