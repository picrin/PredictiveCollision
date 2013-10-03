#Copyright (c) 2013 by
#Adam Kurkiewicz (adam /at\ kurkiewicz /dot\ pl)
#and Tom Wallis.
#All rights reserved.
#This file is available under a BSD-style copyright. See LICENCE for details.

import pygame as py, numpy, random, math, itertools

size = width, height = (800, 600)
wallsNumber = 4
py.init()
screen = py.display.set_mode(size)

class Numerical:

	@staticmethod
	def pointAtAngle(coords, angle, distance):
		return (coords[0] + math.sin(angle)*distance, coords[1] + math.cos(angle)*distance)
	
	@staticmethod
	def solveQuadraticPrune(equation): # choose the fastest
		delta = equation[1]**2 - 4*equation[0]*equation[2]
		if delta < 0:
			return float("+inf")
		else:
			solution = [((-equation[1] + delta**(1.0/2.0))/(2*(equation[0]))), ((-equation[1] - delta**(1.0/2.0))/(2*(equation[0])))]
			if min(solution) > 0:
				return min(solution)
			elif max(solution) > 0:
				return max(solution)
			else:
				return float("+inf")
	
	@staticmethod
	def solveQuadraticPrune_(equation): # choose the fastest. Might not be sufficiently tested.
		solution = numpy.roots(equation) # well, maybe
		solution = numpy.real_if_close(numpy.roots(equation))
		return Numerical.solutionPruning(solution)
	
	@staticmethod
	def solutionPruning(twoSolutions):
		"""
		@dev-only -- return least real positive from a sequence of two complex numbers (or exceptionally one). If there is no such number, returns one.
		"""
		try:
			if twoSolutions[0].imag == 0:
				if min(twoSolutions) > 0:
					return min(twoSolutions)
				elif max(twoSolutions) > 0:
					return max(twoSolutions)
				else:
					return float("+inf")
			else:
				return float("+inf")
		except IndexError:
			print "unusual stuff going on with solution pruning. Leading coefficient == 0?"
			return twoSolutions[0].real
	
	@staticmethod
	def solveLinear(equation):
		try:
			solution = -1 * equation[1]/equation[0]
			if solution > 0:
				return solution
			else:
				return float("+inf")
			#a + bt = 0
			#bt = -a
			#t = -a/b
		except ZeroDivisionError:
			print "unsual stuff going on with linear solver. Speed = 0?!"
			return float("+inf")

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

class Circles:
	#TODO refactor this to work without self.time and move it as an unbound method to Circle class
	def expectedTimeCircles(self, circleA, circleB):
		positionDifference = circleA.currentPosition(self.time) - circleB.currentPosition(self.time)
		velocityDifference = circleA.velocity - circleB.velocity
		radiiSum = circleA.radius + circleB.radius
		leadingCoefficient = velocityDifference[0]**2 + velocityDifference[1]**2
		middleCoefficient = 2*(velocityDifference[0]*positionDifference[0] + velocityDifference[1]*positionDifference[1])
		constantCoefficient = positionDifference[0]**2 + positionDifference[1]**2 - radiiSum**2
		return Numerical.solveQuadraticPrune([leadingCoefficient, middleCoefficient, constantCoefficient]) + self.time

	def expectedTimeWalls(self, circle): # the order is East, West, North, South
		wallsHorizontal = [circle.radius, width - circle.radius]
		wallsVertical = [circle.radius, height - circle.radius]
		for horizontal in wallsHorizontal:
			solution = Numerical.solveLinear([circle.velocity[0], circle.currentPosition(self.time)[0] - horizontal])
			yield solution + self.time
		for vertical in wallsVertical:
			solution = Numerical.solveLinear([circle.velocity[1], circle.currentPosition(self.time)[1] - vertical])
			yield solution + self.time

	@staticmethod
	def newVelocitiesCircles(circleA, circleB):
		normalVector = circleB.position - circleA.position
		commonFactor = normalVector/numpy.dot(normalVector, normalVector)
		normalComponentA = numpy.dot(circleA.velocity, normalVector)*commonFactor
		normalComponentB = numpy.dot(circleB.velocity, normalVector)*commonFactor
		circleANewVelocity = circleA.velocity - normalComponentA + normalComponentB
		circleBNewVelocity = circleB.velocity - normalComponentB + normalComponentA
		return circleANewVelocity, circleBNewVelocity
	
	@staticmethod
	def naiveCollisionCheck(circleA, circleB):
		positionDifference = circleB.position - circleA.position
		distance = numpy.linalg.norm(positionDifference)
		radiiSum = circleA.radius + circleB.radius
		return distance < radiiSum  
	
	def isWithinCurrentTimeslice(self, time):
		return time > self.time and time < self.time + 1
		
	@property
	def circlesNo(self):
		return len(self.circles)
	
	def __init__(self, circles):
		self.circles = circles
		self.time = 0
		self.circleCircle = numpy.ndarray(shape=([self.circlesNo]*2), dtype = float)
		self.circleWall = numpy.ndarray(shape=([self.circlesNo, wallsNumber]), dtype = float) # the order is East, West, North, South
		self.circleCircle.fill(float("inf"))
		#properties of the next collision. To be modified exlusively by self.whenNextCollision:
		self.__nextCollisionTime = 0
		self.__isPairOfCircles = False
		self.__i = (None, None) # can be (int, int) or (int,)
		self.allPairsCollisions()
		self.allWallsCollisions()
		self.whenNextCollision()
	def allWallsCollisions(self):
		for circleIndex in range(self.circlesNo):
			self.updateCircleWallEntry(circleIndex)

	def updateCircleWallEntry(self, circleIndex):
		for wallIndex, time in enumerate(self.expectedTimeWalls(self.circles[circleIndex])):
			self.circleWall[circleIndex][wallIndex] = time
	
	def allPairsCollisions(self):
		for indices in self.yieldPairsIndices():
			self.updateCircleCircleEntry(indices)

	def updateCircleCircleEntry(self, circlesIndices):
		self.circleCircle[circlesIndices] = self.expectedTimeCircles(*(self.circles[index] for index in circlesIndices))

	def yieldPairsIndices(self):
		for xIndex in range(0, self.circlesNo - 1):
			for yIndex in range(xIndex + 1, self.circlesNo):
				yield xIndex, yIndex

	def soonestCircleCircleCollision(self):
		minimum = float("+inf")
		indices = None
		for pair in self.yieldPairsIndices():
			time = self.circleCircle[pair] 
			if time < minimum:
				minimum = time
				indices = pair
		return indices, minimum

	def soonestCircleWallCollision(self):
		minimum = float("+inf")
		index = None
		for circleIndex in range(self.circlesNo):
			for wallIndex in range(wallsNumber):
				time = self.circleWall[circleIndex, wallIndex]
				if time < minimum:
					minimum = time
					index = circleIndex, wallIndex
		return index, minimum
	
	def whenNextCollision(self): # Side efects :(. This function should be exlusive for changing that attributes.
		circles = self.soonestCircleCircleCollision()
		wall = self.soonestCircleWallCollision()
		if circles[1] < wall[1]:
			self.__isPairOfCircles = True
			self.__i = circles[0]
			self.__nextCollisionTime = circles[1]
		else:
			self.__isPairOfCircles = False
			self.__i = wall[0]
			self.__nextCollisionTime = wall[1]


	def carryOutCircleCollision(self):
		assert self.__isPairOfCircles == True
		circles = tuple(self.circles[i] for i in self.__i)
		newVelocities = self.newVelocitiesCircles(*circles)
		
		
		for i, circle in enumerate(circles):
			circle.position = circle.currentPosition(self.__nextCollisionTime)
			circle.velocity = newVelocities[i]
			circle.time = self.__nextCollisionTime

		for i in self.__i:
			self.updateCircleWallEntry(i)
		
		
		self.circleCircle[self.__i] = float("+inf")
		for pairIndex in itertools.chain(self.yieldPairsForIndex(*self.__i), self.yieldPairsForIndex(*self.__i[::-1])):
			self.updateCircleCircleEntry(pairIndex)
	
	def carryOutWallCollision(self):
		assert self.__isPairOfCircles == False
		if self.__i[1] in [0, 1]:
			component = 0
		else:
			component = 1
		circle = self.circles[self.__i[0]]
		circle.position = circle.currentPosition(self.__nextCollisionTime)
		circle.velocity[component] *= -1
		circle.time = self.__nextCollisionTime
		self.updateCircleWallEntry(self.__i[0])
		self.circleWall[self.__i] = float("+inf")

		for pairIndex in self.yieldPairsForIndex(*[self.__i[0]]*2):
			self.updateCircleCircleEntry(pairIndex)

	def carryOutCollision(self):
		assert self.isWithinCurrentTimeslice(self.__nextCollisionTime)
		if self.__isPairOfCircles:
			self.carryOutCircleCollision()
		else:
			self.carryOutWallCollision()

	def animationStep(self):
		if self.isWithinCurrentTimeslice(self.__nextCollisionTime):
			self.carryOutCollision()
			self.whenNextCollision()
		else:
			self.time += 1
			
	def yieldPairsForIndex(self, index, withoutIndex):
		for i in range(index):
			if i != withoutIndex:
				yield i, index
		for i in range(index + 1, self.circlesNo):
			if i != withoutIndex:
				yield index, i

circles = [Circle(screen) for i in xrange(30)]

time = 0.0
circlesObject = Circles(circles)

while True:
	queue = py.event.get()
	for event in queue:
		if event.type == py.QUIT:
			quit()
	screen.fill([0,0,0])
	[circle.plot(circlesObject.time) for circle in circles]
	py.display.update()
	print circlesObject.time
	circlesObject.animationStep()
