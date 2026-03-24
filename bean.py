from ursina import Entity, Vec3, color, time, destroy, random, Mesh, copy, floor, curve, Audio, scene, held_keys
from ursina.shaders import lit_with_shadows_shader
from config import BEAN_HEIGHT, CORRIDOR_HEIGHT, TURN_TIME, CURVE_JUMP_UP, CURVE_JUMP_DOWN, GRAPHICS_SCALE, ROLL_TIME, CURVE_ROLL_DOWN, CURVE_ROLL_UP, SHADOW_ALPHA
import flags
from ursina.prefabs.sprite_sheet_animation import SpriteSheetAnimation
from obstacles import Obstacle
from camera import start_camera_shake
from particles import Particles
from coin import Coin

class Character(Entity):
	def __init__(self, model, scale, position, bean_color, origin, texture='running_guy', on_shop_callback=None):
		super().__init__()
		self.death_sound = Audio('death.mp3', autoplay=False, volume=flags.FX_VOLUME)
		self.model = model
		self.scale = scale
		self.position = position
		self.color = bean_color
		self.origin = origin
		self.collider = 'box'
		self.collider_visible = Entity(
									parent=self,
									model='cube',
									scale=(1, 1),
									position=self.collider.center,
									color=color.rgba(255, 0, 0, 80),
									wireframe=True,
									unlit=True
								)
		self.shadow = True
		self.shader = lit_with_shadows_shader
		self.shadow_A = Entity(
			parent=self,
			model='quad',
			scale=(BEAN_HEIGHT, BEAN_HEIGHT),
			position=Vec3(0, -CORRIDOR_HEIGHT/2+0.0001, -10),
			rotation=Vec3(90, 0, 0),
			color=color.rgba(0, 0, 0, .1),
			transparent=True,
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
			color=color.rgba(0, 0, 0, SHADOW_ALPHA),
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
			color=color.rgba(0, 0, 0, SHADOW_ALPHA),
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
			color=color.rgba(0, 0, 0, SHADOW_ALPHA),
			double_sided=True,
			texture='circle',
			unlit_entity=True,
			enabled=False
		)
		self.shadows = [self.shadow_A, self.shadow_B, self.shadow_C, self.shadow_D]
		self.player_graphics = SpriteSheetAnimation(
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
			y=-2.6
		)
		self.particles = Particles(
			Vec3(0, 0, -10),
			self.scale[1],
			particle_size=0.1,
			particle_number=100,
			debug_position=False,
			parent=scene
			)
		self.magnet = Entity(
			parent=scene,
			model='cube',
			scale=(2.8, 2.8, 5),
			position = (0, 0, -15),
			unlit=True,
			collider='box',
			enabled=False,
			color=color.clear
		
		)

		self.player_graphics.play_animation('run')
		ALIVE = True
		self.player_graphics.play_animation('run')
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
	
	def roll(self, duration=ROLL_TIME):
		flags.ROLLING = True
		self.animate_y(
			-3/2*BEAN_HEIGHT,
			duration=duration/2,
			curve=CURVE_ROLL_DOWN
		)
		self.animate_y(
			0,
			duration=duration/2,
			delay=duration/2,
			curve=CURVE_ROLL_UP
		)
		self.animate_scale_y(
			self.scale_y/2,
			duration=duration/2,
			curve=CURVE_ROLL_DOWN
		)
		self.animate_scale_y(
			self.scale_y,
			duration=duration/2,
			curve=CURVE_ROLL_DOWN,
			delay=duration/2
		)

	def update(self):
		hit = self.intersects(ignore=(self, self.magnet))
		print(self.position + self.origin)
		self.particles.set_position(self.position - self.origin/2)
		# self.particles.set_position(self.position)
		# print(self.particles.position)
		if hit.hit and hit.entity:
			if isinstance(hit.entity, Obstacle):
				if getattr(hit.entity, 'is_obstacle', True):
					self.death_sound.play()
					start_camera_shake(strength=0.2, duration=0.3)
					self.on_death_callback()
					if flags.INVINCIBLE:
						destroy(hit.entity)
				else:
					destroy(hit.entity)
					self.on_shop_callback()
					flags.SCROLL_SPEED = 0
					flags.STORE = True
					self.enabled = False