class Board:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    
    def get_board(self):
        return self.board

    def check_in_board(self, row, column, player):
        try:
            if self.board[row - 1][column - 1] == " ":
                return True
            elif self.board[row - 1][column - 1] == player.symbol:
                return f"You already used this place!\nIt is still your turn, {player.symbol}:"
            elif self.board[row - 1][column - 1] != " " and self.board[row - 1][column - 1] != player.symbol:
                return f"This place has been claimed by the other player.\nIt is still your turn, {player.symbol}:"
            
        except IndexError:
            return f"Your option, row: {row}, col: {column} does not fit in the board. Please try something else."

    def set_player_in_board(self, row, column, player):
        self.row = row
        self.column = column
        self.board[row - 1][column - 1] = player.symbol

    def diagonal_win(self):
        left_diagonal_string = f"{self.board[0][0]}{self.board[1][1]}{self.board[2][2]}"
        right_diagonal_string = f"{self.board[0][2]}{self.board[1][1]}{self.board[2][1]}"
        if left_diagonal_string == "XXX" or right_diagonal_string == "XXX":
            return "X"
        if left_diagonal_string == "OOO" or right_diagonal_string == "OOO":
            return "O"
        return ""

    def vertical_win(self, column):
        concat = ""
        for i in range(len(self.board)):
            concat += self.board[i][column - 1]
        if concat == "XXX":
            return "X"
        if concat == "OOO":
            return "O"
        return ""

    def horizontal_win(self):
        concat = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                concat += self.board[i][j]
        if "XXX" in concat:
            return "X"
        if "OOO" in concat:
            return "O"
        return ""

    def game_win(self, winner):
        if winner == "X" or winner == "O":
            print(f"Congratulations {winner}! You won!")
            return True
    
    def game_tie(self, count):
        if count == 9:
            return True
