from global_values import *
import random, math
import ABCLogger, Circles, Circle
import yaml

class CollisionLogger(ABCLogger.ABCLogger):
	def writeHeader(self):
		return "---\n" + yaml.dump({'simulation':{'width': width, 'height': height, 'walls number': wallsNumber}}, default_flow_style = False)
	def log(self, foreignSelf):
		time = foreignSelf.time
		exactTime = foreignSelf._nextCollisionTime
		isCircleCircle = foreignSelf._isPairOfCircles
		collisionSpecific = []
		collisionInfo = {'time frame': time, 'exact time': exactTime, 'circle-circle': isCircleCircle, 'objects collided': collisionSpecific}
		yamlDict = {'collision': collisionInfo}
		if isCircleCircle:
			circleInstances = [foreignSelf.circles[i] for i in foreignSelf._i]
			for circle in circleInstances:
				 collisionSpecific.append(circle.dictChangables())
		else:
			circleInstance = foreignSelf._i[0]
			collisionSpecific.append(foreignSelf.circles[circleInstance].dictChangables())
		return "---\n" + yaml.dump(yamlDict)
		
class CircleYamled(Circle.Circle):
	def dictChangables(self):
		return {'circle': {'counter': self.counter,'position': [float(number) for number in self.position], 'velocity': [float(number) for number in self.velocity], 'time': self.time}}
	def dictAllRelevant(self):
		return {'circle': {'counter': self.counter,'position': [float(number) for number in self.position], 'velocity': [float(number) for number in self.velocity], 'time': self.time, 'color': self.color, 'radius': self.radius}}


circleA = CircleYamled(screen, position = [width/2 - 100, height/2], angle = + 0.1, speed = 1)
circleB = CircleYamled(screen, position = [width/2 + 100, height/2], angle = math.pi - 0.1, speed = 1)

logger = CollisionLogger("yaml.log")
circlesList = [circleA, circleB]


circles = Circles.Circles(circlesList)
logger.hook(circles.carryOutCollision)
circles.animate()

