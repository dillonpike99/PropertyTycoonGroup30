class Tile:

    def __init__(self, pos, name, group, cbb):
        self.position = pos
        self.name = name
        self.group = group
        self.canBeBought = True if cbb == "Yes" else False

    def printTile(self):
        print(self.position, self.name, self.group)

class Property(Tile):

    houseCost = {"Brown": 50, "Blue": 50, "Purple": 100, "Orange": 100,
                 "Red": 150, "Yellow": 150, "Green": 200, "Deep blue": 200}

    def __init__(self, pos, name, group, cbb, cost, r0, r1, r2, r3, r4, r5):
        super().__init__(pos, name, group, cbb)
        self.cost = cost
        self.rent = [r0, r1, r2, r3, r4, r5]
        self.houses = 0
        self.owner = None
        self.mortgaged = False

    def printTile(self):
        print(self.position, self.name, self.group, self.cost, self.rent)

    def calculateRent(self):
        return self.rent[self.houses]

    def addHouse(self):
        if self.houses < 5:
            self.houses += 1

    def removeHouse(self):
        if self.houses > 0:
            self.houses -= 1

class Station(Tile):

    rent = [25, 50, 100, 200]

    def __init__(self, pos, name, group, cbb, cost):
        super().__init__(pos, name, group, cbb)
        self.cost = cost
        self.owner = None
        self.mortgaged = False

    def printTile(self):
        print(self.position, self.name, self.group, self.cost)

class Utility(Tile):

    def __init__(self, pos, name, group, cbb, cost):
        super().__init__(pos, name, group, cbb)
        self.cost = cost
        self.owner = None
        self.mortgaged = False

    def printTile(self):
        print(self.position, self.name, self.group, self.cost)