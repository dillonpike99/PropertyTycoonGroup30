class Board:

    tiles = []

    def addTile(self, tile):
        self.tiles.append(tile)

    def printTiles(self):
        for tile in self.tiles:
            tile.printTile()