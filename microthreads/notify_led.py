#!/usr/bin/env python
import os
import time
from multiprocessing import Process




 
from microthread import *

# Handle notification LEDs

class notify_led(micro_thread):
    state = 0
    def __init__(self):
        p = Process(target=self.flash, args=())
        p.start()

    def main(self):
        return 600


    def flash(self):
        while 1:
            if(self.state == 0):
                self.state = 1
                os.system("gpio -g write 17 1")
            else:
                os.system("gpio -g write 17 0")
                self.state = 0

            time.sleep(0.5)



