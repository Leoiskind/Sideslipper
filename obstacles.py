from ursina import Entity, color, time, destroy, Vec3, SpriteSheetAnimation
from config import LENGTH, CORRIDOR_HEIGHT
import flags

class Obstacle(Entity):
	global LENGTH, CORRIDOR_HEIGHT
	def __init__(self, scale, is_obstacle=True, **kwargs):
		super().__init__(
			scale=scale,
			model='cube',
			double_sided=True,
			color=color.red,
			collider='box',
			is_obstacle=is_obstacle,
			**kwargs
		)
	
	def update(self):
		hit = self.intersects()
		global LENGTH
		if not flags.GAME_OVER: self.z += flags.SCROLL_SPEED * LENGTH * time.dt
		if self.z > 5:
			destroy(self)

class LowObstacle(Obstacle):
	def __init__(self, wall, scale=(CORRIDOR_HEIGHT, 0.5, 0.5), **kwargs):
		super().__init__(scale, is_obstacle=True, **kwargs)
		distance = CORRIDOR_HEIGHT/2-.25
		match wall:
			case 0:
				self.rotation = (0, 0, 0)
				self.y = -distance
			case 1:
				self.rotation = (0, 0, 90)
				self.x = -distance
			case 2:
				self.rotation = (0, 0, 270)
				self.x = distance
			case 3:
				self.rotation = (0, 0, 180)
				self.y = distance
		self.color = color.orange


class HighObstacle(Obstacle):
	def __init__(self, wall, scale=(CORRIDOR_HEIGHT, 0.75, 0.5), **kwargs):
		super().__init__(scale, is_obstacle=True, **kwargs)
		distance = CORRIDOR_HEIGHT/2-.75
		match wall:
			case 0:
				self.rotation = (0, 0, 0)
				self.y = -distance
			case 1:
				self.rotation = (0, 0, 90)
				self.x = -distance
			case 2:
				self.rotation = (0, 0, 270)
				self.x = distance
			case 3:
				self.rotation = (0, 0, 180)
				self.y = distance
		self.color = color.red


class WallObstacle(Obstacle):
	def __init__(self, wall, scale=(CORRIDOR_HEIGHT, 1.1, 0.5), **kwargs):
		super().__init__(scale, is_obstacle=True, **kwargs)
		distance = CORRIDOR_HEIGHT/2-.55
		match wall:
			case 0:
				self.rotation = (0, 0, 0)
				self.y = -distance
			case 1:
				self.rotation = (0, 0, 90)
				self.x = -distance
			case 2:
				self.rotation = (0, 0, 270)
				self.x = distance
			case 3:
				self.rotation = (0, 0, 180)
				self.y = distance
		self.color = color.green

class MiddleObstacle(Obstacle):
	def __init__(self, wall, scale=(CORRIDOR_HEIGHT/4, CORRIDOR_HEIGHT/4, 0.5), **kwargs):
		super().__init__(scale, is_obstacle=True, **kwargs)
		self.color = color.orange

class StoreObstacle(Obstacle):
	def __init__(self, wall, scale=(CORRIDOR_HEIGHT/3, CORRIDOR_HEIGHT/3), is_obstacle=False, **kwargs):
		super().__init__(scale, is_obstacle, texture='store', **kwargs)

		distance = CORRIDOR_HEIGHT/2-.25
		match wall:
			case 0:
				self.rotation = (0, 0, 180)
				self.y = distance
			case 1:
				self.rotation = (0, 0, -90)
				self.x = distance
			case 2:
				self.rotation = (0, 0, 90)
				self.x = -distance
			case 3:
				self.rotation = (0, 0, 0)
				self.y = -distance
		self.color = color.white
		# self.animation_thing.play_animation('run')

N = 25
n = 10

obstacle_list = []

LowObstacleList = [LowObstacle]*N
obstacle_list += LowObstacleList
LowObstacleList = [HighObstacle]*N
obstacle_list += LowObstacleList
LowObstacleList = [WallObstacle]*N
obstacle_list += LowObstacleList
LowObstacleList = [MiddleObstacle]*N
obstacle_list += LowObstacleList
obstacle_list += [StoreObstacle]*n

