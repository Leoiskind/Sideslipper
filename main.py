from turtle import speed

from ursina import *
from ursina.shaders import lit_with_shadows_shader

"""
URSINA: 4-sided corridor base
- Bean character (third-person view, stationary at origin)
- Four walls per modular segment: floor, ceiling, left, right
- Walls (segments) move towards the bean to simulate running; the bean does not translate
- Static camera behind the bean looking toward corridor center

Controls:
- A / D : attach bean to left / right wall (visual only)
- W / S : attach bean to ceiling / floor (visual only)
- Esc  : quit

Adjustable parameters at the top of the file: SEG_COUNT, SEG_LENGTH, SPEED, WIDTH, HEIGHT
"""

# -----------------
# Config
# -----------------
SEG_COUNT	= 1
SEG_LENGTH	= 100
SPEED		= 0.0    # how fast segments move toward the bean
SCROLL_SPEED= 1.0
TURN_TIME	= 0.5     # how long it takes to rotate segments when switching attachment
WIDTH		= 4.0    # corridor width (x)
HEIGHT		= 1.0    # corridor height (y)
CURVE		= curve.in_expo  # easing curve for segment rotation
ROTATING	= False  # whether segments are currently rotating (to prevent input during rotation)
BEAN_HEIGHT	= 0.5	# Size of the character
ORIGIN		= Vec3(0, 1.5/BEAN_HEIGHT - 0.5, 0)  # origin point for bean
CURVE_JUMP	= curve.out_expo  # easing curve for bean "jump" when switching attachment

app = Ursina()
Entity.default_shader = lit_with_shadows_shader

window.title = '4-sided corridor - Ursina base'
window.borderless = False
window.vsync = False

# simple ambient light + directional
LIGHT = DirectionalLight(x = 0, y=.1, z=-10, shadows=True)
LIGHT.update_bounds(scene)
AmbientLight(color=color.rgba(40,40,40,100))

LIGHT_BALL = Entity(parent=LIGHT, model='sphere', scale=0.2, color=color.yellow)

# arrow_shaft = Entity(parent=LIGHT, model='cylinder', scale=(0.1, .1, 0.1), color=color.yellow)
# arrow_head = Entity(parent=LIGHT, model='cone', scale=(0.3, 0.3, 0.3), color=color.yellow)

# -----------------
# Corridor segment
# -----------------
SIDES_Z_0 = -SEG_LENGTH/2
ORIGIN_SIDES = Vec3(0, 2, 0)

class CorridorSegment(Entity):
	def __init__(self, z_pos, rotation, color=color.gray):
		super().__init__()
		self.z = SIDES_Z_0 + z_pos
		self.model = 'cube'
		self.texture = 'brick'
		self.color = color
		self.shader = lit_with_shadows_shader
		self.scale = (WIDTH, HEIGHT, SEG_LENGTH)
		self.origin = ORIGIN_SIDES
		self.rotation = rotation
		self.shadow = True

sides_A = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, 0)) for i in range(SEG_COUNT)]
sides_B = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, 90), color=color.red) for i in range(SEG_COUNT)]
sides_C = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, -90), color=color.yellow) for i in range(SEG_COUNT)]
sides_D = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, 180), color=color.orange) for i in range(SEG_COUNT)]

sides = sides_A + sides_B + sides_C + sides_D


# -----------------
# Player (bean)
# -----------------
bean = Entity(
	model='sphere',
	scale=(0.7*BEAN_HEIGHT, BEAN_HEIGHT, 0.9*BEAN_HEIGHT),
	position=Vec3(0, 0, -10),
	color=color.orange, origin=ORIGIN,
	shader=lit_with_shadows_shader,
	shadow=True
	)

# -----------------
# Rotation things
# -----------------

vertical_root = Entity()
rotation_pivot = Entity(parent=vertical_root)

bean.parent = rotation_pivot
camera.parent = rotation_pivot

# Static camera behind the bean and looking toward origin (center of corridor)
camera.origin = ORIGIN
camera.position = Vec3(0, 0, 0)
camera.look_at(Vec3(0, 0, -1))

def get_last_z(sides_list):
	"""Helper to find the farthest-back z (most negative) among all sides."""
	return min(side.z for side in sides_list)

def finished_rotation():
	"""Callback for when segment rotation animation finishes."""
	global ROTATING
	ROTATING = False

# -----------------
# Input & update
# -----------------

def input(key):
	"""Keyboard controls for switching attachment (visual only)."""
	print(key)
	global ROTATING
	if rotation_pivot.rotation_z % 90 == 0:
		ROTATING = False
	if (key == 'a' or key == 'a hold') and not ROTATING:
		ROTATING = True
		rotation_pivot.animate_rotation_z(rotation_pivot.rotation_z - 90, duration=TURN_TIME, curve=CURVE)
		bean.animate_position(
			bean.position + Vec3(0, BEAN_HEIGHT*2, 0),
			duration=TURN_TIME/2,
			curve=CURVE
		)

		bean.animate_position(
			bean.position,
			duration=TURN_TIME/2,
			delay=TURN_TIME/2,
			curve=CURVE
		)
	if (key == 'd' or key == 'd hold') and not ROTATING:
		ROTATING = True
		rotation_pivot.animate_rotation_z(rotation_pivot.rotation_z + 90, duration=TURN_TIME, curve=CURVE)
		# camera.animate_rotation(camera.rotation + Vec3(0, 0, -90), duration=TURN_TIME, curve=CURVE)
		# bean.animate_rotation(bean.rotation + Vec3(0, 0, 90), duration=TURN_TIME, curve=CURVE)
		
	if key == 'w' or key == 'up arrow':
		pass
		# apply_surface(2)  # ceiling
	if key == 's' or key == 'down arrow':
		pass
		# apply_surface(0)  # floor
	if key == 'escape':
		application.quit()
	
	speed = 300 * time.dt
	if held_keys['i']: camera.z -= speed
	if held_keys['k']: camera.z += speed
	if held_keys['j']: camera.x += speed
	if held_keys['l']: camera.x -= speed
	if held_keys['u']: camera.rotation_y += speed
	if held_keys['o']: camera.rotation_y -= speed
	if held_keys['shift']: camera.y -= speed
	if held_keys['space']: camera.y += speed

TEXT = Text('', origin=(0, -0.45), scale=1.5)

def update():
	"""Move segments forward to simulate the player running. Recycle segments when they pass the bean."""
	global SPEED, SEG_LENGTH, SIDES_Z_0, LIGHT

	LIGHT.look_at(bean)
	# TEXT.text = str(LIGHT.position)

	for element in [sides_A, sides_B, sides_C, sides_D]:
		for side in element:
			side.texture_offset = (0, (time.time() * -SCROLL_SPEED) % 1)  # scroll texture to simulate movement
			side.z += SPEED * time.dt
			if side.z > SIDES_Z_0 + SEG_LENGTH:
				side.z = get_last_z(element) - SEG_LENGTH


# -----------------
# Start
# -----------------

if __name__ == '__main__':
	print('\nControls: A/D or left/right arrows = left/right wall. W/S or up/down arrows = ceiling/floor.')
	print('The bean does not translate; corridor segments move to simulate running.\n')
	app.run()
