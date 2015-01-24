#!/usr/bin/python

import random

class Calendar:
	def __init__(self):
		self.yearTypes = {'Earth':0,'Fire':1,'Sea':2,'Sky':3}
		self.seasonTypes = {'Spring':0,'Summer':1,'Autumn':2,'Winter':3}
		self.currentYear = 0
		self.currentSeason = 0
		self.wheatHarvest = 0

	def getYear(self):
		return self.currentYear

	def getSeason(self):
		return self.currentSeason

	def changeSeason(self):
		if self.currentSeason+1 == 2:
			self.harvest()
			self.currentSeason += 1
		elif self.currentSeason == 3:
			self.changeYear()
			self.currentSeason = 0
		else:
			self.currentSeason += 1

	def changeYear(self):
		self.currentYear = random.randint(0,3)

	def harvest(self):
		self.wheatHarvest = random.randint(0,7) # Need to weight this to make the extremes are less common?
		print 'This harvest has yielded',self.wheatHarvest,'bushels of wheat'

		# TODO: Maybe move this, as we need to know how many players are still remaining
