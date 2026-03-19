from ursina import Entity, color, time, destroy
from config import SCROLL_SPEED, LENGTH, SCROLL_FACTOR

class Obstacle(Entity):
	def __init__(self, position, scale, **kwargs):
		super().__init__(
			position=position,
			scale=scale,
			model='quad',
			texture='triangle',
			double_sided=True,
			color=color.red,
			**kwargs
		)
	
	def update(self):
		self.z += LENGTH * SCROLL_SPEED * time.dt / SCROLL_FACTOR
		if self.z > 5:
			self.z = -LENGTH
			# destroy(self)