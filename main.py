import copy

def prepareStartGameState():
    countersDict= dict()
    gameState=[]
    counters=5
    for y in range(8):
        gameState.append([])
        for x in range(16):
            if(x<counters):
                gameState[y].append('1')
                # countersDict[f'{x}-{y}']=
            else:
                gameState[y].append('0')
        if 0<y and y<4:
            counters-=1
        else:
            if y>=4:
                counters=0
    countersSaved=0

    arrayToPrepare=[]
    for y in range(8,16):
        if(y==11):
            counters=2
        
        for x in list(range(16))[::-1]:
            if(11<=y and x>15-counters):
                arrayToPrepare.append('2')
            else:
                arrayToPrepare.append('0')
        if(y>=11 and y<14):
            counters+=1
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

def allPossibleMoveForCounter(x, y, whoseMove, gameState, jumpOnly):
    possibleStates=[]

    #sprawdzamy wszystkie możliwe ruchy i zapisujemy możliwe stany
    while True:

        if(whoseMove=='1'):
            #ruch w dół o 1
            possibleStates=moveInDirection(y+1,x,y,x,whoseMove,gameState,possibleStates, jumpOnly)

            #ruch do prawego dolnego rogu
            possibleStates=moveInDirection(y+1,x+1,y,x,whoseMove,gameState,possibleStates, jumpOnly)
            
            #ruch do prawej
            possibleStates=moveInDirection(y,x+1,y,x,whoseMove,gameState,possibleStates, jumpOnly)

        else:
            #ruch do góry o 1
            possibleStates=moveInDirection(y-1,x,y,x,whoseMove,gameState,possibleStates, jumpOnly)
            
            #ruch do lewej
            possibleStates=moveInDirection(y,x-1,y,x,whoseMove,gameState,possibleStates, jumpOnly)
            
            #ruch do lewego górnego rogu
            possibleStates=moveInDirection(y-1,x-1,y,x,whoseMove,gameState,possibleStates, jumpOnly)
        
        #ruch do prawego górnego rogu
        possibleStates=moveInDirection(y-1,x+1,y,x,whoseMove,gameState,possibleStates, jumpOnly)

        #ruch do lewego dolnego rogu
        possibleStates=moveInDirection(y+1,x-1,y,x,whoseMove,gameState,possibleStates, jumpOnly)

        return possibleStates

        #jak daleki skok
        # for up in range(2,15,2):

#pozwala na rekurencyjne sprawdzanie możliwych ruchów
def moveInDirection(yto,xto,ycurrent,xcurrent,whoseMove,gameState, possibleStates, jumpOnly):
    #ruch w dół o 1
    if 0<=yto and yto<=15 and 0<=xto and xto<=15:
        #sprawdzamy, w jakim kierunku jest ruch
        displacement=[xto-xcurrent, yto-ycurrent]
        if gameState[yto][xto] == '0' and not jumpOnly:
            possibleStates.append(moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState))
        else:
            if not gameState[yto][xto] == '0':
                #sprawdzamy, czy skok będzie jeszcze w granicy planszy
                if 0<=yto + displacement[1] and yto + displacement[1]<= 15 and 0<=xto + displacement[0] and xto + displacement[0]<=15:
                    if gameState[yto + displacement[1]][xto + displacement[0]] == '0':
                        possibleStates.append(moveClose(yto + displacement[1], xto + displacement[0], ycurrent, xcurrent, whoseMove, gameState))
                        newStates=allPossibleMoveForCounter(xto + displacement[0], yto + displacement[1], whoseMove, gameState, True)
                        possibleStates.extend(newStates)
    return possibleStates

#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState):
    possibSt=copy.deepcopy(gameState)
    # possibSt=gameState[:]
    # if() ##tu skończyłem

    # if 0<=yto and yto
    if gameState[yto][xto] == '0':
        #możliwy stan
        possibSt[ycurrent][xcurrent]='0'
        possibSt[yto][xto]=whoseMove
    return possibSt
        
#TODO: sprawdzaj wszystkie możliwe skoki (przeskakiwanie przez następne pionki)

# #sprawdza w pętli, jak daleko może skoczyć
# def searchAllPossibleJumps(ycurrent, xcurrent, whoseMove, gameState, possibleStates):
#     #ruch w dół o 1
#         if ycurrent+1<=15:
#             possibleStates.append(jump(ycurrent+1, xcurrent, ycurrent, xcurrent, whoseMove, gameState))
        
#         #ruch do góry o 1
#         if ycurrent-1>=0:
#             possibleStates.append(jump(ycurrent-1, xcurrent, ycurrent, xcurrent, whoseMove, gameState))
        
#         #ruch do prawej
#         if xcurrent+1<=15:
#             possibleStates.append(jump(ycurrent, xcurrent+1, ycurrent, xcurrent, whoseMove, gameState))
        
#         #ruch do lewej
#         if 0<=xcurrent-1:
#             possibleStates.append(jump(ycurrent, xcurrent-1, ycurrent, xcurrent, whoseMove, gameState))
        
#         #ruch do lewego górnego rogu
#         if 0<=xcurrent-1 and 0<=ycurrent-1:
#             possibleStates.append(jump(ycurrent-1, xcurrent-1, ycurrent, xcurrent, whoseMove, gameState))

#         #ruch do prawego górnego rogu
#         if xcurrent+1<=15 and ycurrent-1<=15:
#             possibleStates.append(jump(ycurrent-1, xcurrent+1, ycurrent, xcurrent, whoseMove, gameState))
        
#         #ruch do prawego dolnego rogu
#         if xcurrent+1<=15 and ycurrent+1<=15:
#             possibleStates.append(jump(ycurrent+1, xcurrent+1, ycurrent, xcurrent, whoseMove, gameState))

#         #ruch do lewego dolnego rogu
#         if xcurrent-1<=15 and ycurrent+1<=15:
#             possibleStates.append(jump(ycurrent+1, xcurrent-1, ycurrent, xcurrent, whoseMove, gameState))
        

# def checkPossibleMovesInLine():
#     pass
    
# #wykonuje ruch w określonym kierunku i zwraca stan po ruchu
# def jump(yto, xto, ycurrent, xcurrent, whoseMove, gameState):
#     # if 0<=yto and yto
#     if gameState[yto][xto] == '0':
#         #możliwy stan
#         possibSt=gameState[:]
#         possibSt[ycurrent][xcurrent]='0'
#         possibSt[yto][xto]=whoseMove

#         return possibSt
    
def game(gameState):
    players=['1','2']
    whoseTurn=0
    turn=1

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
            turn+=1


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
    
def areGameStatesTheSame(gameState1, gameState2):
    for i in range(len(gameState1)):
        if not gameState1[i]==gameState2[i]:
            return False
    return True

#mają być przynajmniej 3 różne implementacje heurystyki
if __name__=='__main__':
    gameState=prepareStartGameState()
    printGameState(gameState)
    print('START-------------')
    allPoss = allPossibleMoveForCounter(4,0,'1',gameState, False)
    for pos in allPoss:
        printGameState(pos)
    # game(gameState)