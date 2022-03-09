class Tile:

    def __init__(self, pos, name, group, cbb):
        self.position = pos
        self.name = name
        self.group = group
        self.canBeBought = True if cbb == "Yes" else False

    def printTile(self):
        print(self.position, self.name, self.group)

class Property(Tile):

    houses = 0
    owner = None
    
    def __init__(self, pos, name, group, cbb, cost, r0, r1, r2, r3, r4, r5):
        super().__init__(pos, name, group, cbb)
        self.cost = cost
        self.rent = [r0, r1, r2, r3, r4, r5]

    def printTile(self):
        print(self.position, self.name, self.group, self.cost, self.rent)

    def addHouse(self):
        if self.houses < 5:
            self.houses += 1

    def removeHouse(self):
        if self.houses > 0:
            self.houses -= 1

class Station(Tile):

    owner = None
    
    def __init__(self, pos, name, group, cbb, cost):
        super().__init__(pos, name, group, cbb)
        self.cost = cost

    def printTile(self):
        print(self.position, self.name, self.group, self.cost)

class Utility(Tile):

    owner = None

    def __init__(self, pos, name, group, cbb, cost):
        super().__init__(pos, name, group, cbb)
        self.cost = cost

    def printTile(self):
        print(self.position, self.name, self.group, self.cost)