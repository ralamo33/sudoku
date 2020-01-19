import unittest
from solver import *
from _collections import defaultdict



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



"""
Solves a sudoku board using Knuth's Algorithm."""

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




class MyTestCase(unittest.TestCase):

    def test_sudoku_matrix(self):
        matrix = SudokuMatrix()
        self.assertEqual(len(matrix.grid), 729)
        for row in matrix.grid:
            self.assertEqual(len(row), 324)
        print(matrix.display())

    def test_sudoku_matrix_speed(self):
        # .008s, 8ms
        SudokuMatrix()

    def test_new_rows(self):
        matrix = SudokuMatrix()
        col_actives = [0] * len(matrix.grid[0])
        for row in matrix.grid:
            row_actives = 0
            for index, cell in enumerate(row):
                if cell == 1:
                    row_actives += 1
                    col_actives[index] += 1
            self.assertEqual(row_actives, 4)
        for actives in col_actives:
            self.assertEqual(actives, 9)
        f = open("KnuthMatrix", "w")
        f.write(matrix.display())
        f.close()

    def test_row_builder(self):
        matrix = KnuthMatrix()
        self.assertEqual([10, 94, 175, 247], self.get_indexes(matrix.rows[(1, 1, 5)].knuth_cols))
        self.assertEqual([38, 124, 187, 277], self.get_indexes(matrix.rows[(4, 2, 8)].knuth_cols))
        self.assertEqual([80, 161, 242, 323], self.get_indexes(matrix.rows[(8, 8, 9)].knuth_cols))
        self.assertEqual([59, 135, 207, 306], self.get_indexes(matrix.rows[(6, 5, 1)].knuth_cols))

    def get_indexes(self, cols):
        answer = []
        for col in cols:
            answer.append(col.index)
        return answer

    def test_row_builder_iterator(self):
        row_builders = []
        iterator = RowGenerator()
        for rb in iterator:
            row_builders.append(rb)
        self.assertEqual(729, len(row_builders))

    def test_matrix_(self):
        matrix = KnuthMatrix()
        column_activations = defaultdict(int)
        for header, krow in matrix.rows.items():
            for column in krow.knuth_cols:
                column_activations[column] += 1
        for k, v in column_activations.items():
            self.assertEqual(9, v)

    def test_knuth_algorithm(self):
            selected = KnuthMatrix().knuth_algorithm()

    def test_matrix_select(self, header=(6, 3, 3)):
        matrix = KnuthMatrix()
        row = matrix.rows[header]
        knuth_cols = row.knuth_cols
        matrix.select(row, knuth_cols[0])
        cols = matrix.cols
        self.assertEqual(len(cols), 320)
        for c in knuth_cols:
            self.assertTrue(c not in cols)
        rows = matrix.rows
        for i in range(9):
            self.assertTrue((header[0], header[1], i) not in rows)
            self.assertTrue((i, header[1], header[2]) not in rows)
            self.assertTrue((header[0], i, header[2]) not in rows)
        row_min = (math.floor(header[0] / 3) * 3)
        col_min = math.floor(header[1] / 3) * 3
        for row in range(row_min, row_min + 3):
            for col in range(col_min, col_min + 3):
                self.assertTrue((row, col, header[2]) not in rows)

    def test_matrix_solved(self):
        matrix = KnuthMatrix()
        self.solve_matrix(matrix, 3, 1)
        self.solve_matrix(matrix, 6, 2)
        self.solve_matrix(matrix, 9, 3)
        self.assertTrue(matrix.solved())

    def solve_matrix(self, matrix, row_limit, num):
        for row in range((row_limit - 3), row_limit):
            col_num = num
            for col in range(9):
                chosen_row = matrix.rows[(row, col, col_num)]
                chosen_col = chosen_row.knuth_cols[0]
                matrix.select(chosen_row, chosen_col)
                col_num = (col_num % 9) + 1
            num += 3

    def test_matrix_select_full(self):
        for row in range(9):
            for col in range(9):
                for num in range(1, 10):
                    self.test_matrix_select((row, col, num))



if __name__ == '__main__':
    unittest.main()
"""