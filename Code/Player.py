class Player:

    def __init__(self, n):
        self.name = "Player" + str(n + 1)
        self.position = 1
        self.money = 1500
        self.properties = []
        self.isBankrupt = False
        self.inJail = False
        self.jailTurn = 0
        self.completedOneCircuit = False
        self.getOutOfJailFree = 0

    def passGo(self):
        self.money += 200
        if not self.completedOneCircuit:
            self.completedOneCircuit = True

    def sendToJail(self):
        self.position = 11
        self.inJail = True
        self.jailTurn = 0

class Agent(Player):

    def __init__(self):
        pass

class Token:
    pass