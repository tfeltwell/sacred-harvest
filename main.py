#!/usr/bin/python

import controller_functions
import calendar

# Pygame shit
import pygame, sys
from pygame.locals import *

if __name__ == "__main__":
	
	# Game flags
	isgameover = False
	waiting = True # Waiting for all players to press triggers (on season screen)
	waitingTime = 0 # Num. frames waited in waiting condition
	sacrifice = False # Triggers the sacrifice minigame
	ritualcount = 0
	isrituals = False
	blocked = False # Someone holding down trigger before sacrifice
	movement = False # Movement detected on any controllers (stops no movement condition)
	movementCount = 0 # Count how many times movement is detected
	
	pygame.init()
	pygame.mixer.music.load("walsall.wav")
	pygame.mixer.music.play(-1)
	flute = pygame.mixer.Sound("flute.wav")
	WIDTH = 1023
	HEIGHT = 800
	DISPLAYSURF = pygame.Surface((WIDTH,HEIGHT))
	# DISPLAYSURF2 = pygame.display.set_mode((1023,572),pygame.FULLSCREEN)
	DISPLAYSURF2 = pygame.display.set_mode((1023,572))
	pygame.display.set_caption("Sacred Harvest")
	bgColour = 255,255,255
	fontColour = 0,0,0
	clock = pygame.time.Clock()

	# Load images
	rituals = pygame.image.load("rituals.png")
	transition = pygame.image.load("transition.png")
	seasonWheel = pygame.image.load("seasonWheel2.png")
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
	wheelAngle = 90
	
	# Font and misc
	textFont = pygame.font.SysFont(None,30)
	largeFont = pygame.font.Font("assets/celtic_gaelige.ttf", 45)
	black = (46,46,46)
	bloodRed = (138,7,7)
	triggerPress = largeFont.render("All press trigger to continue", True, bloodRed)
	triggerFinish = largeFont.render("All press trigger when finished", True, bloodRed)
	triggerRelease = largeFont.render("All release trigger to continue", True, bloodRed)
	ritualPrompt = largeFont.render("Perform three rituals five times", True, black)
	movementPrompt = largeFont.render("The Gods demand movement", True, bloodRed)

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
	# print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()

	def printFlags():
		print "GameOver:",isgameover,"waiting:",waiting,"sacrifice:",sacrifice,"isrituals:",isrituals,"blocked:",blocked,"movement:",movement

	def checkProgression():
		if waiting and handler.allTriggers() and waitingTime > 300:
			return True
		else:
			return False

	while True:
		#pygame events
		for event in pygame.event.get():
			if event.type == QUIT or (event.type ==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
				printFlags()

		# Controller update
		handler.update()

		# TODO: Reimplement frame var to use pygame clock
		# Pygame redrawing stuff and rotating wheel
		if not waiting and not isgameover:
			if frame % 13 == 0:
				# Logic to get wheel rotating
				if wheelAngle-1 == -360:
					wheelAngle = 0
				else:
					wheelAngle -= 1
					
		## Trigger once per season here ##

		if wheelAngle % 90 == 0 and not waiting and not isgameover and not isrituals:# == 500 and not waiting and not isgameover:#trigger actual change in season
			waiting = True
			frame = 0
			DISPLAYSURF.fill(bgColour)
			# Winter
			if(calendar.getSeason() == 3): 
				calendar.changeYear()
				if calendar.getYear() == 0:
					DISPLAYSURF.blit(earth,earth.get_rect())#start of season,
				if calendar.getYear() == 1:
					DISPLAYSURF.blit(flame,flame.get_rect())#start of season,
				if calendar.getYear() == 2:
					DISPLAYSURF.blit(sea,sea.get_rect())#start of season,
				if calendar.getYear() == 3:
					DISPLAYSURF.blit(sky,sky.get_rect())#start of season,

			# Summer/harvest
			elif(calendar.getSeason()==1):
				if(calendar.wheatHarvest==0):
					DISPLAYSURF.blit(badharvest,badharvest.get_rect())
				else:
					DISPLAYSURF.blit(goodharvest,goodharvest.get_rect())
			
			# Autumn
			elif(calendar.getSeason()==2):
				if(calendar.wheatHarvest==0):

					# Block the sacrifice condition if triggers are held during transition
					if len(handler.getTriggers()) > 0:
						blocked	= True 

					# Kill player if only 1 remains
					if (len(handler.serials)==1):
						DISPLAYSURF.blit(gameover,gameover.get_rect())
						isgameover = True	
						handler.kill(handler.serials[0])
					else:
						sacrifice = True			
					
				else:
					DISPLAYSURF.blit(goodsamhain,goodsamhain.get_rect())		
			
			# Spring	
			else:		
				isrituals = True
				DISPLAYSURF.blit(rituals,ritualsrect)#start of season
				DISPLAYSURF.blit(ritualPrompt,(200,50))

		## Checks every frame from here down ##
		
		# Spinning the wheel	
		elif not waiting:
			frame += 1

		if isrituals:
			# Vibrate if moving. Check 
			if movementCount >= 20: # More than 20 vibrates means there's been some vibration somewhere
				movement = True
			if handler.checkVibrate(): # Returns whether detected movement
				movementCount += 1
			
		# Sacrifice condition	
		if waiting and sacrifice and not isgameover:
			if len(handler.getTriggers()) > 0 and blocked:
				DISPLAYSURF.blit(triggerRelease, ((WIDTH/2)-300,(HEIGHT/2)))
			else:
				blocked = False
				# print (sacrifice_not_pressed) #Print list of controllers
				DISPLAYSURF.blit(badsamhain,badsamhain.get_rect())
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
					calendar.printSeason()
					DISPLAYSURF.blit(transition,transition.get_rect())
				
				# Basically disconnect the controller that was last
				for s in handler.getTriggers():
					if s in sacrifice_not_pressed:
						sacrifice_not_pressed.remove(s)	
			
		# Check if ready to move to next screen
		if checkProgression() and not sacrifice and not isgameover:
			if isrituals and not movement:
				DISPLAYSURF.blit(movementPrompt,((200),100)) # If noone has moved you can't progress from rituals
			else:
				waiting = False
				waitingTime = 0
				if(isrituals):
					handler.stopRumbling()	
					isrituals = False
				# Redraw background once per season to save processor
				flute.play()
				calendar.changeSeason()
				handler.setLeds(calendar)
				calendar.printSeason()
				DISPLAYSURF.blit(transition,transition.get_rect())

		# Waiting on screen (between wheel rotation)
		if waiting:
			waitingTime += 1
		if waitingTime > 1000 and not blocked and not isgameover:
			if calendar.getSeason() == 0: # Do special stuff if in rituals
				if movement:
					DISPLAYSURF.blit(rituals,ritualsrect)#start of season
					DISPLAYSURF.blit(ritualPrompt,(200,50))
					DISPLAYSURF.blit(triggerFinish,(200,100))
			else:
				DISPLAYSURF.blit(triggerPress,((WIDTH/2)-330,(HEIGHT/2)-30)) # Prompt players to press trigger
		
		rotWheel = pygame.transform.rotate(seasonWheel,wheelAngle)
		rotWheelRect = rotWheel.get_rect()
		rotWheelRect.center = oldCentre
		blittedRect = DISPLAYSURF.blit(rotWheel,rotWheelRect)
		oldCentre = blittedRect.center
		pygame.draw.rect(DISPLAYSURF,bgColour,(0,570,1023,200))
		DISPLAYSURF2.blit(DISPLAYSURF,DISPLAYSURF.get_rect())
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