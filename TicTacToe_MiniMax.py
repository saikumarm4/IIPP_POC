"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    board_clone = board.clone()
    moves = board_clone.get_empty_squares()
    if moves == [] or board_clone.check_win() == provided.DRAW:
        return 0, (-1, -1)
    elif board_clone.check_win() == provided.PLAYERX:
        return SCORES[provided.PLAYERX], (-1, -1)
    elif board_clone.check_win() == provided.PLAYERO:
        return SCORES[provided.PLAYERO], (-1, -1)
    
    scores_moves = []
    for move in moves:
        temp_board_clone = board_clone.clone()
        temp_board_clone.move(move[0], move[1], player)
        if temp_board_clone.check_win() == None:
            scores_moves.append(mm_move(temp_board_clone, provided.switch_player(player)))
        elif temp_board_clone.check_win() == provided.PLAYERX:
            scores_moves.append((SCORES[provided.PLAYERX], (-1, -1)))
        elif temp_board_clone.check_win() == provided.PLAYERO:
            scores_moves.append((SCORES[provided.PLAYERO], (-1, -1)))
        elif temp_board_clone.check_win() == provided.DRAW:
            scores_moves.append((SCORES[provided.DRAW], (-1, -1)))
    scores = [score for score, move in scores_moves]
    if player == provided.PLAYERX:
        return max(scores), moves[scores.index(max(scores))]
    elif player == provided.PLAYERO:
        return min(scores), moves[scores.index(min(scores))]
    
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
