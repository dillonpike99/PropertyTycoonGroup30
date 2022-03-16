from Parser import Parser
from Board import Board
from Game import Game
from Player import Player
from Tile import *

class Main:

    board = Board()
    parser = Parser()

    def __init__(self):
        pass

    def addTilesToBoard(self):
        tiles = self.parser.getTiles()
        for tile in tiles:
            if len(tile) == 4:
                self.board.addTile(Tile(*tile))
            else:
                if tile[2] == "Station":
                    self.board.addTile(Station(*tile))
                elif tile[2] == "Utilities":
                    self.board.addTile(Utility(*tile))
                else:
                    self.board.addTile(Property(*tile))
        #self.board.printTiles()

    def createGame(self):
        players = []
        for i in range(2):
            players.append(Player())
        Game(self.board, players)


if __name__ == '__main__':
    main = Main()
    main.addTilesToBoard()
    main.createGame()