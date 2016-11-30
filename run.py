import pygame, os, sys, string
from button import *
from pygame.locals import *

def get2dIndex(L, obj):
    for each in range(len(L)):
        if obj in L[each]:
            return (each, L[each].index(obj))

def make2dList(rows, cols, val=None):
    a = [[val]*cols for row in range(rows)]
    return a

def getGridCoords(data):
    gap = min((data.WINSIZE[0]-2*data.GRIDMARGIN)//data.levelWidth,
              (data.WINSIZE[1]-2*data.GRIDMARGIN)//data.levelHeight)
    gridCoords = []
    for row in range(data.levelHeight):
        gridCoords.append([])
        for col in range(data.levelWidth):
            coord = (data.GRIDMARGIN + gap*col + gap//2, data.GRIDMARGIN + gap*row + gap//2)
            gridCoords[row].append(coord)
    return gap, gridCoords

def getLineTuples(data):                                                        # Returns list of tuples for line oords
    DIRS = [(0,1), (1,1), (1,0), (1,-1)]
    lineTuples = []
    for row in range(data.levelHeight):
        for col in range(data.levelWidth):
            if data.level[row][col]=='0': pass
            for dirc in DIRS:
                newR, newC = row+dirc[0], col+dirc[1]
                if newR>=0 and newC>=0 and newR<data.levelHeight and newC<data.levelWidth and data.level[newR][newC]!='0':
                    lineTuples.append((data.gridCoords[row][col], data.gridCoords[newR][newC]))
    return lineTuples

def init(data):
    data.THEMEDEEPSPACE = 0                                                     # CONSTANTS
    data.GRIDMARGIN = 100
    data.CELLMARGIN = 0.6
    data.ONOFFSCALE = 0.2121
    data.ONOFFOFFSETSCALE = 0.153
    data.ONOFFOFFSETLIST = [(-1,0), (1,0), (0,-1), (0,1)]

    data.mouseDown = False                                                      # Mouse

    data.theme = data.THEMEDEEPSPACE
    data.colors = [                                                             # Every theme has the following format:
                       [[ (74,178,255) , (0,134,255)  ],                        # Color 1 (inner, outer) [Blue]
                        [ (198,0,0)    , (252,31,32)  ],                        # Color 2 (inner, outer) [Red]
                        [ (206,137,48) , (255,165,21) ],                        # Color 3 (inner, outer) [Yellow]
                        [ (239,235,223), (209,207,184)],                        # Square Inner White, Multicell White
                          (59,59,57), (30,30,30) ]                              # Lines, Background
                  ]

    data.level = []
    level = open('level','r').read()                                            # Load level
    for line in level.splitlines():
        data.level.append([])
        for char in line.split(' '):
            data.level[-1].append(char)
    data.levelHeight, data.levelWidth = len(data.level), len(data.level[0])
    for line in range(data.levelHeight):                                        # Check level is rectangular
        if len(data.level[line]) != data.levelWidth:
            raise Exception("Invalid level: Remember to add '0's for empty cells!")

    data.cellSize, data.gridCoords = getGridCoords(data)                        # Scale assets to fit level
    data.buttonSize = (int(data.CELLMARGIN*data.cellSize), int(data.CELLMARGIN*data.cellSize))

    data.buttons = pygame.sprite.Group()                                        # Generate buttons
    data.buttonList = make2dList(data.levelHeight, data.levelWidth)
    for row in range(data.levelHeight):
        for col in range(data.levelWidth):
            if data.level[row][col] != '0':
                if data.level[row][col].isalpha():
                    if data.level[row][col].isupper():
                        path = "assets/main%s.png" % data.level[row][col]
                        data.buttonList[row][col] = Button(path, data.colors[data.theme][-1], data.buttonSize, main=True)
                    else:
                        path = "assets/one%s.png" % data.level[row][col].upper()
                        data.buttonList[row][col] = Button(path, data.colors[data.theme][-1], data.buttonSize)
                else:
                    path = "assets/%s.png" % data.level[row][col]
                    data.buttonList[row][col] = Button(path, data.colors[data.theme][-1], data.buttonSize, int(data.level[row][col]))
                data.buttons.add(data.buttonList[row][col])
                data.buttonList[row][col].rect.center = data.gridCoords[row][col]

                                                                                # Generate on/off assets
    data.onoffSize = (int(data.buttonSize[0]*data.ONOFFSCALE), int(data.buttonSize[0]*data.ONOFFSCALE))
    data.onoffOffset = int(data.buttonSize[0]*data.ONOFFOFFSETSCALE)
    data.onImg = pygame.transform.scale(pygame.image.load("assets/on.png").convert_alpha(), data.onoffSize)
    data.offImg = pygame.transform.scale(pygame.image.load("assets/off.png").convert_alpha(), data.onoffSize)
    data.onImg.set_colorkey(None)
    data.offImg.set_colorkey(None)
    data.onoffImgRect = data.onImg.get_rect()

    data.lineTuples = getLineTuples(data)                                       # Generate lines

def run():
    class Struct(object): pass

    data = Struct()
    data.WINSIZE = (1920, 1080)
    pygame.init()
    screen = pygame.display.set_mode(data.WINSIZE, pygame.FULLSCREEN)
    init(data)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                data.mouseDown = False
            elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
                x, y = event.pos
                for button in data.buttons:
                    if event.type == MOUSEBUTTONDOWN:
                        if button.main and button.rect.collidepoint(x,y):
                            data.mouseDown = True
                    if button.rect.collidepoint(x,y) and data.mouseDown:
                        if not button.isRotating and not button.hasRotated:
                            button.isRotating = True
                            button.rotate()
                    else:
                        if button.hasRotated: button.rotateReset = True

        screen.fill(data.colors[data.theme][-1])

        ##### LINES #####
        for line in data.lineTuples:
            pygame.draw.line(screen, data.colors[data.theme][-2], line[0], line[1], 5)

        ##### BUTTONS #####
        for button in data.buttons:
            if button.rotateReset:                                              # Prevent rotating while rotating
                if button.hasRotated: button.hasRotated -= 1
                else: button.rotateReset = False

            if not button.isRotating: screen.blit(button.img, button.rect)      # Draw button
            else:
                button.rotate()
                screen.blit(button.rotatedImg, button.rotatedRect)

            if button.passes > 1:                                               # Draw On/Off
                for each in range(button.passes):
                    onoffImgCenter = (button.rect.center[0]+(data.ONOFFOFFSETLIST[each][0]*data.onoffOffset),
                                      button.rect.center[1]+(data.ONOFFOFFSETLIST[each][1]*data.onoffOffset))
                    onoffImgRect = data.onoffImgRect
                    onoffImgRect.center = onoffImgCenter
                    screen.blit(data.offImg, onoffImgRect)
        pygame.display.update()

run()
