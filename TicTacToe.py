"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 3         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
    
def mc_trial(board, player):
    """
    Simulates one Tic - Tac - Toe Game, Returns from the function
    when it does game ends either any one player wins or game ties
    """
    empty_squares = board.get_empty_squares()
    while board.check_win() == None:
        (row, col) = empty_squares[random.randrange(len(empty_squares))]
        board.move(row, col, player)
        player = provided.switch_player(player)
        empty_squares = board.get_empty_squares()
        if empty_squares == []:
            break

def mc_update_scores(scores, board, player):
    """
    Updates scores, based on the simulated game,
    If the game is a draw bypass updating scores
    """
    if board.check_win() != provided.DRAW:
        player_who_won = board.check_win()
        other_player = provided.switch_player(player)
        
        if player_who_won == player:
            for row in range(board.get_dim()):
                for col in range(board.get_dim()):
                    if board.square(row,col) == player:
                        scores[row][col] += SCORE_CURRENT
                    elif board.square(row,col) == other_player:
                        scores[row][col] -= SCORE_OTHER
        else:
            for row in range(board.get_dim()):
                for col in range(board.get_dim()):
                    if board.square(row,col) == player:
                        scores[row][col] -= SCORE_CURRENT
                    elif board.square(row,col) == other_player:
                        scores[row][col] += SCORE_OTHER

def get_best_move(board, scores):
    """
    Computes the best possible move based on the simulation scores
    """
    empty_squares = board.get_empty_squares()
    scores_list = [ scores[dummy_row][dummy_col] for dummy_row in range(board.get_dim())\
                   for dummy_col in range(board.get_dim()) if (dummy_row,dummy_col) in empty_squares]
    maximum_value = max(scores_list)
    best_moves = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col] == maximum_value:
                best_moves.append((row,col))
    row, col = 0,0
    while 1:
        (row, col) = best_moves[random.randrange(len(best_moves))]
        if (row,col) in empty_squares:
            break
    return row, col

def mc_move(board, player, trials):
    """
    Computes the best possible move using Monte Carlo Method,
    running over a given number of trials
    """
    dimension = board.get_dim()
    scores = [ [0 for dummy_col in range(dimension)] for dummy_row in range(dimension)]
    
    for dummy_trial in range(trials):
        # Here we are simulating a Monte Carlo game
        # The below function returns when the game is over
        board_clone_trial = board.clone()
        mc_trial(board_clone_trial, player)
        mc_update_scores(scores, board_clone_trial, player)
        
    return get_best_move(board, scores)
                                                       

#board.move(2, 2, provided.PLAYERO)
#print mc_move(board, provided.PLAYERX, 3)
                                       
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

