import unittest
from solver import *

class MyTestCase(unittest.TestCase):

    def test_linked_matrix(self):
        matrix = LinkedMatrix()
        self.assertEqual(325, len(matrix.cols))
        for col in matrix.cols:
            self.assertEqual(9, col.size())















    def test_sudoku_matrix(self):
        matrix = SudokuMatrix()
        self.assertEqual(len(matrix.grid), 729)
        for row in matrix.grid:
            self.assertEqual(len(row), 324)
        print(matrix.display())

    def test_sudoku_matrix_speed(self):
        #.008s, 8ms
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
        






if __name__ == '__main__':
    unittest.main()
