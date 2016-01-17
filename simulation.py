#!usr/bin/env python

import json
import click
import random
from agents import Agent
from neural_network import Neuron, NeuralNetwork
#from pyprocessing import *

import sys
sys.setrecursionlimit(10000)

# the code below should be converted to a class!

class Simulation():
	def __init__(self):
		self.agents = []
		self.generation = 0
		#self.cur_best_male = None
		#self.cur_best_female = None
		self.male_names = []
		self.female_names = []
		self.food_x = []
		self.food_y = []

	def makeAgents(self,n):
		with open("male_names.txt","r") as m:
			m = m.readlines()
			self.male_names = [x.replace('\n','') for x in m]	
		with open("female_names.txt","r") as f:
			f = f.readlines()
			self.female_names = [x.replace('\n','') for x in f]
		for i in range(n):
			net = NeuralNetwork()
			net.makeNetwork(2,4,2)
			net.initializeRandomWeights()
			if random.randint(0,1) == 0:
				name = random.choice(self.female_names)
				agent = Agent(name,"female",net)
				self.female_names.remove(name)
			else:
				name = random.choice(self.male_names)
				agent = Agent(name,"male",net)
				self.male_names.remove(name)
			self.agents.append(agent)
	
	def growFood(self):
		food_x = random.randint(0,500)
		food_y = random.randint(0,500)
		food_size = random.randint(50,100)
		self.food_x = [x for x in range(food_x, food_x+food_size)] + self.food_x #add on to existing food matrix	
		self.food_y = [x for x in range(food_y, food_y+food_size)] + self.food_y

	def combine(self,m,f):
		print "combining", m.name, "with", f.name	
		#change all this stuff
		m.reset()
		m.name = random.choice(self.male_names)
		return m # CHANGE ME

	def mutate(self,child):
		print "mutating", child.name
		return [Agent(random.choice(self.female_names),"female",None) for x in range(10)] # change me

	def runSim(self):
		if len(self.food_x) < 50:
			print "Growing food."
			self.growFood()
		a = [x for x in self.agents if x.state != "dead"]
		#males = [x for x in a if x.gender == "male"]
		#females = [x for x in a if x.gender == "female"]
		if len(a) < 3:
			child = self.combine(a[0], a[1])
			self.agents = self.mutate(child)
			a = self.agents
			self.generation += 1
			print "\nGeneration:",self.generation
		for agent in a:
			agent.state = "alive"
			agent.move()
			if agent.x in self.food_x and agent.y in self.food_y:
				agent.state = "eating"
				agent.life += 10000
				self.food_x.remove(agent.x)
				self.food_y.remove(agent.y)
			agent.fitness += 1
			agent.life -= .01
			if agent.life <= 0:
				agent.state = "dead"
				print agent.name, "died."
		return True

	def pause(self):
		print "\nWORLD STATE:"
		for agent in self.agents:
			print agent.name+": "+"State: "+agent.state+" Fitness: "+str(agent.fitness)+" Gender: "+agent.gender+" x: "+str(agent.x)+" y: "+str(agent.y)+" Life: "+str(agent.life)
		menu = raw_input()
		if menu == "quit" or menu == "exit" or menu == "q":
			return False
		elif menu == "save" or menu == "s":
			with click.progressbar(self.agents,label="saving agents...") as bar:
				for agent in bar:
					agent.saveJSON()
			print "agents saved." 
		return True

def main():
	#run()
	sim = Simulation()
	sim.makeAgents(10)
	sim.growFood()
	running = True
	while running:
		try:
			running = sim.runSim()
		except KeyboardInterrupt:
			running = sim.pause()

if __name__=="__main__":
	main()
