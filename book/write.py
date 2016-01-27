#!usr/bin/env python

from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
from nltk.tokenize import word_tokenize

class Writer():
	def __init__(self):
		self.db = None

	def chunkSentence(self,sentence):	
		return pos_tag(word_tokenize(sentence))

def main():
	writer = Writer()
	with open('plath_small.txt', 'r') as file_:
		sentences = file_.readlines()
		for sentence in sentences:
			print writer.chunkSentence(sentence)	

if __name__=='__main__': main()
