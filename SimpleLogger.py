import ABCLogger
class SimpleLogger(ABCLogger.ABCLogger):
	def writeHeader(self):
		return "the value of simpleClass.logThis"
	def log(self, foreignInstance):
		return foreignInstance.logThis 

class SimpleClass:
	def __init__(self):
		self.logThis = "I want to be logged"
	@SimpleLogger("log")
	def doFunnyThingsWithAttribute(self):
		self.logThis = self.logThis + " " + "NOT!"

simpleInstance = SimpleClass()
simpleInstance.doFunnyThingsWithAttribute()
simpleInstance.doFunnyThingsWithAttribute()
simpleInstance.doFunnyThingsWithAttribute()
simpleInstance.doFunnyThingsWithAttribute()
simpleInstance.doFunnyThingsWithAttribute()
simpleInstance.doFunnyThingsWithAttribute()


