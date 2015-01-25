import sys, os

# This loads psmoave in from where it lives
apiPath = '/home/ben/Desktop/psmove-for-ben/psmoveapi/build' # This will depend on who's running it...
if os.path.exists(apiPath):
    sys.path.append(apiPath)
    print 'Set path variable for psMove '
else:
	print 'ERROR: Check path variable set for psmoveapi'
	exit()

import psmove

# Functionality for Sacred Harvest to utilise PS Move controllers

# Created: 24/01/2015 by Tom Feltwell

class cHandler():
	def __init__(self):
		print '\n\nInitialising cHanlder object'

		# Count number connected and create that many objects
		self.connected = psmove.count_connected()
		print 'Connected controllers:', self.connected
		self.moves = [(m.get_serial(), m) for m in (psmove.PSMove(i) for i in range(self.connected))]
		self.serials = [m.get_serial() for m in (psmove.PSMove(i) for i in range(self.connected))]

	def update(self, calendar):
		for i, (serial, move) in enumerate(sorted(self.moves)):
			if move.poll():
				# Set colour based on season
				if calendar.getSeason() == 0:
					move.set_leds(0,255,0)
				elif calendar.getSeason() == 1:
					move.set_leds(255,255,0)
				elif calendar.getSeason() == 2:
					move.set_leds(255,60,0)
				elif calendar.getSeason() == 3:
					move.set_leds(125,125,125)
				move.update_leds()

				#trig = move.get_trigger()
				#print '#'+str(i),' Trigger value:', trig # DEBUG Can be used to identify controllers
		# self.recountConnected()

	def rumble(self, move, rumbleAmount): 
		# Pass in a move object (from self.moves) and rumble quantity
		if rumbleAmount >= 0 and rumbleAmount <= 255:
			move.set_rumble(rumbleAmount)
	def getTriggers(self):
		#return a list of serials of triggers currently pressed
		out = []
		for i, (serial, move) in enumerate(sorted(self.moves)):
		    if move.get_trigger() > 200: out.append(serial)
		return out
                
	def allTriggers(self): 
		'''
		Returns true if all connected triggers are depressed at once
		'''
		for i, (serial, move) in enumerate(sorted(self.moves)):
		    if move.get_trigger() < 200: return False
		return True
	def kill(self,s):
		for i, (serial, move) in enumerate(sorted(self.moves)):
		    if serial==s:
		    	#kill
		    	move.set_leds(0,0,255)
		    	self.serials.remove(s)
		    	self.moves.remove((serial,move))
		    	

	def recountConnected(self):
		connections = psmove.count_connected()
		if connections != self.connected:
			print 'Someone disconnected'
			self.connected = connections


