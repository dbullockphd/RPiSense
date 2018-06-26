#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

import sys, tty, termios
from random import randint
from time import sleep

from MakeyJoy import MakeyJoy

class RepeatMe (object):
    """
    Play a game of Repeat After Me. A square will appear on the Sense HAT LED matrix. Press the joystick in the direction of the square. The game will continue adding to the sequence as long as you pick the right direction. Get the sequence right and the display turns green. Get the sequence wrong and the display turns red and you have to start over.

    :param sense: (`SenseHat` instance) A reference to the SenseHat API

    :param time: (`float`) The amount of time to display each entry in the sequence.

    :param makey: (`boolean`) Use Makey Makey (or keyboard) arrows instead of the Sense HAT joystick.
    """

    __yellow = (255, 255,   0)
    __blue   = (  0,   0, 255)
    __red    = (255,   0,   0)
    __green  = (  0, 128,   0)

    def __init__ (self, sense, time=0.5, makey=False):
        self.__sense = sense
        self.__time = time
        self.__keyin = MakeyJoy (sense, makey)
        self.__seq = []
        pass

    def Next (self):
        """
        Get the next entry in the sequence and test the input.
        """
        
        # get a random number and append it to the sequence
        i = randint (0,3)
        self.__seq.append (i)

        # display the sequence
        for term in self.__seq:
            self.__sense.clear ()
            if term == 0: self.__up ()
            elif term == 1: self.__left ()
            elif term == 2: self.__right ()
            else: self.__down ()
            sleep (self.__time)
            self.__sense.clear ()
            sleep (self.__time/2)
            pass

        return self.__test ()

    def __test (self):
        for term in self.__seq:
            self.__sense.clear ()

            # get joystick movements
            event = self.__keyin.GetEvent ()
            if event == 'up':
                val = 0
                self.___up ()
                pass
            elif event == 'left':
                val = 1
                self.__left ()
                pass
            elif event == 'right':
                val = 2
                self.__right ()
                pass
            else: # event == 'down'
                val = 3
                self.__down ()
                pass
            sleep (self.__time/2)

            if val != term: # wrong answer
                self.__sense.clear (self.__red)
                sleep (4*self.__time)
                self.__sense.clear ()
                return False
            pass

        # correct sequence
        self.__sense.clear (self.__green)
        sleep (4*self.__time)
        return True

    def __up (self):
        # display yellow square at top
        for i in (3, 4):
            for j in (0, 1): self.__sense.set_pixel (i, j, self.__yellow)
            pass
        pass

    def __left (self):
        # display blue square at left
        for i in (0, 1):
            for j in (3, 4): self.__sense.set_pixel (i, j, self.__blue)
            pass
        pass

    def __right (self):
        # display red square at right
        for i in (6, 7):
            for j in (3, 4): self.__sense.set_pixel (i, j, self.__red)
            pass
        pass

    def __down (self):
        # display green square at bottom
        for i in (3, 4):
            for j in (6, 7): self.__sense.set_pixel (i, j, self.__green)
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
