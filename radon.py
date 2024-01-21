import RPi.GPIO as gpio
from time import sleep
from datetime import datetime
from I2C_LCD_driver import *
from os.path import exists

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN)

MEASUREMENT_PERIOD = 60

l = lcd()

alphabet = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

measurement_id = ""
for c in alphabet:
    if not exists(f"./mes-{c}.csv"):
        measurement_id = c
        break

l.lcd_display_string(f"Ne huzz ki! {MEASUREMENT_PERIOD}s", 1)
l.lcd_display_string(f"...Bq 0 {c}", 2)
try:
    i = 0
    abs = 0
    start = datetime.now()
    ellapsed = 0
    while True:
        if gpio.input(14):
            i += 1
            print(f"beep {i}")
            sleep(0.1)
        delta = (datetime.now() - start).seconds
        if delta >= MEASUREMENT_PERIOD:
            f = open(f"./mes-{c}.csv", "a", encoding="utf-8")
            ellapsed += delta
            print(f"{ellapsed} {i/MEASUREMENT_PERIOD}Bq")
            f.write(f"{ellapsed},{i/MEASUREMENT_PERIOD}\n")
            f.close()
            l.lcd_display_string(f"{i/MEASUREMENT_PERIOD:.1f}Bq {ellapsed/60:.1f}m {c}", 2)
            start = datetime.now()
            i = 0
            abs += 1
except KeyboardInterrupt:
    gpio.cleanup()

