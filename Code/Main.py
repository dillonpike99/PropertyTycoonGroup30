from Parser import Parser
from Board import Board
from Game import Game
from Card import Cards
from Player import *
from Tile import *

class Main:

    def __init__(self):
        self.parser = Parser()
        self.board = Board()

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
        self.addTilesToBoard()
        cards = Cards(self.parser.getCards())
        players = [Player(i) for i in range(4)]
        Game(self.board, cards, players)


if __name__ == '__main__':
    main = Main()
    main.createGame()