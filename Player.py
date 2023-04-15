class Player:
    def __init__(self, symbol, turn):
        self.turn = turn
        self.symbol = symbol

    def move(self, column, row):
        self.row = row
        self.column = column



