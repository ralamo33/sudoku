import random

"""The logic behind running a game of sudoku."""


class Tile:
    """A single tile of a Sukdou board"""
    def __init__(self):
        self.num = -1

    def assign_number(self, num):
        if not isinstance(num, int):
            raise Exception("Wrong input type.")
        self.num = num

def initialize_board():
    row = []
    for i in range(0, 9):
        row.append(Tile())
    board = []
    for j in range(0, 9):
        board.append(row)
    return board


def ready_board(board, reveal=10):
    """Solve a few tiles to ready the board for the player.

    :parameter reveal The number of tiles presolved for the player.

    :return board The board ready for the player
    """
    coordinates = list(board_coordinates())
    for r in range(0, reveal):
        revealed = random.randint(0, len(coordinates) - 1)
        selected = coordinates[revealed]
        del coordinates[revealed]
        solve_tile(board, selected)
    return board

def solve_tile(board, selected):
    pass



def board_coordinates():
    for i in range(0, 9):
        for j in range(0, 9):
            yield (i, j)


if __name__ == "__main__":
    board = initialize_board()
    ready_board(board)
