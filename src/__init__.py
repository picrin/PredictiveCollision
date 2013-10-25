from ABCLogger import *
from Circle import *
from Circles import *
from Numerical import *
from SimpleLogger import *
from track_and_log import *
from math import *
from numpy import *
from os import *
from inspect import *
from random import *
from yaml import *
import pygame as py

__all__ = ['ABCLogger', 'Circle', 'Circles', 'Numerical', 'SimpleLogger', 'track_and_log']

'''
	Initialisation for the course module for Predictive Collision.
	Project maintained by Adam Kurkiewicz (adam /at\ kurkiewicz /dot\ pl)
	And members of the Scientific Programming subgroup of GUTS at
	Glasgow University.
'''


# For global values:

size = width, height = (800, 600)
py.init()
screen = py.display.set_mode(size)
wallsNumber = 4


# From the old simplelogger.py. Perhaps a prompt should be put here to
#   choose when we actually want to log?

simpleLogger = SimpleLogger("log")
simpleInstance = SimpleClass()
simpleLogger.hook(simpleInstance.doFunnyThingsWithAttribute) 
#print simpleInstance.__dict__
simpleInstance.doFunnyThingsWithAttribute("1")
simpleInstance.doFunnyThingsWithAttribute("3")
simpleInstance.doFunnyThingsWithAttribute("4")
simpleInstance.doFunnyThingsWithAttribute("aaa")


