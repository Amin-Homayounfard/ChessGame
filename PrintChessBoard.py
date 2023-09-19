from os import system, name

class bcolors:
    HEADER = "\033[95m" 
    OKBLUE = "\033[94m" 
    OKCYAN = "\033[96m" 
    OKGREEN = "\033[92m" 
    WARNING = "\033[93m"  
    FAIL = "\033[91m"  
    ENDC = "\033[0m"  
    BOLD = "\033[1m"  
    UNDERLINE = "\033[4m" 


def clearConsole():
    if name == 'nt': system('cls')
    else: system('clear')

def printHeader(color=bcolors.ENDC):
    print(color + " --- ", end="")


def printBox(i, j, color=bcolors.ENDC, marble=" ", marbleColor=bcolors.ENDC):
    if not j:
        print(bcolors.HEADER, 8-i, bcolors.ENDC,  end= "")
    print(color + "| " + marbleColor + marble + color + " |", end="")
    if j!=7:
        print(end=' ')
    if j==7:
        print(bcolors.HEADER, 8-i, bcolors.ENDC,  end= "")


def secondLine():
    print(end= "   ")
    for i in range(8):
        if i % 2 == 0:
            printHeader(bcolors.OKBLUE)
        else:
            printHeader()
        print(end=' ')
    print()


def firstLine():
    print(end= "   ")
    for i in range(8):
        if i % 2 == 1:
            printHeader(bcolors.OKBLUE)
        else:
            printHeader()
        print(end=' ')
    print()

def printChessBoard(chessboard):
    clearConsole()
    print(bcolors.HEADER, "    A     B     C     D     E     F     G     H", bcolors.ENDC)
    for i in range(8):
        if i % 2 == 0:
            firstLine()
            for j in range(8):
                m = " " if len(chessboard[7 - i][j]) == 0 else chessboard[7 - i][j][0]
                mc = bcolors.ENDC
                if len(chessboard[7 - i][j]) != 0 and chessboard[7 - i][j][1] == "b":
                    mc = bcolors.OKBLUE
                if j % 2 == 0:
                    printBox(i, j, marble=m, marbleColor=mc)
                else:
                    printBox(i, j, bcolors.OKBLUE, marble=m, marbleColor=mc)
            print()
            firstLine()
        else:
            secondLine()
            for j in range(8):
                m = " " if len(chessboard[7 - i][j]) == 0 else chessboard[7 - i][j][0]
                mc = bcolors.ENDC
                if len(chessboard[7 - i][j]) != 0 and chessboard[7 - i][j][1] == "b":
                    mc = bcolors.OKBLUE
                if j % 2 == 0:
                    printBox(i, j, bcolors.OKBLUE, m, marbleColor=mc)
                else:
                    printBox(i, j, marble=m, marbleColor=mc)
            print()
            secondLine()
    print(bcolors.HEADER, "    A     B     C     D     E     F     G     H", bcolors.ENDC)



