from ursina import *
from ursina.shaders import lit_with_shadows_shader
from corridor import *
from config import *
from inventory import *
from coin import *
from bean import *
from obstacles import *

"""

"""

app = Ursina()
Entity.default_shader = lit_with_shadows_shader

window.title = '4-sided corridor - Ursina base'
window.borderless = False
window.vsync = False

# simple ambient light + directional
# LIGHT = DirectionalLight(x = 0, y=0.0, z=-10, shadows=True)
# LIGHT.look_at(Vec3(0, -1, -11))
# shadow_box = Entity(model='wireframe_cube', scale=20, visible=True)
# LIGHT.update_bounds(shadow_box)  # update light's shadow bounds to encompass the whole scene
# LIGHT.update_bounds(scene)
AmbientLight(color=color.rgba(1,1,1,100))

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
	model='sphere',
	scale=(0.7*BEAN_HEIGHT, BEAN_HEIGHT, 0.9*BEAN_HEIGHT),
	position=Vec3(0, 0, -10),
	bean_color=color.orange, origin=ORIGIN
	)

# -----------------
# Obstacles
# -----------------
Test_Obstacle = Obstacle(position=(0, -1, -30), scale=(1,1,0.5), parent=rotation_pivot)

# -----------------
# Rotation hierarchy
# -----------------
for shadow in bean.shadows:
	shadow.parent = rotation_pivot

for side in sides:
	side.parent = rotation_pivot

# Static camera behind the bean and looking toward origin (center of corridor)
camera.origin = ORIGIN
camera.position = Vec3(.7, 0, 0)
camera.rotation = Vec3(7, 190, 0)
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
	global ROTATING, JUMPING
	if rotation_pivot.rotation_z % 90 == 0 and bean.y == 0:
		ROTATING = False
	if bean.y == 0:
		JUMPING = False
	if held_keys['d'] and not ROTATING and not JUMPING:
		ROTATING = True
		rotation_pivot.animate_rotation_z(rotation_pivot.rotation_z - 90, duration=TURN_TIME, curve=CURVE)
		bean.jump()
	if held_keys['a'] and not ROTATING and not JUMPING:
		ROTATING = True
		rotation_pivot.animate_rotation_z(rotation_pivot.rotation_z + 90, duration=TURN_TIME, curve=CURVE)
		bean.jump()
	if held_keys['space'] and not ROTATING and not JUMPING:
		JUMPING = True
		bean.jump()
		
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
	
	# Determine which side is currently "down"
	angle = rotation_pivot.rotation_z % 360
	# print(JUMPING, bean.y)

	if 300 <= angle or angle <= 60:
		bean.shadows[0].enabled = True
	else:
		bean.shadows[0].enabled = False
	if 30 <= angle and angle <= 150:
		bean.shadows[1].enabled = True
	else:		
		bean.shadows[1].enabled = False
	if 120 <= angle and angle <= 240:
		bean.shadows[3].enabled = True
	else:
		bean.shadows[3].enabled = False
	if 210 <= angle and angle <= 330:
		bean.shadows[2].enabled = True
	else:
		bean.shadows[2].enabled = False

	angle_A = abs((angle - 0) % 360)
	angle_B = abs((angle - 90) % 360)
	angle_C = abs((angle - 270) % 360)
	angle_D = abs((angle - 180) % 360)

	angles = [angle_A, angle_B, angle_C, angle_D]

	for i, shadow in enumerate(bean.shadows):
		L = CORRIDOR_HEIGHT/(2*math.cos(math.radians(angles[i]))) + 0.0001
		shadow.world_position = Vec3(bean.world_x, -L+.01, bean.world_z)


# -----------------
# Start
# -----------------

if __name__ == '__main__':
	print('\nControls: A/D or left/right arrows = left/right wall. W/S or up/down arrows = ceiling/floor.')
	print('The bean does not translate; corridor segments move to simulate running.\n')
	inventory=Inventory()
	inventory.hide_inventory()
	
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

