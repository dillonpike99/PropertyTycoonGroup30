import random

class Game:

    currentDieRoll = 0
    freeParkingValue = 0

    def __init__(self, board, players):
        self.board = board
        self.players = players
        currentPlayerNo = 0
        while True:
            currentPlayer = self.players[currentPlayerNo]
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
            dieTotal = die[0] + die[1]
            if die[0] == die[1]:
                doubleCount += 1
                if doubleCount == 3:
                    player.sendToJail()
                    print(f"Rolled {die[0]} + {die[1]} = {dieTotal}")
                    print(f"Player {self.players.index(player) + 1} Position {player.position} ({self.board.getTile(player.position).name})")
                    input()
                    break

            player.position += dieTotal
            print(f"Rolled {die[0]} + {die[1]} = {dieTotal}")
            print(f"Player {self.players.index(player) + 1} Position {player.position} ({self.board.getTile(player.position).name})")
            input()
            if die[0] != die[1]:
                break

    def playJailTurn(self, player):
        print(f"Player {self.players.index(player) + 1} is in jail.")
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
