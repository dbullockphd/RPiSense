#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

from os import getenv
from random import randint
from numpy import uint8, where, genfromtxt

class Colors (object):
    """
    Keep a list of colors organized and sorted. You can select colors by name, by index number, and even at random.

    :param order: (`array_like`)
        This defines the hierarchy of field names when sorting. See the colors.csv file for information about these names.

    :param ascending: (`boolean`)
        Sorting can either be ascending or descending.
    """

    __colorscsv = '/home/pi/src/RPiSense/configs/colors.csv'

    def __init__ (self, order=('H','L','S'), ascending=True):
        self.colors = genfromtxt (self.__colorscsv,
                                  dtype=[
                                      ('name',object),
                                      ('r',uint8), ('g',uint8), ('b',uint8),
                                      ('h',uint8), ('s',uint8), ('v',uint8),
                                      ('H',uint8), ('L',uint8), ('S',uint8),
                                  ],
                                  delimiter=',')

        # sort by columns
        self.colors.sort (kind='mergesort', order=order)
        pass

    def random (self, mode='rgb'):
        """
        Select a color at random.

        :param mode: ('string')
            This is a 3-character description for the color category to return. Valid options are 'rgb' (red, green, blue), 'hsv' (hue, saturation, value), and 'HLS' (HUE, LUMINOSITY, SATURATION).

        :return:

            - **name** (`string`) -- The name of the color.

            - **abc** (`tuple`) -- Three 8-bit values for the color.
        """
        
        # pick a random color between low and high
        i = randint (0, self.colors.shape[0]-1)
        name, abc = self.__get (i, mode)
        return name, abc

    def randomColor (self, mode='rgb'):
        """
        Select a color at random.

        :param mode: ('string')
            This is a 3-character description for the color category to return. Valid options are 'rgb' (red, green, blue), 'hsv' (hue, saturation, value), and 'HLS' (HUE, LUMINOSITY, SATURATION).

        :return:

            - **abc** (`tuple`) -- Three 8-bit values for the color.
        """

        # get the tuple from the random method
        name, abc = self.random (mode)
        return abc

    def randomName (self, mode='rgb'):
        """
        Select a color at random.

        :param mode: ('string')
            This is a 3-character description for the color category to return. Valid options are 'rgb' (red, green, blue), 'hsv' (hue, saturation, value), and 'HLS' (HUE, LUMINOSITY, SATURATION).

        :return:

            - **name** (`string`) -- The name of the color.

            - **abc** (`tuple`) -- Three 8-bit values for the color.
        """

        # get the name from the random method
        name, abc = self.random (mode)
        return name

    def fetch (self, key, mode='rgb'):
        """
        Select a color at random.

        :param key: (`string`)
            The name of the color to find.

        :param mode: ('string')
            This is a 3-character description for the color category to return. Valid options are 'rgb' (red, green, blue), 'hsv' (hue, saturation, value), and 'HLS' (HUE, LUMINOSITY, SATURATION).

        :return:

            - **abc** (`tuple`) -- Three 8-bit values for the color.
        """
        
        # get a color by name
        f = where (self.colors['name'] == key)
        if len(f[0]) == 0: raise ValueError ('color {0:s} unknown'.format(key))
        i = f[0][0]
        name, abc = self.__get (i, mode)
        return abc

    def __get (self, i, mode):
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
        name = self.colors['name'][i]
        return name, (a, b, c)

    def __getitem__ (self, key):
        # dictionary-like name access
        if key == 'random': return self.randomColor ()
        else: return self.fetch (key, 'rgb')
        pass
    pass

if __name__ == '__main__':
    from argparse import ArgumentParser as AP

    # get a color by name on the command line
    p = AP (description='get a color by name')
    p.add_argument ('color', default='random')
    args = p.parse_args ()

    # get the color values
    c = Colors ()
    if args.color == 'random': name, rgb = c.random ()
    else:
        name = args.color
        rgb = c[args.color]
        pass

    # display the name of the color and its values
    print ('{0:s}: {1:s}'.format (str(name), str(rgb)))
    pass
