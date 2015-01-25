#!/usr/bin/python

import controller_functions
import calendar

# Pygame shit
import pygame, sys
from pygame.locals import *

if __name__ == "__main__":

	# Pygame shit
	pygame.init()
	WIDTH = 1023
	HEIGHT = 600
	DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption("Sacred Harvest")
	backgroundColor = 212,203,188
	fontBlk = 0,0,0
	DISPLAYSURF.fill(backgroundColor)
	rituals = pygame.image.load("rituals.png")
	ritualsrect = rituals.get_rect()
	DISPLAYSURF.blit(rituals,ritualsrect)
	wheelAngle = 0
	seasonWheel = pygame.image.load("seasonWheel.png")
	seasonWheelRect = seasonWheel.get_rect()
	seasonWheelRect.center = (486,570)
	# wheelCoords = (366,481)
	
	blittedRect = DISPLAYSURF.blit(seasonWheel,seasonWheelRect)
	oldCentre = blittedRect.center
	pygame.display.update()
	clock = pygame.time.Clock()

	handler = controller_functions.cHandler() # Init our controller handler
	calendar = calendar.Calendar()
	frame = 0
	print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()

	while True:
		#pygame
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		# Controller update
		handler.update(calendar)

		# Reimplement this when we decide on graphics engine 
		if frame == 1000:
			calendar.changeSeason()
			frame = 0
			print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()
			# Redraw background once per season to save processor
			DISPLAYSURF.fill(backgroundColor)
			DISPLAYSURF.blit(rituals,ritualsrect)
		else:
			frame += 1

		# Pygame redrawing stuff and rotating wheel
		# DISPLAYSURF.blit(rituals,ritualsrect) # Redraw background
		if frame % 13 == 0:
			# Logic to get wheel rotating
			if wheelAngle-1 == -360:
				wheelAngle = 0
			else:
				wheelAngle -= 1
		rotWheel = pygame.transform.rotate(seasonWheel,wheelAngle)
		rotWheelRect = rotWheel.get_rect()
		rotWheelRect.center = oldCentre

		blittedRect = DISPLAYSURF.blit(rotWheel,rotWheelRect)
		oldCentre = blittedRect.center

		pygame.display.update()
		clock.tick(10000) # Controls the frame rate


	## DEBUG ##
	# Test the connections, press trigger and each one should light up

	# while len(handler.serials) < len(handler.moves):
	# 	    for i, (serial, move) in enumerate(sorted(handler.moves)):
	# 	        if serial in handler.serials:
	# 	            continue

	# 	        move.poll()
	# 	        if move.get_buttons():
	# 	            move.set_leds(0, 255, 0)
	# 	            move.update_leds()
	# 	            handler.serials.append(serial)
	# 	            print i