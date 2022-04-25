import sys, pygame, glob, os

class Display:

    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()
        size = width, height = 1920,1080
        self.display = pygame.display
        self.display.set_caption("Property Tycoon")
        self.screen = self.display.set_mode(size, pygame.FULLSCREEN)

        self.mainMenu()

    def mainMenu(self):
        playImg = pygame.image.load("Images/Play_Button.png").convert_alpha()
        exitImg = pygame.image.load("Images/Exit_Button.png").convert_alpha()
        playButton = Button(500, 600, playImg, 1)
        exitButton = Button(1000, 600, exitImg, 1)

        running = True
        while running:

            self.screen.fill(Colour.white)
            if playButton.draw(self.screen):
                self.game()
            if exitButton.draw(self.screen):
                Display.quitGame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()

            self.update()

    def selectPlayers(self):
        running = True
        while running:

            self.screen.fill(Colour.white)
            if playButton.draw(self.screen):
                self.game()
            if exitButton.draw(self.screen):
                Display.quitGame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()

            self.update()

    def game(self):
        self.drawBoard()

        running = True
        while running:

            # do game stuff

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.update()

    def drawBoard(self):
        self.screen.fill(Colour.white)
        boardBoarder = pygame.Rect((80, 75), (915, 915))
        pygame.draw.rect(self.screen, Colour.black, boardBoarder, 2)

        tileFiles = sorted(os.listdir("Tiles"))
        tileImages = []
        for tile in tileFiles:
            tileImages.append(pygame.image.load(os.path.join("Tiles", tile)).convert_alpha())

        coordx = 950
        coordy = 870
        switcher = 0
        turn = 0
        for tile in tileImages:
            if switcher in [11, 21, 31]:
                turn -= 90
            if switcher in [10, 20, 21 ,31]:
                if turn == 0:
                    coordx -= 120
                elif turn == -90:
                    coordy -= 120
                elif turn == -180:
                    coordx += 120
                elif turn == -270:
                    coordy += 120
            else:
                if turn == 0:
                    coordx -= 75
                elif turn == -90:
                    coordy -= 75
                elif turn == -180:
                    coordx += 75
                elif turn == -270:
                    coordy += 75
            tile = pygame.transform.rotozoom(tile, turn, 0.5)
            
            self.screen.blit(tile, (coordx,coordy))
            switcher += 1

    def movePlayer(self, player, spaces):
        pass

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
        self.click = False

    def draw(self, surface):
        clicked = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.click = True
                clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return clicked

class playerSelector:

    def __init__(self, active, agent, number):
        self.active = False
        self.agent = agent
        self.name = f"Computer {number}" if agent else f"Human {number}"
        self.token = number

    def draw(self, surface, number):

        boardBoarder = pygame.Rect((80, 75), (915, 915))
        pygame.draw.rect(self.screen, Colour.black, boardBoarder, 2)

    def setAgent(self, agent):
        if agent:
            self.agent = True
        else:
            self.agent = False


class Colour:

    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

if __name__ == '__main__':
    Display()