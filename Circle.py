from global_values import *
import math, numpy, random
from Numerical import Numerical
class Circle:
	
	counter = 0 # your program shouldn't rely on this. Purely visual.
	
	def __init__(self, surfaceToBlit = screen, radius = 10, time = 0, position = None, angle = None, speed = 1, color = None, font = None):

		# general attributes, frequently used for both alorithm and plotting.
		self.time = time
		self.radius = radius
		self.position = self.initializePosition(position) 
		self.velocity = self.initializeVelocity(angle) * speed
		
		# attributes that are primarily used for visual representation
		self.surfaceToBlit = surfaceToBlit
		self.color = self.initializeColor(color) 
		self.counter = Circle.counter
		Circle.counter += 1
		self.font = self.initializeFont(font)

	@property
	def angle(self):
		return math.atan2(*self.velocity)

	def initializePosition(self, position):
		#TODO initialization should be first checking for any potential collisions with objects already initialized! 
		if position is None:
			return numpy.array([random.uniform(0 + self.radius, width - self.radius), random.uniform(0 + self.radius, height - self.radius)], dtype=float)
		else:
			return numpy.array(position, dtype=float)
	
	def initializeVelocity(self, angle):
 		if angle is None:
			unitVelocity = random.uniform(0, 2*math.pi)
			return numpy.array([math.cos(unitVelocity), math.sin(unitVelocity)], dtype=float)
		else:
			return numpy.array([math.cos(angle), math.sin(angle)], dtype=float)
	
	def initializeColor(self, color):
		if color is None:
			return [random.randint(0,255) for i in range(3)]
		else:
			return color
	
	def initializeFont(self, font):
		if font is None:
			return py.font.Font(None, self.radius*3)
		else:
			return font
	
	def __str__(self):
		return "position: " + str(self.position) + ", time: " + str(self.time) + ", radius: " + str(self.radius) + ", velocity: " + str(self.velocity)

	def plot(self, time, isArrow = True, isNumber = True):
		circle = py.draw.circle(self.surfaceToBlit, self.color, [int(number) for number in self.currentPosition(time)], self.radius)
		if isNumber:
			self.plotNumber(time)
		if isArrow:
			self.plotArrow(time)

		return circle
	
	def plotArrow(self, time, factorLength = 40, factorWidth = 10, angleArrows = math.pi/4, color = (0, 255, 0)):
		startPos = self.currentPosition(time)
		endPos = startPos + self.velocity*factorLength
		width = numpy.linalg.norm(self.velocity)*factorWidth
		arrowUp = Numerical.pointAtAngle(endPos, math.pi + self.angle - angleArrows, width)
		arrowDown = Numerical.pointAtAngle(endPos, math.pi + self.angle + angleArrows, width)
		py.draw.aaline(self.surfaceToBlit, color, startPos, endPos)
		py.draw.aaline(self.surfaceToBlit, color, endPos, arrowUp)
		py.draw.aaline(self.surfaceToBlit, color, endPos, arrowDown)

	def plotNumber(self, time, color = (255,0,0)):
		pos = self.currentPosition(time)
		fontSurface = self.font.render(str(self.counter), True, color)
		self.surfaceToBlit.blit(fontSurface, pos - [self.radius/2, self.radius])

	def currentPosition(self, time):
		timeDifference = time - self.time
		#assert timeDifference >= 0
		return self.velocity * timeDifference + self.position
