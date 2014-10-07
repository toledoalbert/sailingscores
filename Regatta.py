from jsonable import jsonable

class Regatta(jsonable):
   'Class that represents a Regatta'
   regattaCount  = 0

   def __init__(self, name, host, link):
      self.name = name
      self.host = host
      self.link = link
      self.teams = [] #RotationTeam objects
      Regatta.regattaCount += 1
   
   def displayCount(self):
     print "Total Regatta %d" % Regatta.empCount

   def displayRegatta(self):
      print "Name : ", self.name,  ", Host: ", self.host, ", Link: ", self.link