#!/usr/bin/env python3
#
#   Documentation is like sex.
#   When it's good, it's very good.
#   When it's bad, it's better than nothing.
#   When it lies to you, it may be a while before you realize something's wrong.
#

from svg_read import Slice
from dac_dummy import DAC
#~ from dac import DAC

s = Slice('slices/54.svg', DAC)
s.run()
input()
