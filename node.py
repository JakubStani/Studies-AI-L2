class Node:
    def __init__(self, round, whoseMove, gameState, whoWon, parent, children, depth, calculateheurVal, heuristicType):
        self.round = round
        self.whoseMove = whoseMove
        self.gameState=gameState
        self.whoWon=whoWon
        self.parent=parent
        self.children=children
        self.depth=depth
        self.heuristicValPlayer1=calculateheurVal('1', gameState, heuristicType)
        self.heuristicValPlayer2=calculateheurVal('2', gameState, heuristicType)
        self.heuristicType=heuristicType

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