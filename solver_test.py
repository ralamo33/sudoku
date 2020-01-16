import unittest
from solver import *


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

    def test_matrix(self):
        matrix = build_knuth_matrix()
        write(matrix, "KnuthMatrix")

if __name__ == '__main__':
    unittest.main()
