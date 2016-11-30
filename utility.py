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
