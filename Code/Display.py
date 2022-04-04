import sys, pygame, glob, os

class Display:

    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()

        self.white = 255,255,255
        size = width, height = 1920,1080
        self.display = pygame.display
        self.display.set_caption("Property Tycoon")
        self.screen = self.display.set_mode(size)
        name_list = sorted(os.listdir("Tiles"))
        image_list = []
        for card in name_list:
            image_list.append(pygame.image.load(os.path.join("Tiles", card)))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                left,middle,right = pygame.mouse.get_pressed()
                if left:
                    self.fillBoard(image_list)

            self.display.update()
            clock.tick(60)

    def fillBoard(self, images):
        self.screen.fill(self.white)
        coordx = 875
        coordy = 795
        switcher = 0
        turn = 0
        for tile in images:
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

if __name__ == '__main__':
    Display()