import random
import unittest
import pytest

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
    tile = board[selected[0]][selected[1]]
    if tile.num != -1:
        raise SolvedError("Tile already solved")
    else:
        pass


class SolvedError(Exception):
    """Raise the exception when you attempt to solve an already solved board tile."""

    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors


def board_coordinates():
    for i in range(0, 9):
        for j in range(0, 9):
            yield (i, j)




def test_already_solved():
    board = initialize_board()
    board[0][0].num = 3
    with pytest.raises(SolvedError):
        assert solve_tile(board, (0, 0))

if __name__ == "__main__":
    test_already_solved()
 #   board = initialize_board()
 #   ready_board(board)