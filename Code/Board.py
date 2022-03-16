class Board:

    tiles = []

    def addTile(self, tile):
        self.tiles.append(tile)

    def getTile(self, position):
        return self.tiles[position - 1]

    def printTiles(self):
        for tile in self.tiles:
            tile.printTile()