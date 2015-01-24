#!/usr/bin/python

import controller_functions

if __name__ == "__main__":

	handler = controller_functions.cHandler() # Init our controller handler
	handler.setLEDs()
	while True:
		if handler.move1.poll():
			trig = handler.move1.get_trigger()
			print 'Trigger value:', trig
		handler.move1.update_leds()