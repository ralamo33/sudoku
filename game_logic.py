import random
import math
import unittest
import solver

"""The logic behind running a game of sudoku."""


class Tile:
    """A single tile of a Sukdou board"""

    def __init__(self, num=-1):
        self.num = num

    def assign_number(self, num):
        if not isinstance(num, int):
            raise Exception("Wrong input type.")
        self.num = num

    def display(self):
        """Display this tile.

        :return self.num as a String
        """
        if self.num == -1:
            return "_"
        return str(self.num)

class SolvedError(Exception):
    """Raise the exception when you attempt to solve an already solved board tile."""

    def __init__(self, message="Tile already solved", errors=None):
        super().__init__(message)
        self.errors = errors

def initialize_board():
    board = []
    for i in range(0, 9):
        row = []
        for j in range(0, 9):
            row.append(Tile())
        board.append(row)
    return board

def solve_board(board):
    """Solve the Sudoku board for the user.
    :param board (List of Tile): The Sudoku board.
    """
    rows = solver.knuth_algorithm(solver.KnuthMatrix(solver.init_rows(), solver.init_cols()))
    for row in rows:
        cell = row.get_header()
        board[cell[0]][cell[1]].assign_number(cell[2])
    return display(board)



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

def board_coordinates():
    """Get a list of all the coordinates for the Sudoku tiles."""
    for i in range(0, 9):
        for j in range(0, 9):
            yield (i, j)

def solve_tile(board, coordinates):
    """Solve a single tile on the Sudoku board.

    :parameter board (List) The board Sudoku is played on.
    :parameter coordinates (Tuple) The (row, col) pair where the tile to be solved is

    :return board (List) one more tile has been solved.
    """
    tile = board[coordinates[0]][coordinates[1]]
    if tile.num != -1:
        raise SolvedError()
    else:
        solutions = [i for i in range(1, 10)]
        eliminate_row(board[coordinates[0]], solutions)
        eliminate_col(board, coordinates[1], solutions)
        eliminate_submatrix(board, coordinates, solutions)
        selected_solution = random.randrange(0, len(solutions))
        tile.assign_number(solutions[selected_solution])

def eliminate_row(row, solutions):
    """Remove entries in the tile's row from the list of potential solutions.

    :parameter row (list): The tiles in a row of the board.

    :returns The numbers used to solve tiles in this row.
    """
    for tile in row:
            eliminate_solution(tile.num, solutions)
    return solutions

def eliminate_col(board, col, solutions):
    """Remove entries in the tile's column from the list of potential solutions.

    :parameter board (List): The Sudoku board.
    :paramter col (int): The number of the tile's column.
    :parameter solutions (List): List of potential solutions.

    :return solutions (List): Solutions without any entries from tile's column.
    """
    for r in board:
        solutions = eliminate_solution(r[col].num, solutions)
    return solutions

def eliminate_submatrix(board, coordinates, solutions):
    """Remove entries in the tile's submatrix from the list of potential solutions.

        :parameter board (List): The Sudoku board.
        :paramter coordinates (int, int): The coordinates of the tile.
        :parameter solutions (List): List of potential solutions.

        :return solutions (List): Solutions without any entries from tile's submatrix.
    """
    row = coordinates[0]
    col = coordinates[1]
    startr = math.floor(row / 3) * 3
    startc = math.floor(col / 3) * 3
    endr = startr + 3
    endc = startc + 3
    for r in range(startr, endr):
        for c in range(startc, endc):
            solutions = eliminate_solution(board[r][c].num, solutions)
    return solutions


def eliminate_solution(eliminate, solutions):
    """Remove eliminate from the list of solutions if possible.

    :parameter eliminate (int) A solution to eliminate.
    :parameter solutions (List) List of still valid solutions.

    :return solutions (List) Eliminate is not present in solutions.
    """
    if eliminate != -1 and solutions.__contains__(eliminate):
        solutions.remove(eliminate)
    return solutions


def display(board):
    """Display the given board.

    :parameter board (List): The board Soduku is played on.

    :return image (String): Represents the image of the board.
    """
    r = []
    for row in board:
        col = []
        for tile in row:
            col.append(tile.display())
        r.append(" ".join(col))
    image = "\n".join(r)
    return image

if __name__ == "__main__":
   print(solve_board(initialize_board()))