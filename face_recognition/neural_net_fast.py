import glob
import numpy as np
from PIL import Image

class NeuralNetwork():

        # 3 layer deep network

	# training matrices
	input_training_matrix  = list()
	output_training_matrix = list()

	# testing matrices
	input_testing_matrix   = list()
	output_testing_matrix  = list()

    	def __init__(self):
        	
		self.training_size = 0
		self.loadTrainingData()
		
		#good practice to seed random numbers
		np.random.seed(1)

		# synapses
		if raw_input("Load weights? (y/n): ") == "n":
			print "initializing random weights..."
			# randomly initialize weights with mean 0
			self.syn0 = 2 * np.random.random((4096, self.training_size)) - 1 # weights connecting input and hidden layers
			self.syn1 = 2 * np.random.random((self.training_size, 1)) - 1    # weights connecting hidden and output layers
		else:
			print "loading weights..."	
			self.syn0 = np.load('trained_weights/syn0_weights')
			self.syn1 = np.load('trained_weights/syn1_weights')

	def saveWeights(self):
		with open("syn0_weights", "w") as weights1:
			np.save(weights1, self.syn0) 
		with open("syn1_weights", "w") as weights2:
			np.save(weights2, self.syn1) 

    	def loadTrainingData(self):
        	for file_ in glob.glob("training_images/*"):
			plant = Image.open(file_)
			pix = list(plant.getdata())
			activation = []
			for pixel in pix:
				print pixel
				hexval = hex(pixel[0]) + hex(pixel[1])[:1] + hex(pixel[2])[:1]
				print pixel, hexval
				activation.append((int(hexval,16))/100000.0)
            		self.input_training_matrix.append(activation)
			if "f" in file_:
            			self.output_training_matrix.append([0]) # female
            		else:
                		self.output_training_matrix.append([1]) # male
		self.training_size = len(self.input_training_matrix)
            	self.input_training_matrix = np.array(self.input_training_matrix)
        	self.output_training_matrix = np.array(self.output_training_matrix)

	def sigmoid(self,x,deriv=False):
		if(deriv==True):
	    		return x*(1-x)
		return 1/(1+np.exp(-x))

	def train(self):
		for epoch in xrange(10000000):

			# FEEDFORWARD ACTIVATION

			input_layer  = self.input_training_matrix
			# multiply input_layer and syn0 matrices, 
			# passes product into sigmoid activation function
			# (20 x 1024) dot (1024 x 20) = (20 x 20)?
			hidden_layer  = self.sigmoid(np.dot(input_layer,self.syn0))
			# (20 x 20) dot (1 x 20) = ????????
			output_layer = self.sigmoid(np.dot(hidden_layer,self.syn1))
			# calculating error
			output_layer_error = self.output_training_matrix - output_layer
			
			if epoch % 100000 == 0:
				print "Epoch:", epoch, "Error:", str(np.mean(np.abs(output_layer_error)))	
			
			# BACKPROPAGATION

			# in what direction is the target value?
    			output_layer_delta = output_layer_error*self.sigmoid(output_layer,deriv=True)
    			hidden_layer_error = output_layer_delta.dot(self.syn1.T)
    			hidden_layer_delta = hidden_layer_error * self.sigmoid(hidden_layer,deriv=True)
			# actual backprop
   			self.syn1 += hidden_layer.T.dot(output_layer_delta)
   			self.syn0 += input_layer.T.dot(hidden_layer_delta)

	def test(self):
		input_layer = self.input_training_matrix
		hidden_layer  = self.sigmoid(np.dot(input_layer,self.syn0))
		# (20 x 20) dot (1 x 20) = ????????
		output_layer = self.sigmoid(np.dot(hidden_layer,self.syn1))
		# calculating error
		output_layer_error = self.output_training_matrix - output_layer
		print output_layer_error

net = NeuralNetwork()
print "input training:", net.input_training_matrix.shape
print "output training:", net.output_training_matrix.shape
print "syn0", net.syn0.shape
print "syn1", net.syn1.shape

print "testing..."
net.test()
'''
try:
	print "training..."
	net.train()
except KeyboardInterrupt:
	net.saveWeights()
	print "weights saved"
net.saveWeights()
print "weights saved"
'''
