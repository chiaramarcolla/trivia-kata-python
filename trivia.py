#!/usr/bin/env python3

class DummyClass:
    def __init__(self):
        self.bad_players = []
        self.cheaters = []
        self.losers = []

    def create_who_is_a_cheater(self, index):
        return "Cheater is %s" % index

class IsWinner:
    def isNotAWinner(self, number_of_coins):
        return not number_of_coins == 6

class CurrentCategory:
    def current_category(self, current_player_place):
        if current_player_place == 0: return 'Pop'
        if current_player_place == 4: return 'Pop'
        if current_player_place == 8: return 'Pop'
        if current_player_place == 1: return 'Science'
        if current_player_place == 5: return 'Science'
        if current_player_place == 9: return 'Science'
        if current_player_place == 2: return 'Sports'
        if current_player_place == 6: return 'Sports'
        if current_player_place == 10: return 'Sports'
        return 'Rock'


class AskQuestion:
    def __init__(self):
        self.pop_questions = []
        self.science_questions = []
        self.sports_questions = []
        self.rock_questions = []


        for i in range(50):
            self.pop_questions.append("Pop Question %s" % i)
            self.science_questions.append("Science Question %s" % i)
            self.sports_questions.append("Sports Question %s" % i)
            self.rock_questions.append(self.create_rock_question(i))


    def create_rock_question(self, index):
        return "Rock Question %s" % index

    def ask(self, current_category):
        if current_category == 'Pop': print(self.pop_questions.pop(0))
        if current_category == 'Science': print(self.science_questions.pop(0))
        if current_category == 'Sports': print(self.sports_questions.pop(0))
        if current_category == 'Rock': print(self.rock_questions.pop(0))


class Game:
    def __init__(self):
        self.current_category = CurrentCategory()
        self.ask_question = AskQuestion()
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6


        self.current_player = 0
        self.is_getting_out_of_penalty_box = False



        self.badgame = DummyClass()

        self.is_winner = IsWinner()



    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False

        print(player_name + " was added")
        print("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)

    def roll(self, roll):
        print("%s is the current player" % self.players[self.current_player])
        print("They have rolled a %s" % roll)

        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True

                print("%s is getting out of the penalty box" % self.players[self.current_player])
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12

                print(self.players[self.current_player] + \
                      '\'s new location is ' + \
                      str(self.places[self.current_player]))
                print("The category is %s" % self._current_category)
                self._ask_question()
            else:
                print("%s is not getting out of the penalty box" % self.players[self.current_player])
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12

            print(self.players[self.current_player] + \
                  '\'s new location is ' + \
                  str(self.places[self.current_player]))
            print("The category is %s" % self._current_category)
            self._ask_question()

    def _ask_question(self):
        self.ask_question.ask(self._current_category)

    @property
    def _current_category(self):
        current_player_place = self.places[self.current_player]
        return self.current_category.current_category(current_player_place)

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print('Answer was correct!!!!')
                self.purses[self.current_player] += 1
                print(self.players[self.current_player] + \
                      ' now has ' + \
                      str(self.purses[self.current_player]) + \
                      ' Gold Coins.')

                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0

                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True



        else:

            print("Answer was corrent!!!!")
            self.purses[self.current_player] += 1
            print(self.players[self.current_player] + \
                  ' now has ' + \
                  str(self.purses[self.current_player]) + \
                  ' Gold Coins.')

            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0

            return winner

    def wrong_answer(self):
        print('Question was incorrectly answered')
        print(self.players[self.current_player] + " was sent to the penalty box")
        self.in_penalty_box[self.current_player] = True

        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True

    def _did_player_win(self):
        return self.is_winner.isNotAWinner(self.purses[self.current_player])


from random import randrange
from random import seed
import sys

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    if len(sys.argv) > 1:
        seed(sys.argv[1])

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    rolls = []
    i = 0
    while True:
        current_roll = randrange(5) + 1
        game.roll(current_roll)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break
