"""Solves a sudoku board using Knuth's Algorithm."""

class Row_Builder_Iterator:

    def __init__(self):
        #1 is being used with row and column to keep consistent with number
        self.row = 1
        self.col = 1
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.number < 9:
            self.number += 1
        elif self.col < 9:
            self.number = 1
            self.col += 1
        elif self.row < 9:
            self.number = 1
            self.col = 1
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



cover_matrix = []