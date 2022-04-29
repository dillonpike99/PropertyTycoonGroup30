import random
from Tile import *

"""
The Game class hold all the information for a game of Property Tycoon, from the list
of tiles on the board, cards in Pot Luck/Oppertunity knocks, and the players in the
game. This information is seperated into their own seperate classes and stored here.
"""
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

    def calculateAssets(self, player):
        total = player.money
        for p in self.board.ownedTiles(player):
            total += p.cost
            if hasattr(p, "houses"):
                total += p.houses*Property.houseCost[p.group]
        for p in self.board.mortgagedProperties(player):
            total += p.cost//2
        return total

    def declareBankrupcy(self, player):
        for p in self.board.ownedTiles(player):
            player.money += p.cost
            if hasattr(p, "houses"):
                player.money += p.houses*Property.houseCost[p.group]
                p.houses = 0
            p.owner = None
        for p in self.board.mortgagedProperties(player):
            player.money += p.cost//2
            p.owner = None
        player.isBankrupt = True
            

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
