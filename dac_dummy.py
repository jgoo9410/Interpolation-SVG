#!/usr/bin/env python3
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#

import tkinter as tk
import time

class DAC:
    '''a fake dac class'''
    def __init__(self):
        self.r = tk.Tk()
        self.size = 500
        self.multiplier = 5 # current image is 100x100, so scale by 5
        self.c = tk.Canvas(width=self.size, height=self.size,
            scrollregion=(0,self.size,-self.size,0))
        self.c.pack()
        x = y = self.size / 2 #initialize in the middle
        self.laser_pos = x, y
        self.laser_i = self.c.create_oval(*self.to_coords(self.laser_pos), fill='red')
        self.laser_power = True
        self.r.update()

    @staticmethod
    def to_coords(position):
        x, y = position
        return x-2, y-2, x+3, y+3

    def move(self, position):
        x, y = position
        x, y = x * self.multiplier, y * self.multiplier
        y = self.size-y
        if x < 0 or x > self.size or y < 0 or y > self.size:
            print("ERROR: out of bounds")
            return

        self.c.coords(self.laser_i, *self.to_coords((x, y)))
        if self.laser_power:
            self.c.create_line(self.laser_pos[0], self.laser_pos[1], x, y)
        self.laser_pos = x, y

        self.r.update()
        time.sleep(.01) # emulate blocking dacs

    def laser(self, value):
        '''turn the laser on or off'''
        self.laser_power = value

