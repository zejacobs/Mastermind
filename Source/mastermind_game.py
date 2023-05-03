'''
    CS 5001
    Spring 2022
    Final Project
    Zachary Jacobs

    Program: mastermind_game
    This program contains the main function used to run the Mastermind
    game. A Mastermind Gameboard class object is initialized and then
    the Turtle event handler is set up to run the Gameboard object's
    click_handler method to carry out the game functions upon a click
    on the Turtle screen.
'''
from Source.Gameboard import Gameboard
import turtle

def main():

    screen = turtle.Screen()
    gameboard = Gameboard()
    screen.onclick(gameboard.click_handler)
    screen.mainloop()
    
if __name__ == "__main__":
    main()
