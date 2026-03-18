from turtle import speed

from ursina import *
from ursina.shaders import lit_with_shadows_shader
from corridor import *
from config import *
from inventory import *

"""

"""

app = Ursina()
Entity.default_shader = lit_with_shadows_shader

window.title = '4-sided corridor - Ursina base'
window.borderless = False
window.vsync = False

# simple ambient light + directional
# LIGHT = DirectionalLight(x = 0, y=0.0, z=-10, shadows=True)
# LIGHT.update_bounds(scene)
# AmbientLight(color=color.rgba(40,40,40,100))

# LIGHT_BALL = Entity(parent=LIGHT, model='sphere', scale=0.2, color=color.yellow)

# -----------------
# Rotation things
# -----------------

vertical_root = Entity()
rotation_pivot = Entity(parent=vertical_root)

# -----------------
# Corridor segments
# -----------------

sides_A = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 0), color=color.gray) for i in range(SEG_COUNT)]
sides_B = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 90), color=color.red) for i in range(SEG_COUNT)]
sides_C = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, -90), color=color.yellow) for i in range(SEG_COUNT)]
sides_D = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 180), color=color.orange) for i in range(SEG_COUNT)]

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


# bean.parent = rotation_pivot
# camera.parent = rotation_pivot

for side in sides:
	side.parent = rotation_pivot

# Static camera behind the bean and looking toward origin (center of corridor)
camera.origin = ORIGIN
camera.position = Vec3(0, 0, 0)
camera.look_at(Vec3(0, 0, -1))

def get_last_z(sides_list):
	"""Helper to find the farthest-back z (most negative) among all sides."""
	return min(side.z for side in sides_list)

# -----------------
# Input & update
# -----------------

def input(key):
	"""Keyboard controls for switching attachment (visual only)."""
	print(key)
	global ROTATING
	if rotation_pivot.rotation_z % 90 == 0:
		ROTATING = False
	if held_keys['a'] and not ROTATING:
		ROTATING = True
		rotation_pivot.animate_rotation_z(rotation_pivot.rotation_z - 90, duration=TURN_TIME, curve=CURVE)
		bean.animate_position(
			bean.position + Vec3(0, BEAN_HEIGHT*2, 0),
			duration=TURN_TIME/2,
			curve=CURVE_JUMP_UP
		)

		bean.animate_position(
			bean.position,
			duration=TURN_TIME/2,
			delay=TURN_TIME/2,
			curve=CURVE_JUMP_DOWN
		)
	if held_keys['d'] and not ROTATING:
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
	
	speed = 100 * time.dt
	if held_keys['i']: camera.position += speed*camera.forward
	if held_keys['k']: camera.position -= speed*camera.forward
	if held_keys['j']: camera.x += speed*camera.left
	if held_keys['l']: camera.x -= speed*camera.left
	if held_keys['u']: camera.rotation_y += speed
	if held_keys['o']: camera.rotation_y -= speed
	if held_keys['n']: camera.y -= speed
	if held_keys['m']: camera.y += speed

TEXT = Text('', origin=(0, -0.45), scale=1.5)

def update():
	"""Move segments forward to simulate the player running. Recycle segments when they pass the bean."""
	global SPEED, LENGTH, SIDES_Z_0, LIGHT

	# LIGHT.look_at(bean)
	# TEXT.text = str(LIGHT.position)

	for element in [sides_A, sides_B, sides_C, sides_D]:
		for side in element:
			side.texture_offset = (0, (time.time() * -SCROLL_SPEED) % 1)  # scroll texture to simulate movement
			side.z += SPEED * time.dt
			if side.z > SIDES_Z_0 + LENGTH:
				side.z = get_last_z(element) - LENGTH


# -----------------
# Start
# -----------------

if __name__ == '__main__':
	print('\nControls: A/D or left/right arrows = left/right wall. W/S or up/down arrows = ceiling/floor.')
	print('The bean does not translate; corridor segments move to simulate running.\n')
	inventory=Inventory()
	
	def add_item():
		inventory.append(random.choice(['bag', 'car']))
	
	for i in range(7):
		inventory.append('test item')
	add_item_button = Button(
		scale = (.1,.1),
		x=-.5,
		color=color.lime.tint(-.25),
		text='+',
		tooltip=Tooltip('Add random item'),
		on_click=add_item
	)
	app.run()
