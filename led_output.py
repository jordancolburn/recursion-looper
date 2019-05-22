# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from time import sleep

from neopixel import *
from OSC import OSCServer

import argparse
import signal
import sys
def signal_handler(signal, frame):
        colorWipe(strip, Color(0,0,0))
        sys.exit(0)

def opt_parse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store_true', help='clear the display on exit')
        args = parser.parse_args()
        if args.c:
                signal.signal(signal.SIGINT, signal_handler)

# LED strip configuration:
LED_COUNT      = 5  # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 127     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

ledState = [-1, -1, -1, -1, -1]

def setStatus(strip, status):
	for i in range(len(status)):
		strip.setPixelColor(i, status_colors[status[4-i]])
		strip.show()

def setEdit(strip, status):
        print status[0]
        strip.setPixelColor(0, Color(0, status[0] * 255, 0))
        strip.show()
        strip.setPixelColor(1, Color(0, 0, 0))
        strip.show()
        strip.setPixelColor(2, Color(0, 0, 0))
        strip.show()
        strip.setPixelColor(3, Color(0, 0, 0))
        strip.show()
        strip.setPixelColor(4, Color(0, 0, 0))
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
        # Process arguments
        opt_parse()

	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	
	server = OSCServer( ("localhost", 7111) )
	server.timeout = 0
	run = True

	#-2 - Recording, 1st time
	#-1 - Uninitialized 
	# 0 - Off
	# 1 - Playing
	# 2 - Overdub
	status_colors = {
		-2: Color(255, 0, 0),
		-1: Color(128, 128, 128),
                0: Color(0, 0, 255),
		1: Color(0, 255, 0),
		2: Color(255, 220, 0)
	}
        
	setStatus(strip, [-1, -1, -1, -1, -1]); 
        time.sleep(.2);
	setStatus(strip, [1, 1, 1, 1, 1]); 
        time.sleep(.2);
	setStatus(strip, [-1, -1, -1, -1, -1]); 
        time.sleep(.2);
	setStatus(strip, [1, 1, 1, 1, 1]); 
        time.sleep(.2);
	setStatus(strip, [-1, -1, -1, -1, -1]); 

	# this method of reporting timeouts only works by convention
	# that before calling handle_request() field .timed_out is 
	# set to False
	def handle_timeout(self):
	    self.timed_out = True

	# funny python's way to add a method to an instance of a class
	import types
	server.handle_timeout = types.MethodType(handle_timeout, server)

	def status_callback(path, tags, args, source):
            setStatus(strip, args)

	def edit_callback(path, tags, args, source):
            setEdit(strip, args)
     
	server.addMsgHandler("/status", status_callback )
	server.addMsgHandler("/edit", edit_callback )

        def each_frame():
            # clear timed_out flag
            server.timed_out = False
            # handle all pending requests then return
            while not server.timed_out:
                   server.handle_request()

	while run:
            each_frame()
	    sleep(.08)

	server.close()


