from ursina import Entity, color, time, destroy, Vec3
from config import LENGTH, CORRIDOR_HEIGHT
import flags

class Obstacle(Entity):
	global LENGTH, CORRIDOR_HEIGHT
	def __init__(self, position, scale, is_obstacle=True, **kwargs):
		super().__init__(
			position=position,
			scale=scale,
			model='quad',
			double_sided=True,
			color=color.red,
			collider='box',
			is_obstacle=is_obstacle,
			**kwargs
		)
	
	def update(self):
		global LENGTH
		print(flags.SCROLL_SPEED)
		self.z += flags.SCROLL_SPEED * LENGTH * time.dt
		if self.z > 5:
			destroy(self)

class LowObstacle(Obstacle):
	def __init__(self, z, scale=(CORRIDOR_HEIGHT, 0.5, 0.5), **kwargs):
		super().__init__((0, 0.25-CORRIDOR_HEIGHT/2, z), scale, is_obstacle=True, **kwargs)
		self.color = color.orange


class HighObstacle(Obstacle):
	def __init__(self, z, scale=(CORRIDOR_HEIGHT, 0.5, 0.5), **kwargs):
		super().__init__((0, 0.5-CORRIDOR_HEIGHT/2, z), scale, is_obstacle=True, **kwargs)
		self.color = color.orange


class WallObstacle(Obstacle):
	def __init__(self, z, scale=(CORRIDOR_HEIGHT, 1, 0.5), **kwargs):
		super().__init__((0, 0.5-CORRIDOR_HEIGHT/2, z), scale, is_obstacle=True, **kwargs)
		self.color = color.orange

class MiddleObstacle(Obstacle):
	def __init__(self, z, scale=(CORRIDOR_HEIGHT/4, CORRIDOR_HEIGHT/4, 0.5), **kwargs):
		super().__init__((0, 0, z), scale, is_obstacle=True, **kwargs)
		self.color = color.orange

class StoreObstacle(Obstacle):
	def __init__(self, z, scale=(CORRIDOR_HEIGHT/4, CORRIDOR_HEIGHT/4), is_obstacle=False, **kwargs):
		super().__init__((0, CORRIDOR_HEIGHT/8 - CORRIDOR_HEIGHT/2, z), scale, is_obstacle, **kwargs)
		self.color = color.green