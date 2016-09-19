from FGAme import *
from rope import Rope
import math

MOVING = True

world.add.margin(10)
player = world.add.circle(10, pos=pos.middle)
platform = world.add.circle(30, pos=pos.middle+(0, 200))

rope = Rope(starting_position=platform.pos, \
			ending_position=player.pos, \
			balance_center=pos.middle-(0,300))

player.gravity = 30
k = 10
player.damping = 1
dist_max = 200
if(MOVING):
	platform.vel = (100, -30)

@listen('frame-enter')
def elastic_force():
	global rope

	rope.remove()
	rope = Rope(starting_position=platform.pos, \
				ending_position=player.pos, \
				balance_center=Vec(platform.center.x, platform.center.y-dist_max))

	dist = platform.pos - player.pos
	direction = dist - dist.normalize()*dist_max
	
	direction *= k	
	player.apply_force(direction, 1)

@listen('long-press', 'left')
def wind():
	player.apply_force((-50, 0), 1)

@listen('long-press', 'right')
def wind2():
	player.apply_force((50, 0), 0.5)

run()