import unittest
from solver import *


class MyTestCase(unittest.TestCase):
    def test_intialization(self, matrix=DancingMatrix()):
        self.assertEqual(matrix.header.size(), 324)
        for col in matrix.header:
            self.assertEqual(col.size(), 9)
            for node in col:
                self.assertTrue(col.index in matrix.get_constraints(node.row, node.col, node.num))
                self.assertEqual(col, node.header)
                self.assertEqual(4, node.size())

    def test_remove_restore(self):
        matrix = DancingMatrix()
        col = matrix.header.right
        col.remove()
        self.assertEqual(323, matrix.header.size())
        for element in col:
            for entry in DancingIterator(element, True):
                entry.remove()
        self.assertEqual(9, col.size())
        col.restore()
        for element in col:
            for entry in DancingIterator(element, True):
                entry.restore()
        self.assertEqual(324, matrix.header.size())
        row_total = 0
        for col in matrix.header:
            row_total += col.size()
        self.test_intialization(matrix)
        matrix.select(col.bottom)
        self.assertEqual(320, matrix.header.size())
        matrix.backtrack()
        self.test_intialization(matrix)

    def test_knuth_algorithm(self):
        matrix = DancingMatrix()
        matrix.knuth_algorithm()



if __name__ == '__main__':
    unittest.main()
