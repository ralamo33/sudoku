import unittest
from solver import *
from _collections import defaultdict


class MyTestCase(unittest.TestCase):

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
        """Testing that each column of the matrix is active in 9 rows.
        This is how the matrix of a 3 X 3 sudoku board should be."""
        matrix = KnuthMatrix()
        column_activations = defaultdict(int)
        for header, krow in matrix.rows.items():
            for column in krow.knuth_cols:
                column_activations[column] += 1
        for k, v in column_activations.items():
            self.assertEqual(9, v)

    def test_knuth_algorithm(self):
            selected = KnuthMatrix().knuth_algorithm()
            print(selected)

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
