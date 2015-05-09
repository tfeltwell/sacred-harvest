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
		self.r =0
		self.g=0
		self.b=0
		self.target_leds = [0,0,0]
		self.lastframes = []
		for i, (serial, move) in enumerate(sorted(self.moves)):
			self.lastframes.append(move.get_accelerometer_frame(psmove.Frame_SecondHalf))
		
							
	def setLeds(self,calendar):
		
		if calendar.getSeason() == 0:
			self.target_leds = [0,255,0]
		elif calendar.getSeason() == 1:
			self.target_leds = [255,255,0]
		elif calendar.getSeason() == 2:
			self.target_leds = [255,60,0]
		elif calendar.getSeason() == 3:
			self.target_leds = [125,125,125]
	def stopRumbling(self):
		for i, (serial, move) in enumerate(sorted(self.moves)):
			move.set_rumble(0)
			
	# TODO: Implement a better calculation here, maybe vector calculation.
	def checkVibrate(self):
		vibrateFlag = False
		for i, (serial, move) in enumerate(sorted(self.moves)):
			f = move.get_accelerometer_frame(psmove.Frame_SecondHalf)
			t = f[0]+f[1]+f[2]
			last = self.lastframes[i][0]+self.lastframes[i][1]+self.lastframes[i][2]
			if (t - last)> 0.3 or (last-t)> 0.3:	
				move.set_rumble(150)
				vibrateFlag = True # If it vibrates it's classed as movement
			else:
				move.set_rumble(0)
				
		self.lastframes=[]
		for i, (serial, move) in enumerate(sorted(self.moves)):
			self.lastframes.append(move.get_accelerometer_frame(psmove.Frame_SecondHalf))
		return vibrateFlag
		
	def update(self):
		# Set colour based on season
		
		if self.r<self.target_leds[0]:
			self.r +=1
		if self.r>self.target_leds[0]:
			self.r -=1
		if self.g<self.target_leds[1]:
			self.g +=1
		if self.g>self.target_leds[1]:
			self.g -=1
		if self.b<self.target_leds[2]:
			self.b +=1
		if self.b>self.target_leds[2]:
			self.b -=1
		
		for i, (serial, move) in enumerate(sorted(self.moves)):
			if move.poll():
				
				move.set_leds(self.r,self.g,self.b)
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


