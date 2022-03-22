class Board:

    def __init__(self):
        self.tiles = []

    def addTile(self, tile):
        self.tiles.append(tile)

    def getTile(self, position):
        return self.tiles[position - 1]

    def printTiles(self):
        for tile in self.tiles:
            tile.printTile()

    def getGroup(self, group):
        groupTiles = []
        for tile in self.tiles:
            if tile.group == group:
                groupTiles.append(tile)
        return groupTiles

    def ownsColourGroupNoHouses(self, tile):
        for t in self.getGroup(tile.group):
            if t.houses > 0 or t.owner != tile.owner:
                return False
        return True

    def ownsNoOfStations(self, player):
        count = 0
        for station in self.getGroup("Station"):
            if station.owner == player:
                count += 1
        return count

    def ownsBothUtilities(self, player):
        u = self.getGroup("Utilities")
        return True if u[0].owner == u[1].owner else False