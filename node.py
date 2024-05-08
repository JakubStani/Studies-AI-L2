class Node:
    def __init__(self, round, whoseMove, gameState, whoWon, parent, children, depth):
        self.round = round
        self.whoseMove = whoseMove
        self.gameState=gameState
        self.whoWon=whoWon
        self.parent=parent
        self.children=children
        self.depth=depth

    def setChildren(self, children):
        self.children=children

    def _children(self):
        return self.children
    
    def _gameState(self):
        return self.gameState