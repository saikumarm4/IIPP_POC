import simplegui
import math
import random

# Global Constants
LIVES = 3
ANGULAR_VEL = 0.05
ACCELERATION = [5, 5]
FRICTION = 0.97
MISSILE_MULTIPLE = 5
MAXIMUM_ROCKS = 12

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
time = 0
lives = LIVES

# Global State Variables
started = True
rock_count = 0

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
        return list(self.center)

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
        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return list(self.pos)
    
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
        forward_vector = angle_to_vector(self.angle)
        intial_missile_pos = [self.pos[0] + self.image_size[0] / 2 * forward_vector[0], 
                              self.pos[1] + self.image_size[0] / 2 * forward_vector[1]]
        missile_vel = [(self.vel[0] + MISSILE_MULTIPLE * abs(forward_vector[0])) * forward_vector[0], 
                       (self.vel[1] + MISSILE_MULTIPLE * abs(forward_vector[1]))* forward_vector[1]]
        missile_group.add(Sprite(intial_missile_pos, missile_vel, 0, 0, 
                                        missile_image, missile_info, missile_sound))
        
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
   
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return list(self.pos)
    
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def update(self):
        if self.animated:
            self.image_center[0] = (self.image_center[0] + self.image_size[0])
        else:
            self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
            self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
            self.angle += self.angle_vel
        self.age += 1
        if self.lifespan != None and self.age > self.lifespan:
            return True
        return False
    
    def collide(self, other_sprite):
        distance = self.radius + other_sprite.get_radius()
        actual_distance = dist(other_sprite.get_position(), self.pos)
        if actual_distance <= distance:
            return True
        return False

# Helper Functions

def game_intializer():
    global lives, score, timer, rock_count, started
    global missile_group, rock_group
    
    lives = LIVES
    score = 0
    started = True
    timer.stop()
    rock_count = 0
    missile_group.difference_update(missile_group)
    rock_group.difference_update(rock_group)
    
def process_sprite_group(sprite_group, canvas):
    remove_sprite = set()
    for sprite in sprite_group:
        sprite.draw(canvas)
        if sprite.update():
            remove_sprite.add(sprite)
    sprite_group.difference_update(remove_sprite)

def group_collide(group, other_object):
    global explosion_group
    remove_sprite = set([])
    for sprite in list(group):
        if sprite.collide(other_object):
            explosion_group.add(Sprite(sprite.get_position(), [0, 0], 0, 0,
                                  explosion_image, explosion_info, None))
            remove_sprite.add(sprite)
    group.difference_update(remove_sprite)
    if len(remove_sprite):
        return True
    return False
        
def group_group_collide(first_group, second_group):
    collision_count = 0
    for sprite in list(first_group):
        if group_collide(second_group, sprite):
            first_group.discard(sprite)
            collision_count += 1
    return collision_count

# Event Handlers
def keydown_handler(key):
    for input_key in INPUTS.keys():
        if key == simplegui.KEY_MAP[input_key]:
            INPUTS[input_key][0](INPUTS[input_key][1])

def keyup_handler(key):
    for input_key in INPUTS.keys():
        if key == simplegui.KEY_MAP[input_key] and key != simplegui.KEY_MAP['space']:
            INPUTS[input_key][0](INPUTS[input_key][2])

def mouse_click(pos):
    global started, timer
    if 0.125 * WIDTH <= pos[0] <= 0.875 * WIDTH and 0.125 * HEIGHT <= pos[1] <= 0.875 * HEIGHT:
        started = False
        timer.start()
        
def draw(canvas):
    global time, lives, score, started
    global rock_count, score, lives, timer
    
       
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), 
                      [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # Lives and scores
    canvas.draw_text("Lives " + str(lives), [70, 50], 30, 'White')
    canvas.draw_text("Score " + str(score), [WIDTH - 150, 50], 30, 'White')
    
    # Draw Ships
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    if group_collide(rock_group, my_ship):
        lives -= 1
        
    no_of_collisions = group_group_collide(missile_group, rock_group)
    rock_count -= no_of_collisions
    score += no_of_collisions
    
    process_sprite_group(explosion_group, canvas)
    if lives < 1:
        game_intializer()
        
    if started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(),
                          [WIDTH/2, HEIGHT/2], [0.75 * WIDTH, 0.75 * HEIGHT])
                    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, rock_count, my_ship
    random_num = random.randrange(len(ROCK_VELOCITIES))
    initial_pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
    if dist(initial_pos, my_ship.get_position()) + 2 * my_ship.get_radius()<=\
    asteroid_info.get_radius() + my_ship.get_radius():
        rock_spawner()
    if rock_count < MAXIMUM_ROCKS:
        rock_group.add(Sprite(initial_pos, ROCK_VELOCITIES[random_num], 0, 
                              ROCK_INITIALS[random_num / 2] * ANGULAR_VEL, 
                              asteroid_image, asteroid_info))
        rock_count += 1
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# Defined Global Variables
INPUTS = { 	'left' : [my_ship.set_angle_vel, -ANGULAR_VEL, 0],
            'right' : [my_ship.set_angle_vel, ANGULAR_VEL, 0],
            'up': [my_ship.set_thrust, ACCELERATION, [0, 0]],
            'space' : [my_ship.shoot, None, None]
         }
ROCK_INITIALS = { 	0 : 1,
                    1 : -1
                }
ROCK_VEL_CONSTANT = 0.5
ROCK_VELOCITIES = 	{
                        0 : [ROCK_VEL_CONSTANT, ROCK_VEL_CONSTANT],
                        1 : [ROCK_VEL_CONSTANT, -ROCK_VEL_CONSTANT],
                        2 : [-ROCK_VEL_CONSTANT, ROCK_VEL_CONSTANT],
                        3 : [-ROCK_VEL_CONSTANT, -ROCK_VEL_CONSTANT]
                    }
# register handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_click)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
