'''
    CS 5001
    Spring 2022
    Final Project
    Zachary Jacobs

    Class: Button
    Contains the class description methods for created
    class Button used for the check, cancel, and quit
    buttons in the Mastermind game controls.
'''
import turtle
from Point import Point

class Button:
    def __init__(self, name, position, shape):
        '''
        Method -- __init__
        Initializes an instance of a Button class object. Creates a
        Turtle instance for the Button and changes the shape to
        the desired button image and moves it to the correct location.
        Parameters:
            name -- string of the name of the button
            position -- Point class object containing the x and y
                coordinates of the center of the button.
            shape -- .gif file that the turtle shape will be changed to.
        '''
        self.name = name
        self.pen = self.new_pen()
        self.pen.penup()
        self.pen.speed(0)
        self.position = position
        self.pen.goto(position.x, position.y)
        self.shape = shape
        self.pen.shape(shape)

    def new_pen(self):
        '''
        Method -- new_pen
        Creates and returns a new Turtle instance.
        '''
        return turtle.Turtle()
