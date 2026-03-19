from ursina import Entity, Vec3, color, time, destroy
from ursina.shaders import lit_with_shadows_shader
from config import BEAN_HEIGHT, CORRIDOR_HEIGHT, TURN_TIME, CURVE_JUMP_UP, CURVE_JUMP_DOWN, JUMPING, GRAPHICS_SCALE
from ursina.prefabs.sprite_sheet_animation import SpriteSheetAnimation
from obstacles import Obstacle

class Character(Entity):
	def __init__(self, model, scale, position, bean_color, origin, texture='running_guy'):
		super().__init__()
		self.model = model
		self.scale = scale
		self.position = position
		self.color = bean_color
		self.origin = origin
		self.collider = 'box'
		self.shadow = True
		self.shader=lit_with_shadows_shader
		self.shadow_A = Entity(
			parent=self,
			model='quad',
			scale=(BEAN_HEIGHT, BEAN_HEIGHT),
			position=Vec3(0, -CORRIDOR_HEIGHT/2+0.0001, -10),
			rotation=Vec3(90, 0, 0),
			color=color.black,
			double_sided=True,
			texture='circle',
			unlit_entity=True,
		)
		self.shadow_B = Entity(
			parent=self,
			model='quad',
			scale=(BEAN_HEIGHT, BEAN_HEIGHT),
			position=Vec3(-CORRIDOR_HEIGHT/2+0.0001, 0, -10),
			rotation=Vec3(0, 90, 0),
			color=color.black,
			double_sided=True,
			texture='circle',
			unlit_entity=True,
			enabled=False
		)
		self.shadow_C = Entity(
			parent=self,
			model='quad',
			scale=(BEAN_HEIGHT, BEAN_HEIGHT),
			position=Vec3(CORRIDOR_HEIGHT/2-0.0001, 0, -10),
			rotation=Vec3(0, 90, 0),
			color=color.black,
			double_sided=True,
			texture='circle',
			unlit_entity=True,
			enabled=False
		)
		self.shadow_D = Entity(
			parent=self,
			model='quad',
			scale=(BEAN_HEIGHT, BEAN_HEIGHT),
			position=Vec3(0, CORRIDOR_HEIGHT/2-0.0001, -10),
			rotation=Vec3(90, 0, 0),
			color=color.black,
			double_sided=True,
			texture='circle',
			unlit_entity=True,
			enabled=False
		)
		self.shadows = [self.shadow_A, self.shadow_B, self.shadow_C, self.shadow_D]
		player_graphics = SpriteSheetAnimation('running_guy', tileset_size=(2,2), fps=6, animations={
		'run': ((0, 1), (1, 1))
		},
		unlit=True,
		double_sided=True,
		rotation=(0, 180, 0),
		scale=(GRAPHICS_SCALE, GRAPHICS_SCALE),
		parent=self,
		y=-2.2)

		player_graphics.play_animation('run')
		ALIVE = True

	def jump(self, height=BEAN_HEIGHT/2, duration=TURN_TIME):
		global JUMPING
		JUMPING = True
		self.animate_position(
			self.position + Vec3(0, BEAN_HEIGHT*2, 0),
			duration=TURN_TIME/2,
			curve=CURVE_JUMP_UP
		)
		self.animate_position(
			Vec3(0, 0, -10),
			duration=TURN_TIME/2,
			delay=TURN_TIME/2,
			curve=CURVE_JUMP_DOWN
		)

	def update(self):
		hit = self.intersects()
		if hit.hit and hit.entity and getattr(hit.entity, 'is_obstacle', False):
			print("dead 3")
			self.enabled = False
			for shadow in self.shadows:
				shadow.enabled = False

  