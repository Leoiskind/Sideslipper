from ursina import *
from ursina.shaders import lit_with_shadows_shader
from inventory import *
from coin import *

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
SEG_COUNT	= 10
SEG_LENGTH	= 20
SPEED		= 10.0    # how fast segments move toward the bean
TURN_TIME	= 0.2     # how long it takes to rotate segments when switching attachment
WIDTH		= 4.0    # corridor width (x)
HEIGHT		= 1.0    # corridor height (y)
CURVE		= curve.linear  # easing curve for segment rotation
ROTATING	= False  # whether segments are currently rotating (to prevent input during rotation)

app = Ursina()
window.title = '4-sided corridor - Ursina base'
window.borderless = False

# simple ambient light + directional
LIGHT = DirectionalLight(y=2, z=3, shadows=True)
AmbientLight(color=color.rgba(40,40,40,100))

# -----------------
# Corridor segment
# -----------------
SIDES_Z_0 = -SEG_LENGTH/2
ORIGIN = Vec3(0, 2, 0)

class CorridorSegment(Entity):
	def __init__(self, z_pos, rotation, color=color.gray):
		super().__init__()
		self.z = SIDES_Z_0 + z_pos
		self.model = 'cube'
		self.texture = 'brick'
		self.color = color
		self.shader = lit_with_shadows_shader
		self.scale = (WIDTH, HEIGHT, SEG_LENGTH)
		self.origin = ORIGIN
		self.rotation = rotation

sides_A = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, 0)) for i in range(SEG_COUNT)]
sides_B = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, 90), color=color.red) for i in range(SEG_COUNT)]
sides_C = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, -90), color=color.yellow) for i in range(SEG_COUNT)]
sides_D = [CorridorSegment(z_pos = -i * SEG_LENGTH, rotation=Vec3(0, 0, 180), color=color.orange) for i in range(SEG_COUNT)]

sides = sides_A + sides_B + sides_C + sides_D

# -----------------
# Player (bean)
# -----------------
bean = Entity(model='sphere', scale=(0.7,1.0,0.9), color=color.orange, position=(0,-1,-10), shader=lit_with_shadows_shader)
# make bean look slightly stretched to be "bean-like"
bean.model = 'sphere'

# Static camera behind the bean and looking toward origin (center of corridor)
camera.position = Vec3(0, 0, 0)
camera.look_at(Vec3(0, 0, -1))

def get_last_z(sides_list):
	"""Helper to find the farthest-back z (most negative) among all sides."""
	return min(side.z for side in sides_list)

def rotate_sides(sides_list, direction):
	"""Rotate sides in the specified direction (clockwise or counterclockwise)."""
	if direction == 'clockwise':
		direction = Vec3(0, 0, -90)
	elif direction == 'counterclockwise':
		direction = Vec3(0, 0, 90)
	for side in sides_list:
		side.animate_rotation(side.rotation + direction, duration=0.2, curve=curve.linear)

# -----------------
# Input & update
# -----------------

def input(key):
	"""Keyboard controls for switching attachment (visual only)."""
	global ROTATING
	print(ROTATING)
	if key == 'a' or key == 'left arrow' and not ROTATING:
		ROTATING = True
		for side in sides:
			side.animate_rotation(side.rotation + Vec3(0, 0, 90), duration=TURN_TIME, curve=CURVE)
	if key == 'd' or key == 'right arrow' and not ROTATING:
		ROTATING = True
		for side in sides:
			side.animate_rotation(side.rotation - Vec3(0, 0, 90), duration=TURN_TIME, curve=CURVE)
	if key == 'w' or key == 'up arrow':
		pass
		# apply_surface(2)  # ceiling
	if key == 's' or key == 'down arrow':
		pass
		# apply_surface(0)  # floor
	if key == 'escape':
		application.quit()

TEXT = Text('', origin=(0, -0.45), scale=1.5)

def update():
	"""Move segments forward to simulate the player running. Recycle segments when they pass the bean."""
	global SPEED, SEG_LENGTH, SIDES_Z_0, LIGHT

	LIGHT.position = Vec3(1, math.sin(time.time()*2), 3)
	# TEXT.text = str(LIGHT.position)

	for element in [sides_A, sides_B, sides_C, sides_D]:
		for side in element:
			side.z += SPEED * time.dt
			if side.z > SIDES_Z_0 + SEG_LENGTH:
				side.z = get_last_z(element) - SEG_LENGTH


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
	Coin(position=(0, 0, -30), player=player, coin_counter=coin_counter_ui)
	Coin(position=(0, 0, -40), player=player, coin_counter=coin_counter_ui)
	Coin(position=(0, 0, -50), player=player, coin_counter=coin_counter_ui)
	app.run()
