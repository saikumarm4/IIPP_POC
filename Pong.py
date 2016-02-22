# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# Defined Global Variables

ball_vel = [0, 0]
paddle1_pos = [[0, HEIGHT/2 - HALF_PAD_HEIGHT],
               [PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],
               [PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT],
               [0, HEIGHT/2 + HALF_PAD_HEIGHT]]

paddle2_pos = [[WIDTH - PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],
               [WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],
               [WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT],
               [WIDTH - PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]]
paddle1_vel, paddle2_vel = 20, 20

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == 'left':
        ball_vel = [-random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
    else:
        ball_vel = [random.randrange(120, 240)/60, -random.randrange(60, 180)/60]
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1, score2 = 0, 0
    paddle1_pos = [[0, HEIGHT/2 - HALF_PAD_HEIGHT],
               [PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],
               [PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT],
               [0, HEIGHT/2 + HALF_PAD_HEIGHT]]

    paddle2_pos = [[WIDTH - PAD_WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],
               [WIDTH, HEIGHT/2 - HALF_PAD_HEIGHT],
               [WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT],
               [WIDTH - PAD_WIDTH, HEIGHT/2 + HALF_PAD_HEIGHT]]
    spawn_ball('right')
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    if not (BALL_RADIUS <= ball_pos[1] <= HEIGHT - 1 - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    if (paddle1_pos[1][1] - BALL_RADIUS <= ball_pos[1] <= paddle1_pos[2][1] + BALL_RADIUS) and\
    ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        ball_vel[0] = -(ball_vel[0] * 1.1)
    elif (paddle2_pos[1][1] - BALL_RADIUS <= ball_pos[1] <= paddle2_pos[2][1] + BALL_RADIUS) and\
    ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        ball_vel[0] = -(ball_vel[0] * 1.1)
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        score2 += 1
        spawn_ball('right')
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - 1 - PAD_WIDTH:
        score1 += 1
        spawn_ball('left')
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    # update paddle's vertical position, keep paddle on the screen
    
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'White', 'White')
    canvas.draw_polygon(paddle2_pos, 1, 'White', 'White')     
    # determine whether paddle and ball collide    
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2 - WIDTH/6, HEIGHT/4], 40, 'White')
    canvas.draw_text(str(score2), [WIDTH/2 + WIDTH/6, HEIGHT/4], 40, 'White')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    pos_change = 0
    paddel = None
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['down']:
        
        if key == simplegui.KEY_MAP['s']:
            pos_change = paddle1_vel
            paddle = paddle1_pos
        else:    
            pos_change = paddle2_vel
            paddle = paddle2_pos
            
        if paddle[3][1] + pos_change > HEIGHT -1:
            pos_change = HEIGHT - 1 - paddle[3][1] 
        for indx in range(len(paddle1_pos)):
            paddle[indx][1] += pos_change    
            
    elif key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['up']:
        
        if key == simplegui.KEY_MAP['w']:
            pos_change = -paddle1_vel
            paddle = paddle1_pos
        else:    
            pos_change = -paddle2_vel
            paddle = paddle2_pos
            
        if paddle[0][1] + pos_change < 0:
            pos_change = -paddle[0][1] 
        for indx in range(len(paddle1_pos)):
            paddle[indx][1] += pos_change
    
def keyup(key):
    global paddle1_vel, paddle2_vel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)


# start frame
new_game()
frame.start()
