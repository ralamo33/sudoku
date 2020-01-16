import math

"""Solves a sudoku board using Knuth's Algorithm."""

CONSTRAINT_LENGTH = 81


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
        key = (self.row, self.col, self.number)
        return key, build_knuth_row(self.row, self.col, self.number)


def build_knuth_row(row, col, number):
    """Create a row for the Knuth Matrix.
    :param row (int): The row on the Sudoku board to be represented.
    :param col (int): The column on the Sudoku board to be represented.
    :param number (int): The number on the Sudoku board to be represented.
    
    :return building (List): A fully prepared row for Knuth's matrix.
    """
    active = []
    active.append(row_column_constraints(row, col))
    active.append(row_number_constraints(row, number))
    active.append(column_number_constraints(col, number))
    active.append(box_constraints(row, col, number))
    return active

    
def row_column_constraints(row, col):
    """Activate the appropriate row space for the row number column constraints of this object's row."""
    valid = row * 9 + col
    return valid


def row_number_constraints(row, number):
    """Activate the appropriate row space for the row column constraints of this object's row."""
    valid = CONSTRAINT_LENGTH + (number - 1) + (row * 9)
    return valid


def column_number_constraints(col, number):
    """Activate the appropriate row space for the column number constraints of this object's row."""
    valid = (CONSTRAINT_LENGTH * 2) + (number - 1) + col * 9
    return valid


def box_constraints(row, col, number):
    """Activate the appropriate row space for the box number constraints of this object's row."""
    box = ((math.floor(row / 3)) * 3) + math.floor(col / 3)
    valid = (CONSTRAINT_LENGTH * 3) + (box * 9) + (number - 1)
    return valid


def build_knuth_matrix():
    """Create a Sudoku board converted into an exact cover problem solvable by Knuth's Algorithm.
    
    :return matrix (dict): A sudoku board as a matrix in exact cover problem format.
    """
    matrix = dict()
    for rb in RowGenerator():
        matrix.update({rb[0] : rb[1]})
    return matrix


def display(matrix):
    """Display the given knuth_matrix
    :param matrix (dict): A sudoku board as a matrix in exact cover problem format.

    :return image (String): A string representing the matrix.
    """
    image = []
    for rb in matrix:
        row = [0] * 324
        actives = matrix[rb]
        for valid in actives:
            row[valid] = 1
        image.append(str(row))
    return "\n".join(image).replace(",", " |")


def write(matrix, file):
    """Write the matrix to the file.
    :param matrix (dict): A sudoku board as a matrix in exact cover problem format.
    :param file (String): A string representing the file path to the target file.
    """
    f = open(file, "w")
    f.write(display(matrix))
    f.close()


def knuth_algorithm(already_selected = None, matrix = build_knuth_matrix()):
    """Use knuth's algorithm to solve an exact cover problem.
    :param matrix: (dict): A matrix in a form solvable by this algortihm.
    :param already_selected (List): A list of cells that have already been selected.
    :return selected_cells: The cells that were chosen to be activated."""
    for cell in already_selected:
        select(matrix, cell)

def select(matrix, cell):
    """Select the cell from the matrix and reduce the matrix appopriately.

    :param matrix (dict): A matrix in a form solvable by Knuth Algorithm.
    :param cell (tuple): Indicator of which row in the matrix the selected cell belongs to.
    """
    row = matrix.get(cell)
    active = []
    for index, value in enumerate(row):
        if value:
            active.append(index)



if __name__ == "__main__":
    print(1 == True)
