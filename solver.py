import collections
import math
import random
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

    def __init__(self, row, col, number, knuth_cols=[]):
        self.row = row
        self.col = col
        self.num = number
        self.knuth_cols = []

    def update_knuth_cols(self, knuth_col):
        """Add a column from the KnuthMatrix to this.
        :param knuth_col (KnuthCol): A column for which this row is active.
        """
        self.knuth_cols.append(knuth_col)

    def get_constraints(self):
        """Return the indices of the KnuthColumns active in this."""
        return (self.row_column_constraints(), self.row_number_constraints(),
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

    def get_header(self):
        """Return a unique identifier for this row."""
        Header = collections.namedtuple('Relation', "row col num")
        return Header(self.row, self.col, self.num)

    def display(self):
        """Turn this into a String.
        :return image (String): This as a string.
        """
        image = [" "] * (self.CONSTRAINT_LENGTH * 4)
        for knuth_col in self.knuth_cols:
            image[knuth_col] = "1"
        return "".join(image)

class KnuthColumn:
    """A column of the Knuth matrix. Represents a single constraint in the Sudoku puzzle."""
    def __init__(self, index):
        self.index = index
        self.knuth_rows = []

    def update_knuth_rows(self, knuth_row):
        """Add a KnuthRow to the list of knuth rows this column is activated on.
        :parameter knuth_row (KnuthRow): A row of the KnuthMatrix this is active on.
        """
        knuth_row.get_header()
        if knuth_row not in self.knuth_rows:
            self.knuth_rows.append(knuth_row)

class DancingColumn:
    def __init__(self, index):
        self.index = index
        self.knuth_rows = []
        self.bottom = self
        self.top = self

    def update_knuth_rows(self, knuth_row):
        new_bottom = DancingLink(knuth_row.get_header)
        new_bottom.top = self
        self.bottom.top = knuth_row
        self.bottom = new_bottom


class DancingLink:
    def __init__(self, header):
        self.header = header
        self.top = self
        self.bottom = self




Removed = collections.namedtuple("Removed", "chosen_pair rows cols")


class KnuthMatrix:
    """A matrix representing a Sudoku board converted into an exact cover problem.
    Each column represents a constraint that needs to be met to solve the puzzle.
    """
    def __init__(self):
        """
        :param rows: (List of KnuthRow):Each row represents a specific number placed on a specific Sudoku tile.
        :param cols: (List of KnuthCol):Each column represents a constraint that needs to be met to solve the puzzle.
        """
        #ToDo: Test that this results in each row being attached to appropriate cols, and vice versa
        self.cols = dict()
        #ToDo: Create a second dictionary that holds columns by their number of rows.
        for index in range(324):
            self.cols.update({index: KnuthColumn(index)})
        self.rows = dict()
        for rb in RowGenerator():
            self.rows.update({rb.get_header(): rb})
            for index in rb.get_constraints():
                chosen_col = self.cols[index]
                rb.update_knuth_cols(chosen_col)
                chosen_col.update_knuth_rows(rb)
        #ToDo: Try replacing this list for a stack.
        self.selected = []
        #Rows that caused failure when selected.
        self.wrong = []

    def knuth_algorithm(self):
        """Use knuth's algorithm to solve the exact cover problem represented by self."""
        while not self.solved():
            # print(len(self.rows), len(self.cols))
            chosen_col = self.get_rand_col()
            #ToDo: Replace with something more efficien
            rows = [row for row in chosen_col.knuth_rows if row not in self.wrong]
            if len(rows) == 0:
                self.backtrack()
                continue
            chosen_row = rows[random.randrange(len(rows))]
            self.select(chosen_row, chosen_col)

    def solved(self):
        """Has this Sudoku puzzle been solved?"""
        return len(self.cols) == 0 & len(self.rows) == 0

    def get_rand_col(self):
        #Todo: Store columns in a dict with the number of active rows as the key.
        best_columns = []
        min_rows = 100
        for index, col in self.cols.items():
            active_rows = len(col.knuth_rows)
            if active_rows < min_rows:
                min_rows = active_rows
                best_columns.append(col)
            elif active_rows == min_rows:
                best_columns.append(col)
        return best_columns[random.randrange(0, len(best_columns))]

    def select(self, row, chosen_col):
        """Select the cell from the matrix and reduce the matrix appopriately."""
        to_delete_cols = row.knuth_cols
        to_delete_rows = []
        for col in to_delete_cols:
            for row in col.knuth_rows:
                to_delete_rows.append(row)
            self.cols.pop(col.index, None)
        self.remove_row(to_delete_rows)
        self.selected.append(Removed((row, chosen_col), to_delete_rows, to_delete_cols))

    def remove_row(self, rows):
        """Remove the given row from this Matrix."""
        for row in rows:
            self.rows.pop(row.get_header(), None)
            #ToDO: Consider giving rows and cols booleans for whether they are in the matrix.
            for col in row.knuth_cols:
                if row in self.rows:
                    col.knuth_rows.remove(row)

    def add_row(self, row):
        self.rows.update({row.get_header(): row})
        for col in row.knuth_cols:
            col.knuth_rows.append(row)

    def backtrack(self):
        """Reverse the previous move after a failure."""
        last_move = self.selected.pop()
        self.wrong.append(last_move.chosen_pair)
        for col in last_move.cols:
            self.cols.update({col.index: col})
        for row in last_move.rows:
            self.add_row(row)

if __name__ == "__main__":
    KnuthMatrix().knuth_algorithm()