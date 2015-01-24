#!/usr/bin/python

import controller_functions
import calendar

if __name__ == "__main__":

	handler = controller_functions.cHandler() # Init our controller handler
	calendar = calendar.Calendar()
	frame = 0
	print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()

	while True:
		# print 'Current season',calendar.getSeason()
		handler.update(calendar)

		# Reimplement this when we decide on graphics engine 
		if frame == 1000000:
			calendar.changeSeason()
			frame = 0
			print 'Season',calendar.getSeason(),'Year Type',calendar.getYear()
		else:
			frame += 1


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