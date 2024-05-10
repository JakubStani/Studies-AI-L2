class Node:
    def __init__(self, round, whoseMove, gameState, whoWon, parent, children, depth, calculateHeurVal, heuristicType):
        self.round = round
        self.whoseMove = whoseMove
        self.gameState=gameState
        self.whoWon=whoWon
        self.parent=parent
        self.children=children
        self.depth=depth
        self.heuristicVal=calculateHeurVal(whoseMove, gameState, heuristicType)
        self.heuristicType=heuristicType
        self.childrenMinMaxValue=None
        self.bestChild=None

    def setChildren(self, children):
        self.children=children

    def _children(self):
        return self.children
    
    def _gameState(self):
        return self.gameState
    
    def _round(self):
        return self.round
    
    def _whoWon(self):
        return self.whoWon
    
    def _heuristicType(self):
        return self.heuristicType
    
    def _heuristicVal(self):
        return self.heuristicVal
    
    def setChildrenMinMaxValue(self, childrenMinMaxValue):
        self.childrenMinMaxValue=childrenMinMaxValue

    def setBestChild(self, bestChild):
        self.bestChild=bestChild
