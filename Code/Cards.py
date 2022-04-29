from random import shuffle

"""
The Cards class holds the packs of Pot Luck and Opportunity Knocks cards, and the methods.
that execute their instructions 
"""
class Cards:

    def __init__(self, cards):
        self.potLuck = PotLuck(cards[0])
        self.opportunityKnocks = OpportunityKnocks(cards[1])

    def takeCard(self, player, tile):
        if tile.name == "Pot Luck":
            fine = self.potLuck.takeCard(player)
        else:
            fine = self.opportunityKnocks.takeCard(player)
        return fine

    def returnFreeJailCard(self, player):
        if len(self.potLuck.names) != len(self.potLuck.order):
            self.potLuck.order.append(17)
        else:
            self.opportunityKnocks.order.append(16)
        player.getOutOfJailFree -= 1
    

class Pack:

    def __init__(self, cards):
        self.names = {}
        self.order = []
        for i, card in enumerate(cards):
            self.names[i + 1] = card
            self.order.append(i + 1)
        shuffle(self.order)
        self.freeJailOwner = None

    def takeCard(self, player):
        cardNo = self.order.pop(0)
        if cardNo != len(self.names):
            self.order.append(cardNo)
        fine = self.cardFunctions[cardNo](player)
        if fine:
            return fine, self.names[cardNo]
        else:
            return 0, self.names[cardNo]

class PotLuck(Pack):

    def __init__(self, cards):
        super().__init__(cards)
        self.cardFunctions = {1: self.card1, 2: self.card2, 3: self.card3, 4: self.card4,
                                5: self.card5, 6: self.card6, 7: self.card7, 8: self.card8,
                                9: self.card9, 10: self.card10, 11: self.card11, 12: self.card12,
                                13: self.card13, 14: self.card14, 15: self.card15, 16: self.card16,
                                17: self.card17}

    def card1(self, player):
        player.money += 200

    def card2(self, player):
        player.money += 50

    def card3(self, player):
        player.position = 2

    def card4(self, player):
        player.money += 20

    def card5(self, player):
        player.money += 200

    def card6(self, player):
        player.money -= 100

    def card7(self, player):
        player.money -= 50

    def card8(self, player):
        player.position = 1
        player.passGo()

    def card9(self, player):
        player.money += 50

    def card10(self, player):
        player.money -= 50

    def card11(self, player):
        if 1:
            player.money -= 10
            return 10
        else:
            pass # take oppertunity knocks

    def card12(self, player):
        player.money -= 50
        return 50

    def card13(self, player):
        player.money += 100

    def card14(self, player):
        player.sendToJail()

    def card15(self, player):
        player.money += 25

    def card16(self, player):
        player.money += 10 # * no of players

    def card17(self, player):
        player.getOutOfJailFree += 1
        self.freeJailOwner = player

class OpportunityKnocks(Pack):

    def __init__(self, cards):
        super().__init__(cards)
        self.cardFunctions = {1: self.card1, 2: self.card2, 3: self.card3,
                                4: self.card4, 5: self.card5, 6: self.card6,
                                7: self.card7, 8: self.card8, 9: self.card9,
                                10: self.card10, 11: self.card11, 12: self.card12,
                                13: self.card13, 14: self.card14, 15: self.card15,
                                16: self.card16, 16: self.card16}

    def card1(self, player):
        player.money += 50

    def card2(self, player):
        player.money += 100

    def card3(self, player):
        player.position = 40

    def card4(self, player):
        if player.position > 25:
            player.passGo()
        player.position = 25

    def card5(self, player):
        player.money -= 15
        return 15

    def card6(self, player):
        player.money -= 150

    def card7(self, player):
        if player.position > 16:
            player.passGo()
        player.position = 16

    def card8(self, player):
        player.money += 150

    def card9(self, player):
        pass # house/hotel card

    def card10(self, player):
        player.position = 1
        player.passGo()

    def card11(self, player):
        pass # house/hotel card

    def card12(self, player):
        player.position -= 3

    def card13(self, player):
        if player.position > 12:
            player.passGo()
        player.position = 12

    def card14(self, player):
        player.sendToJail()

    def card15(self, player):
        player.money -= 30
        return 30

    def card16(self, player):
        player.getOutOfJailFree += 1
        self.freeJailOwner = player