#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

from random import randint
from numpy import uint8, where, genfromtxt

class Colors (object):
    """
    Keep a list of colors organized and sorted. You can select colors by name,
    by index number, and even at random.
    """

    def __init__ (self, order=('H','L','S'), ascending=True):
        self.colors = genfromtxt ('colors.csv',
                                  dtype=[('r',uint8), ('g',uint8), ('b',uint8),
                                         ('h',uint8), ('s',uint8), ('v',uint8),
                                         ('H',uint8), ('L',uint8), ('S',uint8),
                                         ('name',object)],
                                  delimiter=',')

        # sort by columns
        self.colors.sort (kind='mergesort', order=order)
        pass

    def random (self, low=-1, high=-1, mode='rgb'):
        # pick a random color between low and high
        if low < 0: low = 0
        if high < 0: high = self.colors.shape[0]
        i = randint (low, high-1)
        rgb = self._get (i, mode)
        return rgb

    def fetch (self, key, mode='rgb'):
        # get a color by name
        f = where (self.colors['name'] == key)
        if len(f[0]) == 0:
            print 'unknown color', key, 'returns None'
            return None
        else:
            i = f[0][0]
            rgb = self._get (i, mode)
            return rgb
        pass

    def _get (self, i, mode):
        # get color by mode
        if mode == 'rgb':
            a = self.colors['r'][i]
            b = self.colors['g'][i]
            c = self.colors['b'][i]
            pass
        elif mode == 'hsv':
            a = self.colors['h'][i]
            b = self.colors['s'][i]
            c = self.colors['v'][i]
            pass
        elif mode == 'HLS':
            a = self.colors['H'][i]
            b = self.colors['L'][i]
            c = self.colors['S'][i]
            pass
        return (a, b, c)

    def __getitem__ (self, key):
        # dictionary-like name access
        return self.fetch (key, 'rgb')
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP

    p = AP (description='get a color by name')
    p.add_argument ('color', default='random')
    p.add_argument ('--dim', action='store_true', default=False,
                    help='force LED matrix dim')
    args = p.parse_args ()

    c = Colors ()
    if args.color == 'random': print c.random ()
    else: print args.color, c[args.color]
    pass
