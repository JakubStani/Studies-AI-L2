import copy
from counter import Counter
from node import Node 
import math
from colorama import Fore

maxDepth=3

def prepareStartGameState():
    gameState={
        'gameboardState': [],
        'counters': {'1':dict(), '2': dict()}
        }
    counters=5
    for y in range(8):
        gameState['gameboardState'].append([])
        for x in range(16):
            if(x<counters):
                gameState['gameboardState'][y].append('1')
                gameState['counters']['1'][f'{x}-{y}-1']= Counter(x, y, '1')

            else:
                gameState['gameboardState'][y].append('0')
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
                gameState['counters']['2'][f'{x}-{y}-2']= Counter(x, y, '2')
            else:
                arrayToPrepare.append('0')
        if(y>=11 and y<14):
            counters+=1
        gameState['gameboardState'].append(arrayToPrepare[::-1])
        arrayToPrepare=[]
    return gameState

def printGameboardState(gameboardState):
    for y in range(len(gameboardState)):
        for x in range(len(gameboardState[y])):
            if(x==0):
                # if(abs(y-15)>=10):
                #     print(f'{abs(y-15)} ||', end= "  ")
                # else:
                #     print(f'{abs(y-15)}  ||', end= "  ")
                if(y>=10):
                    print(f'{Fore.YELLOW}{y}{Fore.YELLOW}||', end= "  ")
                else:
                    print(f'{Fore.YELLOW}{y}{Fore.YELLOW} ||', end= "  ")
            color = Fore.BLUE
            if gameboardState[y][x]=='2':
                color = Fore.RED
            if gameboardState[y][x]=='0':
                color = Fore.WHITE
            
            print(f'{color}{gameboardState[y][x]}', end="    ")
        print()
    print(f'{Fore.YELLOW}__________________________________________________')
    print("  ||  0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15")
    print(Fore.WHITE)
def printAllChildrenStates(parentNode):
    if(not parentNode._children()==None):
        for i in range(len(parentNode._children())):
            print(f'dziecko: {i}')
            printGameboardState(parentNode._children()[i]._gameState()['gameboardState'])
            print()

#UWAGA!: trwa baaardzo długo, ponieważ drzewo jest gromne
def printWholeTreeStates(parentNode):
    if(not parentNode._children()==None):
        print(f'______________RUNDA: {parentNode._round()}_________')
        for i in range(len(parentNode._children())):
            if(parentNode._round()==1):
                print(f'dziecko: {i}')
                printGameboardState(parentNode._children()[i]._gameState()['gameboardState'])
                print()
            printWholeTreeStates(parentNode._children()[i])

def printAllTreeLeafs(parentNode):
    if(not parentNode._children()==None):
        for i in range(len(parentNode._children())):
            printAllTreeLeafs(parentNode._children()[i])
    else:
        print(f'______________RUNDA: {parentNode._round()}_________')
        printGameboardState(parentNode._gameState()['gameboardState'])

def printOneLeaf(parentNode):
    if(not parentNode._children()==None):
        printOneLeaf(parentNode._children()[0])
    else:
        print(f'______________RUNDA: {parentNode._round()}_________')
        printGameboardState(parentNode._gameState()['gameboardState'])





#na wejściu jest parent, który ma już dzieci
#podana runda, to runda, która zostanie przypisana dzieciom parentNoda
def generatePossibleMovesTree(whoseMove, gameState, parentNode, round, minPlayer, maxPlayer):
    global maxDepth
    if not parentNode._children() == None and round <maxDepth: #TODO: ustaw jakąś zmienną na maksymalną głębokość
        for child in parentNode._children():
            generateAllPossibleMovesInThisRound(whoseMove, child._gameState(), child, round+1, minPlayer, maxPlayer)
            nextWhoseMove=str((int(whoseMove)%2)+1)
            generatePossibleMovesTree(nextWhoseMove, child._gameState(), child, round+1, minPlayer, maxPlayer)

            # break #Można odkomentować, aby szybko móc zobaczyć skrajny wymnik dla dużej głębokości

    else: #TODO: sprawdź i ustaw, kto wygrał
        pass

#TODO: pozbądź siękluczy współrzędnych pionków (bo one będą sięzmieniać) i zmieniaj współrzędne pionka po jego ruchu
#na wejściu jest parent, który nie ma dzieci
def generateAllPossibleMovesInThisRound(whoseMove, gameState, parentNode, round, minPlayer, maxPlayer):

    #sprawdzamy dalej możliwe ruchy tylko wtedy, gdy dany parentNode nie reprezentuje stanu zakończonej gry
    if parentNode._whoWon()=='0':
        allPossibleMoves=[]
        for counter in list(gameState['counters'][whoseMove]):
            #sprawdzamy możliwości jego ruchu -> allCounterMoves to lista węzłów
            allCounterMoves = allPossibleMoveForCounter(gameState['counters'][whoseMove][counter]._x(), gameState['counters'][whoseMove][counter]._y(), whoseMove, gameState, False, parentNode, round, gameState['counters'][whoseMove][counter]._x(), gameState['counters'][whoseMove][counter]._y())
            allPossibleMoves.extend(allCounterMoves)
        
        parentNode.setChildren(allPossibleMoves)

def allPossibleMoveForCounter(x, y, whoseMove, gameState, jumpOnly, parentNode, round, previousX, previousY):
    possibleStates=[]

    #sprawdzamy wszystkie możliwe ruchy i zapisujemy możliwe stany
    while True:

        if(whoseMove=='1'):
            #ruch w dół o 1
            possibleStates=moveInDirection(y+1,x,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)

            #ruch do prawego dolnego rogu
            possibleStates=moveInDirection(y+1,x+1,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)
            
            #ruch do prawej
            possibleStates=moveInDirection(y,x+1,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)

        else:
            #ruch do góry o 1
            possibleStates=moveInDirection(y-1,x,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)
            
            #ruch do lewej
            possibleStates=moveInDirection(y,x-1,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)
            
            #ruch do lewego górnego rogu
            possibleStates=moveInDirection(y-1,x-1,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)
        
        #ruch do prawego górnego rogu
        possibleStates=moveInDirection(y-1,x+1,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)

        #ruch do lewego dolnego rogu
        possibleStates=moveInDirection(y+1,x-1,y,x,whoseMove,gameState,possibleStates, jumpOnly, parentNode, round, previousX, previousY)

        return possibleStates

        #jak daleki skok
        # for up in range(2,15,2):
#TODO: napraw nieustanne skakanie po przekątnej
#pozwala na rekurencyjne sprawdzanie możliwych ruchów
def moveInDirection(yto,xto,ycurrent,xcurrent,whoseMove,gameState, possibleStates, jumpOnly, parentNode, round, previousX, previousY):

    #warunek chroniący przed zapętleniem-> wykonaniem ruchu w miejsce, w którym było się przed chwilą
    if(not yto==previousY or not xto == previousX):

        #ruch w dół o 1
        if 0<=yto and yto<=15 and 0<=xto and xto<=15:
            #sprawdzamy, w jakim kierunku jest ruch
            displacement=[xto-xcurrent, yto-ycurrent]
            if gameState['gameboardState'][yto][xto] == '0' and not jumpOnly:
                possibleStates.append(moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState, parentNode, round))
            else:
                if not gameState['gameboardState'][yto][xto] == '0':
                    #sprawdzamy, czy skok będzie jeszcze w granicy planszy
                    if 0<=yto + displacement[1] and yto + displacement[1]<= 15 and 0<=xto + displacement[0] and xto + displacement[0]<=15:
                        if gameState['gameboardState'][yto + displacement[1]][xto + displacement[0]] == '0': #TODO: napraw skakanie w to samo miejsce (bo po przekątnej)
                            nState=moveClose(yto + displacement[1], xto + displacement[0], ycurrent, xcurrent, whoseMove, gameState, parentNode, round)
                            possibleStates.append(nState)
                            previousX = xto
                            previousY = yto
                            newStates=allPossibleMoveForCounter(xto + displacement[0], yto + displacement[1], whoseMove, nState._gameState(), True, parentNode, round, previousX, previousY)
                            possibleStates.extend(newStates)
    return possibleStates

#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState, parentNode, round):
    possibSt=copy.deepcopy(gameState) #TUTAJ można ustalić, co będzie przechowywane w węzłach drzewa (jakie dane)
    # possibSt=gameState[:]
    # if() ##tu skończyłem

    # if 0<=yto and yto
    if gameState['gameboardState'][yto][xto] == '0':
        #możliwy stan
        possibSt['gameboardState'][ycurrent][xcurrent]='0'
        possibSt['gameboardState'][yto][xto]=whoseMove

        #przesunięcie pionka
        del possibSt['counters'][whoseMove][f'{xcurrent}-{ycurrent}-{whoseMove}']
        newCounter = Counter(xto, yto, whoseMove)
        possibSt['counters'][whoseMove][f'{xto}-{yto}-{whoseMove}'] = newCounter

    #przekształcamy wynik na węzeł

    #sprawdzenie, czy gracz, który ma ruch wygrał
    whoWon='0'
    if(checkWin(whoseMove, possibSt['gameboardState'])):
        whoWon=whoseMove

    return Node(round, whoseMove, possibSt, whoWon, parentNode, None, round, calculateHeuristicValue, parentNode._heuristicType()) #TODO: zmień dwie funkcje liczące heurystyki na właściwą wartość
        
def testDoNothing(arg1, arg2):
    pass
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
        printGameboardState(gameState)

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
def move(yto, xto, ycurrent, xcurrent, whoseMove, gameboardState):


    displacement=[xto-xcurrent, yto-ycurrent]
    #funkcja move jest przewidziana tylko dla gracza 1., więc 
    if not (displacement[0]<0 and displacement[1]<=0 or displacement[1]<0 and displacement[0]<=0):

        # if 0<=yto and yto
        if gameboardState[yto][xto] == '0' and gameboardState[ycurrent][xcurrent]==whoseMove:
            #możliwy stan
            possibSt=copy.deepcopy(gameboardState)
            possibSt[ycurrent][xcurrent]='0'
            possibSt[yto][xto]=whoseMove


            return [possibSt, 0]

    print('Podano nieprawidłowe pola')
    return [gameboardState,1]
    
def areGameStatesTheSame(gameState1, gameState2):
    for i in range(len(gameState1)):
        if not gameState1[i]==gameState2[i]:
            return False
    return True

def checkWin(player, gameStateToCheck):
    #górny lewy róg planszy
    if player=='2':
        counters=5
        for y in range(5):
            # gameState['gameboardState'].append([])
            for x in range(counters):
                if not gameStateToCheck[y][x]=='2':
                    return False
            if 0<y:
                counters-=1
        return True
    
    #dolny prawy róg planszy
    else:
        counters=5
        for y in reversed(range(11, 16)):
            # gameState['gameboardState'].append([])
            for x in reversed(range(16-counters, 16)):
                if not gameStateToCheck[y][x]=='1':
                    return False
            if y<15:
                counters-=1
        return True
    

##heurystyki
#TODO: dodaj możliwość łatwego wyboru heurystyki

centerOfMass=None
def calculateHeuristicValue(player, gameState, heuristicType):
    if not player==None:
        sumOfDistances=0
        numOfCounters=len(list(gameState['counters'][player]))
        
        #pierwsza heurystyka
        if(heuristicType=='AvgDistToLeftUpperCorner'):
            for counter in list(gameState['counters'][player]):
                sumOfDistances+= counterDistanceToCorner(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toLeftUpperCorner')

        #druga heurystyka
        elif(heuristicType=='AvgDistToRightBottomCorner'):
            for counter in list(gameState['counters'][player]):
                sumOfDistances+= counterDistanceToCorner(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toRightBottomCorner')

        #trzecia heurystyka
        elif(heuristicType=='AvgDistToLeftUpperCornerBorder'):
            for counter in list(gameState['counters'][player]):
                sumOfDistances+= counterDistanceToStartingBorders(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toLeftUpperCornerBorder')
        
        #czwarta heurystyka
        elif(heuristicType=='CenterOfMassDisplacement'):
            global centerOfMass
            if centerOfMass==None:
                centerOfMass = calculateCenterOfMass(gameState)
            
            currentCenterOfMass=calculateCenterOfMass(gameState)

            return currentCenterOfMass[0]-centerOfMass[0] + (currentCenterOfMass[1]-centerOfMass[1])
        else: #do poprawy
            sumOfDistancesPlayer1=0
            sumOfDistancesPlayer2=0
            heuristicValue=None

            for counter in list(gameState['counters']['1']):
                #odległość od początkowego rogu dla pierwszego gracza
                sumOfDistancesPlayer1+= counterDistanceToCorner(gameState['counters']['1'][counter]._x(), gameState['counters']['1'][counter]._y(), 'toRightBottomCorner')
            distanceForPlayer1=sumOfDistancesPlayer1/numOfCounters

            for counter in list(gameState['counters']['2']):
                #odległość od początkowego rogu dla drugiego gracza
                sumOfDistancesPlayer2+= counterDistanceToCorner(gameState['counters']['2'][counter]._x(), gameState['counters']['2'][counter]._y(), 'toRightBottomCorner')
            distanceForPlayer2=sumOfDistancesPlayer2/numOfCounters
            
            #TUTAJ SKOŃCZYŁEM
            #zakładamy, że tutaj gracz drugi jest graczem minimalizującym, a pierwszy maksymalizującym
            return distanceForPlayer2 + distanceForPlayer1
            
        return sumOfDistances/numOfCounters
    
    else:
        return None

def calculateCenterOfMass(gameState):
    sumOfXDistances=0
    sumOfYDistances=0
    numOfCounters=len(list(gameState['counters']['1']))
    for counter in list(gameState['counters']['1']):
        sumOfXDistances+=gameState['counters']['1'][counter]._x()
        sumOfYDistances+=gameState['counters']['1'][counter]._y()

    numOfCounters+=len(list(gameState['counters']['2']))
    for counter in list(gameState['counters']['2']):
        sumOfXDistances+=gameState['counters']['2'][counter]._x()
        sumOfYDistances+=gameState['counters']['2'][counter]._y()
        #print(list(gameState['counters']['1']))
    #print(f'{sumOfXDistances}/{numOfCounters} i {sumOfYDistances}/{numOfCounters}')
    return [sumOfXDistances/numOfCounters, sumOfYDistances/numOfCounters]

# #pierwsza heurystyka
# def calculateHeuristicAvgDistFromWinningCorner(player, gameState):
#     sumOfDistances=0
#     numOfCounters=len(list(gameState['counters'][player]))
#     for counter in list(gameState['counters'][player]):
#         sumOfDistances+= counterDistanceToCorner(player, gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toWinningCorner')
#     return sumOfDistances/numOfCounters

# #druga heurystyka
# def calculateHeuristicAvgDistFromStartingCorner(player, gameState):
#     sumOfDistances=0
#     numOfCounters=len(list(gameState['counters'][player]))
#     for counter in list(gameState['counters'][player]):
#         sumOfDistances+= counterDistanceToCorner(player, gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toStartingCorner')
#     return sumOfDistances/numOfCounters

def counterDistanceToCorner(counterX, counterY, option):
    if option=='toLeftUpperCorner':
        corner=[0,0]
    else:
        corner=[15,15]
    return math.sqrt((corner[0] - counterX)**2 + (corner[1] - counterY)**2)

# #trzecia heurystyka
# def calculateHeuristicAvgDistToStartingBorders(player, gameState):
#     sumOfDistances=0
#     numOfCounters=len(list(gameState['counters'][player]))
#     for counter in list(gameState['counters'][player]):
#         sumOfDistances+= counterDistanceToStartingBorders(player, gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y())
#     return sumOfDistances/numOfCounters

def counterDistanceToStartingBorders(counterX, counterY, option):
    if option=='toLeftUpperCornerBorder':
        border=[0,0]
    else:
        border=[15,15]
    return abs(border[0] - counterX) + abs(border[1] - counterY)

# def centerOfMass(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y()):
#     return 

def findHeuristicValue(allPossibleMoves, option):
    bestNode=None
    if option=='min':
        value=float('inf')
        for node in allPossibleMoves:
            if node._heuristicVal()<value:
                value=node._heuristicVal()
                bestNode=node
    else:
        value=float('-inf')
        for node in allPossibleMoves:
            if node._heuristicVal()>value:
                value=node._heuristicVal()
                bestNode=node
    return [bestNode, value]

def calcAllHeuristics(node, minPlayer, maxPlayer):
    if not node._children()==None:
        for child in node._children():
            calcAllHeuristics(child, minPlayer, maxPlayer)

        if minPlayer==str((node._round()%2)+1):
            bestNodeAndMinMaxVal = findHeuristicValue(node._children(), 'min')
        else:
            bestNodeAndMinMaxVal = findHeuristicValue(node._children(), 'max')

        node.setChildrenMinMaxValue(bestNodeAndMinMaxVal[1])
        node.setBestChild(bestNodeAndMinMaxVal[0])
    else:
         node.setChildrenMinMaxValue(node._heuristicVal())

##

#mają być przynajmniej 3 różne implementacje heurystyki
if __name__=='__main__':
    gameState=prepareStartGameState()
    # printGameboardState(gameState['gameboardState'])
    # print('START-------------')
    # allPoss = allPossibleMoveForCounter(4,0,'1',gameState, False)
    # for pos in allPoss:
    #     printGameboardState(pos)
    # game(gameState)

    ###
    #budowanie drzewa możliwych ruchów
    heuristicType='CenterOfMassDisplacement'
    parentNode = Node(0, None, gameState, '0', None, None, 0, calculateHeuristicValue, heuristicType)
    minPlayer=None
    maxPlayer=None
    if heuristicType=='AvgDistToLeftUpperCorner':
        maxPlayer='1'
        minPlayer='2'
    elif heuristicType=='AvgDistToRightBottomCorner':
        maxPlayer='2'
        minPlayer='1'
    elif heuristicType=='AvgDistToLeftUpperCornerBorder':
        maxPlayer='1'
        minPlayer='2'
    elif heuristicType=='CenterOfMassDisplacement':
        maxPlayer='1'
        minPlayer='2'
    else: #TODO: do ustalenia
        maxPlayer='1'
        minPlayer='2'

    #TODO: zmień tę logikę, aby działała w trakcie gry i aby nie budowało całego drzewa
    generateAllPossibleMovesInThisRound('1', gameState, parentNode, 1, minPlayer, maxPlayer)

    #tutaj już zmiana gracza, bo w powyższych dwóch linijkach wygenerowaliśmy ruchy dla gracza 1
    generatePossibleMovesTree('2', gameState, parentNode, 1, minPlayer, maxPlayer)

    # printOneLeaf(parentNode)

    #obliczanie heurystyk
    calcAllHeuristics(parentNode, minPlayer, maxPlayer)

    print('Koniec programu')
    ###

    ###gra
    playGameState=gameState['gameboardState']
    print('Plansza:')
    printGameboardState(gameState['gameboardState'])
    previousNode=parentNode
    penultimateNodeHeuristicValue=None
    round=0
    whoseMove='1'
    while True:
        round+=1
        print(f'_______________RUNDA: {round}.______________')
        if whoseMove=='1':
            isIncorrectMove=1
            while isIncorrectMove==1:
                xcurrent = int(input('Podaj wsp. x pionka, który chcesz przesunąć: '))
                ycurrent = int(input('Podaj wsp. y pionka, który chcesz przesunąć: '))
                xto = int(input('Podaj wsp. x pola, na które chcesz przesunąć pionek: '))
                yto = int(input('Podaj wsp. y pola, na które chcesz przesunąć pionek: '))
                #TODO: zamiast nakładania ograniczeń w move, wyszukuj danego stanu w drzewie, a jak nie znajdziesz, to znaczy, że został wykonany zły ruch
                newPlayGameStateAndErrorFlag = move(yto, xto,ycurrent,xcurrent,whoseMove,playGameState)
                # penultimateNodeHeuristicValue=previousNode._heuristicVal()
                #znajdywanie węzła o danym stanie
                isChildFound=False
                isIncorrectMove=newPlayGameStateAndErrorFlag[1]
                for child in previousNode._children():
                    if(areGameStatesTheSame(child._gameState()['gameboardState'], newPlayGameStateAndErrorFlag[0])):
                        previousNode=child
                        isChildFound=True
                        break
                if isChildFound:
                    isChildFound=False
                    playGameState=newPlayGameStateAndErrorFlag[0]
                else:
                    isIncorrectMove=1
        else:
            #w tej części program robi ruch na podstawie drzewa decyzyjnego
            # penultimateNodeHeuristicValue=previousNode._heuristicVal()
            playGameState=previousNode._bestChild()._gameState()['gameboardState']
            previousNode=previousNode._bestChild()

        print(f'Runda {round}: {previousNode}')

        printGameboardState(playGameState)
        if(checkWin(whoseMove, playGameState)):
            print(f'GRACZ {whoseMove} WYGRAŁ!!!')
            break
        else:
            if maxDepth==round:
                if previousNode._heuristicVal()>0:
                    print(f'GRACZ {previousNode._whoseMove()} WYGRAŁ!!!')
                elif previousNode._heuristicVal()==0:
                    print(f'REMIS')
                else:
                    print(f'GRACZ {str((int(previousNode._whoseMove())%2)+1)} WYGRAŁ!!!')

                print(f'Wartość heurystyki (typu: {heuristicType}): {previousNode._heuristicVal()}')
                print(f'Obecny środek masy: {calculateCenterOfMass(previousNode._gameState())}')
                print(f'Początkowy środek masy: {centerOfMass}')
                option = input('Czy zagrać jeszcze raz? (t- tak, n- nie): ')
                if option=='n':
                    break
                if option=='t':
                    previousNode=parentNode
                    penultimateNodeHeuristicValue=None
                    round=0
                    whoseMove='1' #TODO: tutaj wczytuje grę na nowo, ale w niewłaściwy sposób: do naprawienia
        #tu skończyłem
        whoseMove=str((int(whoseMove)%2)+1)

    ###

    #heurystyka 1-> średnia odległość wszystkich pionków od rogu

    # print(f'wynik dla gracza 1: {checkWin('1', gameState["gameboardState"])}') #testowe sprawdzenie, czy ktoś wygrał

    # allPossibleMoveForCounter(0, 0, '1', gameState, False, parentNode, 1, 0, 0)

