# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# Importing Necessary Modules
import simplegui
import random

#Global Variables
secret_number = 0
num_range = 100
num_of_trials = 7

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here

    # remove this when you add your code    
    global secret_number,num_of_trials
    secret_number = random.randrange(num_range)
    print "New game. Range is 0 to", num_range
    if num_range == 100:
        num_of_trials = 7
    else:
        num_of_trials = 10
    print "Number of remaining guesses",num_of_trials
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range,num_of_trials
    num_range,num_of_trials = 100,7
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range, num_of_trials
    num_range,num_of_trials = 1000,10
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    global secret_number,num_of_trials
    num_of_trials -= 1
    print "Guess was",guess
    guess = int(guess)
    if guess == secret_number:
        print "Correct!"
        new_game()
    else:
        if guess > secret_number:
            print "Higher"
        else:
            print "Lower"
        print "Number of remaining guess", num_of_trials
    if num_of_trials == 0:
        print "You Lose"
        new_game()
        
# create frame
frame = simplegui.create_frame("Guess The Number", 200,200)

# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100",range100,150)
frame.add_button("Range: 0 - 1000",range1000,150)
frame.add_input("Enter Guess",input_guess,100)
frame.start()

# call new_game 
new_game()

# always remember to check your completed program against the grading rubric
