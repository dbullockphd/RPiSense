#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

def C2F (C):
    """
    Convert Celsius to Fahrenheit

    :param C: (`float`)
        The temperature in Celsius.

    :return:

        - **F** (`float`) -- The temperature in Fahrenheit.
    """

    F = 9.*C/5. + 32
    return F

def mbar2inHg (mbar):
    """
    Convert millibars to inches of mercury.

    :param mbar: (`float`)
        The pressure in millibars.

    :return:

        - **inHg** (`float`) -- The pressure in inches of mercury.
    """

    inHg = 0.029530 * mbar
    return inHg
