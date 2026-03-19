from ursina import Entity
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.sprite_sheet_animation import SpriteSheetAnimation

class Character(Entity):
	def __init__(self, model, scale, position, color, origin, texture='running_guy'):
		super().__init__()
		self.model = model
		self.scale = scale
		self.position = position
		self.color = color
		self.origin = origin
		self.collider = 'box'
		self.shadow = True
		self.shader=lit_with_shadows_shader

		player_graphics = SpriteSheetAnimation('running_guy', tileset_size=(2,2), fps=6, animations={
			'run': ((0, 1), (1, 1))
		},
		unlit=True,
		double_sided=True,
		rotation=(0, 180, 0),
		scale=(3, 3),
		parent=self,
		y=-2.2)

		player_graphics.play_animation('run')