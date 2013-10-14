import os
class ABCLogger(object):
	"""
	Please mind that only one logger can operate on a given file. Anytime a new logger is created to operate on file already being logged to a class method __new__ returns an old logger. Along with the class being a callable decorator, this is a perfectly valid use (let's assume SimpleLogger to be a properly defined subclass of ABCLogger):
	class SomeClass:
		...
		@SimpleLogger(logFilename)
		def someMethod(self, arguments, keywordargs = foo):
			print "when you decorate me I'll log properly!"
		...
	For a class to be properly subclussed it is sufficient to override two methods writeHeader(self) and log(self, foreignInstance)
	"""
	def writeHeader(self):
		pass #overrideme
	def log(self, foreignInstance):
		pass #overrideme

	def decorate(myself, foreignMethod):
		def augumentedMethod(foreignSelf, *args, **kwargs):
			with myself as me:
				me.logfile.write(me.log(foreignSelf) + "\n")
			return foreignMethod(foreignSelf, *args, **kwargs)
		return augumentedMethod

	instances = {}
	def __new__(cls, filename, *args, **kwargs):
		if filename not in ABCLogger.instances:
			if os.path.isfile(filename):
				os.remove(filename)
			new_instance = object.__new__(cls, filename, *args, **kwargs)
			ABCLogger.instances[filename] = new_instance
			new_instance.logfileName = filename
			with new_instance as self:
				self.logfile.write(self.writeHeader() + "\n")
			return new_instance
		else:
			return instances[filename]
	def __init__(self, *args, **kwargs):
		pass
	def __enter__(self):
		self.logfile = open(self.logfileName, "a+")
		return self
	def __exit__(self, exc_type, exc_value, traceback):
		self.logfile.close()
	def __call__(self, method):
		return self.decorate(method)

