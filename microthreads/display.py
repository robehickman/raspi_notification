#!/usr/bin/env python
 
from multiprocessing import Queue
import collections, time

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.PCF8574 as AGPIO

from microthread import *


# Display Pins
lcd_rs        = 0
lcd_en        = 2
lcd_backlight = 3
lcd_d4        = 4
lcd_d5        = 5
lcd_d6        = 6
lcd_d7        = 7


display_queue = Queue()

class display(micro_thread):
    config   = {}
    displays = {}

    def pass_config(self, name, conf):
        self.config[name] = conf

    def setup(self):
        for name, settings in self.config.iteritems():

            gpio = AGPIO.PCF8574(int(settings['i2c_addr'], 0))

            lcd_columns = settings['cols']
            lcd_rows    = settings['rows']

            lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                           lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)

            lcd.set_backlight(True)

            self.displays[name] = {
                'display':   lcd, 
                'exclusive': None,
                'screens'  : {}, #Sub screens to cycle through
                'scr_keys' : [], #Keys of avalible screens
                'scr_index': 0, #Current displayed screen
                'scr_wait' : 0} # Delay until next screen
    def main(self):

        while not display_queue.empty():
            item = display_queue.get()

            method      = item['method']
            s_name      = item['name']

            if (method == 'replace_screen'):
                data = item['data']
                self.displays[item['display']]['screens'][s_name] = data;
            elif (method == 'delete_screen'):
                if(s_name in self.displays[item['display']]['screens']):
                    del self.displays[item['display']]['screens'][s_name]

        for name, scr in self.displays.iteritems():
            exclusive = scr['exclusive']
            if(exclusive != None):
                lcd = scr['display']
                lcd.home()
                lcd.message(exclusive())
            else:
                if(scr['screens'].keys() != scr['scr_keys']):
                    scr['scr_keys'] = scr['screens'].keys()
                    scr['scr_index'] = 0

                if(scr['scr_keys'] == []):
                    lcd = scr['display']
                    lcd.set_backlight(True)
                    lcd.home()

                    default = "                    \n                    "
                    if 'default' in self.config[name]:
                        default = self.config[name]['default'] + default

                    lcd.message(default)
                else:
                    display_scr = scr['scr_keys'][scr['scr_index']]

                    scr['scr_wait'] -= 1

                    if(scr['scr_wait'] <= 1):
                        lcd = scr['display']
                        if(time.localtime().tm_hour > 8 and time.localtime().tm_hour < 23):
                            lcd.set_backlight(False)
                        else:
                            lcd.set_backlight(True)

                        lcd.home()
                        lcd.message(scr['screens'][display_scr])

                        scr['scr_wait'] = 3

                        scr['scr_index'] += 1

                        if(scr['scr_index'] > len(scr['scr_keys']) - 1):
                            scr['scr_index'] = 0

        return 1 # next run in 1 second

    def set_exclusive(self, screen, callback):
	self.displays[screen]['exclusive'] = callback

