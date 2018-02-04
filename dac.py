#!/usr/bin/env python3
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#

import time

import Adafruit_MCP4725

X_ADDRESS = 0x62
Y_ADDRESS = 0x63

# adjust these to use less than the full range
MIN = 0
MAX = 2**12

range_ = MAX - MIN

DEBUG = False

class DAC:
    def __init__(self):
        self.dac_x = Adafruit_MCP4725.MCP4725(address=X_ADDRESS)
        self.dac_y = Adafruit_MCP4725.MCP4725(address=Y_ADDRESS)

        self.laser_power = False

    def move(self, position):
        ''':position: a float from 0 - 100'''
        x, y = position
        x_bits = int((x / 100) * range_ + MIN)
        y_bits = int((y / 100) * range_ + MIN)

        self.dac_x.set_voltage(x_bits)
        self.dac_y.set_voltage(y_bits)

        if DEBUG:
            print('move to {:>4}, {:>4}'.format(x_bits, y_bits))

        # time to allow the galvos to catch up
        # if the dac write commands are blocking, delete this line.
        time.sleep(.01)

    def laser(self, value):
        '''turn the laser on or off'''
        self.laser_power = value

