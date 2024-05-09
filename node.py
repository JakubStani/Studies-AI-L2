class Node:
    def __init__(self, round, whoseMove, gameState, whoWon, parent, children, depth, calculateheurValPl1FUnc, calculateheurValPl2FUnc):
        self.round = round
        self.whoseMove = whoseMove
        self.gameState=gameState
        self.whoWon=whoWon
        self.parent=parent
        self.children=children
        self.depth=depth
        self.heuristicValPlayer1=calculateheurValPl1FUnc(gameState, '1')
        self.heuristicValPlayer2=calculateheurValPl2FUnc(gameState, '2')

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