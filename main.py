#!/usr/bin/python

import controller_functions

if __name__ == "__main__":

	handler = controller_functions.cHandler() # Init our controller handler

	while True:
		for i, (serial, move) in enumerate(sorted(handler.moves)):
			if move.poll():
				move.set_leds(0,255,0)
				move.update_leds()
				trig = move.get_trigger()
				print '#'+str(i),' Trigger value:', trig

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