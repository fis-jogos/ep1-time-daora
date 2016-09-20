from FGAme import *
from rope import Rope

MOVING = False
CONSTANT_K = 10
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

    ROPE = Rope(starting_position=PLATFORM.pos, \
                ending_position=PLAYER.pos, \
                balance_center=pos.middle-(0, 300))

    PLAYER.gravity = 30
    PLAYER.damping = 1
    if MOVING:
        PLATFORM.vel = (100, -30)
    run()


@listen('frame-enter')
def elastic_force():
    global ROPE
    if ROPE != None:
        ROPE.remove()
        ROPE = Rope(starting_position=PLATFORM.pos, \
                    ending_position=PLAYER.pos, \
                    balance_center=Vec(PLATFORM.center.x, \
                                       PLATFORM.center.y-MAX_DIST))

        dist = PLATFORM.pos - PLAYER.pos
        direction = dist - dist.normalize()*MAX_DIST
        direction *= CONSTANT_K
        PLAYER.apply_force(direction, 1)
    else:
        #Do nothing
        pass

@listen('long-press', 'left', dy=50)
def windleft(dy):
    PLAYER.apply_force((-dy, 0), 1)
@listen('long-press', 'right', dy=50)
def windright(dy):
    PLAYER.apply_force((dy, 0), 0.5)
