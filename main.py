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
	HEIGHT = 800
	DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
	pygame.display.set_caption("Sacred Harvest")
	bgColour = 255,255,255
	fontColour = 0,0,0
	clock = pygame.time.Clock()

	# Load images
	rituals = pygame.image.load("rituals.png")
	seasonWheel = pygame.image.load("seasonWheel.png")
	ritualsrect = rituals.get_rect()
	
	# Season wheel stuff
	seasonWheelRect = seasonWheel.get_rect()
	seasonWheelRect.center = (486,580)
	wheelAngle = 0

	DISPLAYSURF.fill(bgColour)
	DISPLAYSURF.blit(rituals,ritualsrect)
	blittedRect = DISPLAYSURF.blit(seasonWheel,seasonWheelRect)
	oldCentre = blittedRect.center
	pygame.draw.rect(DISPLAYSURF,bgColour,(0,600,1023,200))

	# Font
	# textFont = pygame.font.SysFont(None,30)
	# title = textFont.render("Harvest", True, (45, 46, 40))

	handler = controller_functions.cHandler() # Init our controller handler
	calendar = calendar.Calendar()
	frame = 0
	print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()

	while True:
		#pygame events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		# Controller update
		handler.update(calendar)

		# TODO: Reimplement frame var to use pygame clock
		if frame == 1000:
			calendar.changeSeason()
			frame = 0
			print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()
			# Redraw background once per season to save processor
			DISPLAYSURF.fill(bgColour)
			DISPLAYSURF.blit(rituals,ritualsrect)
		else:
			frame += 1

		# Pygame redrawing stuff and rotating wheel
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
		pygame.draw.rect(DISPLAYSURF,bgColour,(0,570,1023,200))

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