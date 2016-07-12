import time
 
from multiprocessing import Process

from module import *
import display

class clock(module):
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Register exclusive screen handler
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def setup(self):
        for name, settings in self.config.iteritems():
            call_on_module('Display', 'set_exclusive', [settings['display'], self.get_time])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Format date and time for lcd display
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def get_time(self):
        return time.strftime("%a %d %b %Y \n %I %M %S  (%m)", time.localtime())





