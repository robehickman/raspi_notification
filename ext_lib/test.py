#!/usr/bin/python
import math
import time

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.PCF8574 as AGPIO


# Initialize PCF
gpio = AGPIO.PCF8574(0x20)

# Instantiate LCD Display
lcd_rs        = 0
lcd_en        = 2
lcd_backlight = 3
lcd_d4        = 4
lcd_d5        = 5
lcd_d6        = 6
lcd_d7        = 7

lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
			   lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)

lcd.set_backlight(True)

i = 0

while 1:

	lcd.clear()

	# Print a two line message
	lcd.message("Count: %s" % i)

	i += 1

	time.sleep(1)





















import time
from smbus import SMBus

from smbus import SMBus
# RPi.GPIO compatible interface for PCF8574
# Only supports output
class Pcf8574Gpio(object):
    BCM = 0
    OUT = 0
    def __init__(self, busnum, address):
        self.bus = SMBus(busnum)
        self.address = address
        # Set all outputs off
        self.bus.write_byte(self.address, 0x00)
        # Store P-port state
        self.byte = 0x00
    
    def _changebit(self, bit, new_value):
        if new_value == 0:
            self.byte &= ~(1 << bit)
        elif new_value == 1:
            self.byte |= (1 << bit)

    def output(self, pin, value):
        self._changebit(pin, value)
        self.bus.write_byte(self.address, self.byte)

    def setmode(self, mode):
        pass
    
    def setup(self, pin, mode):
        pass

    def cleanup(self):
        # Set all outputs off
        self.bus.write_byte(self.address, 0x00)



import Adafruit_CharLCD as LCD


gpio = Pcf8574Gpio(1, 0x27)

# Instantiate LCD Display
lcd_rs        = 0
lcd_en        = 2
lcd_backlight = 3
lcd_d4        = 4
lcd_d5        = 5
lcd_d6        = 6
lcd_d7        = 7

lcd_columns = 16
lcd_rows    = 2


#out = 0
#while 1:
#	out = not out
#	gpio.output(7, out)
#	time.sleep(1)

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 
                           lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)


#
#lcd = Adafruit_CharLCD(lcd_rs, lcd_en, pins_db, GPIO=gpio)
#lcd.clear()

lcd.message('  Raspberry Pi\n  I2C LCD 0x20')


while 1:
	pass


val = False
while 1:
	if val == False:
		val = True
	elif val == True:
		val = False

	ggg.output(0, val)
	print val
	time.sleep(1)

#for byte in range(0, 256):
#	bus.write_byte(0x27, ~byte)
#	time.sleep(1)









import math
import time

import Adafruit_CharLCD as LCD
import Adafruit_GPIO.PCF8574 as AGPIO

lcd_rs        = 0
lcd_en        = 2
lcd_backlight = 3
lcd_d4        = 4
lcd_d5        = 5
lcd_d6        = 6
lcd_d7        = 7

lcd_columns = 16
lcd_rows    = 2

# Initialize PCF
gpio = AGPIO.PCF8574(0x27)


out = 0
while 1:
	out = not out
	gpio.output(7, out)
	time.sleep(1)


#lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, 

#                           lcd_columns, lcd_rows, lcd_backlight, gpio=gpio)


#lcd.set_backlight(False)

# Print a two line message
#lcd.message('Hello\nworld!')

time.sleep(5)
