class Node:
    def __init__(self, turn, whoseMove, gameState, whoWon, parent, children, depth):
        self.turn = turn
        self.whoseMove = whoseMove
        self.gameState=gameState
        self.whoWon=whoWon
        self.parent=parent
        self.children=children
        self.depth=depth