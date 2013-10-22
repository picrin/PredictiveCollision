#Copyright (c) 2013 by
#Adam Kurkiewicz (adam /at\ kurkiewicz /dot\ pl)
#and Tom Wallis.
#All rights reserved.
#This file is available under a BSD-style copyright. See LICENCE for details.
from global_values import *
import random, math, itertools
import Numerical, ABCLogger, Circles, Circle

circles = [Circle.Circle(screen) for i in xrange(30)]

time = 0.0
#for circle in circles:
#	print circle.strAllRelevantYaml()
Circles.Circles(circles).animate()

