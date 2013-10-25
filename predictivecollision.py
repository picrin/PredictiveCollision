from src import *

circles = [Circle(screen) for i in xrange(30)]

time = 0.0
circlesInstance = Circles(circles)
circlesInstance.animate()
