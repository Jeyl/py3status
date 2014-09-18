# -*- coding: utf8 -*-

from __future__ import division  # python2 compatibility
from time import time

import math
import re
import subprocess

"""
Module for displaying information about battery.

Requires:
    - the 'acpi' command line

@author shadowprince
@license Eclipse Public License
"""

CACHE_TIMEOUT = 10  # time to update battery
HIDE_WHEN_FULL = False  # hide any information when battery is fully charged

MODE = "text"  # for primitive-one-char "bar", or "text" for text percentage ouput

BLOCKS = ["_", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]  # block for bar
TEXT_FORMAT = "{}"  # text with "text" mode. percentage with % replaces {}

# None means - get it from i3 config
COLOR_BAD = None
COLOR_CHARGING = "#FCE94F"
COLOR_DEGRADED = None
COLOR_GOOD = None


class Py3status:
    def battery_level(self, i3status_output_json, i3status_config):
        response = {'name': 'battery-level'}

        acpi = subprocess.check_output(["acpi"]).decode('utf-8')

        proc = int(re.search(r"(\d+)%", acpi).group(1))
        zeit = str(re.search(r"(\d\d:\d\d:\d\d)", acpi).group(1))

        charging = bool(re.match(r".*Charging.*", acpi))
        full = bool(re.match(r".*Unknown.*", acpi)) or bool(re.match(r".*Full.*", acpi))
        charching_char = TEXT_FORMAT.format("⚡ " + str(proc) + "% " + zeit)
        color_256 = proc * 511.0 / 100
		

        if MODE == "bar":
            character = BLOCKS[int(math.ceil(proc/100*(len(BLOCKS) - 1)))]
        else:
            character = TEXT_FORMAT.format("↯ " + str(proc) + "% " + zeit )

          
        response['color'] = "#%02x%02x00" %(min(511-color_256,255), min(color_256,255)) # if battery low more red, if full more green

        if full:
            #response['full_text'] = "" if HIDE_WHEN_FULL else BLOCKS[-1]
            response['full_text'] = charching_char 
        elif charging:
            response['full_text'] = charching_char
        else:
            response['full_text'] = character

        response['cached_until'] = time() + CACHE_TIMEOUT

        return (0, response)
