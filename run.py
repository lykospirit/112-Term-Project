import pygame, os, sys, string, copy, threading, time
from button import *
from generator import *
from solver import *
from utility import *
from pygame.locals import *

class LevelThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.level, self.solution = None, None

    def run(self):
        print('thread started')
        newLevelRow = 5
        newLevelCol = 5
        if newLevelCol==5 and newLevelRow==5: newLevelColor = 3
        elif newLevelCol==3 and newLevelRow==3: newLevelColor = 2
        else: newLevelColor = random.randint(2,3)
        self.solution = buildLevel(newLevelRow, newLevelCol, newLevelColor)

def getGridCoords(data):
    widthGap = (data.WINSIZE[0]-2*data.GRIDMARGIN)//data.levelWidth
    heightGap = (data.WINSIZE[1]-2*data.GRIDMARGIN)//data.levelHeight
    gap = min(widthGap, heightGap)
    if gap == widthGap:
        widthMargin = data.GRIDMARGIN
        heightMargin = (data.WINSIZE[1] - (data.levelHeight * gap))//2
    else:
        heightMargin = data.GRIDMARGIN
        widthMargin = (data.WINSIZE[0] - (data.levelWidth * gap))//2

    gridCoords = []
    for row in range(data.levelHeight):
        gridCoords.append([])
        for col in range(data.levelWidth):
            coord = (widthMargin + gap*col + gap//2, heightMargin + gap*row + gap//2)
            gridCoords[row].append(coord)
    return gap, gridCoords

def getLineTuples(data):                                                        # Returns list of tuples for line oords
    DIRS = [(0,1), (1,1), (1,0), (1,-1)]
    lineTuples = set()
    for row in range(data.levelHeight):
        for col in range(data.levelWidth):
            if data.level[row][col]!=0:
                for dirc in DIRS:
                    newR, newC = row+dirc[0], col+dirc[1]
                    if newR>=0 and newC>=0 and newR<data.levelHeight and newC<data.levelWidth and data.level[newR][newC]!=0:
                        lineTuples.add((data.gridCoords[row][col], data.gridCoords[newR][newC]))
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
                   {
                    'A': [ (198,0,0)    , (252,31,32)  ],                       # Color 1 (inner, outer) [Red]
                    'B': [ (74,178,255) , (0,134,255)  ],                       # Color 2 (inner, outer) [Blue]
                    'C': [ (206,137,48) , (255,165,21) ],                       # Color 3 (inner, outer) [Yellow]
                    'W': [ (239,235,223), (209,207,184)],                       # Square Inner White, Multicell White
                    -2: (59,59,57), -1: (30,30,30)                              # Lines, Background
                   }
                  ]

    data.level = getLevel()
    if data.levelGen: data.solution = copy.deepcopy(data.levelGen.solution)
    data.levelGen = LevelThread()
    data.levelGen.start()
    data.levelHeight, data.levelWidth = len(data.level), len(data.level[0])

    data.cellSize, data.gridCoords = getGridCoords(data)                        # Scale assets to fit level
    data.buttonSize = (int(data.CELLMARGIN*data.cellSize), int(data.CELLMARGIN*data.cellSize))

    data.buttons = pygame.sprite.Group()                                        # Generate buttons
    data.buttonList = make2dList(data.levelHeight, data.levelWidth)
    data.buttonCount = 0
    for row in range(data.levelHeight):
        for col in range(data.levelWidth):
            if data.level[row][col] != 0:
                data.buttonCount += 1
                if isinstance(data.level[row][col], str):
                    if data.level[row][col].isupper():
                        path = "assets/main%s.png" % data.level[row][col]
                        data.buttonList[row][col] = Button(path, data.buttonSize, row, col, main=True, color=data.level[row][col])
                    else:
                        path = "assets/one%s.png" % data.level[row][col].upper()
                        data.buttonList[row][col] = Button(path, data.buttonSize, row, col, color=data.level[row][col].upper())
                else:
                    path = "assets/%s.png" % data.level[row][col]
                    data.buttonList[row][col] = Button(path, data.buttonSize, row, col, data.level[row][col])
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

    data.drawnButtons = {'A': [], 'B': [], 'C': [], 'last': None}
    data.drawnLines = {'A': [], 'B': [], 'C': []}
    data.solvedButtons = set()

def run():
    class Struct(object): pass

    data = Struct()
    data.WINSIZE = (1920, 1080)
    # data.WINSIZE = (600,400)
    data.lastTime = pygame.time.get_ticks()
    newLevelRow = random.randint(3,5)
    newLevelCol = random.randint(3,5)
    if newLevelCol==5 and newLevelRow==5: newLevelColor = 3
    elif newLevelCol==3 and newLevelRow==3: newLevelColor = 2
    else: newLevelColor = random.randint(2,3)
    data.solution = buildLevel(newLevelRow, newLevelCol, newLevelColor)
    data.levelGen = None
    pygame.init()
    screen = pygame.display.set_mode(data.WINSIZE, pygame.FULLSCREEN)
    # screen = pygame.display.set_mode(data.WINSIZE)
    init(data)

    while True:
        if pygame.time.get_ticks() - data.lastTime > 500:
            data.solvedButtons = set()
            for button in data.buttons:
                if button.active<0: button.active = 0
                if button.active == button.passes: data.solvedButtons.add(button)
            data.lastTime = pygame.time.get_ticks()
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
                        validButton = False
                        if button.main: validButton = True
                        for color in data.drawnButtons.keys():
                            if color!='last' and button in data.drawnButtons[color]: validButton = True
                        if validButton and button.rect.collidepoint(x,y):
                            data.mouseDown = True
                            data.currColor = button.color if button.color else button.lastColor
                            data.currRow, data.currCol = button.row, button.col
                            data.newMouseDown = True
                            data.drawnButtons['last'] = button
                    if button.rect.collidepoint(x,y) and data.mouseDown:
                        if data.newMouseDown:
                            data.newMouseDown = False
                            if not button.isRotating and not button.hasRotated:
                                button.isRotating = True
                                button.rotate()
                            buttonPressColor = button.color if button.color else button.lastColor
                            if button.main and button not in data.drawnLines[buttonPressColor]:
                                data.drawnLines[buttonPressColor] = []
                                while data.drawnButtons[buttonPressColor]:
                                    data.drawnButtons[buttonPressColor][-1].active -= 1
                                    data.drawnButtons[buttonPressColor][-1].img = data.drawnButtons[buttonPressColor][-1].inactiveImg
                                    data.solvedButtons.discard(data.drawnButtons[buttonPressColor][-1])
                                    data.drawnButtons[buttonPressColor].pop()
                                data.drawnButtons[buttonPressColor] = [button]
                                button.active = 1
                                data.solvedButtons.add(button)
                            elif data.drawnButtons[buttonPressColor]:
                                while data.drawnButtons[buttonPressColor][-1] != button:
                                    data.drawnLines[buttonPressColor].pop()
                                    data.drawnButtons[buttonPressColor][-1].active -= 1
                                    data.drawnButtons[buttonPressColor][-1].img = data.drawnButtons[buttonPressColor][-1].inactiveImg
                                    data.solvedButtons.discard(data.drawnButtons[buttonPressColor][-1])
                                    data.drawnButtons[buttonPressColor].pop()
                                    if not data.drawnButtons[buttonPressColor]: break
                        elif ((not button.color or button.color == data.currColor)
                                  and abs(button.row-data.currRow)<=1 and abs(button.col-data.currCol)<=1
                                  and data.drawnButtons['last']!=button):
                            if len(data.drawnButtons[data.currColor])>1 and data.drawnButtons[data.currColor][-2] == button:
                                if not button.isRotating and not button.hasRotated:
                                    button.isRotating = True
                                    button.rotate()
                                data.currRow, data.currCol = button.row, button.col
                                data.drawnButtons[data.currColor][-1].active -= 1
                                data.drawnButtons[data.currColor][-1].img = data.drawnButtons[data.currColor][-1].inactiveImg
                                data.solvedButtons.discard(data.drawnButtons[data.currColor][-1])
                                data.drawnButtons['last'] = button
                                data.drawnButtons[data.currColor].pop()
                                data.drawnLines[data.currColor].pop()
                            if not data.drawnButtons[data.currColor] or data.drawnButtons[data.currColor][-1] != button:
                                lineValid = True
                                newLine = (data.drawnButtons['last'].rect.center, button.rect.center)
                                for key in data.drawnLines.keys():
                                    if newLine in data.drawnLines[key] or (newLine[1], newLine[0]) in data.drawnLines[key]:
                                        lineValid = False
                                if abs(button.row-data.currRow)==1 and abs(button.col-data.currCol)==1:
                                    oldC, newC = data.drawnButtons['last'].rect.center, button.rect.center
                                    if button.row-data.currRow == 1 and button.col-data.currCol == 1:           # Nw -> SE
                                        otherDiag = ((oldC[0]+data.cellSize, oldC[1]), (newC[0]-data.cellSize, newC[1]))
                                    elif button.row-data.currRow == -1 and button.col-data.currCol == -1:       # SE -> NW
                                        otherDiag = ((oldC[0]-data.cellSize, oldC[1]), (newC[0]+data.cellSize, newC[1]))
                                    elif button.row-data.currRow == -1 and button.col-data.currCol == 1:        # SW -> NE
                                        otherDiag = ((oldC[0]+data.cellSize, oldC[1]), (newC[0]-data.cellSize, newC[1]))
                                    elif button.row-data.currRow == 1 and button.col-data.currCol == -1:        # NE -> SW
                                        otherDiag = ((oldC[0]-data.cellSize, oldC[1]), (newC[0]+data.cellSize, newC[1]))
                                    for key in data.drawnLines.keys():
                                        if otherDiag in data.drawnLines[key] or (otherDiag[1], otherDiag[0]) in data.drawnLines[key]:
                                            lineValid = False
                                if button.active < button.passes and lineValid:
                                    if not button.isRotating and not button.hasRotated:
                                        button.isRotating = True
                                        button.rotate()
                                    if not button.color: button.lastColor = data.currColor
                                    data.currRow, data.currCol = button.row, button.col
                                    button.active += 1
                                    data.drawnButtons[data.currColor].append(button)
                                    data.drawnLines[data.currColor].append(newLine)
                                    data.drawnButtons['last'] = button
                                    if button.active == button.passes:
                                        button.img = button.activeImg
                                        data.solvedButtons.add(button)
                    else:
                        if button.hasRotated: button.rotateReset = True

        screen.fill(data.colors[data.theme][-1])

        ##### LINES #####
        for line in data.lineTuples:
            pygame.draw.line(screen, data.colors[data.theme][-2], line[0], line[1], 5)

        for key in data.drawnLines.keys():
            for each in data.drawnLines[key]:
                pygame.draw.line(screen, data.colors[data.theme][key][1], each[0], each[1], 20)

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
                    if each < button.active: screen.blit(data.onImg, onoffImgRect)
                    else: screen.blit(data.offImg, onoffImgRect)

        if len(data.solvedButtons) == data.buttonCount:
            init(data)

        pygame.display.update()

run()
