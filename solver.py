import math

"""Solves a sudoku board using Knuth's Algorithm."""

CONSTRAINT_LENGTH = 81
HEADER_SPACE = 1

def cell_to_row(row, cell, number):
    """Use a sudoku cell to get the cooresponding row on Knuth Matrix."""



class KnuthMatrix:
    """A Sudoku board converted into an exact cover problem solvable by Knuth's Algorithm."""

    def __init__(self):
        self.matrix = []
        self.row_builder_iterator = RowBuilderIterator()
        for rb in self.row_builder_iterator:
            self.matrix.append(rb)

    def display(self):
        image = []
        for rb in self.matrix:
            image.append(str(rb.make_row()))
        return "\n".join(image).replace(",", " |")

    def write(self, file):
        f = open(file, "w")
        f.write(self.display())
        f.close()

    def select(self, row, col, number):
        """Choose a """


class RowBuilderIterator:
    """Iterates through the RowBuilders which are critical to Knuth's Matrix."""

    def __init__(self):
        self.row = 0
        self.col = 0
        self.number = 0
        self.number_limit = 9
        self.row_limit = 8
        self.col_limit = 8

    def __iter__(self):
        return self

    def __next__(self):
        if self.number < self.number_limit:
            self.number += 1
        elif self.col < self.col_limit:
            self.number = 1
            self.col += 1
        elif self.row < self.row_limit:
            self.number = 1
            self.col = 0
            self.row += 1
        else:
            raise StopIteration
        return RowBuilder(self.row, self.col, self.number)


class RowBuilder:
    """Use this to build a row of the matrix for the Knuth Algorithm."""

    def __init__(self, row, col, number):
        self.row = row
        self.col = col
        self.number = number
        self.building = self._initialize_row()

    def make_row(self):
        """Create a row of the Knuth Algorithm.

        :return building (List): A fully prepared row for Knuth's matrix.
        """
        self.row_column_constraints()
        self.row_number_constraints()
        self.column_number_constraints()
        self.box_constraints()
        return self.building


    def row_column_constraints(self):
        """Activate the appropriate row space for the row number column constraints of this object's row."""
        valid = self.row * 9 + self.col
        self.building[valid] = 1

    def row_number_constraints(self):
        """Activate the appropriate row space for the row column constraints of this object's row."""
        valid = CONSTRAINT_LENGTH + (self.number - 1) + (self.row * 9)
        self.building[valid] = 1

    def column_number_constraints(self):
        """Activate the appropriate row space for the column number constraints of this object's row."""
        valid = (CONSTRAINT_LENGTH * 2) + (self.number - 1) + self.col * 9
        self.building[valid] = 1

    def box_constraints(self):
        """Activate the appropriate row space for the box number constraints of this object's row."""
        box = ((math.floor(self.row / 3)) * 3) + math.floor(self.col / 3)
        valid = (CONSTRAINT_LENGTH * 3) + (box * 9) + (self.number - 1)
        self.building[valid] = 1

    def _initialize_row(self):
        """Intialize a row of the matrix for the Knuth Algroithm.

        :return row (List): An intialized row for this rowbuilder's road.
        """
#        header = ["R" + str(self.row) + "C" + str(self.col) + "#" + str(self.number)]
        return [0] * 384


def knuth_algorithm(matrix, already_selected = None):
    """Use knuth's algorithm to solve an exact cover problem.
    :parameter matrix (KnuthMatrix): A matrix in a form solvable by this algortihm.
    :parameter selected (List): A list of cells that have already been selected.
    :return selected_cells: The cells that were chosen to be activated."""
    for cell in already_selected:
        select(matrix, cell)

def select(matrix, cell):
    """Select the cell from the matrix and reduce the matrix appopriately.

    :parameter matrix (KnuthMatrix): A matrix in a form solvable by this algortihm.
    :parameter cell (Tuple): A tuple of row,cell,number to indicate which row of the matrix is being selected.
    """

    

class KnuthAlgorithm:

    def __init__(self, matrix=KnuthMatrix(), already_selected=None):
     """
    """

    def solve(self, already_selected = None):

        for cell in already_selected:
            self.matrix.select(cell)
        while len(self.matrix) > 0:
            pass

if __name__ == "__main__":
    print(1 == True)
