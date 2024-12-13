import RPi.GPIO as GPIO
import os
import sys
import time

GPIO.setmode(GPIO.BCM) 

pulseStart = 0.0
REBOOTPULSEMINIMUM = 0.2
REBOOTPULSEMAXIMUM = 1.0
SHUTDOWN = 7
BOOT = 8
RESET_RETROARCH = 10

key_esc = False


GPIO.setup(BOOT, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin_esc, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(SHUTDOWN, GPIO.RISING, callback=powerSwitch)
GPIO.add_event_detect(RESET_RETROARCH, GPIO.RISING, callback=resetRetroArch)

def powerSwitch(callback):
        try:
                while True:
                        shutdownSignal = GPIO.input(SHUTDOWN)
                        pulseStart = time.time()
                        while shutdownSignal:
                                time.sleep(0.2)
                                if(time.time() - pulseStart >= REBOOTPULSEMAXIMUM):
                                        os.system("sudo poweroff")
                                        sys.exit()
                                shutdownSignal = GPIO.input(SHUTDOWN)

                        if time.time() - pulseStart >= REBOOTPULSEMINIMUM:
                                os.system("sudo reboot")
                                sys.exit()
                        if GPIO.input(SHUTDOWN):
                                GPIO.wait_for_edge(SHUTDOWN, GPIO.FALLING)
        except:
                pass 
        finally:
                GPIO.cleanup()

def resetRetroArch(callback):
        try:
                if (not key_esc) and (not GPIO.input(RESET_RETROARCH)): 
                        os.system("killall -9 retroarch")
                        key_esc = True
                if key_esc and GPIO.input(RESET_RETROARCH):
                        key_esc = False
        except Exception as e:
                pass
        finally:
                GPIO.cleanup()
