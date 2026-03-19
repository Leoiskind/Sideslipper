from ursina import Entity
from ursina.shaders import lit_with_shadows_shader

class Character(Entity):
	def __init__(self, model, scale, position, color, origin):
		super().__init__()
		self.model = model
		self.scale = scale
		self.position = position
		self.color = color
		self.origin = origin
		self.collider = 'box'
		self.shadow = True
		self.shader=lit_with_shadows_shader