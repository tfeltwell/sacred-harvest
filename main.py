#!/usr/bin/python

import controller_functions
import calendar

# Pygame shit
import pygame, sys
from pygame.locals import *

if __name__ == "__main__":
	isgameover = False
	# Pygame shit
	waiting = True
	sacrifice = False
	
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
	transition = pygame.image.load("transition.png")
	seasonWheel = pygame.image.load("seasonWheel.png")
	sky = pygame.image.load("sky.png")
	earth = pygame.image.load("earth.png")
	flame = pygame.image.load("flame.png")
	sea = pygame.image.load("sea.png")
	goodharvest = pygame.image.load("goodharvest.png")
	badharvest = pygame.image.load("badharvest.png")
	
	goodsamhain = pygame.image.load("goodsamhain.png")
	badsamhain = pygame.image.load("badsamhain.png")
	gameover = pygame.image.load("gameover.png")
	ritualsrect = rituals.get_rect()
	
	# Season wheel stuff
	seasonWheelRect = seasonWheel.get_rect()
	seasonWheelRect.center = (486,580)
	wheelAngle = 0
	

	DISPLAYSURF.fill(bgColour)
	DISPLAYSURF.blit(sea,sea.get_rect())
	blittedRect = DISPLAYSURF.blit(seasonWheel,seasonWheelRect)
	oldCentre = blittedRect.center
	pygame.draw.rect(DISPLAYSURF,bgColour,(0,600,1023,200))

	# Font
	# textFont = pygame.font.SysFont(None,30)
	# title = textFont.render("Harvest", True, (45, 46, 40))

	handler = controller_functions.cHandler() # Init our controller handler
	
	sacrifice_not_pressed = handler.serials[:]
	
	calendar = calendar.Calendar()
	handler.setLeds(calendar)
	frame = 0
	print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()

	while True:
		#pygame events
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		# Controller update
		handler.update()

		# TODO: Reimplement frame var to use pygame clock
		
		if frame == 500 and not waiting and not isgameover:#trigger actual change in season
			
			waiting = True
			frame = 0
			DISPLAYSURF.fill(bgColour)
			if(calendar.getSeason() == 3): #winter
				calendar.changeYear()
				if calendar.getYear() == 0:
					DISPLAYSURF.blit(earth,earth.get_rect())#start of season,
				if calendar.getYear() == 1:
					DISPLAYSURF.blit(flame,flame.get_rect())#start of season,
				if calendar.getYear() == 2:
					DISPLAYSURF.blit(sea,sea.get_rect())#start of season,
				if calendar.getYear() == 3:
					DISPLAYSURF.blit(sky,sky.get_rect())#start of season,
			elif(calendar.getSeason()==1):#summer/harvest
				if(calendar.wheatHarvest==0):
					DISPLAYSURF.blit(badharvest,badharvest.get_rect())
				else:
					DISPLAYSURF.blit(goodharvest,goodharvest.get_rect())
			
			elif(calendar.getSeason()==2):
				if(calendar.wheatHarvest==0):
					
					sacrifice_not_pressed = handler.serials[:]
					sacrifice = True
					if (len(handler.serials)>1):
						DISPLAYSURF.blit(badsamhain,badsamhain.get_rect())
					else:
						DISPLAYSURF.blit(gameover,gameover.get_rect())
						isgameover = True
						handler.kill(handler.serials[0])
					
				else:
					DISPLAYSURF.blit(goodsamhain,goodsamhain.get_rect())		
				
			else:		
			
				DISPLAYSURF.blit(rituals,ritualsrect)#start of season,
			
		elif not waiting:
			frame += 1
			
			
		if waiting and sacrifice and not isgameover:
			print (sacrifice_not_pressed)
			if(len(sacrifice_not_pressed)==0):
				sacrifice_not_pressed.append(handler.serials[0])#lol
			if(len(sacrifice_not_pressed)==1):
				#kill
				handler.kill(sacrifice_not_pressed[0])
				sacrifice = False
				waiting = False
				# Redraw background once per season to save processor
				
				calendar.changeSeason()
				handler.setLeds(calendar)
				print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()
				DISPLAYSURF.blit(transition,transition.get_rect())
			
				
			for s in handler.getTriggers():
				
				if s in sacrifice_not_pressed:
					sacrifice_not_pressed.remove(s)
				
			
			
		if waiting and handler.allTriggers() and not sacrifice and not isgameover:#all triggers makes the season move on
			waiting = False
			# Redraw background once per season to save processor
			
			calendar.changeSeason()
			handler.setLeds(calendar)
			print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()
			DISPLAYSURF.blit(transition,transition.get_rect())

		# Pygame redrawing stuff and rotating wheel
		if not waiting and not isgameover:
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