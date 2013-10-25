import ABCLogger, pygame as py, numpy, itertools
from Numerical import Numerical
from global_values import *

class CirclesLogger(ABCLogger.ABCLogger):
	def log(self, foreignSelf):
		return repr(foreignSelf._nextCollisionTime)
class Circles:
	def expectedTimeCircles(self, circleA, circleB):
		#TODO refactor this to work without self.time and move it as an unbound method to Circle class
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
		self._nextCollisionTime = 0
		self._isPairOfCircles = False
		self._i = (None, None) # can be (int, int) or (int,)
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
			time = float(self.circleCircle[pair])
			if time < minimum:
				minimum = time
				indices = pair
		return indices, minimum

	def soonestCircleWallCollision(self):
		minimum = float("+inf")
		index = None
		for circleIndex in range(self.circlesNo):
			for wallIndex in range(wallsNumber):
				time = float(self.circleWall[circleIndex, wallIndex])
				if time < minimum:
					minimum = time
					index = circleIndex, wallIndex
		return index, minimum
	
	def whenNextCollision(self): # Side efects :(. This function should be exlusive for changing that attributes.
		circles = self.soonestCircleCircleCollision()
		wall = self.soonestCircleWallCollision()
		if circles[1] < wall[1]:
			self._isPairOfCircles = True
			self._i = circles[0]
			self._nextCollisionTime = circles[1]
		else:
			self._isPairOfCircles = False
			self._i = wall[0]
			self._nextCollisionTime = wall[1]


	def carryOutCircleCollision(self):
		assert self._isPairOfCircles == True
		circles = tuple(self.circles[i] for i in self._i)
		newVelocities = self.newVelocitiesCircles(*circles)
		
		for i, circle in enumerate(circles):
			circle.position = circle.currentPosition(self._nextCollisionTime)
			circle.velocity = newVelocities[i]
			circle.time = float(self._nextCollisionTime)

		for i in self._i:
			self.updateCircleWallEntry(i)
		
		self.circleCircle[self._i] = float("+inf")
		for pairIndex in itertools.chain(self.yieldPairsForIndex(*self._i), self.yieldPairsForIndex(*self._i[::-1])):
			self.updateCircleCircleEntry(pairIndex)
	
	def carryOutWallCollision(self):
		assert self._isPairOfCircles == False
		if self._i[1] in [0, 1]:
			component = 0
		else:
			component = 1
		circle = self.circles[self._i[0]]
		circle.position = circle.currentPosition(self._nextCollisionTime)
		circle.velocity[component] *= -1
		circle.time = float(self._nextCollisionTime)
		self.updateCircleWallEntry(self._i[0])
		self.circleWall[self._i] = float("+inf")

		for pairIndex in self.yieldPairsForIndex(*[self._i[0]]*2):
			self.updateCircleCircleEntry(pairIndex)

	#vim mark X set here. 
	def carryOutCollision(self):
		assert self.isWithinCurrentTimeslice(self._nextCollisionTime)
		if self._isPairOfCircles:
			self.carryOutCircleCollision()
		else:
			self.carryOutWallCollision()

	def animationStep(self):
		if self.isWithinCurrentTimeslice(self._nextCollisionTime):
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


	def animate(self):
		while True:
			queue = py.event.get()
			for event in queue:
				if event.type == py.QUIT:
					quit()
			screen.fill([0,0,0])
			[circle.plot(self.time) for circle in self.circles]
			py.display.update()
			self.animationStep()

