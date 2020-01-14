import unittest
from game_logic import *

class TestGameLogic(unittest.TestCase):

    def test_solved_error(self):
        board = initialize_board()
        board[0][0].num = 3
        with self.assertRaises(SolvedError):
            solve_tile(board, (0, 0))

    def test_intialize_board(self):
        board = initialize_board()
        self.assertEqual(len(board), 9)
        for row in range(0, 9):
            self.assertEqual(len(board[row]), 9)
            for col in range(0, 9):
                tile = board[row][col]
                self.assertIsInstance(tile, Tile)
                self.assertEqual(tile.num, -1)

    def test_solved_tile_submatrix(self):
        board = initialize_board()
        submatrix = set()
        for i in range(0, 3):
            for j in range(0, 3):
                tile = board[i][j]
                solve_tile(board, (i, j))
                self.assertNotEqual(tile.num, -1)
                submatrix.add(tile.num)
        expected_submatrix = set(i for i in range(1, 10))
        self.assertEqual(expected_submatrix, submatrix)

    def test_solved_tile_row(self):
        board = initialize_board()
        row = set()
        i = 3
        for j in range(0, 9):
            tile = board[i][j]
            solve_tile(board, (i, j))
            self.assertNotEqual(tile.num, -1)
            row.add(tile.num)
        expected_row = set(i for i in range(1, 10))
        self.assertEqual(expected_row, row)

    def test_solved_tile_column(self):
        board = initialize_board()
        column = set()
        col = 3
        for row in range(0, 9):
            tile = board[row][col]
            solve_tile(board, (row, col))
            self.assertNotEqual(tile.num, -1)
            column.add(tile.num)
        expected_column = set(i for i in range(1, 10))
        self.assertEqual(expected_column, column)


