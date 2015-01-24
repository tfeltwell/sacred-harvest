import sys, os

# This loads psmoave in from where it lives
apiPath = '/home/dev/src/psmoveapi/build' # This will depend on who's running it...
if os.path.exists(apiPath):
    sys.path.append(apiPath)
    print 'Set path variable for psMove '
else:
	print 'ERROR: Check path variable set for psmoveapi'
	exit()

import psmove

# Basic functions to Sacred Harvest to utilise PS Move controllers

# Created: 24/01/2015 by Tom Feltwell

class cHandler():
	def __init__(self):
		print 'Initialising controllerFunctions object'
		self.move1 = psmove.PSMove()

	def lowRumble(self):
		self.move1.set_rumble(64)

	def mediumRumble(self):
		self.move1.set_rumble(128)

	def highRumble(self):
		self.move1.set_rumble(255)

	def setLEDs(self):
		self.move1.set_leds(0,255,0)

# RED = (255,0,0)
# BLUE = (0,0,255)
# GREEN = (0,255,0)
