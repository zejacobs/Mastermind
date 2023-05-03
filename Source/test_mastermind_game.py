'''
    CS 5001
    Spring 2022
    Final Project
    Zachary Jacobs

    Program: test_mastermind_game
    Contains test functions to test the non-Turtle methods of the
    Gameboard class used in mastermind.py to play the Mastermind game.
'''
import unittest
from datetime import datetime
from Source.Gameboard import Gameboard, MARBLE_COLORS

class TestGameboard(unittest.TestCase):
    '''
    Test class for Gameboard class in Gameboard.py.
    '''
    def test_generate_secret_code(self):
        '''
        Test function for method generate_secret_code in class Gameboard.
        '''
        gameboard = Gameboard()
        secret_code = gameboard.generate_secret_code()
        self.assertEqual(len(secret_code), 4)
        for each in secret_code:
            self.assertTrue(each in MARBLE_COLORS)

    def test_error_log(self):
        '''
        Test function for the method error_log in class Gameboard.
        '''
        now = datetime.now()
        file = "TEST"
        gameboard = Gameboard()
        gameboard.error_log(file, now)
        file_content = []
        with open("../mastermind_errors.err", "r") as errors:
            for each in errors:
                file_content.append(each)
        logged_error = str(now) + f":Error: Could not open {file}"
        self.assertTrue(logged_error in file_content)
 
