class Node:
    def __init__(self, round, whoseMove, gameState, whoWon, parent, children, depth, calculateheurVal):
        self.round = round
        self.whoseMove = whoseMove
        self.gameState=gameState
        self.whoWon=whoWon
        self.parent=parent
        self.children=children
        self.depth=depth
        self.heuristicValPlayer1=calculateheurVal('1', gameState)
        self.heuristicValPlayer2=calculateheurVal('2', gameState)

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