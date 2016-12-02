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

############################### END OF UTILITIES ###############################



######################## LEVEL IMPORTING & VERIFICATION ########################

def getLevel():
    level = []
    levelString = open('level','r').read()                                            # Load level
    for line in levelString.splitlines():
        level.append([])
        for char in line.split(' '):
            if char.isdigit(): level[-1].append(int(char))
            else: level[-1].append(char)
    verifyLevel(level)
    return level

def getColorNum(level):
    colors = set()
    for row in range(len(level)):
        for col in range(len(level[0])):
            if isinstance(level[row][col], str) and level[row][col].isupper():
                colors.add(level[row][col])
    return len(colors)

def findStartEnd(level, color):
    start, end = None, None
    for row in range(len(level)):
        for col in range(len(level[0])):
            if level[row][col] == color:
                if not start: start = (row, col)
                else: end = (row, col); return start, end
    raise Exception('Start and End not both present.')

def verifyLevel(level):
    # Rectangular, mains occur twice each, soln exists
    levelHeight, levelWidth = len(level), len(level[0])
    for line in range(levelHeight):                                             # Check level is rectangular
        if len(level[line]) != levelWidth:
            raise Exception("Invalid level: Remember to add '0's for empty cells!")

#################### END OF LEVEL IMPORTING & VERIFICATION #####################
