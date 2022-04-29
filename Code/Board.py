from Tile import *

"""
The Board class holds the list of tiles on the board, and has many methods for retriving
informtion about them and the player's ownership of them.
"""
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

    def getGroup(self, group):
        groupTiles = []
        for tile in self.tiles:
            if tile.group == group:
                groupTiles.append(tile)
        return groupTiles

    def ownsColourGroup(self, tile):
        for t in self.getGroup(tile.group):
            if t.owner != tile.owner or tile.mortgaged:
                return False
        return True

    def canAddHouse(self, tile):
        for t in self.getGroup(tile.group):
            if abs(tile.houses + 1 - t.houses) > 1 or tile.houses == 5:
                return False
        return True

    def canRemoveHouse(self, tile):
        for t in self.getGroup(tile.group):
            if abs(tile.houses - 1 - t.houses) > 1 or tile.houses == 0:
                return False
        return True

    def houseInGroup(self, tile):
        for t in self.getGroup(tile.group):
            if t.houses > 0:
                return True
        return False

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

    def ownedTiles(self, player):
        properties = []
        for tile in self.tiles:
            if hasattr(tile, "owner"):
                if tile.owner is player and not tile.mortgaged:
                    properties.append(tile)
        return properties

    def ownedProperties(self, player):
        properties = []
        for tile in self.tiles:
            if isinstance(tile, Property):
                if tile.owner is player and not tile.mortgaged:
                    properties.append(tile)
        return properties

    def mortgagedProperties(self, player):
        properties = []
        for tile in self.tiles:
            if hasattr(tile, "owner"):
                if tile.owner is player and tile.mortgaged:
                    properties.append(tile)
        return properties

    def playerPositions(self, players):
        positions = {}
        for player in players:
            if player.position not in positions:
                positions[player.position] = []
            positions[player.position].append(player)
        return positions