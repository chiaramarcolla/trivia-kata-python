from unittest import TestCase

from trivia import IsWinner


class TestIsWinner(TestCase):

    def test_with_6_coins_you_are_not_winner(self):
        assert (IsWinner().isNotAWinner(6) == False)
