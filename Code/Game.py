import random
from Tile import *

class Game:

    def __init__(self, board, cards, players):
        self.board = board
        self.cards = cards
        self.players = players
        self.currentDieRoll = 0
        self.freeParkingValue = 0
        currentPlayerNo = 0

    def movePlayer(player, spaces):
        newPosition = player.position + spaces
        if newPosition > 40:
            newPosition -= 40
            player.passGo()
        return newPosition

    def canBuy(self, player):
        tile = self.board.getTile(player.position)
        if hasattr(tile, "owner"):
            if tile.owner == None:
                return True
        return False

    def rentDue(self, player):
        tile = self.board.getTile(player.position)
        if hasattr(tile, "owner"):
            if tile.owner != player and not tile.mortgaged:
                return True
        return False

    def landedOnCard(self, player):
        tile = self.board.getTile(player.position)
        if tile.group == "Card":
            return True
        return False

    def calculateRent(self, player):
        tile = self.board.getTile(player.position)
        if isinstance(tile, Property):
            if self.board.ownsColourGroupAndNoHouses(tile):
                return tile.rent[0]*2
            else:
                return tile.calculateRent()
        elif isinstance(tile, Station):
            return tile.rent[self.board.ownsXNoOfStations(tile.owner) - 1]
        elif isinstance(tile, Utility):
            if self.board.ownsBothUtilities(tile.owner):
                return self.currentDieRoll*10
            else:
                return self.currentDieRoll*4

    def transferMoney(p1, p2, amount):
        if p1:
            p1.money -= amount
        if p2:
            p2.money += amount
        print(f"{p1.name} paid {p2.name} £{amount}")

    def collectFreeParking(self, player):
        player.money += self.freeParkingValue
        self.freeParkingValue = 0

    def payTax(self, player):
        amount = {5: 200, 39: 100}
        player.money -= amount[player.position]
        self.freeParkingValue += amount[player.position]
        return amount[player.position]

    def eligableAuctionPlayers(self, currentPlayer):
        auctionPlayers = []
        for player in self.players:
            if player.completedOneCircuit and player is not currentPlayer:
                auctionPlayers.append(player)
        return auctionPlayers
