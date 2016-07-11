import time
 
from multiprocessing import Process

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
            print 'exclusive'

            display = call_on_thread('Display', 'set_exclusive', [settings['display'], self.get_time])

            p = Process(target=self.display_time, args=(1, display))
            p.start()

    def display_time(self, ook,  display):
        while True:
            lcd = display['display']
            lcd.home()
            format_time = self.get_time()
            print format_time
            lcd.message(format_time)
            time.sleep(1)

    def get_time(self):
        return time.strftime("%a %d %b %Y \n %I %M %S  (%m)", time.localtime())

    def main(self):
        return 1



