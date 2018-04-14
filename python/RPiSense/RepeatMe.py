#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

import sys, tty, termios
from random import randint
from time import sleep

from MakeyJoy import MakeyJoy

class RepeatMe (object):
    """
    Play a game of Repeat After Me. A square will appear on the Sense Hat LED
    matrix. Press the joystick in the direction of the square. The game will
    continue adding to the sequence as long as you pick the right direction.
    Get the sequence right and the display turns green. Get the sequence wrong
    and the display turns red and you have to start over.
    """

    yellow = (255, 255,   0)
    blue   = (  0,   0, 255)
    red    = (255,   0,   0)
    green  = (  0, 128,   0)

    def __init__ (self, sense, t=0.5, makey=False):
        self.sense = sense # Sense Hat API
        self.t = t         # standard time for display
        self.keyin = MakeyJoy (sense, makey) # keyboard input
        self.seq = []      # internal sequence
        self._append ()    # run program
        pass

    def _append (self):
        # get a random number and append it to the sequence
        i = randint (0,3)
        self.seq.append (i)

        # display the sequence
        for term in self.seq:
            self.sense.clear ()
            if term == 0: self._up ()
            elif term == 1: self._left ()
            elif term == 2: self._right ()
            else: self._down ()
            sleep (self.t)
            self.sense.clear ()
            sleep (self.t/2)
            pass

        self._test ()
        pass

    def _test (self):
        for term in self.seq:
            self.sense.clear ()

            # get joystick movements
            event = self.keyin.GetEvent ()
            if event == 'up':
                val = 0
                self._up ()
                pass
            elif event == 'left':
                val = 1
                self._left ()
                pass
            elif event == 'right':
                val = 2
                self._right ()
                pass
            else: # event == 'down'
                val = 3
                self._down ()
                pass
            sleep (self.t/2)

            if val != term: # wrong answer
                self.sense.clear (self.red)
                sleep (4*self.t)
                self.sense.clear ()
                quit ()
                pass
            pass

        # correct sequence
        self.sense.clear (self.green)
        sleep (4*self.t)

        # append to sequence
        self._append ()
        pass

    def _up (self):
        # display yellow square at top
        for i in (3, 4):
            for j in (0, 1): self.sense.set_pixel (i, j, self.yellow)
            pass
        pass

    def _left (self):
        # display blue square at left
        for i in (0, 1):
            for j in (3, 4): self.sense.set_pixel (i, j, self.blue)
            pass
        pass

    def _right (self):
        # display red square at right
        for i in (6, 7):
            for j in (3, 4): self.sense.set_pixel (i, j, self.red)
            pass
        pass

    def _down (self):
        # display green square at bottom
        for i in (3, 4):
            for j in (6, 7): self.sense.set_pixel (i, j, self.green)
            pass
        pass
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP
    from sense_hat import SenseHat

    p = AP (description='activate RepeatMe')
    p.add_argument ('--makey', action='store_true', default=False,
                    help='use keyboard (e.g. Makey Makey) as input')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    sense = SenseHat ()
    sense.clear ()
    sense.low_light = args.dim

    r = RepeatMe (sense, 0.5, args.makey)
    pass
