import pygame, os, sys, string
from button import *
from pygame.locals import *

def getGridCoords(height, width):
    pass

def init(data):
    data.WINSIZE = (1920, 1080)
    data.THEMEDEEPSPACE = 0
    data.GRIDMARGIN = 60

    data.theme = data.THEMEDEEPSPACE
    data.colors = [                                                             # Every theme has the following format:
                       [[ (74,178,255) , (0,134,255)  ],                        # Color 1 (inner, outer) [Blue]
                        [ (198,0,0)    , (252,31,32)  ],                        # Color 2 (inner, outer) [Red]
                        [ (206,137,48) , (255,165,21) ],                        # Color 3 (inner, outer) [Yellow]
                        [ (239,235,223), (209,207,184)],                        # Square Inner White, Multicell White
                          (30,30,30) ]                                          # Background
                  ]

    data.level = []
    level = open('level','r').read()
    for line in level.splitlines():
        data.level.append([])
        for char in line.split(' '):
            data.level[-1].append(char)

def run():
    class Struct(object): pass
    data = Struct()
    init(data)

    pygame.init()
    screen = pygame.display.set_mode(data.WINSIZE, pygame.FULLSCREEN)

    buttons = pygame.sprite.Group()
    mainA = Button("assets/mainA.png", data.colors[data.theme][-1], (143,143))
    mainB = Button("assets/mainB.png", data.colors[data.theme][-1], (143,143))
    buttons.add(mainA, mainB)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in buttons:
                    if button.rect.collidepoint(x,y):
                        if not button.isRotating:
                            button.isRotating = True
                            button.rotate()

        screen.fill(data.colors[data.theme][-1])
        mainA.rect.left, mainA.rect.top = 594, 173
        mainB.rect.left, mainB.rect.top = 594, 413
        for button in buttons:
            if not button.isRotating: screen.blit(button.img, button.rect)
            else:
                button.rotate()
                screen.blit(button.rotatedImg, button.rotatedRect)
        pygame.display.update()

run()
