import string, copy
from utility import *

def findAllPaths(level, lines, color):
    DIRS = [(-1,-1) , (-1, 0) , (-1, 1),
            ( 0,-1) ,           ( 0, 1),
            ( 1,-1) , ( 1, 0) , ( 1, 1)]
    pathList = []
    bfsQueue = []
    start, end = findStartEnd(level, color)
    path = make2dList(len(level), len(level[0]), 0)
    path[start[0]][start[1]], path[end[0]][end[1]] = color, color
    bfsQueue.append((path, lines, start))
    while bfsQueue:
        path, lines, curr = copy.deepcopy(bfsQueue[0][0]), copy.deepcopy(bfsQueue[0][1]), bfsQueue[0][2]
        for dirc in DIRS:
            newPos = (curr[0]+dirc[0], curr[1]+dirc[1])
            if newPos[0]>=0 and newPos[1]>=0 and newPos[0]<len(level) and newPos[1]<len(level[0]):
                newPosEntry = level[newPos[0]][newPos[1]]
                if newPos == end:
                    newLines, newPath = copy.deepcopy(lines), copy.deepcopy(path)
                    newLines.append((curr, newPos))
                    for row in range(len(newPath)):
                        for col in range(len(newPath[0])):
                            if newPath[row][col] == 1: newPath[row][col] = color.lower()
                    toAppend = True
                    for each in pathList:
                        if newPath == each[0]:
                            if set(newLines) == set(each[1]): toAppend = False
                    if toAppend: pathList.append((newPath, newLines))
                else:
                    if path[newPos[0]][newPos[1]] == newPosEntry: continue
                    elif (isinstance(newPosEntry, str) and newPosEntry.islower()) and path[newPos[0]][newPos[1]]==1: continue
                    elif (isinstance(newPosEntry, str) and newPosEntry.upper() != color) or newPosEntry==0: continue
                    elif (curr, newPos) in lines or (newPos, curr) in lines: continue
                    elif abs(dirc[0])==1 and abs(dirc[1])==1:
                        otherDiag = ((curr[0], newPos[1]), (newPos[0], curr[1]))
                        if otherDiag in lines or (otherDiag[1], otherDiag[0]) in lines: continue
                    newLines, newPath = copy.deepcopy(lines), copy.deepcopy(path)
                    newLines.append((curr, newPos))
                    newPath[newPos[0]][newPos[1]] += 1
                    bfsQueue.append((newPath, newLines, newPos))
        bfsQueue.pop(0)
    return pathList

def subtractPath(level, path):
    for row in range(len(level)):
        for col in range(len(level[0])):
            if level[row][col]==path[row][col]:
                level[row][col]=0
            elif ((isinstance(level[row][col], int) and level[row][col]>0)
                 and (isinstance(path[row][col], str) and path[row][col].islower())):
                level[row][col]-=1
            elif isinstance(path[row][col], int) and path[row][col]>0:
                level[row][col]-=path[row][col]
    return level

def solve(all=False):

    def findAllSolutions(level, colors):
        pass

    def findOneSolution(level, lines, colors, curr=0, soln=None):
        if soln==None: soln = {}
        if curr==colors:
            return soln if level==make2dList(len(level),len(level[0]),0) else None
        color = chr(curr+65)
        pathList = findAllPaths(level, lines, color)
        for path in pathList:
            newSoln = copy.deepcopy(soln)
            newSoln[color] = copy.deepcopy(path)
            newLevel = copy.deepcopy(level)
            subtractPath(newLevel, path[0])
            newLines = lines + path[1]
            result = findOneSolution(newLevel, newLines, colors, curr=curr+1, soln=newSoln)
            if result: return result

        return None

    level = getLevel('solve')
    lines = []
    colors = getColorNum(level)
    sols = []

    if all: return findAllSolutions(level, colors)
    else:
        pathList = findOneSolution(level, lines, colors)
        solution = {}
        for key in pathList.keys():
            solution[key] = copy.deepcopy(pathList[key][1])
        for color in range(colors-1, 0, -1):
            solution[chr(color+65)] = solution[chr(color+65)][len(solution[chr(color+64)]):]
        return solution

print(solve())
