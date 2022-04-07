import sys, pygame, glob, os

class Display:

    def __init__(self):
        self.colour = {"white": (255,255,255), "black": (0,0,0)}

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

            self.screen.fill(self.colour["white"])
            if playButton.draw(self.screen):
                self.game()
            if exitButton.draw(self.screen):
                Display.quitGame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Display.quitGame()

            self.update()

    def game(self):
        self.fillBoard()

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

    def fillBoard(self):
        tileFiles = sorted(os.listdir("Tiles"))
        tileImages = []
        for tile in tileFiles:
            tileImages.append(pygame.image.load(os.path.join("Tiles", tile)).convert_alpha())

        self.screen.fill(self.colour["white"])
        coordx = 875
        coordy = 795
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

    def update(self):
        self.display.update()
        self.clock.tick(60)

    def quitGame():
        pygame.quit()
        sys.exit()

class Button():

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

if __name__ == '__main__':
    Display()