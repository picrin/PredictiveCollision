import math
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
