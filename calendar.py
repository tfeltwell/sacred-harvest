#!/usr/bin/python

# Calendar and other game system functions
# Tracks season and year types, as well as how much wheat has been harvested

import random

class Calendar:
	def __init__(self):
		self.yearTypes = ['Earth','Fire','Sea','Sky']
		self.seasonTypes = ['Spring','Summer','Autumn','Winter']
		self.currentYear = 0
		self.currentSeason = 3
		self.wheatHarvest = 0

	def getYear(self):
		return self.currentYear

	def getSeason(self):
		return self.currentSeason

	def printSeason(self):
		print 'Year of',self.yearTypes[self.getYear()]+',',self.seasonTypes[self.getSeason()]

	def changeSeason(self):
		if self.currentSeason+1 == 1:
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
		self.wheatHarvest = random.randint(0,1) # Need to weight this to make the extremes are less common?
		print 'This harvest has yielded',self.wheatHarvest,'bushels of wheat'

		# TODO: Maybe move this, as we need to know how many players are still remaining
