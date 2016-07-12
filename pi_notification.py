#!/usr/bin/env python

import sys

sys.path = [ './lib' ] + sys.path
sys.path = [ './modules' ] + sys.path
 

from module import *
from notify_led  import *
from display     import *
from email_check import *
from clock       import *


config = read_config('/home/pi/.notification_conf.ini');


# Register modules
modules = {
#   'Notify_LED':  notify_led(),
    'Email_check': email_check(),
    'Display':     display.display(),
    'Clock':       clock()
}

set_modules(modules)
pass_configuration(config)
start_workers()


