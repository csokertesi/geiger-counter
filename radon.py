import RPi.GPIO as gpio
from time import sleep
from datetime import datetime
from I2C_LCD_driver import *

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN)

MEASUREMENT_PERIOD = 10

l = lcd()

l.lcd_display_string(f"Period: {MEASUREMENT_PERIOD}s", 1)
l.lcd_display_string("...Bq", 2)
try:
	i = 0
	abs = 0
	start = datetime.now()
	while True:
		if gpio.input(14):
			i += 1
			print(f"beep {i}")
			sleep(0.1)
		if (datetime.now() - start).seconds >= MEASUREMENT_PERIOD:
			print(f"{i/MEASUREMENT_PERIOD}Bq")
			l.lcd_display_string(f"{i/MEASUREMENT_PERIOD:.1f}Bq {abs}", 2)
			start = datetime.now()
			i = 0
			abs += 1
except KeyboardInterrupt:
	gpio.cleanup()

