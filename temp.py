import pygame, os, sys
from pygame.locals import *

def getGridCoords(height, width):
    pass

def init(data):
    pass
    
def run():
    pygame.init()
    winSize = (1920,1080)
    screen = pygame.display.set_mode(winSize, pygame.FULLSCREEN)
    class Struct(object): pass
    data = Struct()
    data.cellColors = [                                                         # Every theme has the following format:
                       [[(239,235,223), (209,207,184)],                         # Square Inner White, Multicell White
                        [(74,178,255), (0,134,255)],                            # Color 1 (inner, outer) [Blue]
                        [(198,0,0), (252,31,32)],                               # Color 2 (inner, outer) [Red]
                        [(206,137,48), (255,165,21)]]                           # Color 3 (inner, outer) [Yellow]
                    ]
    redmain = pygame.image.load("redmain.png").convert()
    bluemain = pygame.image.load("bluemain.png").convert()
    redmainRect = redmain.get_rect()
    bluemainRect = bluemain.get_rect()
    bkgrndColor = (30,30,30)

    redmain.set_colorkey(bkgrndColor, RLEACCEL)

    gridMargin = 60


    angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if redmainRect.collidepoint(x,y):
                    angle = (angle-5)%90
                    print(angle)
        screen.fill(bkgrndColor)
        redmainRect.left, redmainRect.top = 594, 173
        if angle != 0:
            rotateRedmain = pygame.transform.rotate(redmain, angle)
            rotateRedmainRect = rotateRedmain.get_rect()
            rotateRedmainRect.center = redmainRect.center
            screen.blit(rotateRedmain, rotateRedmainRect)
        else:
            screen.blit(redmain, redmainRect)
        bluemainRect.left, bluemainRect.top = 594, 413
        screen.blit(bluemain, bluemainRect)
        pygame.display.update()

run()
