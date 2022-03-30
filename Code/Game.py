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
                input()
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
                    print(f"{player.name} Position {player.position} ({self.board.getTileName(player)})")
                    break

            player.position = Game.movePlayer(player, dieTotal)
            print(f"{player.name} Rolled {die[0]} + {die[1]} = {dieTotal}, landing on {self.board.getTileName(player)} ({player.position})")
            self.landedOnAction(player)
            print(f"Position {player.position} ({self.board.getTileName(player)}) Cash: {player.money}")
            
            if die[0] != die[1] or player.inJail:
                break # Player's turn only continues if they throw a double and haven't been sent to jail.

    def movePlayer(player, spaces):
        newPosition = player.position + spaces
        if newPosition > 40:
            newPosition -= 40
            player.passGo()
        return newPosition

    def landedOnAction(self, player):
        tile = self.board.getTile(player.position)
        if hasattr(tile, "owner"):
            if tile.owner == None:
                pass#option to buy/auction
            elif tile.owner != player:
                self.payRent(player, tile)
        elif tile.group == "Tax":
            self.payTax(player)
        elif tile.group == "Card":
            fine = self.cards.takeCard(player, tile)
            self.freeParkingValue += fine
        elif tile.name == "Free Parking":
            player.money += self.freeParkingValue
            self.freeParkingValue = 0
        elif tile.name == "Go to Jail":
            player.sendToJail()

    def payRent(self, player, tile):
        if isinstance(tile, Property):
            if self.board.ownsColourGroupAndNoHouses(tile):
                Game.transferMoney(player, tile.owner, tile.rent[0]*2)
            else:
                Game.transferMoney(player, tile.owner, tile.calculateRent())
        elif isinstance(tile, Station):
            Game.transferMoney(player, tile.owner, tile.rent[self.board.ownsXNoOfStations(tile.owner) - 1])
        elif isinstance(tile, Utility):
            if self.board.ownsBothUtilities(tile.owner):
                Game.transferMoney(player, tile.owner, self.currentDieRoll*10)
            else:
                Game.transferMoney(player, tile.owner, self.currentDieRoll*4)

    def transferMoney(p1, p2, amount):
        if p1:
            p1.money -= amount
        if p2:
            p2.money += amount
        print(f"{p1.name} paid {p2.name} £{amount}")

    def payTax(self, player):
        amount = {5: 200, 39: 100}
        player.money -= amount[player.position]
        self.freeParkingValue += amount[player.position]

    def playJailTurn(self, player):
        print(f"{player.name} is in jail.")
        if player.jailTurn == 0:
            if player.getOutOfJailFree > 0:
                ans = input("Use get out of jail free card?")
                if ans == "y":
                    player.inJail = False
                    self.cards.returnJailFreeCard(player)
                else:
                    player.jailTurn += 1
            else:
                ans = input("Pay £50 to leave? ")
                if ans == "y":
                    player.inJail = False
                    player.money -= 50
                    self.freeParkingValue += 50
                else:
                    player.jailTurn += 1
        elif player.jailTurn == 1:
            player.jailTurn += 1
        else:
            player.inJail = False

    def rollDie():
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        return (a,b)
