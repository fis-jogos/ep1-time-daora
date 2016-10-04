from FGAme import *
import math

class Light:
	def __init__(self, pos, size=5):
		self.obj = draw.Circle(size, pos=pos, color=(255, 255, 0))
		world.add(self.obj)

	def draw_lines(self):
		lines = []
		vertices = []
		points = []

		for obj in world:
			if hasattr(obj, 'vertices'):
				for index, vertice in enumerate(obj.vertices):
					index = (index+1)%len(obj.vertices)
					lines.append((vertice, obj.vertices[index]))
					vertices.append(vertice)

		for vertice in vertices:
			dist = vertice - self.obj.pos
			for line in lines:
				x, y = line_intersection(line, (vertice, self.obj.pos))
				# print(x, y)
				if x != None and y != None:
					curr_distance = Vec(x, y) - self.obj.pos
					# print(curr_distance.norm(), dist.norm())
					if curr_distance.norm() < dist.norm():
						dist = curr_distance

			# print(self.obj.pos+dist, self.obj.pos)
			seg = draw.Segment(self.obj.pos+dist, self.obj.pos)
			world.add(seg)
			points.append(self.obj.pos+dist)

		# p = draw.Poly(points, color=(200, 200, 0))
		# world.add(p)

		# world.reverse()

		print(world._render_tree._data[0][1][-1])


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

	# t0 = (q-p)
	# t0 = t0.dot(r)
	# t0 /= r.dot(r)

	# t1 = t0 + s.dot(r)/r.dot(r)

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