import sys, pygame, glob, os
pygame.init()

size = width, height = 1920,1080
clock = pygame.time.Clock()
crashed = False
screen = pygame.display.set_mode(size)
name_list = os.listdir("Tiles")
white = 255,255,255
name_lists = sorted(name_list)

def getImages():
    image_list = []
    for card in name_lists:
        image_list.append(pygame.image.load(os.path.join("Tiles", card)))
    return image_list

def fillBoard(image_list):
    screen.fill(white)
    coordx = 875
    coordy = 795
    switcher = 0
    turn = 0
    for tile in image_list:
        if switcher in [11,21,31]:
            turn -= 90
        if switcher in [10, 20,21 ,31]:
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
        
        screen.blit(tile, (coordx,coordy))
        switcher += 1

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    if event.type == pygame.MOUSEBUTTONDOWN:
        left,middle,right = pygame.mouse.get_pressed()
        if left:
            fillBoard(getImages())

    pygame.display.update()
    clock.tick(60)

    
pygame.quit()
quit()
