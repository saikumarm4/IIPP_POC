import simplegui
import random
import math

FRAME_HEIGHT = 800
FRAME_WIDTH = 800

rocket_image = simplegui.load_image("http://goo.gl/Kn7QDE")

class Rocket:
    def __init__(self, radius, image, angle):
        self.radius = radius
        self.angle = angle
        self.image = image
        self.thrust = False
        self.pos = [50, FRAME_HEIGHT / 2 - 100]
        self.vel = 0
        self.friction = 0.9
    
    def update(self):
        if self.thrust:
            self.pos[0] = (self.pos[0] + self.vel * math.sin(self.angle)) % FRAME_WIDTH
            self.pos[1] = (self.pos[1] - self.vel * math.cos(self.angle)) % FRAME_HEIGHT
            self.vel *= self.friction
            if  self.vel - 0.001 <= 0:
                self.set_thrust(False)

    def set_thrust(self, thrust):
        self.thrust = thrust
    
    def set_angle(self, angle):
        self.angle += angle
        
    def set_vel(self, vel):
        self.vel = vel
        
    def draw(self, canvas):
        canvas.draw_image(self.image, [200, 189], [400, 378], self.pos, [100, 100], self.angle)
    
    
        
def keydown_handler(key):
    global rocket
    if simplegui.KEY_MAP['space'] == key:
        rocket.set_thrust(True)
        rocket.set_vel(10)
    elif simplegui.KEY_MAP['left'] == key:
        rocket.set_angle( -0.1)
    elif simplegui.KEY_MAP['right'] == key:
        rocket.set_angle( 0.1)
        
def draw_handler(canvas):
    rocket.update()
    rocket.draw(canvas)
    
rocket = Rocket(10, rocket_image, math.pi/4)

frame = simplegui.create_frame("Balls ", 600, 600)
frame.set_keydown_handler(keydown_handler)
frame.set_draw_handler(draw_handler)
frame.start() 