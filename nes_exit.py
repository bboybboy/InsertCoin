import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pin_esc = 4

GPIO.setup(pin_esc, GPIO.IN, pull_up_down=GPIO.PUD_UP)

key_esc = False

while True:
	if (not key_esc) and (not GPIO.input(pin_esc)): 
		os.system("killall -9 retroarch")
		key_esc = True
	if key_esc and GPIO.input(pin_esc):
		key_esc = False

	time.sleep(.05)