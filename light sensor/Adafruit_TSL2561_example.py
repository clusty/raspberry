#!/usr/bin/python

from Adafruit_TSL2561 import TSL2561

tsl2561 = TSL2561(True)
print tsl2561.getOutput()
