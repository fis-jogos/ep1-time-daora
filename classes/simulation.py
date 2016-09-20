'''TODO:
        Make a class simulation that includes all these functions
        Put a limit for how much the player can climb up or down
        Make a module for handling inputs?
        Make a module for constants?
        Remove all those globals. pls
'''

from FGAme import *
from rope import Rope
from math import fabs

CONSTANT_K = 5000
MAX_DIST = 200

ROPE = None
PLAYER = None
PLATFORM = None

def margin(dx):
    W, H = conf.get_resolution()

    world.add.aabb(shape=(10, H), pos=(dx/2, pos.middle.y))
    world.add.aabb(shape=(10, H), pos=(W - dx/2, pos.middle.y))


def start():
    global ROPE
    global PLAYER
    global PLATFORM

    # margin(10)
    world.add.margin(10)

    PLAYER = world.add.circle(10, pos=pos.middle)

    PLATFORM = world.add.circle(30, pos=pos.middle+(0, 200), mass=100000000)

    PLAYER.gravity = 500
    PLAYER.damping = 1
    
    run()

@listen('frame-enter')
def update():
    global ROPE
    # move_screen(0.5)

    if ROPE != None:
        ROPE.update(starting_position=PLATFORM.pos, ending_position=PLAYER.pos)

        dist = PLATFORM.pos - PLAYER.pos
        direction = dist - dist.normalize()*MAX_DIST
        direction *= CONSTANT_K

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
        # if fabs(PLATFORM.pos.x-PLAYER.pos.x) < 30: #Hook only if platform is directly above
        ROPE = Rope(starting_position=PLATFORM.pos, \
                    ending_position=PLAYER.pos)
    else:
        PLAYER.force = lambda t: PLAYER.gravity
        ROPE.remove()
        ROPE = None

@listen('long-press', 'up', k=5)
@listen('long-press', 'down', k=-5)
def climb_rope(k):
    global MAX_DIST

    if ROPE != None:
        direction = PLATFORM.pos - PLAYER.pos
        direction = direction.normalize()
        direction *= k

        MAX_DIST -= direction.norm()*(k/fabs(k))
        PLAYER.move(direction)

def move_screen(dy):
    data = world._render_tree._data[0][1]
    for obj in data[2:]: # The first 2 objects are the left and right margins. This is horrible...
        obj.move(0, -dy)