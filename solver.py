import math

"""Solves a sudoku board using Knuth's Algorithm."""

CONSTRAINT_LENGTH = 81

class KnuthMatrix:

    def __init__(self):
        self.matrix = []
        self.row_builder_iterator = RowBuilderIterator()
        for rb in self.row_builder_iterator:
            self.matrix.append(rb.make_row())

    def display(self):
        image = []
        for row in self.matrix:
            image.append(str(row))
        return "\n".join(image).replace(",", " |")

    def write(self, file):
        f = open(file, "w")
        f.write(self.display())
        f.close()


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




if __name__ == "__main__":
    print(1 == True)
