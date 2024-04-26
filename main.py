def prepareStartGameState():
    gameState=[]
    counters=5
    for i in range(8):
        gameState.append([])
        for l in range(16):
            if(l<counters):
                gameState[i].append('1')
            else:
                gameState[i].append('0')
            
        counters-=1
    countersSaved=0

    arrayToPrepare=[]
    for i in range(8,16):
        if(i==11):
            countersSaved=2
            counters=countersSaved
        
        for l in list(range(16))[::-1]:
            if(counters>0):
                arrayToPrepare.append('2')
                counters-=1
            else:
                arrayToPrepare.append('0')
        if(i>=11):
            countersSaved+=1
            counters=countersSaved
        gameState.append(arrayToPrepare[::-1])
        arrayToPrepare=[]
    return gameState

def printGameState(gameState):
    for y in range(len(gameState)):
        for x in range(len(gameState[y])):
            if(x==0):
                # if(abs(y-15)>=10):
                #     print(f'{abs(y-15)} ||', end= "  ")
                # else:
                #     print(f'{abs(y-15)}  ||', end= "  ")

                if(y>=10):
                    print(f'{y} ||', end= "  ")
                else:
                    print(f'{y}  ||', end= "  ")
            print(gameState[y][x], end="    ")
        print()
    print('__________________________________________________')
    print("   ||  0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15")


def generateAllPossibleMovesInThisRound(whoseMove, gameState):
    for y in range(len(gameState)):
        for x in range(len(y)):

            #szukamy pionka
            if gameState[y][x]==whoseMove:

                #sprawdzamy możliwości jego ruchu
                allCounterMoves = allPossibleMoveForCounter(x, y, whoseMove, gameState)

def allPossibleMoveForCounter(x, y, whoseMove, gameState):
    possibleStates=[]

    #sprawdzamy wszystkie możliwe ruchy i zapisujemy możliwe stany
    while True:

        #ruch w dół o 1
        if y+1<=15:
            possibleStates.append(moveClose(y+1, x, y, x, whoseMove, gameState))
        
        #ruch do góry o 1
        if y-1>=0:
            possibleStates.append(moveClose(y-1, x, y, x, whoseMove, gameState))
        
        #ruch do prawej
        if x+1<=15:
            possibleStates.append(moveClose(y, x+1, y, x, whoseMove, gameState))
        
        #ruch do lewej
        if 0<=x-1:
            possibleStates.append(moveClose(y, x-1, y, x, whoseMove, gameState))
        
        #ruch do lewego górnego rogu
        if 0<=x-1 and 0<=y-1:
            possibleStates.append(moveClose(y-1, x-1, y, x, whoseMove, gameState))

        #ruch do prawego górnego rogu
        if x+1<=15 and y-1<=15:
            possibleStates.append(moveClose(y-1, x+1, y, x, whoseMove, gameState))
        
        #ruch do prawego dolnego rogu
        if x+1<=15 and y+1<=15:
            possibleStates.append(moveClose(y+1, x+1, y, x, whoseMove, gameState))

        #ruch do lewego dolnego rogu
        if x-1<=15 and y+1<=15:
            possibleStates.append(moveClose(y+1, x-1, y, x, whoseMove, gameState))

        #jak daleki skok
        # for up in range(2,15,2):
        
#TODO: sprawdzaj wszystkie możliwe skoki (przeskakiwanie przez następne pionki)

#sprawdza w pętli, jak daleko może skoczyć
def searchAllPossibleJumps(ycurrent, xcurrent, whoseMove, gameState, possibleStates):
    #ruch w dół o 1
        if ycurrent+1<=15:
            possibleStates.append(jump(ycurrent+1, xcurrent, ycurrent, xcurrent, whoseMove, gameState))
        
        #ruch do góry o 1
        if ycurrent-1>=0:
            possibleStates.append(jump(ycurrent-1, xcurrent, ycurrent, xcurrent, whoseMove, gameState))
        
        #ruch do prawej
        if xcurrent+1<=15:
            possibleStates.append(jump(ycurrent, xcurrent+1, ycurrent, xcurrent, whoseMove, gameState))
        
        #ruch do lewej
        if 0<=xcurrent-1:
            possibleStates.append(jump(ycurrent, xcurrent-1, ycurrent, xcurrent, whoseMove, gameState))
        
        #ruch do lewego górnego rogu
        if 0<=xcurrent-1 and 0<=ycurrent-1:
            possibleStates.append(jump(ycurrent-1, xcurrent-1, ycurrent, xcurrent, whoseMove, gameState))

        #ruch do prawego górnego rogu
        if xcurrent+1<=15 and ycurrent-1<=15:
            possibleStates.append(jump(ycurrent-1, xcurrent+1, ycurrent, xcurrent, whoseMove, gameState))
        
        #ruch do prawego dolnego rogu
        if xcurrent+1<=15 and ycurrent+1<=15:
            possibleStates.append(jump(ycurrent+1, xcurrent+1, ycurrent, xcurrent, whoseMove, gameState))

        #ruch do lewego dolnego rogu
        if xcurrent-1<=15 and ycurrent+1<=15:
            possibleStates.append(jump(ycurrent+1, xcurrent-1, ycurrent, xcurrent, whoseMove, gameState))

def checkPossibleMovesInLine():
    pass
#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState):
    
    #sprawdzamy, w jakim kierunku jest ruch
    displacement=[xto-xcurrent, yto-ycurrent]
    # if() ##tu skończyłem

    # if 0<=yto and yto
    if gameState[yto][xto] == '0':
        #możliwy stan
        possibSt=gameState[:]
        possibSt[ycurrent][xcurrent]='0'
        possibSt[yto][xto]=whoseMove

        return possibSt
    
#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def jump(yto, xto, ycurrent, xcurrent, whoseMove, gameState):
    # if 0<=yto and yto
    if gameState[yto][xto] == '0':
        #możliwy stan
        possibSt=gameState[:]
        possibSt[ycurrent][xcurrent]='0'
        possibSt[yto][xto]=whoseMove

        return possibSt
    
def game(gameState):
    players=['1','2']
    whoseTurn=0

    while True:
        printGameState(gameState)

        #player moves
        fromWhereX=int(input('Podaj wsp. x pionka, którego chcesz przesunąć: '))
        fromWhereY=int(input('Podaj wsp. y pionka, którego chcesz przesunąć: '))
        toWhereX=int(input('Podaj wsp. x pola, na które chcesz przesunąć pionek: '))
        toWhereY=int(input('Podaj wsp. y pola, na które chcesz przesunąć pionek: '))

        moveResult=move(toWhereY, toWhereX, fromWhereY, fromWhereX, players[whoseTurn], gameState)
        if(moveResult[1]<1):
            whoseTurn+=1
            whoseTurn%=2
            gameState=moveResult[0]


#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def move(yto, xto, ycurrent, xcurrent, whoseMove, gameState):
    
    #sprawdzamy, w jakim kierunku jest ruch
    displacement=[xto-xcurrent, yto-ycurrent]
    # if() ##tu skończyłem

    # if 0<=yto and yto
    if gameState[yto][xto] == '0' and gameState[ycurrent][xcurrent]==whoseMove:
        #możliwy stan
        possibSt=gameState[:]
        possibSt[ycurrent][xcurrent]='0'
        possibSt[yto][xto]=whoseMove

        return [possibSt, 0]
    else:
        print('Podano nieprawidłowe pola')
        return [gameState,1]


if __name__=='__main__':
    gameState=prepareStartGameState()
    game(gameState)