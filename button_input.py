import RPi.GPIO as GPIO
import OSC
import time
import datetime
import os

GPIO.setmode(GPIO.BCM)

pins = [19, 16, 13, 20, 12]
pin_data = {}
pin_first_tap = {}
pin_last_tap = {}
pin_last_release = {}
pin_tap_count = {} 

for pin in pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(pin, GPIO.RISING, callback=detectPress, bouncetime=200)
    pin_data[pin] = {}
    pin_data[pin]['pin_first_tap'] = time.time() 
    pin_data[pin]['pin_last_tap'] = time.time() 
    pin_data[pin]['pin_last_release'] = time.time() 
    pin_data[pin]['pin_tap_count'] = 0 
    pin_data[pin]['last_status'] = True


time.sleep(1)

c = OSC.OSCClient()
c.connect(('127.0.0.1', 7110))

lights = OSC.OSCClient()
lights.connect(('127.0.0.1', 7111))

# allow wifi to be disabled at startup
held_button = GPIO.input(19)
if not held_button:
    # button held
    os.system('ifconfig wlan0 down')
    lights.send(OSC.OSCMessage("/status", [2, 2, 2, 2, 2]))
    time.sleep(2)
    lights.send(OSC.OSCMessage("/status", [-1, -1, -1, -1, -1]))
else:
    # button not held
    #lights.send(OSC.OSCMessage("/status", [1, 1, 1, 1, 1]))
    time.sleep(2)

while True:
    for pin in pins:
        input_state = GPIO.input(pin)
        data = pin_data[pin]
        if not input_state:
            #rising edge
            time_from_last_rising = time.time() - data['pin_last_tap'] 
            if time_from_last_rising > 0.15:
                if data['last_status'] == True:
                    if time_from_last_rising < 0.35:
                        data['pin_tap_count'] += 1
                    else:
                        data['pin_tap_count'] = 1
                        data['pin_first_tap'] = time.time()
                    data['pin_last_tap'] = time.time()
                else:
                    if time_from_last_rising > .5 and data['pin_tap_count'] > 0:
                        try:
                            c.send( OSC.OSCMessage("/button/tap_and_hold", [pin, data['pin_tap_count']] ) )
                        except:
                            pass
                        print(data['pin_tap_count'], 'hold', pin)
                        data['pin_tap_count'] = 0
        else:
            time_from_first = time.time() - data['pin_first_tap'] 
            if data['last_status'] == False and time_from_first > 0.018 and time_from_first < .5:
                try:
                    c.send( OSC.OSCMessage("/button/realtime_tap", [pin] ) )
                except:
                    pass
                print('realtime tap', pin)
                print(datetime.datetime.now().time());
            if data['pin_tap_count'] > 0 and time_from_first > 0.35 * data['pin_tap_count']: 
                try:
                    c.send( OSC.OSCMessage("/button/tap", [pin, data['pin_tap_count']] ) )
                except:
                    pass
                print(data['pin_tap_count'], 'tap', pin)
                data['pin_tap_count'] = 0
        data['last_status'] = input_state
    time.sleep(.001)
