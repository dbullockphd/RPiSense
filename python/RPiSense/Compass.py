#!/usr/bin/env python

from time import sleep
from numpy import sqrt

class Compass (object):
    """
    Display the direction of North on the LED matrix.

    :param sense: (`SenseHat` instance)
        A reference to the SenseHat API

    :param fg: (`tuple`)
        The three 8-bit color values to use for a dot.

    :param bg: (`list`)
        The three 8-bit color values to use for a circle.
    """

    def __init__ (self, sense, fg=(255,0,0), bg=(0,0,255)):
        self.__sense = sense
        self.__fg = fg[0]
        self.__bg = bg[0]
        pass

    def Update (self):
        """
        Refresh the LED matrix according to its current orientation.
        """

        # clear the display and draw a circle
        self.__blank ()

        # get the compass data and display a dot in that direction
        d = self.__sense.get_compass_raw ()
        x = d['x']
        y = d['y']
        r = sqrt (x**2 + y**2)

        # scale and shift for display
        PX = int(round(-x/r * 4 + 3.5, 0))
        PY = int(round(-y/r * 4 + 3.5, 0))

        # boundary limits
        if PX < 0: PX = 0
        elif PX > 7: PX = 7
        if PY < 0: PY = 0
        elif PY > 7: PY = 7

        # display pixel
        self.__sense.set_pixel (PX, PY, self.__fg)

        # wait to prevent stroboscopic artifacting        
        sleep (0.1)
        pass

    def __blank (self):
        # clear the screen and draw a circle
        self.__sense.clear ()

        # top and bottom pixels
        for i in xrange (2, 6):
            for j in (0, 7): self.__sense.set_pixel (i, j, self.__bg)
            pass

        # corner pixels
        for i in (1, 6):
            for j in (1, 6): self.__sense.set_pixel (i, j, self.__bg)
            pass

        # left and right pixels
        for i in (0, 7):
            for j in xrange (2, 6): self.__sense.set_pixel (i, j, self.__bg)
            pass
        pass
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP
    from sense_hat import SenseHat

    # start the compass from the command line
    p = AP (description='activate compass')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    # start new session with the Sense HAT
    sense = SenseHat ()
    sense.clear ()
    sense.low_light = args.dim

    # configure compass as a red dot on a blue circle
    c = Compass (sense, fg=(255,0,0), bg=(0,0,255))
    while True: c.Update ()
    pass
