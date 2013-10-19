import ABCLogger
class SimpleLogger(ABCLogger.ABCLogger):
	def writeHeader(self):
		return "the value of simpleClass.logThis"
	def log(self, foreignInstance):
		return str(foreignInstance.logThis) + " " + str(foreignInstance.logThat) 
		
class SimpleClass:
	def __init__(self):
		self.logThis = "I want to be logged"
		self.logThat = "something else"
	def doFunnyThingsWithAttribute(self, append):
		self.logThis = self.logThis + " " + append

simpleLogger = SimpleLogger("log")
simpleInstance = SimpleClass()
simpleLogger.hook(simpleInstance.doFunnyThingsWithAttribute) 
#print simpleInstance.__dict__
simpleInstance.doFunnyThingsWithAttribute("1")
simpleInstance.doFunnyThingsWithAttribute("3")
simpleInstance.doFunnyThingsWithAttribute("4")
simpleInstance.doFunnyThingsWithAttribute("aaa")

