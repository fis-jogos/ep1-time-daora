from FGAme import *
import math

f = draw.Poly(((0,0), (0, 600), (800, 600), (800, 0)))

class Light:
	def __init__(self, pos, size=5):
		self.obj = world.add.circle(size, pos=pos, color=(255, 255, 0), vel=(100, 0))
		self.seg = []
		self.light_area = []
		self.points = []
		self.color = False
		world.add(self.obj)

	def draw_lines(self):
		while len(self.seg) > 0:
			remove(self.seg[-1])
			self.seg.pop()

		if len(self.light_area) > 0 and self.color:
			remove(self.light_area)
			self.light_area = []

		lines = []
		vertices = []
		points = []
		rays = []		
		for obj in world:
			if hasattr(obj, 'vertices'):
				for index, vertice in enumerate(obj.vertices):
					index = (index+1)%len(obj.vertices)
					lines.append((vertice, obj.vertices[index]))
					vertices.append(vertice)
		print(obj)

		for vertice in vertices:
			dist = vertice - self.obj.pos
			rays.append(dist)

		lines.append((Vec(0, 600), Vec(800, 600)))
		lines.append((Vec(0, 0), Vec(800, 0)))
		for ray in rays:
			dist = ray

			for line in lines:
				x, y = line_intersection(line, (dist+self.obj.pos, self.obj.pos))
				if x != None and y != None:
					curr_distance = Vec(x, y) - self.obj.pos
					if curr_distance.norm() < dist.norm():
						dist = curr_distance
			point = self.obj.pos+dist

			for vertice in vertices:
				if math.fabs(point.x-vertice.x) < 1e-6 and math.fabs(point.y-vertice.y) < 1e-6:
					rays.append(ray.rotate((math.pi/180)*0.0001)*100)
					rays.append(ray.rotate((math.pi/180)*-0.0001)*100)

			seg = draw.Segment(self.obj.pos+dist, self.obj.pos)
			self.seg.append(seg)
			world.add(seg)
			points.append(point)

		points.sort(key=lambda p: math.atan2(p.y-self.obj.pos.y,p.x-self.obj.pos.x))

		if self.color:
			self.light_area = draw.Poly(points, color=(200, 200, 0))
			world.add(self.light_area)


	def switch(self):
		self.color = not self.color
		if self.color == True:
			world.add(f)
		else:
			remove(f)
			remove(self.light_area)
			self.light_area = []

	def update(self):
		self.draw_lines()

def remove(obj):
	rt = world._render_tree._data[0][1]
	world_objects = world._objects

	rt.remove(obj)
	world_objects.remove(obj)

def line_intersection(line1, line2):
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	div = det(xdiff, ydiff)
	if div == 0:
		return None, None

	q, c = line1
	s = c - q
	p, c = line2
	r = c - p

	t = q-p
	t = t.cross(s)
	t /= r.cross(s)

	u = q-p
	u = u.cross(r)
	u /= r.cross(s)

	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div

	if r.cross(s) != 0 and t >= 0  and t <= 1 and u >= 0 and u <= 1:
		return x, y
	else:
		return None, None