#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

from time import sleep
from numpy import sqrt

class Level (object):
    """
    Display a white dot in the LED matrix to mimic the behavior of a bubble in
    a leveller.
    """
    
    white = (255, 255, 255)
    
    def __init__ (self, sense, scale=30):
        self.sense = sense # Sense Hat API
        self.scale = scale # sensitivity (higher = more sensitive)
        pass

    def Update (self):
        self.sense.clear ()

        # read from the acceleromter
        d = self.sense.get_accelerometer_raw ()
        x = d['x']
        y = d['y']
        z = d['z']
        r = sqrt (x**2 + y**2 + z**2)

        # scale and shift for display
        PX = int(round(-x/r * self.scale + 3.5, 0))
        PY = int(round(-y/r * self.scale + 3.5, 0))

        # limiting values
        if PX < 0: PX = 0
        elif PX > 7: PX = 7
        if PY < 0: PY = 0
        elif PY > 7: PY = 7

        # display white dot at coordinates
        self.sense.set_pixel (PX, PY, self.white)
        sleep (0.1)
        pass
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP
    from sense_hat import SenseHat

    p = AP (description='activate level')
    p.add_argument ('--scale', type=int, default=30,
                    help='scale sensitivity')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    sense = SenseHat ()
    sense.clear ()
    sense.low_light = args.dim

    l = Level (sense, args.scale)
    while True: l.Update ()
    pass
