class Player:

	position = 1
	money = 1500
	properties = []
	isBankrupt = False
	inJail = False
	jailTurn = 0
	completedOneCircuit = False
	getOutOfJailFree = 0

	def __init__(self):
		pass

	def sendToJail(self):
		self.position = 11
		self.inJail = True
		self.jailTurn = 0

class Agent(Player):

	def __init__(self):
		pass