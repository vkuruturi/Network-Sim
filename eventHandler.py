import globals

class EventHandler:
	def __init__(self):
		print 'globals time : ', globals.time
		globals.time = 0

	def getTime(self):
		return globals.time

	def setTime(self,t):
		globals.time = t