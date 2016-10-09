'''TODO:
        Make a class simulation that includes all these functions
        Make a module for handling inputs?
        Make a module for constants?
        Remove all those globals. pls
'''

from FGAme import *
from rope import Rope
from platforms import Platforms
from math import fabs
from light import Light

MIN_ROPE_LENGTH = 50
MAX_ROPE_LENGTH = 300

# Change these pls
ROPE = None
PLAYER = None
LIGHT = None
PLATFORM = Platforms()

def start():
    global PLAYER
    global PLATFORM
    global LIGHT


    margin(10)
    # world.add.margin(10)

    # PLAYER = world.add.circle(10, pos=pos.middle)

    LIGHT = Light(pos=pos.middle)
    s = world.add.rectangle(shape=(50, 50), pos=pos.middle-(100, 0))
    s = world.add.rectangle(shape=(50, 50), pos=pos.middle+(50, 50))
    # PLATFORM.add(pos=pos.middle+(0, 200))
    # PLATFORM.add(pos=pos.middle+(200, 500))

    # PLAYER.gravity = 500
    # PLAYER.damping = 1

    LIGHT.draw_lines()
    run()

@listen('frame-enter')
def update():
    # move_screen(0.5)
    LIGHT.draw_lines()
    if ROPE != None:
        ROPE.update()

        dist = ROPE.platform.pos - PLAYER.pos
        direction = dist - dist.normalize()*ROPE.length
        direction *= ROPE.k

        PLAYER.force = lambda t: direction
    else:
        #Do nothing
        pass

dx = 10

@listen('long-press', 'left', dx=-dx)
@listen('long-press', 'right', dx=dx)
def wind(dx):
    PLAYER.vel += (dx, 0)

@listen('key-down', 'space')
def hook():
    global ROPE
    global PLAYER

    if ROPE == None:
        for platform in PLATFORM.items:
            if fabs(platform.pos.x-PLAYER.pos.x) < 30 and platform.pos.y > PLAYER.pos.y: #Hook only if platform is directly above
                ROPE = Rope(platform=platform, \
                            player=PLAYER)
    else:
        ROPE.remove()
        ROPE = None

@listen('long-press', 'up', climbing_distance=5)
@listen('long-press', 'down', climbing_distance=-5)
def climb_rope(climbing_distance):
    if ROPE != None:
        direction = ROPE.platform.pos - PLAYER.pos
        direction = direction.normalize()

        direction *= climbing_distance
        norm = ROPE.length - direction.norm()*(climbing_distance/fabs(climbing_distance))
        if norm > MIN_ROPE_LENGTH and norm < MAX_ROPE_LENGTH:
            ROPE.length = norm
        else:
            direction = Vec(0, 0)
        if climbing_distance > 0:
            move_screen(climbing_distance)
        PLAYER.move(direction)
    else:
        #Do nothing
        pass

def move_screen(dy):
    data = world._render_tree._data[0][1]
    for obj in data[2:]: # The first 2 objects are the left and right margins. This is horrible...
        obj.move(0, -dy)
        
def margin(dx):
    W, H = conf.get_resolution()

    world.add.aabb(shape=(10, H), pos=(dx/2, pos.middle.y), mass='inf')
    world.add.aabb(shape=(10, H), pos=(W - dx/2, pos.middle.y), mass='inf')