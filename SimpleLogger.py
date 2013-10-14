import ABCLogger
class SimpleLogger(ABCLogger.ABCLogger):
	def writeHeader(self):
		return "the value of simpleClass.logThis"
	def log(self, foreignInstance):
		return str(foreignInstance.logThis) + " " + str(foreignInstance.logThat) 

class SimpleClass:
	def __init__(self):
		self.logThis = "I want to be logged"
		self.logThat = "fuck off"
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


