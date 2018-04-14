#!/usr/bin/env python

from time import sleep
from numpy import sqrt

class Compass (object):
    """
    Display the direction of North on the LED matrix.
    """

    red  = (255,   0,   0)
    blue = (  0,   0, 255)
    
    def __init__ (self, sense):
        self.sense = sense
        pass

    def Update (self):
        self._blank () # 

        # get the compass data and display a red dot in that direction
        d = self.sense.get_compass_raw ()
        x = d['x']
        y = d['y']
        r = sqrt (x**2 + y**2)
        
        PX = int(round(-x/r * 4 + 3.5, 0))
        PY = int(round(-y/r * 4 + 3.5, 0))

        if PX < 0: PX = 0
        elif PX > 7: PX = 7
        if PY < 0: PY = 0
        elif PY > 7: PY = 7
    
        self.sense.set_pixel (PX, PY, self.red)
        sleep (0.1)
        pass

    def _blank (self):
        # clear the screen and draw a blue circle
        self.sense.clear ()

        for i in xrange(2, 6):
            for j in (0, 7): self.sense.set_pixel (i, j, self.blue)
            pass

        for i in (1, 6):
            for j in (1, 6): self.sense.set_pixel (i, j, self.blue)
            pass

        for i in (0, 7):
            for j in xrange(2, 6): self.sense.set_pixel (i, j, self.blue)
            pass
        pass
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP
    from sense_hat import SenseHat

    p = AP (description='activate compass')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    sense = SenseHat ()
    sense.clear ()
    sense.low_light = args.dim

    c = Compass (sense)
    while True: c.Update ()
    pass
