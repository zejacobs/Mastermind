'''
    CS 5001
    Spring 2022
    Final Project
    Zachary Jacobs

    Class: Gameboard
    Class file containing the Gameboard class. The Gameboard object is
    used to control the Mastermind gameboard using Turtle and carry
    out the different game mechanics necessary to play the game and
    keep track of the game leaders and errors.
'''
from Point import Point
from Marble import Marble
from Source.Button import Button
from datetime import datetime
import turtle, random

MARBLE_COLORS = ["red", "blue", "green", "yellow", "purple", "black"]
# Gameboard dimensions
GUESSES_TOP_LEFT= Point(-380, 340)
GUESSES_LENGTH = 540
GUESSES_WIDTH = 440
CONTROLS_TOP_LEFT = Point(-380, -210)
CONTROLS_LENGTH = 120
CONTROLS_WIDTH = 760
LEADERBOARD_TOP_LEFT = Point(80, 340)
LEADERBOARD_LENGTH = 540
LEADERBOARD_WIDTH = 300
LEADERBOARD_TITLE = Point(120, 300)
# Marble and Guess dimensions
GUESSES = 10
MARBLE_SPACING = 55
GUESS_X_SPACE = 50
GUESS_Y_SPACE = 50
SM_RADIUS = 5
SM_X_SPACING = 20
# Button Coordinates
CHECK_CORDS = Point(0, -270)
CANCEL_CORDS = Point(80, -270)
QUIT_CORDS = Point(260, -270)

class Gameboard:
    def __init__(self):
        '''
        Method -- __init__
        Initializes the Gameboard instance and draws the gameboard in
        a Turtle screen. Calls several methods to create a gameboard
        turtle, create the Marble objects for the controls and to keep
        track of guesses, and create the Button objects check, cancel,
        and quit. Also calls the method to read and write leadboard
        information to be displayed on the gameboard.
        '''
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.speed(0)
        self.screen = turtle.Screen()
        self.player_name = self.set_player_name()
        self.draw_gameboard()
        self.secret_code = self.generate_secret_code()
        self.write_mode = self.write_leaderboard()
        self.marbles = self.create_marbles()
        self.buttons = self.create_buttons()
        self.guesses = self.create_guess_rows(GUESSES)
        self.guess_row = 0
        self.move_row_pointer()
        self.buttons[0].pen.onclick(self.click_check)
        self.buttons[1].pen.onclick(self.click_cancel)
        self.buttons[2].pen.onclick(self.click_quit)

    def draw_gameboard(self):
        '''
        Method -- draw_gameboard()
        Sets the Turtle screen size and draws the differenent sections
        of the Mastermind gameboard.
        '''
        self.pen.hideturtle()
        self.pen.speed(0)
        self.screen.setup(800, 700)
        self.screen.title("CS5001 Mastermind")
        self.draw_rectangle(GUESSES_TOP_LEFT, GUESSES_LENGTH,
                            GUESSES_WIDTH)
        self.draw_rectangle(CONTROLS_TOP_LEFT, CONTROLS_LENGTH,
                            CONTROLS_WIDTH)
        self.pen.pencolor("blue")
        self.draw_rectangle(LEADERBOARD_TOP_LEFT, LEADERBOARD_LENGTH,
                            LEADERBOARD_WIDTH)

    def generate_secret_code(self):
        '''
        Method -- generate_secret_code
        Generates the random 4 color sequence that the player must guess
        to win the Mastermind game.
        Returns a list containing the winning 4 color sequence.
        '''
        colors = []
        for each in MARBLE_COLORS:
            colors.append(each)
        secret_code = []
        for i in range(4):
            random_num = random.randint(0, (len(colors) - 1))
            choice = colors[random_num]
            secret_code.append(choice)
            colors.pop(random_num)
        return secret_code

    def create_marbles(self):
        '''
        Method -- create_marbles
        Creates the Marble class objects used to control and make
        guesses in the Mastermind game.
        Returns a list containg the created Marble objects.
        '''
        marbles = []
        for i in range(len(MARBLE_COLORS)):
            color = MARBLE_COLORS[i]
            marbles.append(Marble(Point(-350 + (MARBLE_SPACING * i),
                                        -280), color))
            marbles[i].draw()
        return marbles

    def create_buttons(self):
        '''
        Method -- create_buttons
        Creates the check, cancel, and quit Button class objects used
        to control and make guesses in the mastermind game.
        Returns a list containg the created Button objects.
        '''
        buttons_gif = ["media/checkbutton.gif", "media/xbutton.gif", "media/quit.gif"]
        for each in buttons_gif:
            self.pen.screen.addshape(each)

        check_button = Button("check", CHECK_CORDS, buttons_gif[0])
        cancel_button = Button("cancel", CANCEL_CORDS, buttons_gif[1])
        quit_button = Button("quit", QUIT_CORDS, buttons_gif[2])
        buttons = [check_button, cancel_button, quit_button]
        return buttons

    def create_guess_rows(self, guesses):
        '''
        Method -- create_guess_rows
        Creates the Marble class objects used to record the player's
        guesses in the mastermind game.
        Parameters:
            guesses -- number of guesses the player gets used to
                determine how many guess rows will be created.
        Returns a list containing the created Marble objects.
        '''
        guess_list = []
        for i in range(guesses):
            guess_row = []
            # Create Marble objects to keep track of guesses
            for j in range(4):
                marble = Marble(Point(-300 + (GUESS_X_SPACE * j),
                                      280 - (GUESS_Y_SPACE * i)),
                                "white")
                marble.draw_empty()
                guess_row.append(marble)
            # Create Marble objects showing correct color/position guess
            for k in range(4):
                if k < 2:
                    marble = Marble(Point(-60 + (SM_X_SPACING * k),
                                          300 - (GUESS_Y_SPACE * i)),
                                    "white", SM_RADIUS)
                    marble.draw_empty()
                    guess_row.append(marble)
                else:
                    h = k - 2
                    marble = Marble(Point(-60 + (SM_X_SPACING * h),
                                          280 - (GUESS_Y_SPACE * i)),
                                    "white", SM_RADIUS)
                    marble.draw_empty()
                    guess_row.append(marble)
            guess_list.append(guess_row)
        return guess_list  

    def write_leaderboard(self):
        '''
        Method -- write_leaderboard
        Loads information from leaderboard.txt and displays the game
        leaders on the screen. Raises an error and displays an error
        message on the turtle screen if leaderboard.txt cannot be found.
        Returns file write mode be used to update the leaderboard if the
        player wins (either a or w).
        '''
        self.pen.penup()
        self.pen.goto(LEADERBOARD_TITLE.x, LEADERBOARD_TITLE.y)
        self.pen.write("LEADERBOARD", font=('Arial', 18, 'normal'))
        leaderboard_data = []
        # Try to open leaderboard.txt. Raise error and message if fail
        try:
            with open("leaderboard.txt", "r") as leaderboard:
                for each in leaderboard:
                    leaderboard_data.append(each)
        except IOError:
            now = datetime.now()
            self.error_log("leaderboard.txt", now)
            self.screen.addshape("media/leaderboard_error.gif")
            self.pen.goto(0, 0)
            self.pen.shape("media/leaderboard_error.gif")
            self.screen.ontimer(self.pen.showturtle(), 4000)
            self.pen.hideturtle()
        # If leader data found, sort leaders and print to turtle screen
        if leaderboard_data != []:
            write_mode = "a"
            for i in range(len(leaderboard_data)):
                leaderboard_data[i] = leaderboard_data[i].split()
            func = lambda x: int(x[0])
            leaderboard_data = sorted(leaderboard_data, key=func)
            for i in range((len(leaderboard_data))):
                leaderboard_data[i] = ' '.join(leaderboard_data[i])
                                         
            x = LEADERBOARD_TITLE.x + 10
            y = LEADERBOARD_TITLE.y - 40
            if len(leaderboard_data) > 15:
                scores_displayed = 15
            else:
                scores_displayed = len(leaderboard_data)
            for i in range(scores_displayed):
                self.pen.goto(x, y - (i * 30))
                self.pen.write(leaderboard_data[i],
                               font=("Arial", 12, "normal"))
        else:
            write_mode = "w"
        # Return "a" if leaderboard.txt exists and "w" if it does not
        return write_mode

    def error_log(self, file, time):
        '''
        Method -- error_log
        Writes an error into mastermind_errors.err file with name of
        the file that could not be opened, date, and time of the error.
        Parameters:
            file -- string of the file name that could not be found.
            time -- string of time and date of error
        '''
        #now = datetime.now()
        with open("mastermind_errors.err", "a") as error_log:
            error_log.write(f"\n{time}:Error: Could not open"\
                            f" {file}")

    def set_player_name(self):
        '''
        Method -- set_player_name
        Opens a text window on the screen and prompts the player to
        enter their name.
        Returns a string containing the player's entered name.
        '''
        return self.screen.textinput("Mastermind", "Your Name")
 
    def move_row_pointer(self):
        '''
        Method -- move_row_pointer
        Moves the arrow pointing to the current guess row being
        used by the player.
        '''
        self.pen.goto(-340, 295 - (GUESS_Y_SPACE * self.guess_row))
        if not self.pen.isvisible():
            self.pen.shape("arrow")
            self.pen.showturtle()
        
    def click_handler(self, x, y):
        '''
        Method -- click_handler
        Checks to see if any of the Marble objects circle drawings
        have been clicked. If one has been clicked it then calls
        the marble_event method to determine further actions of the
        game.
        Parameters:
            x -- x coordinate of click from Turtle screen click handler
            y -- y coordinate of click from Turtle screen click handler
        '''
        for i in range(len(self.marbles)):
            if self.marbles[i].clicked_in_region(x, y):
                self.marble_event(self.marbles[i])

    def marble_event(self, marble):
        '''
        Method -- marble_event
        Checks the conditions of the gameboard to determine what should
        be done when a Marble control object is clicked. Checks if the
        clicked marble has already been clicked to prevent duplicate
        colors in a guess and if the guess is less than 4 colors long
        to determine if the clicked marble color should be added to
        the current guess
        Parameters:
            marble -- Marble object that was clicked by the player
        '''
        guess_row = self.guess_row
        guesses = self.guesses
        color = marble.get_color()
        if not marble.get_empty():
            for i in range(4):
                if guesses[guess_row][i].get_empty():
                    marble.draw_empty()
                    guesses[guess_row][i].set_color(color)
                    guesses[guess_row][i].draw()
                    break
        
    def click_check(self, x, y):
        '''
        Method -- click_check
        Handles the games behavior when the "check" button is clicked.
        Checks to see that there are four colors in the player's
        guess and then calls the check_guess method to check if the
        player has guessed correctly.
        '''
        guess_colors = []
        if not self.guesses[self.guess_row][3].get_empty():
            for i in range(4):
                guess_colors.append(
                    self.guesses[self.guess_row][i].get_color())
            self.check_guess(guess_colors, self.secret_code)
            
    def check_guess(self, guess_colors, secret_code):
        '''
        Method -- check_guess
        Compares the player's guess to the secret code to see if they
        won. If the guess is incorrect the marbles indicating a correct
        color + position or a correct color in the guess will be updated
        and the game will move on to the next guess row.
        Parameters:
            guess_colors -- a list containing the players guesss
            secret_code -- a list containing the correct color sequence
        '''
        if guess_colors == secret_code:
            self.player_wins()
        else:
            correct, correct_color = 0, 0
            # Check if any correct color/positions were in the guess
            for j in range(len(guess_colors)):
                if guess_colors[j] == secret_code[j]:
                    correct += 1
                elif guess_colors[j] in secret_code:
                    correct_color += 1
            # Updates scoring pegs to next to the player's guess
            for k in range(4, 8):
                if correct > 0:
                    self.guesses[self.guess_row][k].set_color("black")
                    self.guesses[self.guess_row][k].draw()
                    correct -= 1
                elif correct_color > 0:
                    self.guesses[self.guess_row][k].set_color("red")
                    self.guesses[self.guess_row][k].draw()
                    correct_color -= 1
            self.guess_row += 1
            # Check if player made last guess and has lost
            if self.guess_row == GUESSES:
                self.player_loses()
            # Reset control marbles and proceed to next guess row
            else:
                self.move_row_pointer()
                self.reset_marbles()
    
    def reset_marbles(self):
        '''
        Method -- reset_marbles
        Resets the control marbles so that they are all drawn filled
        and able to be clicked to make a guess.
        '''
        for i in range(len(self.marbles)):
            self.marbles[i].draw()

    def reset_guess(self):
        '''
        Method -- reset_guess
        Resets the current guess row marbles so that they are drawn
        empty and able to be changed to a new color in a new guess.
        '''
        for i in range(4):
            self.guesses[self.guess_row][i].draw_empty()
    
    def display_gif(self, gif):
        '''
        Method -- display_gif
        Changes the gameboard's turtle pen to the passed .gif file
        and displays the image in the middle of the game screen.
        Parameters:
            gif -- string of the name of the .gif file that will be
                displayed on screen.
        '''
        try:
            self.screen.addshape(gif)
            self.pen.goto(0, 0)
            self.pen.shape(gif)
            self.screen.ontimer(self.pen.showturtle(), 5000)
        except:
            now = datetime.now()
            self.error_log(gif, now)
           
    def player_wins(self):
        '''
        Method -- player_wins
        Displays the win message on screen to the player and calls the
        method update_leaderboard to add the players score to the
        leaderboard if the player guesses the secret code.
        '''
        self.display_gif("media/winner.gif")
        self.screen.bye()
        self.update_leaderboard()

    def update_leaderboard(self):
        '''
        Method -- update_leaderboard
        Adds the player's score to the leaderboard.txt file or creates
        a leaderboard.txt file if one does not exist already.
        '''
        score = str(self.guess_row + 1) + " : " + self.player_name 
        with open("leaderboard.txt", self.write_mode) as leaderboard:
            if self.write_mode == "a":
                leaderboard.write("\n" + score)
            else:
                leaderboard.write(score)

    def player_loses(self):
        '''
        Method -- player_loses
        Displays a lose message on screen to the player and then shows
        the correct secret code.
        '''
        self.display_gif("media/Lose.gif")
        self.screen.textinput("Secret Code was:",
                              f"{self.secret_code}")
        self.screen.bye()
        
    def click_cancel(self, x, y):
        '''
        Method -- click_cancel
        Calls the reset_marbles and reset_guess methods upon the player
        clicking the cancel ("X") button to clear their current guess
        and allow them to make a new one.
        '''
        self.reset_marbles()
        self.reset_guess()

    def click_quit(self, x, y):
        '''
        Method -- click_quit
        Displays a quit message to the screen when the player clicks the
        quit button and closes the game.
        '''
        self.display_gif("media/quitmsg.gif")
        self.screen.bye()

    def draw_rectangle(self, point, length, width):
        '''
        Method -- draw_rectangle
        Draws a rectangle of a passed in length and width with the top
        left corner at the x/y coordinates passed in by the "point"
        parameter.
        Parameters:
            point -- Point class object containing the x/y coordinates
                of the top left corner of the drawn rectangle.
            length -- integer of the length of the drawn rectangle.
            width -- integer of the width of the drawn rectangle.
        '''
        x = point.x
        y = point.y
        self.pen.penup()
        self.pen.pensize(5)
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.goto((x + width), y)
        self.pen.goto((x + width), (y - length))
        self.pen.goto(x, (y - length))
        self.pen.goto(x, y)
        
