import collections
import math
import random
"""Solves a sudoku board using Knuth's Algorithm."""

class SudokuMatrix():
    """A matrix representing the Sudoku board as an exact cover problem."""

    def __init__(self, submatrix_size=3):
        """
        :param submatrix_size: The size of a box in the Sudoku board. This is 3 for a standard game.
        """
        self.submatrix = submatrix_size
        #Size of a side of the Sudoku puzzle
        self.size = submatrix_size ** 2
        self.constraint_length = self.size ** 2
        self.rows = self.size ** 3
        self.cols = (self.size ** 2) * 4
        self.grid = []
        for row in range(self.rows):
            self.grid.append([0] * self.cols)
            self.get_constraints(row)

    def get_constraints(self, index):
        """Return the indices of the KnuthColumns active in this."""
        row = math.floor(index / (self.size ** 2))
        col = math.floor((index % (self.size ** 2)) / self.size)
        num = index % self.size + 1
        self.grid[index][self._cell_constraints(row, col)] = 1
        self.grid[index][self._row_constraints(row, num)] = 1
        self.grid[index][self._column_constraints(col, num)] = 1
        self.grid[index][self._submatrix_constraints(row, col, num)] = 1

    def _cell_constraints(self, row, col):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return row * self.size + col

    def _row_constraints(self, row, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return self.constraint_length + (num - 1) + (row * self.size)

    def _column_constraints(self, col, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return (self.constraint_length * 2) + (num - 1) + col * self.size

    def _submatrix_constraints(self, row, col, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        box = ((math.floor(row / self.submatrix)) * self.submatrix) + math.floor(col / self.submatrix)
        return (self.constraint_length * self.submatrix) + (box * self.size) + (num - 1)

    def display(self):
        image = []
        for row in self.grid:
            row_image = []
            for cell in row:
                if cell == 0:
                    row_image.append(" ")
                else:
                    row_image.append(str(cell))
            image.append(" ".join(row_image))
        return "\n".join(image)


class DancingNode:
    """A quadrably linked node."""
    def __init__(self, index=0):
        self.left = self.right = self.bottom = self.top = self
        self.index = index



    def link_top(self, top):
        top.bottom = self
        top.top = self.top
        self.top.bottom = top
        self.top = top
        
    def link_bottom(self, bottom):
        bottom.top = self
        bottom.bottom = self.bottom
        self.bottom.top = bottom
        self.bottom = bottom
        
    def link_left(self, left):
        left.right = self
        left.left = self.left
        self.left.right = left
        self.left = left
        
    def link_right(self, right):
        right.left = self
        right.right = self.right
        self.right.left = right
        self.right = right

    def remove_horizontal(self):
        self.left.right = self.right
        self.right.left = self.left

    def remove_vertical(self):
        self.top.bottom = self.bottom
        self.bottom.top = self.top

    def restore_horizontal(self):
        self.left.right = self
        self.right.left = self

    def restore_vertical(self):
        self.top.bottom = self
        self.bottom.top = self


class DancingColumn:
    def __init__(self, index):
        self.index = index
        self.size = 0
        self.dancing_link = DancingNode()
        self.tried = []

    def link_bottom(self, node):
        self.dancing_link.link_bottom(node)
        self.size += 1

    def link_top(self, node):
        self.dancing_link.link_top(node)

    def link_right(self, node):
        self.dancing_link.link_right(node)

    def link_left(self, node):
        self.dancing_link.link_left(node)

    def remove(self):
        """Remove this column from the dancing matrix."""
        self.dancing_link.remove_horizontal()
        below = self.dancing_link.bottom
        while below is not self:
            below.remove_horizontal()
            below = below.bottom

    def restore(self):
        """Restore this colun back into the dancing matrix."""
        self.dancing_link



class LinkedMatrix:
    """A matrix of dancing links representing a Sodou board converted into an exact cover problem."""
    def __init__(self, size=9):
        """
        :param size: The size of a side of the Soduku board.
        """
        self.size = size
        self.submatrix = math.sqrt(self.size)
        self.constraint_length = self.size ** 2
        self.header = DancingNode()
        self.cols = [self.header]
        for i in range(1, ((size ** 2) * 4) + 1):
            col = DancingColumn(i)
            self.cols[-1].link_right(col)
            self.cols.append(col)
        for i in range(size ** 3):
            node = DancingNode(i)
        for constraint in self.get_constraints(i):
            self.cols[constraint].link_bottom(node)


    def get_constraints(self, index):
        """Return the indices of the KnuthColumns active in this."""
        row = math.floor(index / (self.size ** 2))
        col = math.floor((index % (self.size ** 2)) / self.size)
        num = index % self.size + 1
        return (self._cell_constraints(row, col), self._row_constraints(row, num),
               self._column_constraints(col, num), self._submatrix_constraints(row, col, num))

    def _cell_constraints(self, row, col):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return row * self.size + col + 1

    def _row_constraints(self, row, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return self.constraint_length + num + (row * self.size)

    def _column_constraints(self, col, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        return (self.constraint_length * 2) + num + col * self.size

    def _submatrix_constraints(self, row, col, num):
        """Return the knuth column activated by this row's row-number-column constraints
        :return int"""
        box = ((math.floor(row / self.submatrix)) * self.submatrix) + math.floor(col / self.submatrix)
        return int((self.constraint_length * self.submatrix) + (box * self.size) + num)




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
            print(len(self.rows), len(self.cols))
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