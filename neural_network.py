#!usr/bin/env python

from PIL import Image
import random
import glob
import math
import os

class Neuron():
	def __init__(self):
		self.act = None
		self.inputConnections = []
		self.hiddenConnections = []
		self.outputConnections = []

class NeuralNetwork():
	def __init__(self):
		#self.purpose = purpose
		self.inputLayer = []
		self.hiddenLayer = []
		self.outputLayer = []
		self.inputActivations = []
		self.hiddenActivations = []
		self.outputActivations = []
		self.epochError = 0
		self.epochs = 0
		self.stateList = []

	def makeNetwork(self,inputSize, hiddenSize, outputSize):
		for input_node in range(inputSize):
			self.inputLayer.append(Neuron())
		for hidden_node in range(hiddenSize):
			self.hiddenLayer.append(Neuron())
		for output_node in range(outputSize):
			self.outputLayer.append(Neuron())	

	def genInputActivations(self):
		inputCounter = {"airplane":0, "automobile":0, 
				"bird": 0, "cat":0,
				"deer": 0, "dog": 0,
				"frog": 0, "horse": 0,
				"ship": 0, "truck": 0}
		for file_ in glob.glob("images/saved/*"):	
			label = Image.open(file_)
			pix = list(label.getdata())
			activation = []
			for pixel in pix:
				hexval = hex(pixel[0]) + hex(pixel[1])[:1] + hex(pixel[2])[:1]
				activation.append((int(hexval,16))/100000.0)
			filename = file_[13:-5]
			category = ""
			for char in filename:
				if char not in ["_","0","1","2","3","4","5","6","7","8","9"]:
					category += char
			inputCounter[category] += 1
			if category in ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]:
				if inputCounter[category] < 8:	
					self.inputActivations.append((activation,category))

	def setInputActivation(self,x,y):
		self.inputActivations.append(x)
		self.inputActivations.append(y)

	def sigmoid(self,activation):
		try:
			return 1 / (1 + math.exp(-activation))	
		except OverflowError:
			return 0 
	
	def hiddenActivationFunction(self,node,index):
		xw = 0
		zw = 0
		for input_node in self.inputLayer:
			xw += input_node.hiddenConnections[index] * float(input_node.act) 
		for output_node in self.outputLayer:
			zw += output_node.hiddenConnections[index] * float(input_node.act)
		return self.sigmoid(xw + zw)

	def outputActivationFunction(self,node,index):
		f = 0
		for hidden_node in self.hiddenLayer:
			f += hidden_node.outputConnections[index] * float(hidden_node.act)
		return self.sigmoid(f)

	def getLabel(self,node):
		if node == self.outputLayer[0]:
			return "airplane"
		elif node == self.outputLayer[1]:
			return "automobile"
		elif node == self.outputLayer[2]:
			return "bird"
		elif node == self.outputLayer[3]:
			return "cat"	
		elif node == self.outputLayer[4]:
			return "deer"
		elif node == self.outputLayer[5]:
			return "dog"	
		elif node == self.outputLayer[6]:
			return "frog"
		elif node == self.outputLayer[7]:
			return "horse"
		elif node == self.outputLayer[8]:
			return "ship"
		elif node == self.outputLayer[9]:
			return "truck"		
		
	def getExpected(self,node,label):
		if label[1] == "airplane":
			if node == self.outputLayer[0]:
				return 1
			else:
				return 0
		elif label[1] == "automobile":
			if node == self.outputLayer[1]:
				return 1
			else:
				return 0
		elif label[1] == "bird":
			if node == self.outputLayer[2]:
				return 1
			else:
				return 0
		elif label[1] == "cat":
			if node == self.outputLayer[3]:
				return 1
			else:
				return 0
		elif label[1] == "deer":
			if node == self.outputLayer[4]:
				return 1
			else:
				return 0
		elif label[1] == "dog":
			if node == self.outputLayer[5]:
				return 1
			else:
				return 0
		elif label[1] == "frog":
			if node == self.outputLayer[6]:
				return 1
			else:
				return 0
		elif label[1] == "horse":
			if node == self.outputLayer[7]:
				return 1
			else:
				return 0
		elif label[1] == "ship":
			if node == self.outputLayer[8]:
				return 1
			else:
				return 0
		elif label[1] == "truck":
			if node == self.outputLayer[9]:
				return 1
			else:
				return 0
		
	def trainingEpoch(self):
		file_ = 0
		for label in self.inputActivations:
			output = self.minusPhase(file_)
			correct, outval = self.checkMinusPhaseOutput(label,output)
			if self.plusPhase(label,output) == False:
				self.epochError += 1
			file_ += 1
	
	def minusPhase(self,file_):
		input_counter = 0
		for input_node in self.inputLayer:
			input_node.act = self.inputActivations[file_][0][input_counter]	
			input_counter += 1
		hiddenConnection = 0 
		for hidden in self.hiddenLayer:
			hidden.act = self.hiddenActivationFunction(hidden,hiddenConnection)
			hiddenConnection += 1
		outputConnection = 0
		layerActivity = []
		for output in self.outputLayer:
			output.act = self.outputActivationFunction(output,outputConnection)
			layerActivity.append((output,output.act))
			outputConnection += 1
		return max(layerActivity, key = lambda x: x[1])

	def checkMinusPhaseOutput(self,label,minusPhaseOutput):
		expected = self.getExpected(minusPhaseOutput[0],label)
		phon = self.getLabel(minusPhaseOutput[0])
		correct = False
		if label[1] == phon:
			correct = True
		return correct, phon		

	def plusPhase(self,label,minusPhaseOutput):
		correct, phon = self.checkMinusPhaseOutput(label,minusPhaseOutput)
		outputCounter = 0
		for output in self.outputLayer:
			error = self.getExpected(output,label) - output.act
			hiddenCounter = 0
			for hidden in self.hiddenLayer:
				new_weight = (hidden.act * error) + output.hiddenConnections[hiddenCounter]
				output.hiddenConnections[hiddenCounter] = new_weight
				hidden.outputConnections[outputCounter] = new_weight
				inputCounter = 0
				for input_ in self.inputLayer:
					backprop_counter = 0
					tw = 0
					zw = 0
					for output_backprop in self.outputLayer:
						weight = output_backprop.hiddenConnections[hiddenCounter]
						tw += self.getExpected(output_backprop,label) * weight 
						zw += output_backprop.act * weight
						backprop_counter += 1
					new_weight = ((tw - zw) * (hidden.act * (1 - hidden.act) * input_.act)) + hidden.inputConnections[inputCounter]
					hidden.inputConnections[inputCounter] = new_weight
					input_.hiddenConnections[hiddenCounter] = new_weight
					inputCounter += 1
				hiddenCounter += 1
			outputCounter += 1
		if correct == False:
			return False
		else:
			return True

	def initializeRandomWeights(self):
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				randomWeight = random.uniform(-1,1)
				input_node.hiddenConnections.append(randomWeight)
				hidden_node.inputConnections.append(randomWeight)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				randomWeight = random.uniform(-1,1)
				hidden_node.outputConnections.append(randomWeight)
				output_node.hiddenConnections.append(randomWeight)

	def loadWeights(self,file_):
		file_ = open(file_,"r")
		weights = []
		for weight in file_:
			weights.append(float(weight)) 
		file_.close()
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				input_node.hiddenConnections.append(weights[0])
				hidden_node.inputConnections.append(weights[0])
				weights.pop(0)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				hidden_node.outputConnections.append(weights[0])
				output_node.hiddenConnections.append(weights[0])
				weights.pop(0)

	def train(self):
		self.epochError = 0
		self.trainingEpoch()
		self.epochs += 1
		print str(self.epochs)+":", "#" * int(100 * float(self.epochError)/float(len(self.inputActivations)))
		if self.epochError < 1:
			return
		else:
			return self.train()

	def test(self):
		trial = 0
		for activation, label in self.inputActivations:
			if verbose:
				os.system("mpg321 trial.mp3 --quiet") 
				os.system("mpg321 " + str(trial) + ".mp3 " + "--quiet")
				os.system("mpg321 expected_output.mp3 --quiet")
				os.system("mpg321 japanese_mp3s/" + label + ".mp3 " + "--quiet")
			print "\nTrial: ", trial
			print "Label: ", label[:-2]
			print "Gender: ", label[-1:]
			output = self.minusPhase((activation,label))
			correct, phon = self.checkMinusPhaseOutput((activation,label),output)
			if correct == True:
				print "Correct!", "Output: ", phon
			else:
				print "Test failed.", "Output: ", phon
			if verbose:
				os.system("mpg321 output.mp3 --quiet")
				os.system("mpg321 japanese_mp3s/" + phon + ".mp3 " + "--quiet")
			trial += 1

	def saveWeights(self):
		#weights = open(raw_input("Enter file name: "),"w")
		weights = open("weights/"+self.purpose.replace(" ","_"),"w")
		for node in self.inputLayer:
			for connection in node.hiddenConnections:
				weights.write(str(connection))
				weights.write("\n")
		for node in self.hiddenLayer:
			for connection in node.outputConnections:
				weights.write(str(connection))
				weights.write("\n")
		weights.close()

def main():
	#net = NeuralNetwork()
	net.makeNetwork()
	print "generating input activations...\n"
	net.genInputActivations()
	if raw_input("Would you like to load weights? (y/n) ") == "y":
		print "loading weights...\n"
		net.loadWeights()
	else:
		print "initializing random weights...\n"
		net.initializeRandomWeights()
		try:
			#net.test()
			print "beginning training...\n"
			net.train()
			print "Success!"
			print "Error across 100 epochs: ", net.epochError
			print "Epochs to convergence:", net.epochs
			#print net.stateList
		except:
			print "training failed"
	print "testing network...\n"
	net.test()
	#if raw_input("Would you like to save the network's weights? (y/n) ") == "y":
	#	net.saveWeights()	
	net.saveWeights()
	print "weights saved\n"

if __name__=="__main__":
	net = NeuralNetwork()
	verbose = False
	main()
