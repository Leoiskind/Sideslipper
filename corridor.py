from ursina import Entity, color, Vec3
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

def create_sides(n_segments):
	sides_A = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 0), color=color.gray) for i in range(n_segments)]
	sides_B = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 90), color=color.red) for i in range(n_segments)]
	sides_C = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, -90), color=color.yellow) for i in range(n_segments)]
	sides_D = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 180), color=color.orange) for i in range(n_segments)]

	return sides_A + sides_B + sides_C + sides_D

def hide_sides(sides):
	for side in sides:
		side.enabled = False

def show_sides(sides):
	for side in sides:
		side.enabled = True