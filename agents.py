#!usr/bin/env python

class Agent():
	def __init__(self,name,gender,network):
		self.fitness = 0
		self.name = name.replace("\n","")
		self.gender = gender
		self.net = network
		from random import randint
		self.x = randint(0,600)
		self.y = randint(0,600)
		self.color = [randint(0,255) for x in range(3)]
		self.life = 10000.0+randint(0,10000)
		self.state = "alive"
		self.json_data = {"name":name,
			"gender":gender,
			"fitness":self.fitness,
			"x":self.x, "y":self.y,
			"color":self.color,
			"life":self.life,
			"state":self.state} 
	
	def reset(self):
		self.fitness = 0
		from random import randint
		self.life = 100000.0+randint(0,10000)
		self.state = "alive"
	
	def saveJSON(self):
		import json
		self.json_data["fitness"] = self.fitness
		with open("agents/"+self.name, "w") as outfile:
			json.dump(self.json_data, outfile)
