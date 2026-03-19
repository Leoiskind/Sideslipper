from turtle import speed

from ursina import *
from ursina.shaders import lit_with_shadows_shader
from corridor import *
from config import *
from inventory import *
from coin import *
from bean import *

"""

"""

app = Ursina()
Entity.default_shader = lit_with_shadows_shader

window.title = '4-sided corridor - Ursina base'
window.borderless = False
window.vsync = False

# simple ambient light + directional
LIGHT = DirectionalLight(x = 0, y=0.0, z=-10, shadows=True)
LIGHT.look_at(Vec3(0, -1, -11))
shadow_box = Entity(model='wireframe_cube', scale=20, visible=True)
LIGHT.update_bounds(shadow_box)  # update light's shadow bounds to encompass the whole scene
# LIGHT.update_bounds(scene)
# AmbientLight(color=color.rgba(40,40,40,100))

# LIGHT_BALL = Entity(parent=LIGHT, model='sphere', scale=0.2, color=color.yellow, unlit_entity=True)

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
bean = Character(
	model=None,
	scale=(0.7*BEAN_HEIGHT, BEAN_HEIGHT, 0.9*BEAN_HEIGHT),
	position=Vec3(0, 0, -10),
	color=color.orange, origin=ORIGIN
	)

bean_shadow_A = Entity(
	parent=rotation_pivot,
	model='quad',
	scale=(BEAN_HEIGHT, BEAN_HEIGHT),
	position=Vec3(0, -CORRIDOR_HEIGHT/2+0.0001, -10),
	rotation=Vec3(90, 0, 0),
	color=color.black,
	double_sided=True,
	texture='circle',
	unlit_entity=True,
)

bean_shadow_B = Entity(
	parent=rotation_pivot,
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

bean_shadow_C = Entity(
	parent=rotation_pivot,
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

bean_shadow_D = Entity(
	parent=rotation_pivot,
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

# bean_shadow_B.parent = rotation_pivot

# thing = Entity(model='quad', color=color.black, double_sided=True)

# bean.parent = rotation_pivot
# camera.parent = rotation_pivot

for side in sides:
	side.parent = rotation_pivot

# Static camera behind the bean and looking toward origin (center of corridor)
camera.origin = ORIGIN
camera.position = Vec3(0, 0, 0)
camera.look_at(Vec3(0, 0, -1))
camera.fov = FOV

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
		
	if key == 'w' or key == 'up arrow':
		pass
		# apply_surface(2)  # ceiling
	if key == 's' or key == 'down arrow':
		pass
		# apply_surface(0)  # floor
	if key == 'escape':
		application.quit()
	
	speed = 100 * time.dt
	if held_keys['i']: camera.position += camera.forward*speed
	if held_keys['k']: camera.position += camera.back*speed
	if held_keys['j']: camera.position += camera.left*speed
	if held_keys['l']: camera.position += camera.right*speed
	if held_keys['u']: camera.rotation_y -= speed
	if held_keys['o']: camera.rotation_y += speed
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
	
	cos_theta = math.cos(math.radians(rotation_pivot.rotation_z))
	if abs(cos_theta) > 0.01:   # avoid division by zero / extreme angles
		floor_y = - (CORRIDOR_HEIGHT/2) / cos_theta + 0.0001   # small bias to avoid z-fighting
		bean_shadow_A.world_position = Vec3(bean.world_x, floor_y, bean.world_z)
		bean_shadow_A.enabled = True
	else:
		# Floor is vertical – shadow cannot stay at same X,Z; disable or move onto wall
		bean_shadow_A.enabled = False


# -----------------
# Start
# -----------------

if __name__ == '__main__':
	print('\nControls: A/D or left/right arrows = left/right wall. W/S or up/down arrows = ceiling/floor.')
	print('The bean does not translate; corridor segments move to simulate running.\n')
	inventory=Inventory()
	inventory.hide_inventory()
	
	def add_item():
		inventory.append(random.choice(['nachos', 'fries', 'hash_brown', 'rice']))
	
	for i in range(7):
		inventory.append('nachos')
	add_item_button = Button(
		scale = (.1,.1),
		x=-.5,
		color=color.lime.tint(-.25),
		text='+',
		tooltip=Tooltip('Add random item'),
		on_click=add_item
	)
	hide_inventory_button = Button(
		scale = (.1,.1),
		x=.5,
		color=color.red.tint(-.25),
		text='-',
		tooltip=Tooltip('hide inventory'),
		on_click=inventory.hide_inventory
	)
	show__inventory_button = Button(
		scale = (.1,.1),
		x=.5,
		y=.15,
		color=color.green.tint(-.25),
		text='+',
		tooltip=Tooltip('show inventory'),
		on_click=inventory.show_inventory
	)
	player = bean
	player.coins = 0
    
    # 2. Create the physical UI Text element on the screen
	coin_counter_ui = Text(text='Coins: 0', position=(-0.85, 0.45), scale=2, color=color.gold)
	Coin(position=(0, -1.25, -30), player=player, coin_counter=coin_counter_ui, parent=rotation_pivot)
	Coin(position=(1.25, 0, -40), player=player, coin_counter=coin_counter_ui, parent=rotation_pivot)
	Coin(position=(0, 1.25, -50), player=player, coin_counter=coin_counter_ui, parent=rotation_pivot)
	app.run()

