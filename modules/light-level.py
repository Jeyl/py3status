# -*- coding: utf8 -*-

from __future__ import division  # python2 compatibility
from time import time

import math
import re
import subprocess

"""
Module for displaying information about backlight.

"""

CACHE_TIMEOUT = 3  # time to update light status

class Py3status:

	def light_level(self, i3status_output_json, i3status_config):
		response = {'name': 'light-level'}

		with open ("/sys/class/backlight/acpi_video0/max_brightness","r") as f:
			maxLight = int(f.readline()[:-1])

		with open ("/sys/class/backlight/acpi_video0/brightness", "r") as g:
			actLight = int(g.readline()[:-1])

		light = 100.0 * actLight / maxLight

		response['full_text'] = '☀%i' %light
		
		response['cached_until'] = time() + CACHE_TIMEOUT
		
		return (0, response)
