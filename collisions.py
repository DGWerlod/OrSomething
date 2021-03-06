from math import hypot

def pointRect(point,rect): # not tested
	if point[0] < rect.x + rect.w:
		if point[0] > rect.x:
			if point[1] < rect.y + rect.h:
				if point[1] > rect.y:
					return True
	return False

def rectangles(a,b):
	if a.x < b.x + b.w:
		if a.x + a.w > b.x:
			if a.y < b.y + b.h:
				if a.h + a.y > b.y:
					dx = abs((a.x+a.w/2)-(b.x+b.w/2)) / b.w
					dy = abs((a.y+a.h/2)-(b.y+b.h/2)) / b.h
					if dy < dx: return 1
					else: return 2
	return 0

def pointCircle(point,circ): # not tested
	dx = abs(circ.x-point[0])
	dy = abs(circ.y-point[1])
	dt = hypot(dx,dy)
	if dt < circ.r:
		return True
	return False

def circles(a,b):
	# if distance between their centers is less than the sum of their radii
	dx = abs(a.x - b.x)
	dy = abs(a.y - b.y)
	dt = hypot(dx,dy)
	if dt < a.r + b.r:
		return True
	return False

def circleRect(circ,rect):
	# get x and y distance from their centers
	dx = abs(circ.x - rect.x - rect.w / 2)
	dy = abs(circ.y - rect.y - rect.h / 2)
	dxMin = abs(rect.w / 2) + circ.r
	dyMin = abs(rect.h / 2) + circ.r

	# test collision, return false if not colliding
	if dx > dxMin: return False
	elif dy > dyMin: return False
	# elif dx <= rect.w / 2: return True
	# elif dy <= rect.h / 2: return True
	
	# find bounce direction, return associated number
	if dy / rect.h < dx / rect.w: # ratios dissociate from unequal sides of rectangles
		if dx + abs(circ.spd[0]) <= dxMin: # if this function would return true next tick
			return 3 # flip both directions
		else:
			return 1 # flip x direction
	else: # dx / rect.w < dy / rect.h:
		if dy + abs(circ.spd[1]) <= dyMin:
			return 3 # flip both directions
		else:
			return 2 # flip y direction