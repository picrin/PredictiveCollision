from global_values import *
import random, math
import ABCLogger, Circles, Circle

class CirclesLogger(ABCLogger.ABCLogger):
	def writeHeader(self):
		return "circle-circle: frameNo , exactTime\n\tcircleNo , [positionX, positionY] "
	def log(self, foreignSelf):
		time = str(foreignSelf.time)
		exactTime = str(foreignSelf._nextCollisionTime)
		toreturn = time + "," + exactTime
		if foreignSelf._isPairOfCircles == True:
			circleInstances = [foreignSelf.circles[i] for i in foreignSelf._i]
			labels = [circle.counter for circle in circleInstances]
			labelA = str(labels[0])
			positionA = str(circleInstances[0].position)
			speedA = str(circleInstances[0].velocity)
			labelB = str(labels[1])
			positionB = str(circleInstances[1].position)
			speedB = str(circleInstances[1].velocity)
			toreturn += "\n\t" + labelA + "," + positionA + "," + speedA + "\n\t" + labelB + "," + positionB + "," + speedB
			
		return toreturn


logger = CirclesLogger("controlled.log")
circlesList = [Circle.Circle(screen) for i in xrange(30)]


circles = Circles.Circles(circlesList)
logger.hook(circles.carryOutCollision)
circles.animate()

