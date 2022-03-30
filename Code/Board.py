class Board:

    def __init__(self):
        self.tiles = []

    def addTile(self, tile):
        self.tiles.append(tile)

    def getTile(self, position):
        return self.tiles[position - 1]

    def getTileName(self, player):
        if player.position == 11:
            return "Jail" if player.inJail else "Just visiting"
        else:
            return self.getTile(player.position).name

    def printTiles(self):
        for tile in self.tiles:
            tile.printTile()

    def getGroup(self, group):
        groupTiles = []
        for tile in self.tiles:
            if tile.group == group:
                groupTiles.append(tile)
        return groupTiles

    def ownsColourGroup(self, tile):
        for t in self.getGroup(tile.group):
            if t.owner != tile.owner:
                return False
        return True

    def ownsColourGroupAndNoHouses(self, tile):
        for t in self.getGroup(tile.group):
            if t.houses > 0 or t.owner != tile.owner:
                return False
        return True

    def ownsXNoOfStations(self, player):
        count = 0
        for station in self.getGroup("Station"):
            if station.owner == player:
                count += 1
        return count

    def ownsBothUtilities(self, player):
        util = self.getGroup("Utilities")
        return True if util[0].owner == util[1].owner else False