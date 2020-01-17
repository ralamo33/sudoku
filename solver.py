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

    def __copy__(self):
        return KnuthRow(self.row, self.col, self.num)

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

    def get_header(self):
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
        return "".join(image)


def init_rows():
    rows = dict()
    for rb in RowGenerator():
        rows.update({rb.get_header(): rb})
    return rows


def init_cols():
    return [index for index in range(324)]


class KnuthMatrix:
    """A matrix that converts a Sudoku board into an exact cover problem. This can be solved by Knuth's Algorithm."""
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def __copy__(self):
        new_rows = dict()
        for header, row in self.rows.items():
            new_rows.update({header:row.__copy__()})
        return KnuthMatrix(new_rows, self.cols.copy())

    def solved(self):
        return (len(self.rows) == 0) & (len(self.cols) == 0)

    def failed(self):
        return (len(self.rows) == 0) ^ (len(self.cols) == 0)

    def select(self, header):
        """Select the cell from the matrix and reduce the matrix appopriately.
        :param matrix (dict): A matrix in a form solvable by Knuth Algorithm.
        :param header (tuple): Indicator of which row in the matrix the selected cell belongs to.
        """
        actives = self.rows.get(header).knuth_cols
        to_delete = []
        for header, row in self.rows.items():
            knuth_cols = row.knuth_cols
            if knuth_cols[0] == actives[0] or knuth_cols[1] == actives[1] or knuth_cols[2] == actives[2] or knuth_cols[3] == actives[3]:
                to_delete.append(header)
        for key in to_delete:
            del self.rows[key]
        for active in actives:
            self.cols.remove(active)

    def get_random_col(self):
        best_columns = []
        min_rows = 100
        for col in self.cols:
            active_rows = len(self.get_active_rows(col))
            if active_rows < min_rows:
                min_rows = active_rows
                best_columns.append(col)
            elif active_rows == min_rows:
                best_columns.append(col)
        return best_columns[random.randrange(0, len(best_columns))]

    def get_active_rows(self, col):
        """Get the rows that are activate at the given column.
        :param col (int): The index of the column.
        :return rows (List): A list of rows that are active at the given column"""
        index = math.floor(col / 81)
        actives = []
        for header, row in self.rows.items():
            if row.knuth_cols[index] == col:
                actives.append(row.__copy__())
        return actives


    def display(self):
        image = []
        for header, row in self.rows.items():
            image.append(row.display())
        return "\n".join(image)

    def write(self, file):
        """Write the matrix to the file.
        :param matrix (dict): A sudoku board as a matrix in exact cover problem format.
        :param file (String): A string representing the file path to the target file.
        """
        f = open(file, "w")
        f.write(self.display())
        f.close()


def knuth_algorithm(matrix, selected=[]):
    """Use knuth's algorithm to solve an exact cover problem.
    :param selected (List): A list of rows that have already been selected.
    :param matrix (KnuthMatrix): A matrix designed for use by Knuth's Algroithm.
    :return selected: The rows that were chosen to be activated."""
    if matrix.solved():
        return selected
    if matrix.failed():
        print("Failed!")
        return None
    col = matrix.get_random_col()
    rows = matrix.get_active_rows(col)
    for row in rows:
        new_matrix = matrix.__copy__()
        new_selected = selected.copy()
        new_matrix.select(row.get_header())
        new_selected.append(row)
        answer = knuth_algorithm(new_matrix, new_selected)
        if answer is None:
            continue
        else:
            return answer





if __name__ == "__main__":
    print((math.ceil(8 / 3)) * 3)