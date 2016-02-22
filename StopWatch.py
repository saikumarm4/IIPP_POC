# template for "Stopwatch: The Game"
import simplegui

# define global variables
tenth_seconds = 0
timer = None
is_timer_stopped = False
stopped = 0
stopped_success = 0
is_started = False
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global tenth_seconds
    temp_tenth_seconds = tenth_seconds
    tenth_seconds_val = temp_tenth_seconds % 10
    temp_tenth_seconds /= 10
    seconds = temp_tenth_seconds % 60
    minutes = temp_tenth_seconds / 60
    return "%d:%02d.%d" % (minutes, seconds, tenth_seconds_val)
    
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def stop():
    global timer, tenth_seconds, stopped, stopped_success, is_timer_stopped, is_started
    if is_started:
        is_started = False
        if not is_timer_stopped:
            timer.stop()
            stopped += 1
            is_timer_stopped = True
        if tenth_seconds % 10 == 0:
            stopped_success += 1

def start():
    global timer, is_timer_stopped, is_started
    is_started = True
    timer.start()
    is_timer_stopped = False

def reset():
    global tenth_seconds, timer, stopped, stopped_success, is_timer_stopped
    timer.stop()
    tenth_seconds = 0
    stopped , stopped_success, is_timer_stopped = 0, 0, False
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenth_seconds
    tenth_seconds += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tenth_seconds), [80, 100], 20,"White")
    canvas.draw_text(str(stopped_success) + "/" + str(stopped), [160,40], 20, "White")
# create frame
frame = simplegui.create_frame("Stop Watch", 200, 200)


# register event handlers
frame.set_draw_handler(draw_handler)
frame.add_button("Start", start, 80)
frame.add_button("Stop", stop, 80)
frame.add_button("Reset", reset, 80)
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()
#timer.start()

# Please remember to review the grading rubric
