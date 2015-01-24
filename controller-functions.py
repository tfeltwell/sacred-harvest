import sys, os

# This loads psmoave in from where it lives
apiPath = '/home/dev/src/psmoveapi/build' # This will depend on who's running it...
if os.path.exists(apiPath):
    sys.path.append(apiPath)
    print 'Set path variable for psMove '

import psmove

# Basic functions to Sacred Harvest to utilise PS Move controllers

# Created: 24/01/2015 by Tom Feltwell

move = psmove.PSMove()

move.set_leds(0,255,0)
# move.set_rumble(255)

while True:
	if move.poll():
		trig = move.get_trigger()
		print 'Trigger value:', trig
	move.update_leds()