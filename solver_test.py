import unittest
from solver import *
from _collections import defaultdict


def find_actives(row, col, number):
    """Helper to test_row_builder. Creates an array with all the indices in the row that are active."""
    row = build_knuth_row(row, col, number)
    active = []
    for index, value in enumerate(row):
        if value:
            active.append(index)
    return active


class MyTestCase(unittest.TestCase):

    def test_row_builder(self):
        active = find_actives(1, 1, 5)
        self.assertEqual([10, 94, 175, 247], build_knuth_row(1, 1, 5))
        active = find_actives(4, 2, 8)
        self.assertEqual([38, 124, 187, 277], build_knuth_row(4, 2, 8))
        active = find_actives(8, 8, 9)
        self.assertEqual([80, 161, 242, 323], build_knuth_row(8, 8, 9))
        active = find_actives(6, 5, 1)
        self.assertEqual([59, 135, 207, 306], build_knuth_row(6, 5, 1))

    def test_row_builder_iterator(self):
        row_builders = []
        iterator = RowGenerator()
        for rb in iterator:
            row_builders.append(rb)
        self.assertEqual(729, len(row_builders))

    def test_matrix_(self):
        """Testing that each column of the matrix is active in 9 rows.
        This is how the matrix of a 3 X 3 sudoku board should be."""
        matrix = build_knuth_matrix()
        column_activations = defaultdict(int)
        for k, v in matrix.items():
            for column in v:
                column_activations[column] += 1
        for k, v in column_activations.items():
            self.assertEqual(9, v)



if __name__ == '__main__':
    unittest.main()
