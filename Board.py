
class Board:
    board = [["| | ", "| | ", "| |"], ["| | ", "| | ", "| | "], ["| | ", "| | ", "| |"]]

    def __init__(self):
        self.setup()

    def setup(self):
        for row in range(0, len(self.board)):
            for col in range(0, 3):
                print(self.board[row][col], end='')
                if col == 2:
                    print('\n')
