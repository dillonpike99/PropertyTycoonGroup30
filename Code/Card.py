class Cards:
    potLuck = []
    opportunityKnocks = []


class Card:
    typesOfAction = ["Pay", "Receive", "Move", "Jail", "JailFree"]


class PotLuck:

    def card1(player):
        player.money += 200

    def card2(player):
        player.money += 50

    def card3(player):
        player.position = 1

    def card4(player):
        player.money += 20

    def card5(player):
        player.money += 200

    def card6(player):
        player.money -= 100

    def card7(player):
        player.money -= 50

    def card8(player):
        player.position = 0
        player.passGo()

    def card9(player):
        player.money += 50

    def card10(player):
        player.money -= 50

    def card11(player):
        if 1:
            player.money -= 10
        else:
            pass # take oppertunity knocks

    def card12(player):
        player.money -= 50

    def card13(player):
        player.money += 100

    def card14(player):
        player.sendToJail()

    def card15(player):
        player.money += 25

    def card16(player):
        player.money += 10 # * no of players

    def card17(player):
        player.getOutOfJailFree += 1

class OpportunityKnocks:

    def card1(player):
        player.money += 50

    def card2(player):
        player.money += 100

    def card3(player):
        player.position = 39

    def card4(player):
        if player.position > 24:
            player.passGo()
        player.position = 24

    def card5(player):
        player.money -= 15

    def card6(player):
        player.money -= 150

    def card7(player):
        if player.position > 15:
            player.passGo()
        player.position = 15

    def card8(player):
        player.money += 150

    def card9(player):
        # house/hotel card

    def card10(player):
        player.position = 0
        player.passGo()

    def card11(player):
        # house/hotel card

    def card12(player):
        player.position -= 3

    def card13(player):
        if player.position > 11:
            player.passGo()
        player.position = 11

    def card14(player):
        player.sendToJail()

    def card15(player):
        player.money -= 30

    def card16(player):
        player.getOutOfJailFree += 1