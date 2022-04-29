import sys, pygame, glob, os, random
from Parser import Parser
from Board import Board
from Game import Game
from Cards import Cards
from Player import *
from Tile import *

class Display:

    def __init__(self, board, cards):

        self.board = board
        self.cards = cards

        pygame.init()
        self.clock = pygame.time.Clock()
        size = width, height = 1920,1080
        self.display = pygame.display
        self.display.set_caption("Property Tycoon")
        self.screen = self.display.set_mode(size)
        #self.screen = self.display.set_mode(size, pygame.FULLSCREEN)

        self.mainMenu()

    def mainMenu(self):
        playImg = pygame.image.load("Images/Buttons/Play_Button.png").convert_alpha()
        exitImg = pygame.image.load("Images/Buttons/Exit_Button.png").convert_alpha()
        playButton = Button(500, 600, playImg, 1)
        exitButton = Button(1000, 600, exitImg, 1)

        running = True
        while running:

            self.screen.fill(Colour.white)
            playRect = playButton.draw(self.screen)
            exitRect = exitButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Display.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if playRect.collidepoint(pos):
                        self.selectPlayers()
                    elif exitRect.collidepoint(pos):
                        Display.quitGame()

            self.update()

    def selectPlayers(self):
        names = ["Computer 1", "Human 1"]
        tokens = ["Smartphone", "Boot"]
        noOfAgents = 1
        noOfHumans = 1

        nameFont = pygame.font.SysFont("myriadpro", 45)
        editNameImg = pygame.image.load("Images/Buttons/EditName_Button.png").convert_alpha()
        editTokenImg = pygame.image.load("Images/Buttons/EditToken_Button.png").convert_alpha()
        plusHumanImg = pygame.image.load("Images/Buttons/PlusHuman_Button.png").convert_alpha()
        plusComputerImg = pygame.image.load("Images/Buttons/PlusComputer_Button.png").convert_alpha()
        minusImg = pygame.image.load("Images/Buttons/Minus_Button.png").convert_alpha()
        playImg = pygame.image.load("Images/Buttons/Play_Button.png").convert_alpha()

        running = True
        while running:
            self.screen.fill(Colour.white)

            noOfPlayers = noOfAgents + noOfHumans
            editNameButtons = []
            editNameRects = []
            editTokenButtons = []
            editTokenRects = []
            minusButtons = [None, None]
            minusRects = [None, None]

            y = 200
            for i in range(noOfPlayers):
                pygame.draw.rect(self.screen, Colour.black, pygame.Rect((400, y), (500, 70)), 2)
                self.screen.blit(nameFont.render(names[i], True, Colour.black), (430, y+20))
                tokenImg = pygame.image.load(Token.path(tokens[i])).convert_alpha()
                tokenImg = pygame.transform.scale(tokenImg, (70, 70))
                self.screen.blit(tokenImg, (830, y))
                if "Computer" in names[i]:
                    editTokenButtons.append(Button(930, y, editTokenImg, 1))
                    editTokenRects.append(editTokenButtons[i].draw(self.screen))
                    editNameButtons.append(None)
                    editNameRects.append(None)
                else:
                    editTokenButtons.append(Button(930, y, editTokenImg, 1))
                    editTokenRects.append(editTokenButtons[i].draw(self.screen))
                    editNameButtons.append(Button(1160, y, editNameImg, 1))
                    editNameRects.append(editNameButtons[i].draw(self.screen))
                if i > 1:
                    minusButtons.append(Button(1390, y, minusImg, 1))
                    minusRects.append(minusButtons[i].draw(self.screen))

                y += 100
            
            if noOfPlayers < 6:
                plusHumanButton = Button(400, 200+(100*noOfPlayers), plusHumanImg, 1)
                plusComuterButton = Button(650, 200+(100*noOfPlayers), plusComputerImg, 1)
                plusHumanRect = plusHumanButton.draw(self.screen)
                plusComputerRect = plusComuterButton.draw(self.screen)
            else:
                plusHumanRect = plusComputerRect = pygame.Rect((0, 0), (0, 0))

            playButton = Button(1650, 910, playImg, 1)
            playRect = playButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(editTokenRects):
                        if rect.collidepoint(pos):
                            tokens[i] = self.editPlayerToken(tokens[i], tokens)
                    for i, rect in enumerate(editNameRects):
                        if rect:
                            if rect.collidepoint(pos):
                                names[i] = self.editPlayerName(names[i])
                    for i, rect in enumerate(minusRects):
                        if rect:
                            if rect.collidepoint(pos):
                                if "Computer" in names[i]:
                                    noOfAgents -= 1
                                else:
                                    noOfHumans -= 1
                                del names[i]
                                del tokens[i]
                    if plusHumanRect.collidepoint(pos):
                        noOfHumans += 1
                        names.append(f"Human {noOfHumans}")
                        tokens.append(Token.unusedTokens(tokens)[0])
                    elif plusComputerRect.collidepoint(pos):
                        noOfAgents += 1
                        names.append(f"Computer {noOfAgents}")
                        tokens.append(Token.unusedTokens(tokens)[0])
                    elif playRect.collidepoint(pos):
                        players = []
                        for name, token in zip(names, tokens):
                            if "Human" in name:
                                players.append(Human(name, token))
                            else:
                                players.append(Agent(name, token))
                        self.game(players)
                        running = False


            self.update()

    def editPlayerName(self, name):
        newName = name
        nameFont = pygame.font.SysFont("myriadpro", 45)

        cancelImg = pygame.image.load("Images/Buttons/Cancel_Button.png").convert_alpha()
        confirmImg = pygame.image.load("Images/Buttons/Confirm_Button.png").convert_alpha()
        cancelButton = Button(400, 530, cancelImg, 1)
        confirmButton = Button(700, 530, confirmImg, 1)

        running = True
        while running:
            self.screen.fill(Colour.white)

            pygame.draw.rect(self.screen, Colour.black, pygame.Rect((400, 400), (500, 70)), 2)
            self.screen.blit(nameFont.render(newName, True, Colour.black), (430, 420))

            cancelRect = cancelButton.draw(self.screen)
            confirmRect = confirmButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return name
                    elif event.key == pygame.K_RETURN:
                        return newName
                    elif event.key == pygame.K_BACKSPACE:
                        newName = newName[:-1]
                    elif len(newName) < 20:
                        newName += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if cancelRect.collidepoint(pos):
                        return name
                    elif confirmRect.collidepoint(pos):
                        return newName

            self.update()

    def editPlayerToken(self, currentToken, tokens):
        unusedTokens = [currentToken] + Token.unusedTokens(tokens)
        cancelImg = pygame.image.load("Images/Buttons/Cancel_Button.png").convert_alpha()
        cancelButton = Button(400, 550, cancelImg, 1)

        running = True
        while running:
            self.screen.fill(Colour.white)

            tokenRects = []
            x = 400
            for token in unusedTokens:
                tokenImg = pygame.image.load(Token.path(token)).convert_alpha()
                tokenRect = tokenImg.get_rect()
                tokenRect.topleft = (x, 300)
                tokenRects.append(tokenRect)
                self.screen.blit(tokenImg, (x, 300))
                x += 200

            cancelRect = cancelButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return currentToken
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(tokenRects):
                        if rect.collidepoint(pos):
                            return unusedTokens[i]
                    if cancelRect.collidepoint(pos):
                        return currentToken

            self.update()


    def game(self, players):
        self.game = Game(self.board, self.cards, players)
        titleFont = pygame.font.SysFont("myriadpro", 60)
        self.dieOne = 6
        self.dieTwo = 6
        rolled = False
        doubleCount = 0
        self.currentPlayerNo = 0

        rollButtonImg = pygame.image.load("Images/Buttons/Roll_Button.png").convert_alpha()
        buyHouseButtonImg = pygame.image.load("Images/Buttons/BuyHouse_Button.png").convert_alpha()
        sellHouseButtonImg = pygame.image.load("Images/Buttons/SellHouse_Button.png").convert_alpha()
        sellPropertyButtonImg = pygame.image.load("Images/Buttons/SellProperty_Button.png").convert_alpha()
        morgagePropertyButtonImg = pygame.image.load("Images/Buttons/MorgageProperty_Button.png").convert_alpha()
        repayMorgageButtonImg = pygame.image.load("Images/Buttons/RepayMorgage_Button.png").convert_alpha()
        endTurnButtonImg = pygame.image.load("Images/Buttons/EndTurn_Button.png").convert_alpha()
        rollButton = Button(1330, 275, rollButtonImg, 1)
        buyHouseButton = Button(1100, 425, buyHouseButtonImg, 1)
        sellHouseButton = Button(1350, 425, sellHouseButtonImg, 1)
        repayMorgageButton = Button(1600, 425, repayMorgageButtonImg, 1)
        morgagePropertyButton = Button(1100, 550, morgagePropertyButtonImg, 1)
        sellPropertyButton = Button(1350, 550, sellPropertyButtonImg, 1)
        endTurnButton = Button(1600, 550, endTurnButtonImg, 1)

        self.game.board.tiles[6].owner = self.game.players[0]
        self.game.board.tiles[8].owner = self.game.players[0]
        self.game.board.tiles[9].owner = self.game.players[0]
        self.game.board.tiles[11].owner = self.game.players[1]

        running = True
        while running:
            player = self.game.players[self.currentPlayerNo]
            self.screen.fill(Colour.white)
            self.drawBoard()
            self.displayPlayersOnBoard()
            playerInfoRects = self.displayPlayersInfo()
            self.screen.blit(titleFont.render(f"{self.game.players[self.currentPlayerNo]}'s turn", True, Colour.black), (1050, 50))
            self.screen.blit(pygame.image.load(f"Images/Dice/{self.dieOne}.png").convert_alpha(), (1300, 150))
            self.screen.blit(pygame.image.load(f"Images/Dice/{self.dieTwo}.png").convert_alpha(), (1430, 150))
            rollRect = rollButton.draw(self.screen)
            buyHouseRect = buyHouseButton.draw(self.screen)
            sellHouseRect = sellHouseButton.draw(self.screen)
            morgagePropertyRect = morgagePropertyButton.draw(self.screen)
            repayMorgageRect = repayMorgageButton.draw(self.screen)
            sellPropertyRect = sellPropertyButton.draw(self.screen)
            endTurnRect = endTurnButton.draw(self.screen)

            if player.inJail:
                if player.jailTurn == 3:
                    player.inJail = False
                    player.money -= 50
                    self.game.freeParkingValue += 50
                else:
                    self.jailPopUp()
                    rolled = True

            for i, tileRect in enumerate(self.tileRects):
                if tileRect.collidepoint(pygame.mouse.get_pos()):
                    self.displayTileInfo(i)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, playerInfoRect in enumerate(playerInfoRects):
                        if playerInfoRect.collidepoint(pos):
                            pass
                    if rollRect.collidepoint(pos):
                        if not rolled:
                            self.rollDie()
                            self.game.currentDieRoll = self.dieOne + self.dieTwo
                            if self.dieOne == self.dieTwo:
                                doubleCount += 1
                                if doubleCount == 3:
                                    self.popUp(f"Three doubles! Go to jail.")
                                    player.sendToJail()
                                    rolled = True
                            else:
                                rolled = True
                            player.position = Game.movePlayer(player, self.game.currentDieRoll)
                            if self.game.canBuy(player):
                                tile = self.game.board.getTile(player.position)
                                if player.completedOneCircuit:
                                    self.displayTileInfo(player.position-1)
                                    if player.money >= tile.cost:
                                        self.buyPopUp(tile)
                                    else:
                                        self.popUp(f"You don't have enough money to buy this property!")
                            elif self.game.rentDue(player):
                                rent = self.game.calculateRent(player)
                                owner = self.game.board.getTile(player.position).owner
                                self.displayTileInfo(player.position-1)
                                self.popUp(f"Pay ${rent} to {owner}.")
                                Game.transferMoney(player, owner, rent)
                            elif player.position in [5, 39]:
                                self.popUp(f"Pay ${self.game.payTax(player)} in taxes.")
                            elif player.position == 21:
                                self.popUp(f"Receive ${self.game.freeParkingValue} from free parking!")
                                self.game.collectFreeParking(player)
                            elif player.position == 31:
                                self.popUp(f"Go to jail.")
                                player.sendToJail()
                                rolled = True
                            elif self.game.landedOnCard(player):
                                fine, message = self.game.cards.takeCard(player, self.game.board.getTile(player.position))
                                self.popUp(message)
                                self.game.freeParkingValue += fine
                                if player.inJail:
                                    rolled = True
                    if endTurnRect.collidepoint(pos):
                        if rolled:
                            self.currentPlayerNo = self.currentPlayerNo + 1 if self.currentPlayerNo < len(self.game.players) - 1 else 0
                            rolled = False
                            doubleCount = 0
                        else:
                            self.popUp("You must roll first!")
                    elif buyHouseRect.collidepoint(pos):
                        if rolled:
                            pass
                        else:
                            self.popUp("You must roll first!")
                    elif sellHouseRect.collidepoint(pos):
                        if rolled:
                            pass
                        else:
                            self.popUp("You must roll first!")
                    elif morgagePropertyRect.collidepoint(pos):
                        if rolled:
                            properties = self.game.board.ownedProperties(player)
                            if properties:
                                tile = self.chooseProprety(properties)
                                if tile:
                                    tile.mortgaged = True
                                    player.money += tile.cost//2
                            else:
                                self.popUp("You have no properties!")

                        else:
                            self.popUp("You must roll first!")
                    elif repayMorgageRect.collidepoint(pos):
                        if rolled:
                            properties = self.game.board.mortgagedProperties(player)
                            if properties:
                                tile = self.chooseProprety(properties)
                                if tile:
                                    if player.money >= tile.cost//2:
                                        tile.mortgaged = False
                                        player.money -= tile.cost//2
                                    else:
                                        self.popUp("You don't have enough money!")
                            else:
                                self.popUp("You have no mortgaged properties!")
                    elif sellPropertyRect.collidepoint(pos):
                        if rolled:
                            pass
                        else:
                            self.popUp("You must roll first!")

            self.update()

    def rollDie(self):
        for i in range(10):
            a = random.randint(1, 6)
            b = random.randint(1, 6)
            self.screen.blit(pygame.image.load(f"Images/Dice/{a}.png").convert_alpha(), (1300, 150))
            self.screen.blit(pygame.image.load(f"Images/Dice/{b}.png").convert_alpha(), (1430, 150))
            self.update()
            pygame.time.wait(100)
        self.dieOne = a
        self.dieTwo = b

    def drawBoard(self):
        self.screen.fill(Colour.white)
        boardBoarder = pygame.Rect((80, 75), (915, 915))
        pygame.draw.rect(self.screen, Colour.black, boardBoarder, 2)

        tileFiles = sorted(os.listdir("Images/Tiles"))
        tileImages = []
        for tile in tileFiles:
            tileImages.append(pygame.image.load(os.path.join("Images/Tiles", tile)).convert_alpha())
        self.tileRects = []

        x = 950
        y = 870
        switcher = 0
        turn = 0
        for tile in tileImages:
            if switcher in [11, 21, 31]:
                turn -= 90
            if switcher in [10, 20, 21 ,31]:
                if turn == 0:
                    x -= 120
                elif turn == -90:
                    y -= 120
                elif turn == -180:
                    x += 120
                elif turn == -270:
                    y += 120
            else:
                if turn == 0:
                    x -= 75
                elif turn == -90:
                    y -= 75
                elif turn == -180:
                    x += 75
                elif turn == -270:
                    y += 75
            tile = pygame.transform.rotozoom(tile, turn, 0.5)
            tileRect = tile.get_rect()
            tileRect.topleft = (x, y)
            self.tileRects.append(tileRect)
            
            self.screen.blit(tile, (x, y))
            switcher += 1

    def displayPlayersOnBoard(self):
        positions = self.game.board.playerPositions(self.game.players)
        if 1 in positions:
            x, y = self.tileRects[0].bottomleft
            for i, player in enumerate(positions[1]):
                self.displayToken(player.token, x, y)
                if i == 2:
                    x += 40
                    y -= 40
                elif i > 2:
                    y -= 40
                else:
                    x += 40
        for i in range(2, 11):
            if i in positions:
                x, y = self.tileRects[i-1].bottomleft
                for i, player in enumerate(positions[i]):
                    self.displayToken(player.token, x, y)
                    if i in [1, 3]:
                        x -= 35
                        y += 35
                    else:
                        x += 35
        if 11 in positions:
            notInJail = [player for player in positions[11] if not player.inJail]
            inJail = [player for player in positions[11] if player.inJail]
            x, y = self.tileRects[10].topleft
            x -= 40
            for i, player in enumerate(notInJail):
                self.displayToken(player.token, x, y)
                if i == 2:
                    x += 40
                    y += 40
                elif i > 2:
                    x += 40
                else:
                    y += 40
            x, y = self.tileRects[10].topright
            x -= 90
            y += 15
            for i, player in enumerate(inJail):
                self.displayToken(player.token, x, y)
                if i in [1, 3]:
                    x -= 35
                    y += 35
                else:
                    x += 35
        for i in range(12, 21):
            if i in positions:
                x, y = self.tileRects[i-1].topleft
                x -= 40
                for i, player in enumerate(positions[i]):
                    self.displayToken(player.token, x, y)
                    if i in [1, 3]:
                        y -= 35
                        x -= 35
                    else:
                        y += 35
        if 21 in positions:
            x, y = self.tileRects[20].topright
            y -= 40
            x -= 40
            for i, player in enumerate(positions[21]):
                self.displayToken(player.token, x, y)
                if i == 2:
                    x -= 40
                    y += 40
                elif i > 2:
                    y += 40
                else:
                    x -= 40
        for i in range(22, 31):
            if i in positions:
                x, y = self.tileRects[i-1].topright
                y -= 40
                x -= 40
                for i, player in enumerate(positions[i]):
                    self.displayToken(player.token, x, y)
                    if i in [1, 3]:
                        x += 35
                        y -= 35
                    else:
                        x -= 35
        if 31 in positions:
            x, y = self.tileRects[30].bottomright
            y -= 40
            for i, player in enumerate(positions[31]):
                self.displayToken(player.token, x, y)
                if i == 2:
                    y -= 40
                    x -= 40
                elif i > 2:
                    x -= 40
                else:
                    y -= 40
        for i in range(32, 41):
            if i in positions:
                x, y = self.tileRects[i-1].bottomright
                y -= 40
                for i, player in enumerate(positions[i]):
                    self.displayToken(player.token, x, y)
                    if i in [1, 3]:
                        x += 35
                        y += 35
                    else:
                        y -= 35

    def displayToken(self, token, x, y):
        tokenImg = pygame.image.load(Token.path(token)).convert_alpha()
        tokenImg = pygame.transform.scale(tokenImg, (40, 40))
        self.screen.blit(tokenImg, (x, y))

    def displayPlayersInfo(self):
        nameFont = pygame.font.SysFont("myriadpro", 35)
        viewButtonImg = pygame.image.load("Images/Buttons/View_Button.png").convert_alpha()
        viewButtons = []
        viewRects = []
        y = 1000
        for i, player in enumerate(reversed(self.game.players)):
            if len(self.game.players) - self.currentPlayerNo == i + 1:
                pygame.draw.rect(self.screen, Colour.lightGreen, pygame.Rect((1100, y), (800, 50)), 2)
            else:
                pygame.draw.rect(self.screen, Colour.black, pygame.Rect((1100, y), (800, 50)), 2)
            self.displayToken(player.token, 1120, y+5)
            self.screen.blit(nameFont.render(player.name, True, Colour.black), (1180, y+15))
            self.screen.blit(nameFont.render(f"${player.money}", True, Colour.black), (1500, y+15))
            viewButtons.append(Button(1750, y+5, viewButtonImg, 1))
            viewRects.append(viewButtons[i].draw(self.screen))
            y -= 60
        return reversed(viewRects)

    def displayTileInfo(self, tileNo):
        tileFont = pygame.font.SysFont("myriadpro", 35)
        infoFont = pygame.font.SysFont("myriadpro", 25)
        
        tile = self.game.board.getTile(tileNo+1)
        if hasattr(tile, "owner"):
            pygame.draw.rect(self.screen, Colour.black, pygame.Rect((395, 350), (245, 340)), 2)
            pygame.draw.rect(self.screen, Colour.tileColours[tile.group], pygame.Rect((397, 352), (241, 45)))
            self.screen.blit(tileFont.render(tile.name, True, Colour.black), (400, 400))
            self.screen.blit(infoFont.render(f"Cost: {tile.cost}", True, Colour.black), (400, 430))
            self.screen.blit(infoFont.render(f"Owner: {tile.owner}", True, Colour.black), (400, 450))
            if isinstance(tile, Property):
                self.screen.blit(infoFont.render(f"Rent: {tile.rent[0]}", True, Colour.black), (400, 470))
                self.screen.blit(infoFont.render(f"Rent (colour group): {tile.rent[0]*2}", True, Colour.black), (400, 490))
                self.screen.blit(infoFont.render(f"Rent (1 house): {tile.rent[1]}", True, Colour.black), (400, 510))
                self.screen.blit(infoFont.render(f"Rent (2 houses): {tile.rent[2]}", True, Colour.black), (400, 530))
                self.screen.blit(infoFont.render(f"Rent (3 houses): {tile.rent[3]}", True, Colour.black), (400, 550))
                self.screen.blit(infoFont.render(f"Rent (4 houses): {tile.rent[4]}", True, Colour.black), (400, 570))
                self.screen.blit(infoFont.render(f"Rent (hotel): {tile.rent[5]}", True, Colour.black), (400, 590))
                self.screen.blit(infoFont.render(f"House cost: {Property.houseCost[tile.group]}", True, Colour.black), (400, 610))
                self.screen.blit(infoFont.render(f"Mortgage value: {tile.cost//2}", True, Colour.black), (400, 630))
            elif isinstance(tile, Station):
                self.screen.blit(infoFont.render(f"Rent: {Station.rent[0]}", True, Colour.black), (400, 480))
                self.screen.blit(infoFont.render(f"Rent (2 stations owned): {Station.rent[1]}", True, Colour.black), (400, 510))
                self.screen.blit(infoFont.render(f"Rent (3 stations owned): {Station.rent[2]}", True, Colour.black), (400, 540))
                self.screen.blit(infoFont.render(f"Rent (4 stations owned): {Station.rent[3]}", True, Colour.black), (400, 570))
                self.screen.blit(infoFont.render(f"Mortgage value: {tile.cost//2}", True, Colour.black), (400, 600))
            elif isinstance(tile, Utility):
                self.screen.blit(infoFont.render("If one Utility is owned,", True, Colour.black), (420, 480))
                self.screen.blit(infoFont.render("rent is 4 times amount", True, Colour.black), (400, 500))
                self.screen.blit(infoFont.render("shown on dice.", True, Colour.black), (400, 520))
                self.screen.blit(infoFont.render("If two Utilities are owned,", True, Colour.black), (420, 550))
                self.screen.blit(infoFont.render("rent is 10 times amount", True, Colour.black), (400, 570))
                self.screen.blit(infoFont.render("shown on dice.", True, Colour.black), (400, 590))
                self.screen.blit(infoFont.render(f"Mortgage value: {tile.cost//2}", True, Colour.black), (400, 620))
            if tile.mortgaged:
                self.screen.blit(infoFont.render("PROPERTY MORTGAGED", True, Colour.black), (400, 650))
        elif tile.name == "Free Parking":
            self.screen.blit(tileFont.render(f"Free Parking value: {self.game.freeParkingValue}", True, Colour.black), (400, 400))
        self.update()

    def auction(self, tile):
        titleFont = pygame.font.SysFont("myriadpro", 45)
        nameFont = pygame.font.SysFont("myriadpro", 35)
        bid10Img = pygame.image.load("Images/Buttons/bid10_Button.png").convert_alpha()
        bid100Img = pygame.image.load("Images/Buttons/bid100_Button.png").convert_alpha()
        leaveImg = pygame.image.load("Images/Buttons/leave_Button.png").convert_alpha()
        running = True
        auctionPlayers = self.game.eligableAuctionPlayers(self.game.players[self.currentPlayerNo])
        if len(auctionPlayers) < 2:
            self.popUp("There are not enough players to run an auction.")
            running = False
        auctionTurn = 0
        auctionPrice = 0
        self.screen.fill(Colour.white)
        self.displayTileInfo(tile.position-1)
        while running:
            pygame.draw.rect(self.screen, Colour.white, pygame.Rect((750, 0), (1170, 1080)))
            self.screen.blit(titleFont.render(f"Auction for {tile.name}", True, Colour.black), (1050, 50))
            self.screen.blit(nameFont.render(f"Current price: ${auctionPrice}", True, Colour.black), (1050, 250))
            y = 700
            for i, player in enumerate(auctionPlayers):
                if auctionTurn == i:
                    pygame.draw.rect(self.screen, Colour.lightGreen, pygame.Rect((800, y), (1000, 50)), 2)
                    bid10Button = Button(1300, y+5, bid10Img, 1)
                    bid100Button = Button(1440, y+5, bid100Img, 1)
                    leaveButton = Button(1580, y+5, leaveImg, 1)
                    bid10Rect = bid10Button.draw(self.screen)
                    bid100Rect = bid100Button.draw(self.screen)
                    leaveRect = leaveButton.draw(self.screen)
                else:
                    pygame.draw.rect(self.screen, Colour.black, pygame.Rect((800, y), (1000, 50)), 2)
                self.displayToken(player.token, 820, y+5)
                self.screen.blit(nameFont.render(player.name, True, Colour.black), (880, y+15))
                self.screen.blit(nameFont.render(f"${player.money}", True, Colour.black), (1200, y+15))
                y -= 60

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if bid10Rect.collidepoint(pos):
                        if auctionPlayers[i].money >= auctionPrice + 10:
                            auctionPrice += 10
                            auctionTurn = auctionTurn + 1 if auctionTurn < len(auctionPlayers) - 1 else 0
                        else:
                            self.popUp("You don't have enough money to bid $10.")
                    elif bid100Rect.collidepoint(pos):
                        if auctionPlayers[i].money >= auctionPrice + 100:
                            auctionPrice += 100
                            auctionTurn = auctionTurn + 1 if auctionTurn < len(auctionPlayers) - 1 else 0
                        else:
                            self.popUp("You don't have enough money to bid $100.")
                    elif leaveRect.collidepoint(pos):
                        del auctionPlayers[auctionTurn]
                        if len(auctionPlayers) == 1:
                            self.popUp(f"{auctionPlayers[0].name} has won for {auctionPrice}!")
                            tile.owner = auctionPlayers[0]
                            auctionPlayers[0].money -= auctionPrice
                            running = False

            self.update()

    def popUp(self, message):
        infoFont = pygame.font.SysFont("myriadpro", 45)
        okayImg = pygame.image.load("Images/Buttons/Okay_Button.png").convert_alpha()
        okayButton = Button(820, 510, okayImg, 1)
        running = True
        while running:
            pygame.draw.rect(self.screen, Colour.white, pygame.Rect((800, 450), (850, 200)))
            pygame.draw.rect(self.screen, Colour.darkGrey, pygame.Rect((800, 450), (850, 200)), 5)
            self.screen.blit(infoFont.render(message, True, Colour.black), (815, 470))
            okayRect = okayButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if okayRect.collidepoint(pos):
                        running = False

            self.update()

    def jailPopUp(self):
        infoFont = pygame.font.SysFont("myriadpro", 45)
        stayImg = pygame.image.load("Images/Buttons/StayInJail_Button.png").convert_alpha()
        payImg = pygame.image.load("Images/Buttons/PayToLeave_Button.png").convert_alpha()
        cardImg = pygame.image.load("Images/Buttons/UseCard_Button.png").convert_alpha()
        stayButton = Button(620, 510, stayImg, 1)
        payButton = Button(840, 510, payImg, 1)
        cardButton = Button(1060, 510, cardImg, 1)
        running = True
        while running:
            pygame.draw.rect(self.screen, Colour.white, pygame.Rect((600, 400), (700, 250)))
            pygame.draw.rect(self.screen, Colour.darkGrey, pygame.Rect((600, 400), (700, 250)), 5)
            self.screen.blit(infoFont.render("You are in jail.", True, Colour.black), (615, 420))
            self.screen.blit(infoFont.render(f"{3 - self.game.players[self.currentPlayerNo].jailTurn} rounds left.", True, Colour.black), (615, 460))
            stayRect = stayButton.draw(self.screen)
            payRect = payButton.draw(self.screen)
            if self.game.players[self.currentPlayerNo].getOutOfJailFree:
                cardRect = cardButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if stayRect.collidepoint(pos):
                        self.game.players[self.currentPlayerNo].jailTurn += 1
                        running = False
                    elif payRect.collidepoint(pos):
                        self.game.players[self.currentPlayerNo].inJail = False
                        self.game.players[self.currentPlayerNo].money -= 50
                        self.game.freeParkingValue += 50
                        running = False
                    if self.game.players[self.currentPlayerNo].getOutOfJailFree:
                        if cardRect.collidepoint(pos):
                            self.game.players[self.currentPlayerNo].inJail = False
                            self.game.cards.returnJailFreeCard(self.game.players[self.currentPlayerNo])
                            running = False

            self.update()

    def buyPopUp(self, tile):
        infoFont = pygame.font.SysFont("myriadpro", 45)
        buyImg = pygame.image.load("Images/Buttons/Buy_Button.png").convert_alpha()
        auctionImg = pygame.image.load("Images/Buttons/Auction_Button.png").convert_alpha()
        buyButton = Button(820, 510, buyImg, 1)
        auctionButton = Button(1040, 510, auctionImg, 1)
        running = True
        while running:
            pygame.draw.rect(self.screen, Colour.white, pygame.Rect((800, 450), (850, 200)))
            pygame.draw.rect(self.screen, Colour.darkGrey, pygame.Rect((800, 450), (850, 200)), 5)
            self.screen.blit(infoFont.render(f"Buy {tile.name} for ${tile.cost}?", True, Colour.black), (815, 470))
            buyRect = buyButton.draw(self.screen)
            auctionRect = auctionButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if buyRect.collidepoint(pos):
                        tile.owner = self.game.players[self.currentPlayerNo]
                        self.game.players[self.currentPlayerNo].money -= tile.cost
                        running = False
                    if auctionRect.collidepoint(pos):
                        self.auction(tile)
                        running = False

            self.update()

    def chooseProprety(self, properties):
        infoFont = pygame.font.SysFont("myriadpro", 45)
        nameFont = pygame.font.SysFont("myriadpro", 35)
        backImg = pygame.image.load("Images/Buttons/Back_Button.png").convert_alpha()
        
        running = True
        while running:
            propertyRects = []
            y = 250
            pygame.draw.rect(self.screen, Colour.white, pygame.Rect((800, 200), (400, 150+50*(len(properties)+1))))
            pygame.draw.rect(self.screen, Colour.darkGrey, pygame.Rect((800, 200), (400, 150+50*(len(properties)+1))), 5)
            self.screen.blit(infoFont.render("Properties:", True, Colour.black), (815, 215))
            for p in properties:
                pygame.draw.rect(self.screen, Colour.tileColours[p.group], pygame.Rect((800, y), (50, 50)))
                self.screen.blit(nameFont.render(p.name, True, Colour.black), (860, y+5))
                propertyRects.append(pygame.Rect((800, y), (200, 50)))
                y += 50
            backButton = Button(815, y, backImg, 1)
            backRect = backButton.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(propertyRects):
                        if rect.collidepoint(pos):
                            return properties[i]

            self.update()

    def update(self):
        self.display.update()
        self.clock.tick(60)

    def quitGame():
        pygame.quit()
        sys.exit()

class Button:

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return self.rect


class Colour:

    black = (0,0,0)
    white = (255,255,255)
    lightGrey = (206,206,206)
    darkGrey = (75,75,75)
    brown = (91,65,36)
    lightBlue = (0,159,227)
    pink = (102,36,131)
    orange = (233,120,24)
    red = (204,20,23)
    yellow = (251,224,23)
    green = (11,142,54)
    darkBlue = (36,55,141)
    lightGreen = (11,244,32)
    tileColours = {"Brown": brown, "Blue": lightBlue, "Purple": pink, "Orange": orange,
                    "Red": red, "Yellow": yellow, "Green": green, "Deep blue": darkBlue,
                    "Station": black, "Utilities": lightGrey}

class Main:

    def __init__(self):
        self.parser = Parser()

    def addTilesToBoard(self):
        tiles = self.parser.getTiles()
        board = Board()
        for tile in tiles:
            if len(tile) == 4:
                board.addTile(Tile(*tile))
            else:
                if tile[2] == "Station":
                    board.addTile(Station(*tile))
                elif tile[2] == "Utilities":
                    board.addTile(Utility(*tile))
                else:
                    board.addTile(Property(*tile))
        return board

    def createGame(self):
        board = self.addTilesToBoard()
        cards = Cards(self.parser.getCards())
        Display(board, cards)

if __name__ == '__main__':
    main = Main()
    main.createGame()