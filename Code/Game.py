import random
from Tile import *

class Game:

    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.currentDieRoll = 0
        self.freeParkingValue = 0
        currentPlayerNo = 0

        #self.board.tiles[6].owner = self.players[0]
        #self.board.tiles[8].owner = self.players[0]
        #self.board.tiles[9].owner = self.players[0]
        #self.board.tiles[11].owner = self.players[1]
        #self.board.tiles[13].owner = self.players[1]
        #self.board.tiles[14].owner = self.players[1]
        #self.board.tiles[14].houses = 1
        #self.board.tiles[5].owner = self.players[0]
        #self.board.tiles[25].owner = self.players[0]
        #self.board.tiles[12].owner = self.players[1]
        #self.board.tiles[28].owner = self.players[1]

        while True:
            currentPlayer = self.players[currentPlayerNo]
            if not currentPlayer.isBankrupt:
                if currentPlayer.inJail:
                    self.playJailTurn(currentPlayer)
                else:
                    self.playTurn(currentPlayer)
            currentPlayerNo = currentPlayerNo + 1 if currentPlayerNo < len(self.players) - 1 else 0

    def rollOrder(self):
        pass

    def playTurn(self, player):
        doubleCount = 0
        while True:
            die = Game.rollDie()
            dieTotal = self.currentDieRoll = die[0] + die[1]
            if die[0] == die[1]:
                doubleCount += 1
                if doubleCount == 3:
                    player.sendToJail()
                    print(f"Rolled {die[0]} + {die[1]} = {dieTotal}")
                    print(f"Player {self.players.index(player)} Position {player.position} ({self.board.getTile(player.position).name})")
                    input()
                    break

            player.position = Game.movePlayer(player, dieTotal)
            print(f"Rolled {die[0]} + {die[1]} = {dieTotal}")
            print(f"Player {self.players.index(player)} Position {player.position} ({self.board.getTile(player.position).name}) Cash: {player.money}")
            self.landedOn(player)
            input()
            if die[0] != die[1]:
                break

    def landedOn(self, player):
        tile = self.board.getTile(player.position)
        if hasattr(tile, "owner"):
            if tile.owner == None:
                pass#option to buy/auction
            elif tile.owner != player:
                self.payRent(player, tile)

    def payRent(self, player, tile):
        if isinstance(tile, Property):
            if self.board.ownsColourGroupNoHouses(tile):
                self.transferMoney(player, tile.owner, tile.rent[0]*2)
            else:
                self.transferMoney(player, tile.owner, tile.calculateRent())
        elif isinstance(tile, Station):
            self.transferMoney(player, tile.owner, tile.rent[self.board.ownsNoOfStations(tile.owner) - 1])
        elif isinstance(tile, Utility):
            if self.board.ownsBothUtilities(tile.owner):
                self.transferMoney(player, tile.owner, self.currentDieRoll*10)
            else:
                self.transferMoney(player, tile.owner, self.currentDieRoll*4)

    def transferMoney(self, p1, p2, amount):
        p1.money -= amount
        p2.money += amount
        print(f"{p1.name} paid {p2.name} £{amount}")

    def movePlayer(player, spaces):
        newPosition = player.position + spaces
        if newPosition > 40:
            newPosition -= 40
            player.passGo()
        return newPosition

    def playJailTurn(self, player):
        print(f"Player {self.players.index(player)} is in jail.")
        if player.jailTurn == 0:
            ans = input("Pay £50 to leave? ")
            if ans == "y":
                player.inJail = False
                player.money -= 50
                self.freeParkingValue += 50
            else:
                player.jailTurn += 1
        elif player.jailTurn == 1:
            player.jailTurn += 1
            input()
        else:
            player.inJail = False
            input()

    def rollDie():
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        return (a,b)
