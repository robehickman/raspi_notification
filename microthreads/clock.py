#!/usr/bin/env python

import time
 
from microthread import *
import display

class clock(micro_thread):
    config   = {}
    def __init__(self):
        pass

    def pass_config(self, name, conf):
        self.config[name] = conf

    def setup(self):
        for name, settings in self.config.iteritems():
            call_on_thread('Display', 'set_exclusive', [settings['display'], self.get_time])

    def get_time(self):
        return time.strftime("%a %d %b %Y \n %I %M %S  (%m)", time.localtime())

    def main(self):
        #tm = time.strftime("%d %b(%m) %Y \n %I %M %S", time.localtime())
        #display.display_queue.put(tm)

        return 1



