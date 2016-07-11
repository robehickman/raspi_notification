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
            display = call_on_thread('Display', 'set_exclusive', [settings['display'], self.get_time])

            p = Process(target=self.display_time, args=(1, display))
            p.start()

    def display_time(self, display):
        while True:
            display.home()
            display.message(self.get_time())
            time.sleep(1)

    def get_time(self):
        return time.strftime("%a %d %b %Y \n %I %M %S  (%m)", time.localtime())

    def main(self):
        return 1



