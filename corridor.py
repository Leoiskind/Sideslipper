from ursina import Entity, color
from ursina.shaders import lit_with_shadows_shader
from config import WIDTH, HEIGHT, LENGTH, CORRIDOR_HEIGHT, SIDES_Z_0, ORIGIN_SIDES

class CorridorSegment(Entity):
	def __init__(self, z_pos, rotation, color=color.gray, parent=None):
		super().__init__()
		self.z = SIDES_Z_0 + z_pos
		self.model = 'cube'
		self.texture = 'brick'
		self.color = color
		self.shader = lit_with_shadows_shader
		self.scale = (WIDTH, HEIGHT, LENGTH)
		self.origin = ORIGIN_SIDES
		self.rotation = rotation
		self.shadow = True