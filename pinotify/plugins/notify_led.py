import os
import time
from multiprocessing import Process

from pinotify.module_system import *

# Handle notification LEDs

class notify_led(module):
    state = 0
    config = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Store configuration item
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def pass_config(self, name, conf):
        self.config[name] = conf

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
# Start led flasher process
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def start_process(self):
        p = Process(target=self.flash, args=())
        p.start()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
# Flash the led
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def flash(self):
        while 1:
            if(self.state == 0):
                self.state = 1
                os.system("gpio -g write 17 1")
            else:
                os.system("gpio -g write 17 0")
                self.state = 0

            time.sleep(0.5)



