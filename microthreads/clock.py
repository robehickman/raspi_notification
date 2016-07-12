import time
 
from multiprocessing import Process

from microthread import *
import display

class clock(micro_thread):
    config   = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Store config value
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pass_config(self, name, conf):
        self.config[name] = conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Register exclusive screen handler
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def setup(self):
        for name, settings in self.config.iteritems():
            call_on_thread('Display', 'set_exclusive', [settings['display'], self.get_time])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Format date and time for lcd display
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def get_time(self):
        return time.strftime("%a %d %b %Y \n %I %M %S  (%m)", time.localtime())

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Null process starter
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def start_process(self):
        pass






