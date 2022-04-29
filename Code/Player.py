"""
The Player class hold all the information about a player within the game.
"""
class Player:

    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.position = 1
        self.money = 1500
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

    def __str__(self):
        return self.name

"""
In a complete game, there would be differences between how a human player and an autonomous
player agent would function. However, due to lack of personel and time these differences
were not achieved.
"""
class Human(Player):

    def __init__(self, name, token):
        super().__init__(name, token)

class Agent(Player):

    def __init__(self, name, token):
        super().__init__(name, token)

class Token:
    
    tokens = ["Boot", "Cat", "Hat Stand", "Iron", "Ship", "Smartphone"]

    def path(token):
        return f"Images/Tokens/{token}.png"

    def unusedTokens(usedTokens):
        return [token for token in Token.tokens if token not in usedTokens]