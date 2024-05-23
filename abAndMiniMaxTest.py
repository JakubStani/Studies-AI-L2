from node import Node

###ALPHA BETA

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
        print(node._gameState()) #for tests
        return node
    
    #poniższe operacje wykonujemy dla liści
    else:
         print(node._gameState()) #for tests
         #ustawiamy wartość min max węzła na jego wartość heurystyczną
         node.setChildrenMinMaxValue(node._heuristicVal()) 
         #zwracamy z flagą True- zwrot od liścia
         return node

###END OF ALPHA BETA    


###MINIMAX

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
        print(node._gameState()) #for tests
        return [bestNodeAndMinMaxVal[0], retInfo]
    else:
         print(node._gameState()) #for tests
         node.setChildrenMinMaxValue(node._heuristicVal())

### END OF MINIMAX

def calH(something, sElse):
    return None


if __name__=='__main__':

    print('Drzewo o głębokości 2 i 2 liściach przy węźle')
    #dla drzewa o głębokości 2 i 2 liście przy każdym węźle
    A = Node(1, '2', 'A', '0', None, None,None, calH, None)
    B = Node(2, '1', 'B', '0', A, None,None, calH, None)
    C = Node(2, '1', 'C', '0', A, None,None, calH, None)
    A.setChildren([B, C])

    #Liście
    D = Node(3, '2', 'D', '0', B, None,None, calH, None)
    E = Node(3, '2', 'E', '0', B, None,None, calH, None)
    B.setChildren([D, E])

    F = Node(3, '2', 'F', '0', C, None,None, calH, None)
    G = Node(3, '2', 'G', '0', C, None,None, calH, None)
    C.setChildren([F, G])


    D.setHeuristicVal(1)
    E.setHeuristicVal(2)
    F.setHeuristicVal(3)
    G.setHeuristicVal(-1)



    print('---------MINIMAX:---------')
    calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(A,'2', '1')
    print('---------ALPHA BETA:---------')
    AlphaBetaCalcAllHeuristicsAndReturnChildLeadingToBestHeuristic(A, '2', '1', float('-inf'), float('inf'))


    print('Drzewo o głębokości 3 i 2 liściach przy węźle')
    #dla drzewa o głębokości 3 i 3 liście przy każdym węźle
    A = Node(1, '2', 'A', '0', None, None,None, calH, None)
    B = Node(2, '1', 'B', '0', A, None,None, calH, None)
    C = Node(2, '1', 'C', '0', A, None,None, calH, None)
    A.setChildren([B, C])

    D = Node(3, '2', 'D', '0', B, None,None, calH, None)
    E = Node(3, '2', 'E', '0', B, None,None, calH, None)
    B.setChildren([D, E])

    F = Node(3, '2', 'F', '0', C, None,None, calH, None)
    G = Node(3, '2', 'G', '0', C, None,None, calH, None)
    C.setChildren([F, G])
    
    #Liście
    H = Node(1, '1', 'H', '0', D, None,None, calH, None)
    I = Node(1, '1', 'I', '0', D, None,None, calH, None)
    D.setChildren([H,I])

    J = Node(1, '1', 'J', '0', D, None,None, calH, None)
    K = Node(1, '1', 'K', '0', E, None,None, calH, None)
    E.setChildren([J, K])

    L = Node(1, '1', 'L', '0', E, None,None, calH, None)
    M = Node(1, '1', 'M', '0', E, None,None, calH, None)
    F.setChildren([L,M])

    N = Node(1, '1', 'N', '0', F, None,None, calH, None)
    O = Node(1, '1', 'O', '0', F, None,None, calH, None)
    G.setChildren([N,O])

    H.setHeuristicVal(2)
    I.setHeuristicVal(3)
    J.setHeuristicVal(5)
    K.setHeuristicVal(9)
    L.setHeuristicVal(0)
    M.setHeuristicVal(1)
    N.setHeuristicVal(7)
    O.setHeuristicVal(5)

    print('---------MINIMAX:---------')
    calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(A,'1', '2')
    print('---------ALPHA BETA:---------')
    AlphaBetaCalcAllHeuristicsAndReturnChildLeadingToBestHeuristic(A, '1', '2', float('-inf'), float('inf'))



    print('Drzewo o głębokości 3 i 3 liściach przy węźle')
    #dla drzewa o głębokości 3 i 3 liście przy każdym węźle
    A = Node(1, '2', 'A', '0', None, None,None, calH, None)
    B = Node(2, '1', 'B', '0', A, None,None, calH, None)
    C = Node(2, '1', 'C', '0', A, None,None, calH, None)
    A.setChildren([B, C])

    D = Node(3, '2', 'D', '0', B, None,None, calH, None)
    E = Node(3, '2', 'E', '0', B, None,None, calH, None)
    B.setChildren([D, E])

    F = Node(3, '2', 'F', '0', C, None,None, calH, None)
    G = Node(3, '2', 'G', '0', C, None,None, calH, None)
    C.setChildren([F, G])
    
    #Liście
    H = Node(1, '1', 'H', '0', D, None,None, calH, None)
    I = Node(1, '1', 'I', '0', D, None,None, calH, None)
    J = Node(1, '1', 'J', '0', D, None,None, calH, None)
    D.setChildren([H,I, J])

    K = Node(1, '1', 'K', '0', E, None,None, calH, None)
    L = Node(1, '1', 'L', '0', E, None,None, calH, None)
    M = Node(1, '1', 'M', '0', E, None,None, calH, None)
    E.setChildren([K, L, M])

    N = Node(1, '1', 'N', '0', F, None,None, calH, None)
    O = Node(1, '1', 'O', '0', F, None,None, calH, None)
    P = Node(1, '1', 'P', '0', F, None,None, calH, None)
    F.setChildren([N,O,P])

    R = Node(1, '2', 'R', '0', G, None,None, calH, None)
    S = Node(1, '2', 'S', '0', G, None,None, calH, None)
    T = Node(1, '2', 'T', '0', G, None,None, calH, None)
    G.setChildren([R,S,T])

    H.setHeuristicVal(2)
    I.setHeuristicVal(3)
    J.setHeuristicVal(1)
    K.setHeuristicVal(5)
    L.setHeuristicVal(9)
    M.setHeuristicVal(4)
    N.setHeuristicVal(0)
    O.setHeuristicVal(1)
    P.setHeuristicVal(3)
    R.setHeuristicVal(7)
    S.setHeuristicVal(5)
    T.setHeuristicVal(6)

    print('---------MINIMAX:---------')
    calcAllHeuristicsAndReturnChildLeadingToBestHeuristic(A,'1', '2')
    print('---------ALPHA BETA:---------')
    AlphaBetaCalcAllHeuristicsAndReturnChildLeadingToBestHeuristic(A, '1', '2', float('-inf'), float('inf'))

