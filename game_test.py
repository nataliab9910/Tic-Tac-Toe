"""Testy modułu game."""

import unittest

import game


class MinimaxTest(unittest.TestCase):
    # pylint: disable=missing-function-docstring
    # pylint: disable=missing-class-docstring

    def setUp(self):
        self.game = game.Game()

    def test_computer_win_row(self):
        self.game.board = [1, 1, ' ',
                           0, 0, ' ',
                           ' ', ' ', ' ']
        self.game.current_player = game.COMPUTER
        self.game.computers_move()
        self.assertEqual(self.game.board, [1, 1, 1,
                                           0, 0, ' ',
                                           ' ', ' ', ' '])
        self.assertEqual(self.game.current_player, game.COMPUTER_WIN)

    def test_computer_lose_row(self):
        self.game.board = [1, ' ', ' ',
                           0, 0, ' ',
                           ' ', ' ', ' ']
        self.game.current_player = game.COMPUTER
        self.game.computers_move()
        self.assertEqual(self.game.board, [1, ' ', ' ',
                                           0, 0, 1,
                                           ' ', ' ', ' '])
        self.assertEqual(self.game.current_player, game.HUMAN)

    def test_computer_win_column(self):
        self.game.board = [1, 1, 0,
                           0, 1, ' ',
                           0, ' ', ' ']
        self.game.current_player = game.COMPUTER
        self.game.computers_move()
        self.assertIn(self.game.board, ([1, ' ', 0,
                                         0, 1, ' ',
                                         0, ' ', 1],
                                        [' ', 1, 0,
                                         0, 1, ' ',
                                         0, 1, ' ']))
        self.assertEqual(self.game.current_player, game.COMPUTER_WIN)

    def test_computer_lose_column(self):
        self.game.board = [1, ' ', ' ',
                           0, 1, 0,
                           ' ', ' ', 0]
        self.game.current_player = game.COMPUTER
        self.game.computers_move()
        self.assertEqual(self.game.board, [1, ' ', 1,
                                           0, 1, 0,
                                           ' ', ' ', 0])
        self.assertEqual(self.game.current_player, game.HUMAN)

    def test_computer_win_diagonal(self):
        self.game.board = [1, ' ', 0,
                           0, 1, 1,
                           0, ' ', ' ']
        self.game.current_player = game.COMPUTER
        self.game.computers_move()
        self.assertEqual(self.game.board, [1, ' ', 0,
                                           0, 1, ' ',
                                           0, ' ', 1])
        self.assertEqual(self.game.current_player, game.COMPUTER_WIN)

    def test_computer_lose_diagonal(self):
        self.game.board = [0, 1, ' ',
                           1, 0, 1,
                           ' ', 0, ' ']
        self.game.current_player = game.COMPUTER
        self.game.computers_move()
        self.assertIn(self.game.board, ([0, 1, ' ',
                                         ' ', 0, 1,
                                         ' ', 0, 1],
                                        [0, 1, ' ',
                                         1, 0, ' ',
                                         ' ', 0, 1]))
        self.assertEqual(self.game.current_player, game.HUMAN)

    def test_evaluate(self):
        self.assertEqual(game.Game.evaluate([' ', 0, 0,
                                             1, 1, 1,
                                             ' ', ' ', 0]), game.WIN_SCORE)
        self.assertEqual(game.Game.evaluate([0, 0, 1,
                                             ' ', 1, ' ',
                                             1, ' ', 0]), game.WIN_SCORE)
        self.assertEqual(game.Game.evaluate([' ', 0, 1,
                                             0, 0, 1,
                                             ' ', ' ', 1]), game.WIN_SCORE)
        self.assertEqual(game.Game.evaluate([0, 0, 0,
                                             1, 1, ' ',
                                             ' ', ' ', 1]), game.LOSE_SCORE)
        self.assertEqual(game.Game.evaluate([' ', ' ', 0,
                                             1, 0, 1,
                                             0, ' ', 1]), game.LOSE_SCORE)
        self.assertEqual(game.Game.evaluate([' ', 0, ' ',
                                             1, 0, 1,
                                             ' ', 0, 1]), game.LOSE_SCORE)
        self.assertEqual(game.Game.evaluate([1, 0, 0,
                                             1, 1, 0,
                                             ' ', ' ', ' ']), game.NO_WINNER)
        self.assertEqual(game.Game.evaluate([' ', 0, 0,
                                             0, 1, 1,
                                             ' ', ' ', 1]), game.NO_WINNER)


if __name__ == '__main__':
    unittest.main()
