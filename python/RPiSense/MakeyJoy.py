#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

import sys, tty, termios

class MakeyJoy (object):
    """
    Return a direction of input from either the joystick or the keyboard.

    :param sense: (`SenseHat` instance)
        A reference to the SenseHat API

    :param makey: (`boolean`)
        Use Makey Makey (or keyboard) arrows instead of the Sense HAT joystick.
    """

    def __init__ (self, sense, makey=False):
        self.__sense = sense
        self.__makey = makey
        pass

    def GetEvent (self):
        """
        Get the event and intepret it as a direction.

        :return:

            - **direction** (`string`) -- The arrow event, i.e. 'up', 'down', 'left', or 'right.
        """
        
        if self.__makey:
            # read keyboard direction
            while True:
                while True:
                    k = self.__getch ()
                    if k != '': break
                    else: return 'blank'
                    pass
                if k == '\x1b[A': return 'up'
                elif k == '\x1b[B': return 'down'
                elif k == '\x1b[C': return 'right'
                elif k == '\x1b[D': return 'left'
                else: return k
                pass
            pass

        else:
            # read joystick direction
            # only count movements toward a direction
            while True:
                event = self.__sense.stick.wait_for_event ()
                # only return forced direction
                if event.action == 'released': continue
                elif event.direction == 'middle': continue
                return event.direction
            pass
        pass

    def __getch (self):
        # read keyboard press
        fd = sys.stdin.fileno ()
        old_settings = termios.tcgetattr (fd)
        try:
            tty.setraw (sys.stdin.fileno())
            ch = sys.stdin.read (1)
            # some characters are 3-tuples
            if ch == '\x1b': ch += sys.stdin.read (2)
            pass
        finally: termios.tcsetattr (fd, termios.TCSADRAIN, old_settings)
        return ch
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP
    from sense_hat import SenseHat

    # get the direction of the joystick or keyboard arrows
    p = AP (description='activate RepeatMe')
    p.add_argument ('--makey', action='store_true', default=False,
                    help='use keyboard (e.g. Makey Makey) as input')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    # start a new session with the Sense HAT
    sense = SenseHat ()
    sense.clear ()
    sense.low_light = args.dim

    # start the class and wait for an arrow input
    keyin = MakeyJoy (sense, args.makey)
    event = keyin.GetEvent ()
    print (event)
    pass
