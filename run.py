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
        newLevelRow = random.randint(3,5)
        newLevelCol = random.randint(3,5)
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

def newLevelGen(data):
    data.levelGen = LevelThread()
    data.levelGen.start()

def levelGen(data):
    data.level = copy.deepcopy(data.tutLevels[data.tutProgress]) if data.scene==3 else getLevel()
    if data.levelGen: data.solution = copy.deepcopy(data.levelGen.solution)
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
                btnCoord = data.gridCoords[row][col]
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
                data.buttonList[row][col].rect.center = btnCoord

    data.lineTuples = getLineTuples(data)                                       # Generate lines

    data.onoffSize = (int(data.buttonSize[0]*data.ONOFFSCALE), int(data.buttonSize[0]*data.ONOFFSCALE))
    data.onoffOffset = int(data.buttonSize[0]*data.ONOFFOFFSETSCALE)
    data.onImg = pygame.transform.scale(pygame.image.load("assets/on.png").convert_alpha(), data.onoffSize)
    data.offImg = pygame.transform.scale(pygame.image.load("assets/off.png").convert_alpha(), data.onoffSize)
    data.onImg.set_colorkey(None)
    data.offImg.set_colorkey(None)
    data.onoffImgRect = data.onImg.get_rect()

def init(data):
    data.THEMEDEEPSPACE = 0                                                     # CONSTANTS
    data.GRIDMARGIN = 100
    data.CELLMARGIN = 0.6
    data.ONOFFSCALE = 0.2121
    data.ONOFFOFFSETSCALE = 0.153
    data.ONOFFOFFSETLIST = [(-1,0), (1,0), (0,-1), (0,1)]
    data.LINEWIDTH = 5
    data.DRAWNLINEWIDTH = data.LINEWIDTH * 5
    data.SCROLLSPEED = 7

    data.mouseDown = False                                                      # Mouse
    data.scene = 3                                                              # 0: menu; 1: gen; 2: solve; 3: tut
    data.prevScene = 3
    data.transiting = True
    data.transitdX = data.WINSIZE[0]
    data.whiteTransitdX = 0
    data.whitePerc = 0

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

    data.menuButtonSize = (data.WINSIZE[0]//4, data.WINSIZE[0]//20)
    data.menuGenImg = pygame.transform.scale(pygame.image.load("assets/generate.png").convert_alpha(), data.menuButtonSize)
    data.menuGenImg.set_colorkey(None)
    data.menuGenRect = data.menuGenImg.get_rect()
    data.menuGenRect.center = (data.WINSIZE[0]//2, data.WINSIZE[1]//2)

    data.tutLevels = getTutLevels()
    data.tutProgress = 0
    data.first = False

def reset(data):
    data.drawnButtons = {'A': [], 'B': [], 'C': [], 'last': None}
    data.drawnLines = {'A': [], 'B': [], 'C': []}
    data.solvedButtons = set()

def run():
    class Struct(object): pass

    data = Struct()
    # data.WINSIZE = (1920, 1080)
    data.WINSIZE = (1080,720)
    data.lastTime = pygame.time.get_ticks()
    newLevelRow = random.randint(3,5)
    newLevelCol = random.randint(3,5)
    if newLevelCol==5 and newLevelRow==5: newLevelColor = 3
    elif newLevelCol==3 and newLevelRow==3: newLevelColor = 2
    else: newLevelColor = random.randint(2,3)
    data.solution = buildLevel(newLevelRow, newLevelCol, newLevelColor)
    data.levelGen = None
    pygame.init()
    # screen = pygame.display.set_mode(data.WINSIZE, pygame.FULLSCREEN)
    screen = pygame.display.set_mode(data.WINSIZE)
    init(data)
    levelGen(data)
    newLevelGen(data)
    reset(data)

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
                if data.transiting: continue
                if data.scene == 1:
                    data.scene = 0
                    data.transiting = True
                    data.prevScene = 1
                    data.transitdX = 0
                elif data.scene == 0 or data.scene == 3: sys.exit()
            elif event.type == MOUSEBUTTONUP:
                data.mouseDown = False
            elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
                x, y = event.pos
                if data.scene == 0:
                    if data.menuGenRect.collidepoint(x,y) and event.type == MOUSEBUTTONDOWN:
                        data.scene = 1
                        data.first = True
                        data.transiting = True
                        data.prevScene = 0
                        levelGen(data)
                elif data.scene == 1 or data.scene == 3:
                    for button in data.buttons:
                        if event.type == MOUSEBUTTONDOWN:
                            validButton = False
                            if button.main: validButton = True
                            for color in data.drawnButtons.keys():
                                if color!='last' and button in data.drawnButtons[color]: validButton = True
                            if validButton and button.rect.collidepoint(x,y):
                                data.mouseDown = True
                                data.currColor = button.color if button.color else button.lastColor[-1]
                                data.currRow, data.currCol = button.row, button.col
                                data.newMouseDown = True
                                data.drawnButtons['last'] = button
                        if button.rect.collidepoint(x,y) and data.mouseDown:
                            if data.newMouseDown:
                                data.newMouseDown = False
                                if not button.isRotating and not button.hasRotated:
                                    button.isRotating = True
                                    button.rotate()
                                data.currColor = button.color if button.color else button.lastColor[-1]
                                if button.main and button not in data.drawnLines[data.currColor]:
                                    data.drawnLines[data.currColor] = []
                                    while data.drawnButtons[data.currColor]:
                                        if not data.drawnButtons[data.currColor][-1].color:
                                            if (data.drawnButtons[data.currColor][-1].lastColor
                                                and data.drawnButtons[data.currColor][-1].lastColor[-1] == data.currColor):
                                                data.drawnButtons[data.currColor][-1].lastColor.pop()
                                        data.drawnButtons[data.currColor][-1].active -= 1
                                        data.drawnButtons[data.currColor][-1].img = data.drawnButtons[data.currColor][-1].inactiveImg
                                        data.solvedButtons.discard(data.drawnButtons[data.currColor][-1])
                                        data.drawnButtons[data.currColor].pop()
                                    data.drawnButtons[data.currColor] = [button]
                                    button.active = 1
                                    data.solvedButtons.add(button)
                                elif data.drawnButtons[data.currColor]:
                                    while data.drawnButtons[data.currColor][-1] != button:
                                        if not data.drawnButtons[data.currColor][-1].color:
                                            if (data.drawnButtons[data.currColor][-1].lastColor
                                                and data.drawnButtons[data.currColor][-1].lastColor[-1] == data.currColor):
                                                data.drawnButtons[data.currColor][-1].lastColor.pop()
                                        data.drawnLines[data.currColor].pop()
                                        data.drawnButtons[data.currColor][-1].active -= 1
                                        data.drawnButtons[data.currColor][-1].img = data.drawnButtons[data.currColor][-1].inactiveImg
                                        data.solvedButtons.discard(data.drawnButtons[data.currColor][-1])
                                        data.drawnButtons[data.currColor].pop()
                                        if not data.drawnButtons[data.currColor]: break
                            elif ((not button.color or button.color == data.currColor)
                                      and abs(button.row-data.currRow)<=1 and abs(button.col-data.currCol)<=1
                                      and data.drawnButtons['last']!=button):
                                if (len(data.drawnButtons[data.currColor])>1
                                    and data.drawnButtons[data.currColor][0].main
                                    and data.drawnButtons[data.currColor][-1].main):
                                    if button != data.drawnButtons[data.currColor][-2]: continue
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
                                        if not button.color and (not button.lastColor or button.lastColor[-1]!=data.currColor):
                                            button.lastColor.append(data.currColor)
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

        ################################# DRAW #################################

        screen.fill(data.colors[data.theme][-1])

        if data.scene == 0:
            if data.prevScene == 1 or data.prevScene == 3:
                data.transitdX = max(data.transitdX - data.SCROLLSPEED, -data.WINSIZE[0])
                data.newMenuGenRect = copy.copy(data.menuGenRect)
                data.newMenuGenRect.center = (data.menuGenRect.center[0]+data.transitdX+data.WINSIZE[0], data.menuGenRect.center[1])
                screen.blit(data.menuGenImg, data.newMenuGenRect)
                if data.transitdX == -data.WINSIZE[0]:
                    data.transiting = False
                    data.prevScene = 0
                    data.transitdX = data.WINSIZE[0]
            else:
                screen.blit(data.menuGenImg, data.menuGenRect)

        if data.scene==1 or data.scene==3 or data.prevScene==1 or data.prevScene==3:
            if data.transiting:
                # print('transit', data.transitdX, data.whiteTransitdX)
                if data.transitdX > 0: data.transitdX = max(data.transitdX - data.SCROLLSPEED, 0)
                if data.whiteTransitdX > 0: data.whiteTransitdX = max(data.whiteTransitdX - data.SCROLLSPEED, 0)
                if data.prevScene == 0:
                    data.newMenuGenRect = copy.copy(data.menuGenRect)
                    data.newMenuGenRect.center = (data.menuGenRect.center[0]+data.transitdX-data.WINSIZE[0], data.menuGenRect.center[1])
                    screen.blit(data.menuGenImg, data.newMenuGenRect)
                if data.transitdX == 0 or ((data.prevScene==1 or data.prevScene==3) and data.transitdX == -data.WINSIZE[0]):
                    data.transiting = False
                    data.first = False
                    data.whitePerc = 0
                    data.prevScene = 1 if data.scene==1 else 3
                    reset(data)
                    newLevelGen(data)

            ##### LINES #####
            for line in data.lineTuples:
                if data.transiting and data.scene!=0: lineColor = data.colors[data.theme][-2]
                elif data.scene==0: lineColor = data.colors[data.theme][-1]
                else: lineColor = getIntermColor(data.colors[data.theme][-2], data.colors[data.theme][-1], min(data.whitePerc,100))
                lineTop = (line[0][0]+data.transitdX, line[0][1])
                lineBtm = (line[1][0]+data.transitdX, line[1][1])
                pygame.draw.line(screen, lineColor, lineTop, lineBtm, data.LINEWIDTH)

            if not data.transiting:
                for key in data.drawnLines.keys():
                    for each in data.drawnLines[key]:
                        pygame.draw.line(screen, data.colors[data.theme][key][1], each[0], each[1], data.DRAWNLINEWIDTH)

            ##### MOUSE FOLLOWERS #####
            if data.mouseDown:
                flwClr = data.colors[data.theme][data.currColor][1]
                alphaColor = (flwClr[0], flwClr[1], flwClr[2], 128)
                flwSize = (data.buttonSize[0]*2, data.buttonSize[1]*2)
                flwSurface = pygame.Surface(flwSize, pygame.SRCALPHA)
                flwSurface.fill(alphaColor)
                screen.blit(flwSurface, (x-flwSize[0]//2, y-flwSize[1]//2))

            ##### BUTTONS #####
            if not (data.prevScene==3 and data.scene==0):
                for button in data.buttons:
                    if button.rotateReset:                                          # Prevent rotating while rotating
                        if button.hasRotated: button.hasRotated -= 1
                        else: button.rotateReset = False

                    if not button.isRotating:                                       # Draw button
                        transitRect = copy.copy(button.rect)
                        transitRect.center = (transitRect.center[0]+data.transitdX, transitRect.center[1])
                        screen.blit(button.img, transitRect)
                    else:
                        button.rotate()
                        screen.blit(button.rotatedImg, button.rotatedRect)

                    if button.passes > 1:                                           # Draw On/Off
                        for each in range(button.passes):
                            onoffImgCenter = (button.rect.center[0]+(data.ONOFFOFFSETLIST[each][0]*data.onoffOffset) + data.transitdX,
                                              button.rect.center[1]+(data.ONOFFOFFSETLIST[each][1]*data.onoffOffset))
                            onoffImgRect = data.onoffImgRect
                            onoffImgRect.center = onoffImgCenter
                            if each < button.active: screen.blit(data.onImg, onoffImgRect)
                            else: screen.blit(data.offImg, onoffImgRect)

            if len(data.solvedButtons) == data.buttonCount:
                if data.scene == 3 and not (data.transiting or data.whitePerc):
                    data.tutProgress += 1
                white = data.colors[data.theme]['W'][0]
                data.oldDrawnLines = copy.deepcopy(data.drawnLines)
                data.oldButtonList = copy.deepcopy(data.buttonList)
                data.oldLevelHeight = copy.copy(data.levelHeight)
                data.oldLevelWidth = copy.copy(data.levelWidth)
                if not data.whiteTransitdX: data.whiteTransitdX = data.WINSIZE[0]
                if data.whitePerc <= 100:
                    data.whitePerc += 1.5
                else:
                    if data.scene==3 and data.tutProgress == len(data.tutLevels):
                        data.scene = 0
                    data.transitdX = data.WINSIZE[0]
                    data.transiting = True
                    levelGen(data)

            if not data.first and data.whitePerc:
                for key in data.oldDrawnLines.keys():
                    for line in data.oldDrawnLines[key]:
                        whiteColor = getIntermColor(data.colors[data.theme][-2], white, min(data.whitePerc,100))
                        lineTop = (line[0][0]+data.whiteTransitdX-data.WINSIZE[0], line[0][1])
                        lineBtm = (line[1][0]+data.whiteTransitdX-data.WINSIZE[0], line[1][1])
                        pygame.draw.line(screen, whiteColor, lineTop, lineBtm, data.DRAWNLINEWIDTH)
                for row in range(data.oldLevelHeight):
                    for col in range(data.oldLevelWidth):
                        if data.oldButtonList[row][col]:
                            btnRect = copy.copy(data.oldButtonList[row][col].rect)
                            btnRect.center = (btnRect.center[0]+data.whiteTransitdX-data.WINSIZE[0], btnRect.center[1])
                            if data.oldButtonList[row][col].color:
                                btnColor = data.colors[data.theme][data.oldButtonList[row][col].color][1]
                                whiteColor = getIntermColor(btnColor, white, min(data.whitePerc,100))
                                btnRect = (btnRect.left, btnRect.top, btnRect.width, btnRect.height)
                                pygame.draw.rect(screen, whiteColor, btnRect)
                            else:
                                octCtr, octHgt, octWid = btnRect.center, btnRect.height, btnRect.width
                                xCoords = (octCtr[0]-octWid//2, octCtr[0]-((2**0.5-1)/2)*octWid,
                                            octCtr[0]+((2**0.5-1)/2)*octWid, octCtr[0]+octWid//2)
                                yCoords = (octCtr[1]-octHgt//2, octCtr[1]-((2**0.5-1)/2)*octHgt,
                                            octCtr[1]+((2**0.5-1)/2)*octHgt, octCtr[1]+octHgt//2)
                                octCoords = ((xCoords[0], yCoords[1]), (xCoords[1], yCoords[0]),
                                             (xCoords[2], yCoords[0]), (xCoords[3], yCoords[1]),
                                             (xCoords[3], yCoords[2]), (xCoords[2], yCoords[3]),
                                             (xCoords[1], yCoords[3]), (xCoords[0], yCoords[2]))
                                whiteColor = getIntermColor(data.colors[data.theme]['W'][1], white, min(data.whitePerc, 100))
                                pygame.draw.polygon(screen, whiteColor, octCoords)

        pygame.display.update()

run()
