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

def getLevel():
    levelList = []
    level = open('level','r').read()                                            # Load level
    for line in level.splitlines():
        levelList.append([])
        for char in line.split(' '):
            levelList[-1].append(char)
    levelHeight, levelWidth = len(levelList), len(levelList[0])
    for line in range(levelHeight):                                             # Check level is rectangular
        if len(levelList[line]) != levelWidth:
            raise Exception("Invalid level: Remember to add '0's for empty cells!")
    return levelList
