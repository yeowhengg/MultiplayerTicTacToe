import Board as board

class Player:
    def __init__(self, symbol):
        self.turn = False
        self.position = None
        self.symbol = symbol
    
    def TurnToMove(self, turn):
        self.turn = turn

    def move(self, column, row):
        self.row = row
        self.column = column



