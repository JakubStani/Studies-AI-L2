import copy
from counter import Counter
from node import Node 
import math
from colorama import Fore



def prepareStartGameState():
    gameState={
        'gameboardState': [],
        'counters': {'1':dict(), '2': dict()},
        'numOfJumps': 0,
        'numOfMovesStraightToWin':0
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





#na wejściu jest parent, który nie ma jeszcze dzieci
#podana runda, to runda, która zostanie przypisana dzieciom parentNoda
#currentDepth służy do rozpoznawania, który poziom drzewa jest w danym momencie sprawdzany-> zaczynamy od 0
def generatePossibleMovesTree(whoseMove, gameState, parentNode, round, minPlayer, maxPlayer, currentDepth):
    global maxDepth
    # if not parentNode._children() == None and round <maxDepth: #TODO: ustaw jakąś zmienną na maksymalną głębokość
    #     for child in parentNode._children():
    #         generateAllPossibleMovesInThisRound(whoseMove, child._gameState(), child, round+1, minPlayer, maxPlayer)
    #         nextWhoseMove=str((int(whoseMove)%2)+1)
    #         generatePossibleMovesTree(nextWhoseMove, child._gameState(), child, round+1, minPlayer, maxPlayer)

    #         # break #Można odkomentować, aby szybko móc zobaczyć skrajny wymnik dla dużej głębokości

    # else: #TODO: sprawdź i ustaw, kto wygrał
    #     pass

    #najpierw sprawdzamy, czy poprzedni ruch (tzn parentNode- poprzedni, bo wygenerowany w poprzednim działaniu funkcji generującej drzewo)
    #zawiera stan końcowy gry
    if not checkWin(str((int(whoseMove)%2)+1), gameState['gameboardState']):

        #jeżeli parent node nie reprezentuje stanu końca gry, generujemy jego dzieci
        generateAllPossibleMovesInThisRound(whoseMove, gameState, parentNode, round, minPlayer, maxPlayer)
        
        #sprawdzamy, czy drzewo nie przekroczyło maksymalnej głębokości
        if currentDepth <maxDepth:

            #jeżeli głębokość nie została przekroczona, proces powtarzamy dla wszystkich dzieci
            for child in parentNode._children():
                nextWhoseMove=str((int(whoseMove)%2)+1)
                generatePossibleMovesTree(nextWhoseMove, child._gameState(), child, round+1, minPlayer, maxPlayer, currentDepth+1)

                # break #Można odkomentować, aby szybko móc zobaczyć skrajny wymnik dla dużej głębokości

        #w tym wypadku maksymalna głębokość została przekroczona
        else:
            pass
    #w tym wypadku parent node reprezentuje stan gry, w którym str((int(whoseMove)%2)+1) wygrał
    else:
        pass

#TODO: pozbądź siękluczy współrzędnych pionków (bo one będą sięzmieniać) i zmieniaj współrzędne pionka po jego ruchu
#na wejściu jest parent, który nie ma dzieci
def generateAllPossibleMovesInThisRound(whoseMove, gameState, parentNode, round, minPlayer, maxPlayer):

    # #sprawdzamy dalej możliwe ruchy tylko wtedy, gdy dany parentNode nie reprezentuje stanu zakończonej gry
    # if parentNode._whoWon()=='0':
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

        if 0<=yto and yto<=15 and 0<=xto and xto<=15:
            
            #zmienna licząca ruchy po przekątnej
            #prowadzącej prosto do końcowego rogu planszy
            numOfMovesStraightToWinToAdd=0

            #sprawdzamy, w jakim kierunku jest ruch
            displacement=[xto-xcurrent, yto-ycurrent]
            if displacement[0]<0 and displacement[1]<0:
                numOfMovesStraightToWinToAdd=-1
            elif displacement[0]>0 and displacement[1]>0:
                numOfMovesStraightToWinToAdd=1
            if gameState['gameboardState'][yto][xto] == '0' and not jumpOnly:
                possibleStates.append(moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState, parentNode, round, 0, numOfMovesStraightToWinToAdd))
            else:
                if not gameState['gameboardState'][yto][xto] == '0':
                    #sprawdzamy, czy skok będzie jeszcze w granicy planszy
                    if 0<=yto + displacement[1] and yto + displacement[1]<= 15 and 0<=xto + displacement[0] and xto + displacement[0]<=15:
                        if gameState['gameboardState'][yto + displacement[1]][xto + displacement[0]] == '0': #TODO: napraw skakanie w to samo miejsce (bo po przekątnej)
                            
                            #ponieważ tutaj robimy skok, zwiększamy lub zmniejszamy liczbę skoków,
                            #w zależności od kierunku 
                            numOfJumpsToAdd=0
                            #pod uwagę nie beirzemy ruchów po przekątnej planszy, 
                            #która nie przybliża do wygrywającego końca: 
                            if displacement!=[-1,1] and displacement!=[1,-1]:

                                #jeżeli jest to przedział ruchów gracza 1 ...
                                if displacement[0]>=0 and displacement[1]>=0:
                                    #... zwiększamy liczbę skoków
                                    numOfJumpsToAdd=1
                                    if displacement[0]>0 and displacement[1]>0:
                                        numOfMovesStraightToWinToAdd=2

                                else:
                                    #jeżeli jest to przedział ruchów gracza 2 ...
                                    if displacement[0]<=0 and displacement[1]<=0:
                                        #... zmniejszamy liczbę skoków
                                        numOfJumpsToAdd=-1

                                        if displacement[0]<0 and displacement[1]<0:
                                            numOfMovesStraightToWinToAdd=-2

                            nState=moveClose(yto + displacement[1], xto + displacement[0], ycurrent, xcurrent, whoseMove, gameState, parentNode, round, numOfJumpsToAdd, numOfMovesStraightToWinToAdd)
                            possibleStates.append(nState)
                            previousX = xto
                            previousY = yto
                            newStates=allPossibleMoveForCounter(xto + displacement[0], yto + displacement[1], whoseMove, nState._gameState(), True, parentNode, round, previousX, previousY)
                            possibleStates.extend(newStates)
    return possibleStates

#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def moveClose(yto, xto, ycurrent, xcurrent, whoseMove, gameState, parentNode, round, numOfJumpsToAdd, numOfMovesStraightToWinToAdd):
    possibSt=copy.deepcopy(gameState) #TUTAJ można ustalić, co będzie przechowywane w węzłach drzewa (jakie dane)
    # possibSt=gameState[:]
    # if() #

    # if 0<=yto and yto
    if gameState['gameboardState'][yto][xto] == '0':
        #możliwy stan
        possibSt['gameboardState'][ycurrent][xcurrent]='0'
        possibSt['gameboardState'][yto][xto]=whoseMove

        possibSt['numOfJumps']+=numOfJumpsToAdd

        possibSt['numOfMovesStraightToWin']+=numOfMovesStraightToWinToAdd

        #przesunięcie pionka
        del possibSt['counters'][whoseMove][f'{xcurrent}-{ycurrent}-{whoseMove}']
        newCounter = Counter(xto, yto, whoseMove)
        possibSt['counters'][whoseMove][f'{xto}-{yto}-{whoseMove}'] = newCounter

    #przekształcamy wynik na węzeł

    #sprawdzenie, czy gracz, który ma ruch wygrał
    whoWon='0'
    # if(checkWin(whoseMove, possibSt['gameboardState'])):
    #     whoWon=whoseMove

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
    
# def game(gameState):
#     players=['1','2']
#     whoseTurn=0
#     turn=1

#     while True:
#         printGameboardState(gameState)

#         #player moves
#         fromWhereX=int(input('Podaj wsp. x pionka, którego chcesz przesunąć: '))
#         fromWhereY=int(input('Podaj wsp. y pionka, którego chcesz przesunąć: '))
#         toWhereX=int(input('Podaj wsp. x pola, na które chcesz przesunąć pionek: '))
#         toWhereY=int(input('Podaj wsp. y pola, na które chcesz przesunąć pionek: '))

#         moveResult=move(toWhereY, toWhereX, fromWhereY, fromWhereX, players[whoseTurn], gameState)
#         if(moveResult[1]<1):
#             whoseTurn+=1
#             whoseTurn%=2
#             gameState=moveResult[0]
#             turn+=1


#wykonuje ruch w określonym kierunku i zwraca stan po ruchu
def move(yto, xto, ycurrent, xcurrent, whoseMove, gameState):


    displacement=[xto-xcurrent, yto-ycurrent]
    #funkcja move jest przewidziana tylko dla gracza 1., więc 
    if not (displacement[0]<0 and displacement[1]<=0 or displacement[1]<0 and displacement[0]<=0):

        # if 0<=yto and yto
        if gameState['gameboardState'][yto][xto] == '0' and gameState['gameboardState'][ycurrent][xcurrent]==whoseMove:
            #możliwy stan
            possibSt=copy.deepcopy(gameState)
            possibSt['gameboardState'][ycurrent][xcurrent]='0'
            possibSt['gameboardState'][yto][xto]=whoseMove
            
            #przesunięcie pionka
            del possibSt['counters'][whoseMove][f'{xcurrent}-{ycurrent}-{whoseMove}']
            newCounter = Counter(xto, yto, whoseMove)
            possibSt['counters'][whoseMove][f'{xto}-{yto}-{whoseMove}'] = newCounter

            return [possibSt, 0]

    print('Podano nieprawidłowe pola')
    return [gameState,1]
    
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
                # print('y',y)
                if not gameStateToCheck[y][x]=='1':
                    return False
            if y<15:
                counters-=1
        return True
    

##heurystyki
#TODO: dodaj możliwość łatwego wyboru heurystyki

centerOfMass=None
def calculateHeuristicValue(gameState, heuristicType):
    # if not player==None:
        sumOfDistances=0
        
        # #pierwsza heurystyka
        # if(heuristicType=='AvgDistToLeftUpperCorner'):
        #     for counter in list(gameState['counters'][player]):
        #         sumOfDistances+= counterDistanceToCorner(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toLeftUpperCorner')

        # #druga heurystyka
        # elif(heuristicType=='AvgDistToRightBottomCorner'):
        #     for counter in list(gameState['counters'][player]):
        #         sumOfDistances+= counterDistanceToCorner(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toRightBottomCorner')

        # #trzecia heurystyka #TODO: przerób na odległość plus aby pionki były jak najbliżej siebie
        # elif(heuristicType=='AvgDistToLeftUpperCornerBorder'):
        #     for counter in list(gameState['counters'][player]):
        #         sumOfDistances+= counterDistanceToStartingBorders(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toLeftUpperCornerBorder')

        #dobra
        if(heuristicType=='AvgDistToLeftUpperCornerBorder'):
            for counter in list(gameState['counters']['1']):
                sumOfDistances+= counterDistanceToStartingBorders(gameState['counters']['1'][counter]._x(), gameState['counters']['1'][counter]._y())
            
            for counter in list(gameState['counters']['2']):
                sumOfDistances+= counterDistanceToStartingBorders(gameState['counters']['2'][counter]._x(), gameState['counters']['2'][counter]._y())

            return sumOfDistances / (len(list(gameState['counters']['1'])) + len(list(gameState['counters']['2'])))

        # #trzecia heurystyka #TODO: przerób na odległość plus aby pionki były jak najbliżej siebie
        # elif(heuristicType=='CloseCountersAndAvgDistToLeftUpperCornerBorder'):
        #     for counter in list(gameState['counters'][player]):
        #         sumOfDistances+= counterDistanceToStartingBorders(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y(), 'toLeftUpperCornerBorder')
        
        #dobra
        elif(heuristicType=='CounterJumps'):
            return gameState['numOfJumps']
        
        #dobra
        elif(heuristicType=='MoveStraightToWin'):
            return gameState['numOfMovesStraightToWin']
        
        # #czwarta heurystyka
        # elif(heuristicType=='CenterOfMassDisplacement'):
        #     global centerOfMass
        #     if centerOfMass==None:
        #         centerOfMass = calculateCenterOfMass(gameState)
            
        #     currentCenterOfMass=calculateCenterOfMass(gameState)

        #     return currentCenterOfMass[0]-centerOfMass[0] + (currentCenterOfMass[1]-centerOfMass[1])
        # else: #do poprawy
        #     sumOfDistancesPlayer1=0
        #     sumOfDistancesPlayer2=0
        #     heuristicValue=None

        #     for counter in list(gameState['counters']['1']):
        #         #odległość od początkowego rogu dla pierwszego gracza
        #         sumOfDistancesPlayer1+= counterDistanceToCorner(gameState['counters']['1'][counter]._x(), gameState['counters']['1'][counter]._y(), 'toRightBottomCorner')
        #     distanceForPlayer1=sumOfDistancesPlayer1/numOfCounters

        #     for counter in list(gameState['counters']['2']):
        #         #odległość od początkowego rogu dla drugiego gracza
        #         sumOfDistancesPlayer2+= counterDistanceToCorner(gameState['counters']['2'][counter]._x(), gameState['counters']['2'][counter]._y(), 'toRightBottomCorner')
        #     distanceForPlayer2=sumOfDistancesPlayer2/numOfCounters
            
            
        #     #zakładamy, że tutaj gracz drugi jest graczem minimalizującym, a pierwszy maksymalizującym
        #     return distanceForPlayer2 + distanceForPlayer1
            
        # return sumOfDistances/numOfCounters
    
    # else:
    #     return None

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

# def counterDistanceToStartingBorders(counterX, counterY, option):
#     if option=='toLeftUpperCornerBorder':
#         border=[0,0]
#     else:
#         border=[15,15]
#     return abs(border[0] - counterX) + abs(border[1] - counterY)

def counterDistanceToStartingBorders(counterX, counterY):
    return math.sqrt(counterX**2 + counterY**2)

def calculateCountersField(gameStateCountersPlayer):
    #gameState['counters'][player]
    minY=float('inf')
    minX=float('inf')
    maxY=0
    maxX=0

    for counter in list(gameStateCountersPlayer):
        if counter._x()<minX:
            minX=counter._x()
        if counter._y()<minY:
            minY=counter._y()

        if counter._x()>maxX:
            maxX=counter._x()
        if counter._y()>maxY:
            maxY=counter._y()
    #zwracane jest pole, tworzone przez najbardziej wysunięte pionki z dodatkiem
    return (maxX-minX) * (maxY-minY)

    

# def centerOfMass(gameState['counters'][player][counter]._x(), gameState['counters'][player][counter]._y()):
#     return 

def findMinMaxHeuristicValue(allPossibleMoves, option):
    bestNode=None
    if option=='min':
        value=float('inf')
        for node in allPossibleMoves:
            if node._childrenMinMaxValue()<value:
                value=node._childrenMinMaxValue()
                bestNode=node
    else:
        value=float('-inf')
        for node in allPossibleMoves:
            if node._childrenMinMaxValue()>value:
                value=node._childrenMinMaxValue()
                bestNode=node
    return [bestNode, value]

#tutaj skończyłem
def calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(node, minPlayer, maxPlayer):
    if not node._children()==None:
        for child in node._children():
            #nad tym trzeba pomyśleć
            calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(child, minPlayer, maxPlayer)

        if minPlayer==str((node._round()%2)+1):
            retInfo = 'min'
            bestNodeAndMinMaxVal = findMinMaxHeuristicValue(node._children(), 'min')
        else:
            retInfo='max'
            bestNodeAndMinMaxVal = findMinMaxHeuristicValue(node._children(), 'max')

        node.setChildrenMinMaxValue(bestNodeAndMinMaxVal[1])
        node.setBestChild(bestNodeAndMinMaxVal[0])
        return [bestNodeAndMinMaxVal[0], retInfo]
    else:
         node.setChildrenMinMaxValue(node._heuristicVal())

#zakładamy, że dla nas alpha, to minPlayer, a betha to maxplayer
#alphaBestValue to na początku float('inf'), betha przeciwnik
def AlphaBetaCalcAllHeuristicsAndReturnChildLeadingToBestHeuristic(node, minPlayer, maxPlayer, alphaBestValue, bethaBestValue):
    #poniższe operacje wykonujemy dla węzłów, które mają dzieci
    if not node._children()==None:
        bestVal=None
        bestNodeForThisNode=None
        returnedAlphaBestValue=float('inf')
        returnedBethaBestValue=float('-inf')

        #dla dzieci węzła sprawdzamy, jaka będzie wartość alphy bądź bety
        for child in node._children():
            #
            result=AlphaBetaCalcAllHeuristicsAndReturnChildLeadingToBestHeuristic(child, minPlayer, maxPlayer, alphaBestValue, bethaBestValue)
            
            #flaga, czy zwracane od liścia
            # if result[3]:
            #     returnedAlphaBestValue=result[1]
            #     returnedBethaBestValue=result[2]
            # else:
            #     returnedAlphaBestValue=result[2]
            #     returnedBethaBestValue=result[1]
            # result=result[0]

            #porównujemy tylko, gdy dane dziecko zwróciło lepszą wartość
            if not result._childrenMinMaxValue()==None:

                #jeżeli dany węzeł jest minimalizującym (czyli u nas też betha),
                #wybiera najmniejsząwartośc bethy
                if minPlayer==str((node._round()%2)+1):

                    # #sprawdzamy to tylko, gdy dana gałąź nie była obcięta
                    # if not result==None:

                    #jeżeli zwrócona wartość jest mniejsza, niż aktualny alpha
                    #następuje zapisanie niższej wartości i węzła
                    if bethaBestValue>result._childrenMinMaxValue():
                        bethaBestValue=result._childrenMinMaxValue()
                        bestVal=bethaBestValue
                        bestNodeForThisNode=child

                #jeżeli węzeł nie jest minimalizujący,
                #jest maksymalizujący
                else:

                    #gdy wcześniej znaleziona wartość alpha jest mniejsza,
                    #niż wartość tego węzłą, nie dojdzie do niej, ponieważ
                    
                    if alphaBestValue<result._childrenMinMaxValue():
                        alphaBestValue=result._childrenMinMaxValue()
                        bestNodeForThisNode=child
                        bestVal=alphaBestValue
            
            if bethaBestValue<=alphaBestValue: 
                        #jeżeli tak, przestajemy szukać dzieci
                        break

        node.setChildrenMinMaxValue(bestVal)
        node.setBestChild(bestNodeForThisNode)
        # print(node._gameState()) #for tests
        return node
    
    #poniższe operacje wykonujemy dla liści
    else:
        #  print(node._gameState()) #for tests
         #ustawiamy wartość min max węzła na jego wartość heurystyczną
         node.setChildrenMinMaxValue(node._heuristicVal()) 
         #zwracamy z flagą True- zwrot od liścia
         return node
    
    # if not node._children()==None:
    #     if minPlayer==str((node._round()%2)+1):
    #             retInfo = 'min'
    #             bestVal = float('inf')
    #     else:
    #         retInfo='max'
    #         bestVal = float('-inf')

    #     childrenValues=[]
    #     for child in node._children():
    #         #nad tym trzeba pomyśleć
    #         result = calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(child, minPlayer, maxPlayer, bestChildForThisNode)

    #         if minPlayer==str((node._round()%2)+1):
    #             if betha<=result._childrenMinMaxValue():
    #                 break
    #             elif bestVal>result._childrenMinMaxValue():
    #                 bestVal=result._childrenMinMaxValue()
    #                 bestChildForThisNode=result
    #         else:
    #             retInfo='max'
    #             bestNodeAndMinMaxVal = findMinMaxHeuristicValue(node._children(), 'max')

    #     node.setChildrenMinMaxValue(bestNodeAndMinMaxVal[1])
    #     node.setBestChild(bestNodeAndMinMaxVal[0])
    #     return [bestNodeAndMinMaxVal[0], retInfo]
    # else:
    #      node.setChildrenMinMaxValue(node._heuristicVal())
    #      return node
##


def checkEndOfGame(round, previousNode, playGameState, whoseMove, heuristicType):
    print(f'Runda {round}: {previousNode}')

    printGameboardState(playGameState['gameboardState'])
    if(checkWin(whoseMove, playGameState['gameboardState'])):
        print(f'GRACZ {whoseMove} WYGRAŁ!!!')
        # return [None, None, None, False]

        print(f'Wartość heurystyki (typu: {heuristicType}): {previousNode._heuristicVal()}')
        print(f'Obecny środek masy: {calculateCenterOfMass(previousNode._gameState())}')
        print(f'Początkowy środek masy: {centerOfMass}')
        option = input('Czy zagrać jeszcze raz? (t- tak, n- nie): ')
        if option=='n':
            return [None, None, None, False]
        if option=='t':
            previousNode=parentNode
            round=0
            whoseMove='1' #TODO: tutaj wczytuje grę na nowo, ale w niewłaściwy sposób: do naprawienia
            return [previousNode, round, whoseMove, True]
    
    #TODO: sprawdzenie, czy gra nie utknęła i nie da sie doprowadzić gry do końca (np. pionek 00 cały czas stoi w miejscu)



    # else:
    #     if maxDepth==round:
    #         if previousNode._heuristicVal()>0:
    #             print(f'GRACZ {previousNode._whoseMove()} WYGRAŁ!!!')
    #         elif previousNode._heuristicVal()==0:
    #             print(f'REMIS')
    #         else:
    #             print(f'GRACZ {str((int(previousNode._whoseMove())%2)+1)} WYGRAŁ!!!')

    #         print(f'Wartość heurystyki (typu: {heuristicType}): {previousNode._heuristicVal()}')
    #         print(f'Obecny środek masy: {calculateCenterOfMass(previousNode._gameState())}')
    #         print(f'Początkowy środek masy: {centerOfMass}')
    #         option = input('Czy zagrać jeszcze raz? (t- tak, n- nie): ')
    #         if option=='n':
    #             return [None, None, None, False]
    #         if option=='t':
    #             previousNode=parentNode
    #             round=0
    #             whoseMove='1' #TODO: tutaj wczytuje grę na nowo, ale w niewłaściwy sposób: do naprawienia
    #             return [previousNode, round, whoseMove, True]
    return None

def takeOutFirstLevelOfChildren(parent):
    parentChildren=[]
    for child in parent._children():
        child.setChildren(None)
        parentChildren.append(child)
    return parentChildren

#mają być przynajmniej 3 różne implementacje heurystyki
if __name__=='__main__':

    loopGame=True

    while loopGame:

        hOpt=input(
            """Choose heuristic type:
            1- Average Distance To Left Upper Corner Border
            2- Counter Jumps
            3- Move Straight To Win
            """
            )
        
        if hOpt=='1':
            heuristicType='AvgDistToLeftUpperCornerBorder'
            maxPlayer='1'
            minPlayer='2'
        elif hOpt=='2':
            heuristicType='CounterJumps'
            maxPlayer='1'
            minPlayer='2'
        elif hOpt=='3':
            heuristicType='MoveStraightToWin'
            maxPlayer='1'
            minPlayer='2'

        withABorNot=input('Should use alpha betha pruning?: y- yes, n- no')
        
        global maxDepth
        maxDepth=int(input('Enter max depth value: '))



        gameState=prepareStartGameState()

        ###
        #budowanie drzewa możliwych ruchów
        # heuristicType='MoveStraightToWin'
        parentNode = Node(0, None, gameState, '0', None, None, 0, calculateHeuristicValue, heuristicType)

        ###gra
        playGameState=gameState
        print('Plansza:')
        printGameboardState(gameState['gameboardState'])
        previousNode=parentNode
        penultimateNodeHeuristicValue=None
        round=0

        #ustawienie na 2, aby zaczynał gracz 1
        whoseMove='2'

        # #początkowe budowanie drzewa
        # prevNodeCopy=copy.deepcopy(previousNode)
        # generatePossibleMovesTree(whoseMove, playGameState, prevNodeCopy, round+1, minPlayer, maxPlayer, 0)
        # calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(prevNodeCopy, minPlayer, maxPlayer) #poprzedni komentarz "tu skończyłem" prowadzi też do tego wiersza
        # previousNode.setChildren(takeOutFirstLevelOfChildren(prevNodeCopy))

        while True:

            #następny gracz ma ruch
            whoseMove=str((int(whoseMove)%2)+1)
            #przejście do kolejnej rundy
            round+=1
            print(f'_______________RUNDA: {round}.______________')
            if whoseMove=='1':
                isIncorrectMove=1
                while isIncorrectMove==1:
                    xcurrent = int(input('Podaj wsp. x pionka, który chcesz przesunąć: '))
                    ycurrent = int(input('Podaj wsp. y pionka, który chcesz przesunąć: '))
                    xto = int(input('Podaj wsp. x pola, na które chcesz przesunąć pionek: '))
                    yto = int(input('Podaj wsp. y pola, na które chcesz przesunąć pionek: '))

                    # #TODO: zamiast nakładania ograniczeń w move, wyszukuj danego stanu w drzewie, a jak nie znajdziesz, to znaczy, że został wykonany zły ruch
                    # newPlayGameStateAndErrorFlag = move(yto, xto,ycurrent,xcurrent,whoseMove,playGameState)
                    # # penultimateNodeHeuristicValue=previousNode._heuristicVal()
                    # #znajdywanie węzła o danym stanie
                    # isChildFound=False
                    # isIncorrectMove=newPlayGameStateAndErrorFlag[1]
                    # if isIncorrectMove==0:
                        
                    #     for child in previousNode._children():
                    #         if(areGameStatesTheSame(child._gameState()['gameboardState'], newPlayGameStateAndErrorFlag[0]['gameboardState'])):
                    #             previousNode=child
                    #             isChildFound=True
                    #             break
                    # if isChildFound:
                    #     isChildFound=False
                    #     playGameState=newPlayGameStateAndErrorFlag[0]
                    # else:
                    #     isIncorrectMove=1

                    #gracz dokonuje ruchu
                    newPlayGameStateAndErrorFlag = move(yto, xto,ycurrent,xcurrent,whoseMove,playGameState)

                    #funkcja move sprawdza, czy ruch był on wykonany poprawnie- tę informację zwraca jako jedną z wartości wyniku
                    isIncorrectMove=newPlayGameStateAndErrorFlag[1]

                    #flaga mówiąca, czy stan gry został znaleziony w zbiorze możliwych stanów gry po ruchu gracza
                    isChildFound=False

                    #jeżeli ruch był po części poprawny (po części, ponieważ tylko niektóre warunki ruchu zostały sprawdzone)
                    if isIncorrectMove==0:

                        #generujemy możliwe ruchy dla gracza i w pełni sprawdzamy, czy ruch, który wykonał, był poprawny
                        #podaną rundę będą miały zapisane dzieci previousNode
                        generateAllPossibleMovesInThisRound(whoseMove, playGameState, previousNode, round, minPlayer, maxPlayer)

                        
                        # calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(previousNode, minPlayer, maxPlayer) #poprzedni komentarz "tu skończyłem" prowadzi też do tego wiersza

                        #szukamy stanu, który jest taki sam, jak ten po ruchu gracza
                        for child in previousNode._children():
                            if(areGameStatesTheSame(child._gameState()['gameboardState'], newPlayGameStateAndErrorFlag[0]['gameboardState'])):

                                #węzeł dokonanego przez gracza ruchu ustawiamy jako dziecko previous noda,
                                #a previous noda ustawiamy jako rodzic węzła dokonanego przez gracza ruchu
                                previousNode.setChildren([child])
                                child.setParent(previousNode)
                                isChildFound=True
                                break
                    if isChildFound:
                        isChildFound=False

                        #zapisujemy stan gry
                        playGameState=newPlayGameStateAndErrorFlag[0]
                        #previous noda ustawiamy jako węzeł dokonanego przez gracza ruchu
                        previousNode=previousNode._children()[0]
                    #jeżeli nie znaleziono stanu gry w zbiorze możliwych stanów gry po ruchu gracza,
                    #ruch był nieprawidłowy
                    else:
                        isIncorrectMove=1
                        print('Nieprawidłowy ruch')

                        #zapisujemy nowy stan gry i tworzymy węzeł dokonanego przez gracza ruchu
                        # playGameState=newPlayGameStateAndErrorFlag[0]
                        # previousNode= Node(round,whoseMove, playGameState, '0', previousNode, None, round, calculateHeuristicValue, heuristicType)

                    #ponieważ ten kawałek kodu jest w pętli while, będzie się wykonywał,
                    #aż gracz dokona prawidłowego ruchu
                
                #po wykonaniu prawidłowego ruchu przez gracza, sprawdzamy, czy zakończył on grę
                prNoRoWhoseFlag=checkEndOfGame(round, previousNode, playGameState, whoseMove, heuristicType)
                
                #sprawdzenie, czy gra nie dobiegła końca
                if prNoRoWhoseFlag==None:
                    #od tej linii gracz wykonał swój ruch
                    #teraz czas na ruch algorytmu
                    round+=1
                    whoseMove=str((int(whoseMove)%2)+1)
                    
                    #dla wybranego węzła trzeba będzie zbudować nowe drzewo
                    #nie wybieramy jednak od razu najlepszego rozwiązania tuż po previous node, 
                    #tylko wybieramy najlepsze z liści drzewa (chcemy dojść do generalnie najlepszego rozwiązania
                    #w drzewie możliwych ruchów, które sprawdzimy)

                    #generujemy drzewo możliwych ruchów dla ruchu komputera
                    # generatePossibleMovesTree(whoseMove, playGameState, previousNode, round, minPlayer, maxPlayer, 0)
                    generatePossibleMovesTree(whoseMove, playGameState, previousNode, round, minPlayer, maxPlayer, 0)
                    if withABorNot=='y':
                        result =AlphaBetaCalcAllHeuristicsAndReturnChildLeadingToBestHeuristic(previousNode, minPlayer, maxPlayer, float('-inf'), float('inf'))._bestChild()
                    else:
                        result = calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(previousNode, minPlayer, maxPlayer)[0]
                    # result = calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(previousNode, minPlayer, maxPlayer)
                    
                    #usuwamy dzieci najkorzystniejszego ruchu komputera
                    result.setChildren(None)

                    #usuwamy wcześniej wygenerowane dzieci previous noda i ustawiamy najkorzystniejszy ruch komputera (gracza drugiego), jako jego dziecko
                    previousNode.setChildren([result])

                    #ustawiamy previous node jako rodzic najkorzystniejszego ruchu komputera
                    result.setParent(previousNode)

                    #ustawiamy previous node na najkorzystniejszy ruch komputera
                    previousNode=result
                    playGameState=previousNode._gameState()
                    #algorytm wykonał ruch
                    #sprawdzenie, czy komputer zakończył grę
                    prNoRoWhoseFlag=checkEndOfGame(round, previousNode, playGameState, whoseMove, heuristicType)

                    #jeżeli gra została zakończona
                    if not prNoRoWhoseFlag==None:
                        #czy uruchomić ponownie
                        if prNoRoWhoseFlag[3]:
                            # previousNode=prNoRoWhoseFlag[0]
                            # round=prNoRoWhoseFlag[1]
                            # whoseMove=prNoRoWhoseFlag[2]
                            break
                        #jeżeli nie, zakończ pętlę while
                        else:
                            loopGame=False
                            break
                
                #jeżeli gra dobiegła końca, to czy ma zostać ponownie uruchomiona
                else:
                    #czy uruchomić ponownie
                    if prNoRoWhoseFlag[3]:
                        # previousNode=prNoRoWhoseFlag[0]
                        # round=prNoRoWhoseFlag[1]
                        # whoseMove=prNoRoWhoseFlag[2]
                        break
                    #jeżeli nie, zakończ pętlę while
                    else:
                        loopGame=False
                        break


    ###

    #heurystyka 1-> średnia odległość wszystkich pionków od rogu

    # print(f'wynik dla gracza 1: {checkWin('1', gameState["gameboardState"])}') #testowe sprawdzenie, czy ktoś wygrał

    # allPossibleMoveForCounter(0, 0, '1', gameState, False, parentNode, 1, 0, 0)

