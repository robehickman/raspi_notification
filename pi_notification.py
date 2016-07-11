#!/usr/bin/env python

import sys
import ConfigParser

sys.path = [ './lib' ] + sys.path
sys.path = [ './microthreads' ] + sys.path
 

from microthread import *
from notify_led  import *
from display     import *
from email_check import *
from clock       import *


def read_config(file):
	conf_file = ConfigParser.ConfigParser()
	conf_file.read(file)

	config = {}

	for section in conf_file.sections():
		sect = {}

		options = conf_file.options(section)

		for option in options:
			sect[option] = conf_file.get(section, option)
		config[section] = sect
	return config

config = read_config('/home/pi/.notification_conf.ini');



# Register micro threads
microthreads = {
#	'Notify_LED':  notify_led(),
	'Email_check': email_check(),
	'Display':     display.display(),
	'Clock':       clock()
}

set_microthreads(microthreads)

for section in config:
	module = config[section]['module']
	microthreads[module].pass_config(section, config[section])


active_microthreads = []

delay = 0
for t in microthreads.values():
	t.setup()
	active_microthreads.append((delay, t))
	delay += 0.5

#microthread_scheduler(active_microthreads)






