import numpy as np
import random, copy, string
from utility import *

def drawLine(level, lines, start, curr, target, color):
    DIRS = [(-1,-1) , (-1, 0) , (-1, 1),
            ( 0,-1) ,           ( 0, 1),
            ( 1,-1) , ( 1, 0) , ( 1, 1)]

    if curr == target: return (level, lines)

    order = np.random.permutation(len(DIRS))
    for each in range(len(DIRS)):
        dirc = DIRS[order[each]]
        newPos = (curr[0]+dirc[0], curr[1]+dirc[1])
        if newPos == start: continue
        if newPos[0]>=0 and newPos[1]>=0 and newPos[0]<len(level) and newPos[1]<len(level[0]):
            newPosEntry = level[newPos[0]][newPos[1]]

            if (isinstance(newPosEntry, str) and newPosEntry.isupper() and newPosEntry != color) or newPosEntry==4: continue
            elif (curr, newPos) in lines or (newPos, curr) in lines: continue
            elif abs(dirc[0])==1 and abs(dirc[1])==1:
                otherDiag = ((curr[0], newPos[1]), (newPos[0], curr[1]))
                if otherDiag in lines or (otherDiag[1], otherDiag[0]) in lines: continue
            newLines, newLevel = copy.deepcopy(lines), copy.deepcopy(level)
            newLines.append((curr, newPos))
            if isinstance(newLevel[newPos[0]][newPos[1]], int):
                newLevel[newPos[0]][newPos[1]] += 1
            elif newLevel[newPos[0]][newPos[1]].islower():
                newLevel[newPos[0]][newPos[1]] = 2
            result = drawLine(newLevel, newLines, start, newPos, target, color)
            if result: return result

    return None

def buildLevel(rows, cols, colors):
    level = make2dList(rows, cols, 0)
    lines = []
    mains = []
    levelBuilt = False
    while not levelBuilt:
        levelBuilt = True

        # Init start/end for all colors
        for color in range(colors):
            mains.append([])
            while True:
                start = (random.randint(0,rows-1), random.randint(0,cols-1))
                end = (random.randint(0,rows-1), random.randint(0,cols-1))
                if abs(start[0]-end[0])+abs(start[1]-end[1]) < 3: continue
                elif start!=end and level[start[0]][start[1]]==0 and level[end[0]][end[1]]==0:
                    level[start[0]][start[1]] = chr(color+65)
                    level[end[0]][end[1]] = chr(color+65)
                    mains[color].extend([start, end])
                    break

        # Draw line for each color
        solution = {}
        for color in range(colors):
            result = drawLine(level, lines, mains[color][0], mains[color][0], mains[color][1], chr(color+65))
            if not result:
                level = make2dList(rows, cols, 0)
                lines = []
                mains = []
                levelBuilt = False
                break
            level = copy.deepcopy(result[0])
            lines = copy.deepcopy(result[1])
            solution[chr(color+65)] = copy.deepcopy(result[1])
            for row in range(len(level)):
                for col in range(len(level[0])):
                    if level[row][col] == 1: level[row][col] = chr(color+97)

        if levelBuilt:
            for color in range(colors-1, 0, -1):
                solution[chr(color+65)] = solution[chr(color+65)][len(solution[chr(color+64)]):]

            # Evaluate level
            complexity = 0
            for row in range(len(level)):
                for col in range(len(level[0])):
                    if isinstance(level[row][col], int):
                        complexity += level[row][col] if level[row][col] else -1
            if complexity < (rows+cols):
                level = make2dList(rows, cols, 0)
                lines = []
                mains = []
                levelBuilt = False

    # Write to file
    f = open('level','w')
    for row in range(len(level)):
        for col in range(len(level[0])):
            level[row][col] = str(level[row][col])
        f.write(' '.join(level[row]) + '\n')

    for key in solution.keys():
        print(key, solution[key])
    return solution
