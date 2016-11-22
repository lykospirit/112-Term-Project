import pygame, sys
from pygame.locals import *

pygame.init()
winSize = (1920,1080)
screen = pygame.display.set_mode(winSize, pygame.FULLSCREEN)

# yogurt = pygame.image.load("yogurt.png").convert()
# yogurtRect = yogurt.get_rect()

# cellColors = [ [(239,235,223), (209,207,184)],                                  # CellWhite, OtherWhite
#             [(74,178,255), (0,134,255)],                                        # Blue (inner, outer)
#             [(198,0,0), (252,31,32)],                                           # Red
#             [(206,137,48), (255,165,21)]                                        # Yellow
#             ]

redmain = pygame.image.load("redmain.png").convert()
bluemain = pygame.image.load("bluemain.png").convert()
redmainRect = redmain.get_rect()
bluemainRect = bluemain.get_rect()

gridMargin = 60
def getGridCoords(height, width):
    pass

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
    # screen.fill((30,30,30))
    redmainRect.left, redmainRect.top = 594, 173
    if angle != 0:
        screen.blit(pygame.transform.rotate(redmain, angle), pygame.transform.rotate(redmain, angle).get_rect().move(700,700))
    else:
        screen.blit(redmain, redmainRect)
    bluemainRect.left, bluemainRect.top = 594, 413
    screen.blit(bluemain, bluemainRect)
    pygame.draw.rect(screen, (255,255,255), (0,0,300,300))
    pygame.display.update()
