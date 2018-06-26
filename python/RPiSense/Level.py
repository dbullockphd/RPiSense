#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

from time import sleep
from numpy import sqrt

class Level (object):
    """
    Display a white dot in the LED matrix to mimic the behavior of a bubble in a leveller.

    :param sense: (`SenseHat` instance)
        A reference to the SenseHat API

    :param fg: (`tuple`)
        The three 8-bit color values to use for the bubble.

    :param scale: (`integer`)
        The sensitivity to tilting. Higher values are more sensitive.
    """
    
    def __init__ (self, sense, fg=(255,255,255), scale=30):
        self.__sense = sense
        self.__fg = fg[0]
        self.__scale = scale
        pass

    def Update (self):
        """
        Refresh the LED matrix according to its current tilt.
        """

        # clear the display
        self.__sense.clear ()

        # read from the acceleromter
        d = self.__sense.get_accelerometer_raw ()
        x = d['x']
        y = d['y']
        z = d['z']
        r = sqrt (x**2 + y**2 + z**2)

        # scale and shift for display
        PX = int(round(-x/r * self.__scale + 3.5, 0))
        PY = int(round(-y/r * self.__scale + 3.5, 0))

        # boundary limits
        if PX < 0: PX = 0
        elif PX > 7: PX = 7
        if PY < 0: PY = 0
        elif PY > 7: PY = 7

        # display bubble at coordinates
        self.__sense.set_pixel (PX, PY, self.__fg)

        # wait to prevent stroboscopic artifacting
        sleep (0.1)
        pass
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP
    from sense_hat import SenseHat

    # start the leveller from the command line
    p = AP (description='activate level')
    p.add_argument ('--scale', type=int, default=30,
                    help='scale sensitivity')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    # start new session with the Sense HAT
    sense = SenseHat ()
    sense.clear ()
    sense.low_light = args.dim

    # configure compass as a white dot
    l = Level (sense, fg=(255,255,255), scale=args.scale)
    while True: l.Update ()
    pass
