from ursina import Entity, color, time, destroy
from config import SCROLL_SPEED, LENGTH, CORRIDOR_HEIGHT

class Obstacle(Entity):
	global SCROLL_SPEED, LENGTH, CORRIDOR_HEIGHT
	def __init__(self, position, scale, is_obstacle=True, **kwargs):
		super().__init__(
			position=position,
			scale=scale,
			model='quad',
			double_sided=True,
			color=color.red,
			collider='box',
			speed=SCROLL_SPEED * LENGTH,
			is_obstacle=is_obstacle,
			**kwargs
		)
	
	def update(self):
		self.z += self.speed * time.dt
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