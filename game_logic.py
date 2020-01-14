"""The logic behind running a game of sudoku."""

board = [[-1 * 9] * 9]

class Tile:
    """A single tile of a Sukdou board"""

    def __init__(self):
        self.num = -1

    def assign_number(self, num):
        if not isinstance(num, int):
            raise Exception("Wrong input type.")
        self.num = num