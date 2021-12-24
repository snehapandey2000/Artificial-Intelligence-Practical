import pygame
import os

pygame.init()

w, h = 218, 218


gameDisplay = pygame.display.set_mode((w, h))
pygame.display.set_caption("GoT")


board = [[7, 6, 1], [2, -1, 4], [3, 5, 0]]
blankX = 1  # empty tile coordinates
blankY = 1
n = 3

application_path = os.path.dirname(__file__)
application_path = application_path.replace('\\', '/')

tile = pygame.image.load(application_path+"/TILE.png")

blank = pygame.image.load(application_path+"/BLANK.png")


def navigate(direction, blankX, blankY):
    if(direction == "D"):
        if(blankY+1 < n):
            t = board[blankY+1][blankX]
            board[blankY+1][blankX] = board[blankY][blankX]
            board[blankY][blankX] = t
            blankY += 1

    elif(direction == "U"):
        if(blankY-1 >= 0):
            t = board[blankY-1][blankX]
            board[blankY-1][blankX] = board[blankY][blankX]
            board[blankY][blankX] = t
            blankY -= 1
    elif(direction == "L"):
        if(blankX-1 >= 0):
            t = board[blankY][blankX-1]
            board[blankY][blankX-1] = board[blankY][blankX]
            board[blankY][blankX] = t
            blankX -= 1
    elif(direction == "R"):
        if(blankX+1 < n):
            t = board[blankY][blankX+1]
            board[blankY][blankX+1] = board[blankY][blankX]
            board[blankY][blankX] = t
            blankX += 1
    return blankX, blankY


crashed = False
while crashed == False:
    # Capture frame-by-frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                blankX, blankY = navigate("U", blankX, blankY)
            if event.key == pygame.K_LEFT:
                blankX, blankY = navigate("L", blankX, blankY)
            if event.key == pygame.K_RIGHT:
                blankX, blankY = navigate("R", blankX, blankY)
            if event.key == pygame.K_DOWN:
                blankX, blankY = navigate("D", blankX, blankY)
    counter = -1
    for y in range(0, n):
        for x in range(0, n):
            #print(x, position[x])
            font = pygame.font.Font('freesansbold.ttf', 22)
            tileNum = font.render(
                str(board[y][x]+1), True, (0, 0, 0)).convert_alpha()
            counter += 1
            if board[y][x] == -1:
                gameDisplay.blit(blank, (x*64+10, y*64+10))
                continue
            else:
                gameDisplay.blit(tile, (x*64+10, y*64+10))
                # print(x%n*120,x/n*120)
            gameDisplay.blit(tileNum, (x*64+30, y*64+30))
    pygame.display.update()
