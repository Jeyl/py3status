# -*- coding: utf8 -*-

from __future__ import division  # python2 compatibility
from time import time

import math
import re
import subprocess

"""
Module for displaying information about sound.

"""

CACHE_TIMEOUT = 2  # time to update sound status

class Py3status:

	def sound_level(self, i3status_output_json, i3status_config):
		response = {'name': 'sound-level'}

		response['cached_until'] = time() + CACHE_TIMEOUT

		output = subprocess.check_output(["pacmd", "dump"]).decode('utf-8').split("\n")
		output.reverse()
 
		state = 0 
 
		for line in output:
   
			if len(line) == 0:
				continue
   
			parts = line.split()
   
			if parts[0] == "set-default-sink":
				device = parts[1]
   
			elif parts[0] == "set-sink-mute" and parts[1] == device:
				mute = (parts[2] == "yes")
				state |= 1
				if state == 3:
					break
   
			elif parts[0] == "set-sink-volume" and parts[1] == device:
				volume = parts[2]
				state |= 2
				if state == 3:
					break
 
		if state != 3:
			response['color'] = "FF0000"
			response['full_text'] = "♫ ???"
		elif (int(volume, 0) * 100 / 65535) == 0:
			response['full_text'] = "♫ mute"
		else:
			response['color'] = "FFFF00"
			response['full_text'] ="♫ " + "%i%%" % (int(volume, 0) * 100 / 65535)

		return (0, response)
