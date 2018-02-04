#!/usr/bin/env python3
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#
# TODO: fill the paths that need filling
# TODO: add svg type rect
# TODO: add svg type circle
# TODO: add svg type ellipse
# TODO: add svg type line
# TODO: add svg type polyline
# TODO: add svg type polygon

import xml.etree.ElementTree as et
from math import hypot

svg_path_cmds = dict(
    M = 'moveto',
    L = 'lineto',
    H = 'horizontal lineto',
    V = 'vertical lineto',
    C = 'curveto',
    S = 'smooth curveto',
    Q = 'quadratic Bézier curve',
    T = 'smooth quadratic Bézier curveto',
    A = 'elliptical Arc',
    Z = 'closepath',
    )

def linspace(start, stop, num):
    range_ = stop - start
    step = range_ / num
    yield from (start + (i*step) for i in range(int(num)))
    yield stop

def load_svg_paths(tree, ns):
    raw_paths = (path.get('d') for path in tree.findall('.//svg:path', ns))

    # some of the paths contain multiple paths which need to be separated
    paths = []
    for path in raw_paths:
        paths += path.strip().split('Z')
    paths = filter(None, [p.strip() for p in paths])

    for raw_data in paths:
        for command in 'HVCSQTA':
            if command in raw_data:
                raise ValueError('path command {} ({}) not yet supported'.format(command, svg_path_cmds[command]))
        pairs = raw_data[1:].split("L") # make a list of pairs
        converted = [tuple(map(float, pair.split())) for pair in pairs] # convert to floats
        yield converted

def load_svg(fn):
    tree = et.parse(fn)
    ns = {'svg':tree.getroot().tag.split('}')[0][1:]}
    for path in load_svg_paths(tree, ns):
        yield path
    # add other svg structures here.

def find_distance(pos1, pos2):
    x1, y1, x2, y2 = pos1+pos2
    return hypot(x2 - x1, y2 - y1)

class Slice:
    def __init__(self, fn, DAC):
        self.position = None
        self.speed = .5 # units per tick
        self.dac = DAC()
        self.paths = list(load_svg(fn))
        print("{:,} points loaded from {}".format(sum(map(len, self.paths)), fn))

    def move(self, position):
        distance = find_distance(position, self.position)
        steps = distance / self.speed
        if steps >= 2:
            start_x, start_y = self.position
            end_x, end_y = position
            interpolated_x = linspace(start_x, end_x, steps)
            interpolated_y = linspace(start_y, end_y, steps)
            for X, Y in zip(interpolated_x, interpolated_y):
                self.dac.move((X, Y))
        else: # only one step needed
            self.dac.move(position)
        self.position = position

    def run(self):
        for path in self.paths:
            self.dac.laser(False)
            self.dac.move(path[0]) # move to first spot
            self.position = path[0]
            self.dac.laser(True) # turn on the laser
            for spot in path[1:]:
                self.move(spot)
            self.dac.laser(False)

