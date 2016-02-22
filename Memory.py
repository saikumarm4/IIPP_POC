# implementation of card game - Memory

import simplegui
import random

# Global Variables
CARD_WIDTH = 50
memory_list = range(8) + range(8)
exposed = [False] * 16
random.shuffle(memory_list)
state = 0
idxes = [-1] * 2
turns = 0

# helper function to initialize globals
def new_game():
    global memory_list, exposed, state, idxes, turns
    memory_list = range(8) + range(8)
    random.shuffle(memory_list)
    exposed = [False] * 16
    state, turns = 0, 0
    idxes =[-1] * 2

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, idxes, turns
    if exposed[pos[0] / 50] == True:
        return
    if state == 0:
        idxes[state] = pos[0] / CARD_WIDTH
        exposed[idxes[state]] = True
        state = 1
    elif state == 1:
        turns += 1
        idxes[state] = pos[0] / CARD_WIDTH
        exposed[idxes[state]] = True
        state = 2
    else:
        state = 1
        if memory_list[idxes[0]] != memory_list[idxes[1]]:
            exposed[idxes[0]], exposed[idxes[1]] = False, False
        idxes[0] = pos[0] / CARD_WIDTH
        exposed[idxes[0]] = True
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = 0
    for idx in range(16):
        if exposed[idx]:
            canvas.draw_text(str(memory_list[idx]), [pos + 15, 60], CARD_WIDTH, 'White')
        else:
            canvas.draw_polygon([[pos, 0], [pos + CARD_WIDTH, 0], 
                                 [pos + CARD_WIDTH, 100], [pos, 100]], 1, 'Black', 'Yellow')
        pos += CARD_WIDTH
    label.set_text("Turns = " + str(turns))
        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric