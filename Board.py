class Board:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    
    def get_board(self):
        return self.board

    def check_in_board(self, row, column, player):
        if self.board[row - 1][column - 1] == " ":
            return True
        elif self.board[row - 1][column - 1] == player.symbol:
            return f"You already used this place!\nIt is still your turn, {player.symbol}:"
        elif self.board[row - 1][column - 1] != " " and self.board[row - 1][column - 1] != player.symbol:
            return f"This place has been claimed by the other player.\nIt is still your turn, {player.symbol}:"

    def set_player_in_board(self, row, column, player):
        self.row = row
        self.column = column
        self.board[row - 1][column - 1] = player.symbol

    def DiagonalWin(self):
        leftDiagonalString = f"{self.board[0][0]}{self.board[1][1]}{self.board[2][2]}"
        rightDiagonalString = f"{self.board[0][2]}{self.board[1][1]}{self.board[2][1]}"
        if leftDiagonalString == "XXX" or rightDiagonalString == "XXX":
            return "X"
        if leftDiagonalString == "OOO" or rightDiagonalString == "OOO":
            return "O"
        return ""

    def VerticalWin(self, column):
        concat = ""
        for i in range(len(self.board)):
            concat += self.board[i][column - 1]
        if concat == "XXX":
            return "X"
        if concat == "OOO":
            return "O"
        return ""

    def HorizontalWin(self):
        concat = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                concat += self.board[i][j]
        if "XXX" in concat:
            return "X"
        if "OOO" in concat:
            return "O"
        return ""

    def GameWinOrLose(self, count, winner):
        if count == 9:
            return True
        if winner == "X" or winner == "O":
            print(f"Congratulations {winner}! You won!")
            return True
