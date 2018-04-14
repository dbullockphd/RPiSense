#!/usr/bin/env python

# https://github.com/dbullockphd/RPiSense

def C2F (C):
    # convert celsius to fahrenheit
    F = 9.*C/5. + 32
    return F

def mbar2inHg (mbar):
    # convert millibars to inches of mercury
    inHg = 0.029530 * mbar
    return inHg
