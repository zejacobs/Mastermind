# Mastermind

### CS 5001 Spring 2022 Final Project

The file mastermind.py contains a main function that runs my version
of the game Mastermind. In this game a sequence of 4 colors is chosen
at random and the player has 10 guesses to correctly guess the secret
code. Next to each guess are 4 pegs that give feedback about the entered
guess. A black peg means there is a color correctly guessed in the
correct position, a red peg means that a guessed color is present in the
secret code but in the wrong position, and a white peg means that a
color in the guess is not in the secret code. The game ends when the
player correctly guesses the secret code and their score (# of guesses)
is added to the leaderboard file to be displayed on subsequent plays.

This program is entirely built upon the created Gameboard class and
utilizes an object oriented design. Using the Turtle graphics, the
Gameboard class object draws the gameboard and processes screen clicks.
The Gameboard object also reads and writes leaderboard information to a
file and keeps track of guess information, generates the random secret
code, and handles game events by checking a variety of game conditions
stored in it's attributes and using different class methods.
An additonal created class, Marble, is also used to display the controls
of the game guesses as well as keep track of each player's guess.
These Marble objects are integrated into the Gameboard class methods
to carry out game actions and mechanics and utilize Turtle to present
visual feedback of game actions and events to the player.
