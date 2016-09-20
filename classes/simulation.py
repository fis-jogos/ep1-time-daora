from FGAme import *
from rope import Rope
from math import fabs

MOVING = False
CONSTANT_K = 10000
MAX_DIST = 200

ROPE = None
PLAYER = None
PLATFORM = None

def start():
    global ROPE
    global PLAYER
    global PLATFORM

    world.add.margin(10)
    PLAYER = world.add.circle(10, pos=pos.middle)

    PLATFORM = world.add.circle(30, pos=pos.middle+(0, 200))

    PLAYER.gravity = 1000
    PLAYER.damping = 1
    
    PLATFORM.vel = (100, 0)
    run()

@listen('frame-enter')
def update():
    global ROPE
    if ROPE != None:
        ROPE.update(starting_position=PLATFORM.pos, ending_position=PLAYER.pos)

        dist = PLATFORM.pos - PLAYER.pos
        direction = dist - dist.normalize()*MAX_DIST
        direction *= CONSTANT_K

        PLAYER.force = lambda t: direction
    else:
        #Do nothing
        pass

@listen('long-press', 'left', dx=-5)
@listen('long-press', 'right', dx=5)
def windleft(dx):
    PLAYER.move(dx, 0)
@listen('key-down', 'space')
def hook():
    global ROPE
    global PLAYER

    if ROPE == None:
        # if fabs(PLATFORM.pos.x-PLAYER.pos.x) < 30:
        ROPE = Rope(starting_position=PLATFORM.pos, \
                    ending_position=PLAYER.pos)
    else:
        PLAYER.force = lambda t: PLAYER.gravity
        ROPE.remove()
        ROPE = None