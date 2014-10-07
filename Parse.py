from Data import Data
import json

data = Data()
regattas = data.getRegattas()
# print regattas
for regatta in regattas:
	r = json.loads(regatta)
	# name = r["name"]
	# host = r["host"]
	link = r["link"] + "rotations"
	# print name + " | " + host
	# print "========================================"
	r["teams"] = []
	for school in data.getTeams(link):
		r["teams"].append(school)
	print r
	
# print regatta["link"]
# url = regatta.link
# url = "http://scores.collegesailing.org/f14/edward-teach/rotations/"
# print data.getTeams(url)[3]