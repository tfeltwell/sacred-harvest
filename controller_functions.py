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
		print '\n\nInitialising cHanlder object'

		# Count number connected and create that many objects
		self.connected = psmove.count_connected()
		print 'Connected controllers:', self.connected
		self.moves = [(m.get_serial(), m) for m in (psmove.PSMove(i) for i in range(self.connected))]

		self.serials = []

	# Below here still needs fixing

	def lowRumble(self):
		self.moves.set_rumble(64)

	def mediumRumble(self):
		self.moves.set_rumble(128)

	def highRumble(self):
		self.moves.set_rumble(255)

	def setLEDs(self,colour):
		# Pass in colour as string
		if colour == 'r':
			cVal = (255,0,0)
		elif colour == 'g':
			cVal = (0,255,0)
		elif colour == 'b':
			cVal = (0,0,255)
		elif colour == 'y':
			cVal = (255,255,0)

		self.moves.set_leds(cVal[0],cVal[1],cVal[2])
