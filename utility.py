import string, copy

################################## UTILITIES ###################################

def make2dList(rows, cols, val=None):
    a = [[val]*cols for row in range(rows)]
    return a

def get2dIndex(L, obj):
    for each in range(len(L)):
        if obj in L[each]:
            return (each, L[each].index(obj))

def prettyPrint(*args):
    for L in args:
        for row in L:
            print(row)
        print("-----")

def getIntermColor(color1, color2, perc):
    dR = color2[0]-color1[0]
    dG = color2[1]-color1[1]
    dB = color2[2]-color1[2]
    perc /= 100
    return (int(color1[0]+dR*perc), int(color1[1]+dG*perc), int(color1[2]+dB*perc))

############################### END OF UTILITIES ###############################



######################## LEVEL IMPORTING & VERIFICATION ########################

def verifyLevel(level):                                                         # As name suggests
    # Rectangular, mains occur twice each, soln exists
    levelHeight, levelWidth = len(level), len(level[0])
    for line in range(levelHeight):                                             # Check level is rectangular
        if len(level[line]) != levelWidth:
            raise Exception("Invalid level: Remember to add '0's for empty cells!")

def getLevel():
    level = []
    levelString = open('level','r').read()                                      # Load level
    for line in levelString.splitlines():
        level.append([])
        for char in line.split(' '):
            if char.isdigit(): level[-1].append(int(char))
            else: level[-1].append(char)
    verifyLevel(level)
    return level

def getTutLevels():
    tutLevels = []
    levelString = open('tutorial','r').read()                                   # Load tutorial
    for line in levelString.splitlines():
        level1D = line[line.find(' ', line.find(' ')+1)+1:].split(' ')
        levelRows = int(line[0:line.find(' ')])
        levelCols = int(line[line.find(' ')+1:line.find(' ', line.find(' ')+1)])
        level = make2dList(levelRows, levelCols)
        for row in range(levelRows):
            for col in range(levelCols):
                entry = level1D[row*levelCols + col]
                if entry.isdigit(): entry = int(entry)
                level[row][col] = entry
        verifyLevel(level)
        tutLevels.append(level)
    return tutLevels

def getColorNum(level):                                                         # Get number of colors (A,B,C...)
    colors = set()
    for row in range(len(level)):
        for col in range(len(level[0])):
            if isinstance(level[row][col], str) and level[row][col].isupper():
                colors.add(level[row][col])
    return len(colors)

def findStartEnd(level, color):                                                 # Find start & end mains of given color
    start, end = None, None
    for row in range(len(level)):
        for col in range(len(level[0])):
            if level[row][col] == color:
                if not start: start = (row, col)
                else: end = (row, col); return start, end
    raise Exception('Start and End not both present.')


#################### END OF LEVEL IMPORTING & VERIFICATION #####################
