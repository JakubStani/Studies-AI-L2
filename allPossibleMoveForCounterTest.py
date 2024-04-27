#test dał pozytywny wynik
import copy

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

def printGameState(gameState):
    for y in range(len(gameState)):
        for x in range(len(gameState[y])):
            print(gameState[y][x], end="    ")
        print()
    print('-------------')

if __name__=='__main__':
    testGameState=[['0','0','0','0','0'],['0','0','2','0','0'], ['0','0','2','0','0'], ['0','0','0','0','0'], ['0','0','0','0','0'], ['0','0','0','0','0']]
    printGameState(testGameState)
    print('START-------------')
    allPoss = allPossibleMoveForCounter(2,2,'2',testGameState, False)
    for pos in allPoss:
        printGameState(pos)
        # print('-------------')
    # printGameState(testGameState)
