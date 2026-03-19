from ursina import *
from ursina.shaders import lit_with_shadows_shader
from corridor import *
from config import *
from inventory import *
from coin import *
from bean import *
from obstacles import *
from shop import *
from effects import EffectsManager
from camera import *
import flags

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
	bean_color=color.clear, origin=ORIGIN
	)

# -----------------
# Obstacles
# -----------------
Test_Lower = LowObstacle(z=-30, parent=rotation_pivot)
Test_Higher = HighObstacle(z=-40, parent=rotation_pivot)
Test_Wall = WallObstacle(z=-50, parent=rotation_pivot)
Middle_obstacle = MiddleObstacle(z=-60, parent=rotation_pivot)
Test_Shop = StoreObstacle(z=-80, parent=rotation_pivot)
# obs_scale = .75
# Test_Obstacle = Obstacle(
# 	position=(0, (obs_scale-CORRIDOR_HEIGHT)/2, -30),
# 	scale=(CORRIDOR_HEIGHT,obs_scale,0.5),
# 	parent=rotation_pivot
# 	)

# -----------------
# Rotation hierarchy
# -----------------
for shadow in bean.shadows:
	shadow.parent = rotation_pivot

for side in sides:
	side.parent = rotation_pivot

# fisheye_shader.set_shader_input('strength', 1.0)  # full effect
camera.shader = fisheye_shader
camera.set_shader_input('strength', 0.1)
# camera.shader = None
camera.origin = ORIGIN
camera.position = Vec3(.7, 0, 0)
camera.rotation = Vec3(7, 190, 0)
camera.fov = FOV

def get_last_z(sides_list):
	"""Helper to find the farthest-back z (most negative) among all sides."""
	return min(side.z for side in sides_list)

# --- GAME STATE & SCORE VARIABLES ---
GAME_OVER = False
SCORE = 0

def trigger_death():
	global GAME_OVER, SPEED
	if GAME_OVER: return # Prevent dying twice!

	print("Player died!")
	GAME_OVER = True
	SPEED = 0  # Stop the walls from moving
	
	# Update and show the death screen
	final_score_ui.text = f'Final Score: {int(SCORE)}'
	death_screen.enabled = True

bean.on_death_callback = trigger_death

def restart_game():
	global GAME_OVER, SCORE, SPEED
	
	print("Restarting game...")
	GAME_OVER = False
	SCORE = 0
	SPEED = 0  # Reset to your base starting speed
	
	# Reset Player Stats
	player.coins = 0
	coin_counter_ui.text = 'Coins: 0'
	score_ui.text = 'Score: 0'
	player.enabled = True
	player.position= Vec3(0, 0, -10)
	
	# Reset the corridor rotation back to the floor
	rotation_pivot.rotation_z = 0
	
	# Hide the death screen so the player can see again
	for entity in scene.entities:
		if getattr(entity, 'is_obstacle', False) or isinstance(entity, Coin):
			destroy(entity)

	player.enabled = True
	death_screen.enabled = False
	

def toggle_pause():
	# Don't allow pausing if the player is already dead!
	if GAME_OVER: 
		return 

	# Flip the built-in Ursina pause state
	application.paused = not application.paused
	
	# Turn the visual pause screen on or off to match
	pause_screen.enabled = application.paused


# -----------------
# Input & update
# -----------------

def input(key):
	"""Keyboard controls for switching attachment (visual only)."""
	global camera_base_pos, camera_base_rot
	print(key)
	global ROTATING, JUMPING
	if key=='p':
		toggle_pause()

	if key=='k':
		trigger_death()
	
	if rotation_pivot.rotation_z %90 == 0:
		ROTATING=False

	if rotation_pivot.rotation_z % 90 == 0 and bean.y == 0:
		ROTATING = False
	if bean.y == 0:
		JUMPING = False
	if held_keys['d'] and not ROTATING and not JUMPING:
		ROTATING = True
		# start_camera_shake(strength=0.05, duration=0.3)  # shake the camera when we switch sides!
		rotation_pivot.animate_rotation_z(rotation_pivot.rotation_z - 90, duration=TURN_TIME, curve=CURVE)
		bean.jump()
	if held_keys['a'] and not ROTATING and not JUMPING:
		ROTATING = True
		# start_camera_shake(strength=0.05, duration=0.3)  # shake the camera when we switch sides!
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
	if held_keys['i']: camera_base_pos += camera.forward*speed
	if held_keys['k']: camera_base_pos += camera.back*speed
	if held_keys['j']: camera_base_pos += camera.left*speed
	if held_keys['l']: camera_base_pos += camera.right*speed
	if held_keys['u']: camera_base_rot[1] -= speed
	if held_keys['o']: camera_base_rot[1] += speed
	if held_keys['n']: camera_base_pos[1] -= speed
	if held_keys['m']: camera_base_pos[1] += speed

TEXT = Text('', origin=(0, -0.45), scale=1.5)

def update():
	"""Move segments forward to simulate the player running. Recycle segments when they pass the bean."""
	global SPEED, LENGTH, SIDES_Z_0, JUMPING, SPEED, SCORE
	SCROLL_SPEED = flags.SCROLL_SPEED
	
	# LIGHT.look_at(bean)
	# TEXT.text = str(LIGHT.position)

	update_camera_shake(camera)
	if GAME_OVER:
		return
	
	SCORE += time.dt * 10
	score_ui.text = f'Score: {int(SCORE)}'

	for element in [sides_A, sides_B, sides_C, sides_D]:
		for side in element:
			side.texture_offset = (0, (time.time() * -SCROLL_SPEED) % 1)  # scroll texture to simulate movement
			side.z += SPEED * time.dt
			if side.z > SIDES_Z_0 + LENGTH:
				side.z = get_last_z(element) - LENGTH
	
	if flags.SCROLL_SPEED != 0:
		coin_spawner(player=bean, coin_counter_ui=coin_counter_ui, parent=rotation_pivot)

	if bean.enabled:
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
	else:
		for shadow in bean.shadows:
			shadow.enabled = False


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

	# --- ADD THIS: Initialize the Shop ---
	# Pass the player, the inventory, and the UI text so the shop can edit them!
	catalog={
		'nachos': 2,
		'rice'  : 5,
		'hash_brown': 10
	}
	item_shop = Shop(player=player, inventory=inventory, coin_counter_ui=coin_counter_ui, catalog=catalog)

	#------
	# Manages effects
	#------
	# 1. Create a "Remote Control" function so the EffectsManager can safely edit SPEED
	def update_game_speed(amount):
		global SPEED
		SPEED += amount

	# 2. Start up the new Effects Manager and hand it the player, the UI, and the remote control
	effect_manager = EffectsManager(
		player=player, 
		coin_counter_ui=coin_counter_ui, 
		speed_callback=update_game_speed
	)

	# 3. Tell the inventory to use the manager's logic when items are eaten!
	inventory.use_item_callback = effect_manager.apply_item_effects

	# --- 1. SCORE UI ---
	score_ui = Text(text='Score: 0', position=(-0.85, 0.38), scale=2, color=color.white)

	# --- 2. DEATH SCREEN UI ---
	death_screen = Entity(parent=camera.ui, enabled=False, z=1)
	Entity(parent=death_screen, model='quad', scale=(2, 2), color=color.rgba(0, 0, 0, 200))
	Text(parent=death_screen, text='YOU DIED', origin=(0, 0), position=(0, 0.2), scale=4, color=color.red, z=-1)
	final_score_ui = Text(parent=death_screen, text='Score: 0', origin=(0, 0), position=(0, 0), scale=2, color=color.white, z=-1)
	Button(parent=death_screen, text='RESTART', scale=(0.3, 0.1), position=(0, -0.2), color=color.azure, on_click=Func(lambda: restart_game()))

	# --- 3. PAUSE SCREEN UI ---
	pause_screen = Entity(parent=camera.ui, enabled=False, z=-1)
	Entity(parent=pause_screen, model='quad', scale=(2, 2), color=color.rgba(0, 0, 0, 180))
	Text(parent=pause_screen, text='PAUSED', origin=(0, 0), position=(0, 0), scale=5, color=color.white)
	Text(parent=pause_screen, text='Press P to Resume', origin=(0, 0), position=(0, -0.15), scale=1.5, color=color.gray)

	# --- 4. OPEN SHOP BUTTON ---
	# Uses Sequence to simultaneously open the shop AND pause the game!
	open_shop_btn = Button(
		scale=(0.15, 0.05),
		position=(-0.75, 0.3),
		color=color.azure,
		text='Open Shop',
		on_click=Sequence(Func(item_shop.show_shop), Func(setattr, application, 'paused', True)) 
	)


	app.run()