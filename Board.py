import Player


class Board:
    board = [["|", " ", "|", " ", "|", " ", "|"], ["|", " ", "|", " ", "|", " ", "|"],
             ["|", " ", "|", " ", "|", " ", "|"]]

    def __init__(self):
        self.count = None
        self.setup()

    def setup(self):
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                print(self.board[row][col], end='')
            print("\n")

    def CheckInBoard(self, selectedIndex, selectedPlacement, player):
        self.selectedIndex = selectedIndex
        self.selectedPlacement = selectedPlacement;

    def SetPlayerInBoard(self, count, player):
        self.count = count
        for row in range(0, len(self.Board.board)):
            for col in range(0, len(self.Board.board[row])):
                self.Board.CheckInBoard(self, row, col, player)
                if count == 1:
                    Board.board[0][count] = player.symbol
                if count == 2:
                    Board.board[0][count + 1] = player.symbol
                if count == 3:
                    Board.board[0][count + 2] = player.symbol
                if count == 4:
                    Board.board[1][count - 3] = player.symbol
                if count == 5:
                    Board.board[1][count - 2] = player.symbol
                if count == 6:
                    Board.board[1][count - 1] = player.symbol
                if count == 7:
                    Board.board[2][count - 6] = player.symbol
                if count == 8:
                    Board.board[2][count - 5] = player.symbol
                if count == 9:
                    Board.board[2][count - 4] = player.symbol

                print(self.Board.board[row][col], end='')
            print("\n")

    def DiagonalWin(self):
        pass

    def VerticalWin(self):
        pass

    def HorizontalWin(self):
        pass
