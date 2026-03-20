from ursina import Entity, Vec3, color, time, destroy, random, Mesh, copy, floor, curve
from ursina.shaders import lit_with_shadows_shader
from config import BEAN_HEIGHT, CORRIDOR_HEIGHT, TURN_TIME, CURVE_JUMP_UP, CURVE_JUMP_DOWN, GRAPHICS_SCALE
import flags
from ursina.prefabs.sprite_sheet_animation import SpriteSheetAnimation
from obstacles import Obstacle
from camera import start_camera_shake
from particles import Particles

class Character(Entity):
	def __init__(self, model, scale, position, bean_color, origin, texture='running_guy', on_shop_callback=None):
		super().__init__()
		self.model = model
		self.scale = scale
		self.position = position
		self.color = bean_color
		self.origin = origin
		self.collider = 'box'
		self.shadow = True
		self.shader = lit_with_shadows_shader
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
		self.on_shop_callback = on_shop_callback
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
		player_graphics = SpriteSheetAnimation(
			'running_guy',
			tileset_size=(2,2),
			fps=6,
			animations={
				'run': ((0, 1), (1, 1))
			},
			unlit=True,
			double_sided=True,
			rotation=(0, 180, 0),
			scale=(GRAPHICS_SCALE, GRAPHICS_SCALE),
			parent=self,
			y=-2.2
		)
		self.particles = Particles(
			Vec3(0, -1.5, 0),
			self.scale[1],
			particle_size=0.1,
			debug_position=True,
			parent=self
			)

		player_graphics.play_animation('run')
		ALIVE = True
		player_graphics.play_animation('run')
		self.on_death_callback = None

	def jump(self, height=BEAN_HEIGHT*2, duration=TURN_TIME):
		flags.JUMPING = True
		self.animate_y(
			self.y + height,
			duration=duration/2,
			curve=CURVE_JUMP_UP
		)
		self.animate_y(
			0,
			duration=duration/2,
			delay=duration/2,
			curve=CURVE_JUMP_DOWN
		)

	def update(self):
		hit = self.intersects()
		# self.particles.set_position(self.position)
		# print(self.particles.position)
		if hit.hit and hit.entity:
			if isinstance(hit.entity, Obstacle):
				if getattr(hit.entity, 'is_obstacle', True):
					print("Bean killed by", hit.entity)
					self.particles.play(.3, curve.linear)
					start_camera_shake(strength=0.2, duration=0.3)
					self.on_death_callback()
					self.enabled = False
					for shadow in self.shadows:
						shadow.enabled = False
				else:
					print("Enter store")
					destroy(hit.entity)
					self.on_shop_callback()
					flags.SCROLL_SPEED = 0
					flags.STORE = True
					self.enabled = False