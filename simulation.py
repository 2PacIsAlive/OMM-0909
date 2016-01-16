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
		#self.cur_best_male = None
		#self.cur_best_female = None
		self.male_names = []
		self.female_names = []
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
	
	def combine(self,m,f):
		print "combining", m.name, "with", f.name	
		#change all this stuff
		m.reset()
		m.name = random.choice(self.male_names)
		return m # CHANGE ME

	def mutate(self,child):
		return [Agent(random.choice(self.female_names),"female",None) for x in range(10)] # change me

	def runSim(self):
		a = [x for x in self.agents if x.state != "dead"]
		#males = [x for x in a if x.gender == "male"]
		#females = [x for x in a if x.gender == "female"]
		if len(a) < 3:
			child = self.combine(a[0], a[1])
			self.agents = self.mutate(child)
			a = self.agents
		for agent in a:
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
	running = True
	while running:
		try:
			running = sim.runSim()
		except KeyboardInterrupt:
			running = sim.pause()

if __name__=="__main__":
	main()
