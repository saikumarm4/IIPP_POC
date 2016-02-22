# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
ANGULAR_VEL = 0.01
ACCELERATION = [2, 2]
FRICTION = 0.95
MISSILE_MULTIPLE = 2
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0.00
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.missiles = []
        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        
    def set_thrust(self, acceleration):
        if acceleration.count(0) != 2:
            ship_thrust_sound.play()
            self.thrust = True
            self.vel = list(acceleration)
            self.image_center[0] += ship_info.get_size()[0]
        else:
            ship_thrust_sound.rewind()
            self.thrust = False
            self.image_center[0] -= ship_info.get_size()[0]  
            
    def set_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
    
    def shoot(self, dummy = None):
        #print "Shoot"
        if self.missiles != []:
            self.missiles.pop(0)
        forward_vector = angle_to_vector(self.angle)
        intial_missile_pos = [self.pos[0] + self.image_size[0] / 2 * forward_vector[0], 
                              self.pos[1] + self.image_size[0] / 2 * forward_vector[1]]
        missile_vel = [(self.vel[0] + MISSILE_MULTIPLE * abs(forward_vector[0])) * forward_vector[0], 
                       (self.vel[1] + MISSILE_MULTIPLE * abs(forward_vector[1]))* forward_vector[1]]
        self.missiles.append(Sprite(intial_missile_pos, missile_vel, 0, 0, 
                                        missile_image, missile_info, missile_sound))
            
    def draw_missiles(self, canvas):
        for missile in self.missiles:
            missile.draw(canvas)
    
    def update_missiles(self):
        for missile in self.missiles:
            missile.update()
            
    def update(self):
        # Transitional Motion
        forward_vector = angle_to_vector(self.angle)
        self.pos[0] = (self.pos[0] + self.vel[0] * forward_vector[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1] * forward_vector[1]) % HEIGHT
        
        if not self.thrust:
            self.vel[0] *= FRICTION
            self.vel[1] *= FRICTION
        
        # Angular Motion
        self.angle += self.angle_vel
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.angle += self.angle_vel

def keydown_handler(key):
    for input_key in INPUTS.keys():
        if key == simplegui.KEY_MAP[input_key]:
            INPUTS[input_key][0](INPUTS[input_key][1])

def keyup_handler(key):
    for input_key in INPUTS.keys():
        if key == simplegui.KEY_MAP[input_key] and key != simplegui.KEY_MAP['space']:
            INPUTS[input_key][0](INPUTS[input_key][2])

def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Lives and scores
    canvas.draw_text("Lives " + str(lives), [70, 50], 30, 'White')
    canvas.draw_text("Score " + str(score), [WIDTH - 150, 50], 30, 'White')
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    my_ship.draw_missiles(canvas)
    #a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    my_ship.update_missiles()
    #a_missile.update()
    
    # drawing missiles in any
    
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    random_num = random.randrange(len(ROCK_INITIALS))
    initial_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    a_rock = Sprite(initial_pos, [1, 1], 0, ROCK_INITIALS[random_num] * ANGULAR_VEL, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, ANGULAR_VEL, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# Declaring Global Variables
# Defined Global Variables
INPUTS = { 	'left' : [my_ship.set_angle_vel, -ANGULAR_VEL, 0],
            'right' : [my_ship.set_angle_vel, ANGULAR_VEL, 0],
            'up': [my_ship.set_thrust, ACCELERATION, [0, 0]],
            'space' : [my_ship.shoot, None, None]
         }
ROCK_INITIALS = { 	0 : 1,
                    1 : -1
                }
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
