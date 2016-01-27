#!usr/bin/env python

from bs4 import BeautifulSoup
import requests
import click

class PoemCrawler():
	def __init__(self):
		self.urls  = ['www.poetryoutloud.org/poems-and-performance/random-poem']  #['www.poets.org/poetsorg/poem/history', 'www.poets.org/poetsorg/poem/american-sonnet-10' ]
		self.soup  = None
		self.poems = list()

	def getSoup(self,poem):
		url  = poem 
		r    = requests.get("http://" + url)
		data = r.text
		self.soup = BeautifulSoup(data, "html.parser")
		
	def parseSoup(self):
		self.poems.append(self.soup.find_all('div', attrs={'class': 'poem-text'}))

	def findPoems(self):
		for link in self.soup.find_all('a'):
			print(link.get('href'))

	def savePoems(self):
		with open('poems.txt','w') as file_:
			for poem in self.poems:
				for line in poem:
					file_.write(line.text.encode('utf8'))

#print soup.prettify()

crawler = PoemCrawler()
#for url in crawler.urls:
with click.progressbar(range(1000), label="scraping poems...") as bar:
	for x in bar:
		crawler.getSoup('www.poetryoutloud.org/poems-and-performance/random-poem')
		#print crawler.soup.prettify()
		crawler.parseSoup()

print "saving poems..."
crawler.savePoems()
print "poems saved."
