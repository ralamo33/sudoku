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
