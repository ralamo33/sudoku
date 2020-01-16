import math
import random
import collections

"""Solves a sudoku board using Knuth's Algorithm."""

class RowGenerator:
    """Iterates through the rows of the Knuth's Matrix.
    Specifically, next generates a header and row pair.
    """

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
        return KnuthRow(self.row, self.col, self.number)

class KnuthRow():
    """A row of the Knuth matrix. Stores the header and active columns."""
    CONSTRAINT_LENGTH = 81

    def __init__(self, row, col, number):
        self.row = row
        self.col = col
        self.num = number
        self.knuth_cols = (self.row_column_constraints(), self.row_number_constraints(),
                           self.column_number_constraints(), self.box_constraints())

    def row_column_constraints(self):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return self.row * 9 + self.col

    def row_number_constraints(self):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return self.CONSTRAINT_LENGTH + (self.num - 1) + (self.row * 9)

    def column_number_constraints(self):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return (self.CONSTRAINT_LENGTH * 2) + (self.num - 1) + self.col * 9

    def box_constraints(self):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        box = ((math.floor(self.row / 3)) * 3) + math.floor(self.col / 3)
        return (self.CONSTRAINT_LENGTH * 3) + (box * 9) + (self.num - 1)

    def get_id(self):
        """Return a unique identifier for this row."""
        Header = collections.namedtuple('header', "row col num")
        return Header(self.row, self.col, self.num)


    def display(self):
        """Turn this into a String.
        :return image (String): This as a string.
        """
        image = [" "] * (self.CONSTRAINT_LENGTH * 4)
        for knuth_col in self.knuth_cols:
            image[knuth_col] = "1"
        return image

class KnuthMatrix():
    """A matrix that converts a Sudoku board into an exact cover problem. This can be solved by Knuth's Algorithm."""
    def __init__(self):
        self.rows = dict()
        for rb in RowGenerator():
            self.rows.update({rb.get_id() : rb})

    def display(self):
        image = []
        for header, row in self.matrix.items():
            image.append(row.display())
        return "\n".join(image)

    def write(self, file):
        """Write the matrix to the file.
        :param matrix (dict): A sudoku board as a matrix in exact cover problem format.
        :param file (String): A string representing the file path to the target file.
        """
        f = open(file, "w")
        f.write(self.display)
        f.close()


def knuth_algorithm(selected = None, matrix = None):
    """Use knuth's algorithm to solve an exact cover problem.
    :param already_selected (List): A list of cells that have already been selected.
    :return selected_cells: The cells that were chosen to be activated."""
    columns = [i for i in range(324)]
    selected_column = columns[random.randrange(0, len(columns))]
    rows = []
    constraint = math.floor(selected_column / 81)
    for row, actives in matrix.items():
        if actives[constraint] == selected_column:
            rows.append(row)
    for row in rows:
        select(matrix, row, columns)


def select(matrix, cell, columns):
    """Select the cell from the matrix and reduce the matrix appopriately.

    :param matrix (dict): A matrix in a form solvable by Knuth Algorithm.
    :param cell (tuple): Indicator of which row in the matrix the selected cell belongs to.
    """
    actives = matrix.get(cell)
    for row in matrix:
        other = matrix.get(row)
        if other[0] == actives[0] or other[1] == actives[1] or other[2] == actives[2] or other[3] == actives[3]:
            del matrix[row]
    columns -= actives
    return matrix

        





if __name__ == "__main__":
    print(1 == True)
