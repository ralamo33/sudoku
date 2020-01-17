import unittest
from solver import *
from _collections import defaultdict


class MyTestCase(unittest.TestCase):

    def test_row_builder(self):
        self.assertEqual((10, 94, 175, 247), KnuthRow(1, 1, 5).knuth_cols)
        self.assertEqual((38, 124, 187, 277), KnuthRow(4, 2, 8).knuth_cols)
        self.assertEqual((80, 161, 242, 323), KnuthRow(8, 8, 9).knuth_cols)
        self.assertEqual((59, 135, 207, 306), KnuthRow(6, 5, 1).knuth_cols)

    def test_row_builder_iterator(self):
        row_builders = []
        iterator = RowGenerator()
        for rb in iterator:
            row_builders.append(rb)
        self.assertEqual(729, len(row_builders))

    def test_matrix_(self):
        """Testing that each column of the matrix is active in 9 rows.
        This is how the matrix of a 3 X 3 sudoku board should be."""
        matrix = KnuthMatrix(init_rows(), init_cols())
        column_activations = defaultdict(int)
        for header, krow in matrix.rows.items():
            for column in krow.knuth_cols:
                column_activations[column] += 1
        for k, v in column_activations.items():
            self.assertEqual(9, v)

    def test_get_active_rows(self):
        """Test get active rows method in Matrix."""
        matrix = KnuthMatrix(init_rows(), init_cols())
        active = matrix.get_active_rows(0)
        self.assertEqual(9, len(active))
        for row in active:
            self.assertEqual(0, row.row)
            self.assertEqual(0, row.col)

    def test_knuth_algorithm(self):
            selected = knuth_algorithm(KnuthMatrix(init_rows(), init_cols()))
            print(selected)

    def test_copy(self):
        original = KnuthRow(1, 1, 5)
        new = original.__copy__()
        self.assertEqual(original.get_header(), new.get_header())
        original.num = 8
        self.assertNotEqual(original.get_header(), new.get_header())

    def test_matrix_select(self, header=(6, 3, 3)):
        matrix = KnuthMatrix(init_rows(), init_cols())
        row = matrix.rows[header]
        knuth_cols = row.knuth_cols
        matrix.select(header)
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
        matrix = KnuthMatrix(init_rows(), init_cols())
        self.solve_matrix(matrix, 3, 1)
        self.solve_matrix(matrix, 6, 2)
        self.solve_matrix(matrix, 9, 3)
        self.assertTrue(matrix.is_empty())
        self.assertFalse(matrix.failed())

    def solve_matrix(self, matrix, row_limit, num):
        for row in range((row_limit - 3), row_limit):
            col_num = num
            for col in range(9):
                print(row, col, col_num)
                matrix.select((row, col, col_num))
                col_num = (col_num % 9) + 1
            num += 3

    #Commented out because it takes 45seconds to run. This did pass.
    """    def test_matrix_select_full(self):
        for row in range(9):
            for col in range(9):
                for num in range(1, 10):
                    self.test_matrix_select((row, col, num))"""""

    def test_matrix_copy(self):
        original = KnuthMatrix(init_rows(), init_cols())
        original.select((4, 4, 4))
        copy = original.__copy__()
        self.assertEqual(original.rows.keys(), copy.rows.keys())
        copy.select((2, 1, 8))
        self.assertNotEqual(original.rows.keys, copy.rows.keys())



if __name__ == '__main__':
    unittest.main()
