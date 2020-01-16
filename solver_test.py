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
        matrix = KnuthMatrix()
        column_activations = defaultdict(int)
        for header, krow in matrix.rows.items():
            for column in krow.knuth_cols:
                column_activations[column] += 1
        for k, v in column_activations.items():
            self.assertEqual(9, v)



if __name__ == '__main__':
    unittest.main()
