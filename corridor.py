from ursina import Entity, color, Vec3, invoke, curve
from ursina.shaders import lit_with_shadows_shader
from config import WIDTH, HEIGHT, LENGTH, CORRIDOR_HEIGHT, SIDES_Z_0, ORIGIN_SIDES, SPEED_CHANGE, DEFAULT_SCROLL_SPEED
import flags
from camera import nausea_shader, fisheye_shader, camera_base_pos, camera_base_rot

class CorridorSegment(Entity):
	def __init__(self, z_pos, rotation, color=color.gray, parent=None, effect=None):
		super().__init__()
		self.z = SIDES_Z_0 + z_pos
		self.model = 'cube'
		self.texture = 'brick'
		self.color = color
		self.shader = lit_with_shadows_shader
		self.scale = (WIDTH, HEIGHT, LENGTH)
		self.origin = ORIGIN_SIDES
		self.rotation = rotation
		self.shadow = True

def create_sides(n_segments):
	sides_A = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 0), color=color.gray) for i in range(n_segments)]
	sides_B = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 90), color=color.red) for i in range(n_segments)]
	sides_C = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, -90), color=color.yellow) for i in range(n_segments)]
	sides_D = [CorridorSegment(z_pos = -i * LENGTH, rotation=Vec3(0, 0, 180), color=color.orange) for i in range(n_segments)]

	return sides_A + sides_B + sides_C + sides_D

def hide_sides(sides):
	for side in sides:
		side.enabled = False

def show_sides(sides):
	for side in sides:
		side.enabled = True

class EffectWall():
	def __init__(self, apply, clear, *args):
		self.apply = apply
		self.clear = clear
		self.args = args

	def apply_effect(self):
		self.apply(*self.args)

	def clear_effect(self):
		self.clear(*self.args)

# Possible effects

def change_speed(speed):
	flags.SCROLL_SPEED = speed

def increase_speed(bean, factor):
	global SPEED_CHANGE, DEFAULT_SCROLL_SPEED
	n_steps = 10
	for i in range(n_steps):
		invoke(change_speed, flags.SCROLL_SPEED + i*factor/n_steps*DEFAULT_SCROLL_SPEED, delay=i/n_steps*SPEED_CHANGE)
	bean.animate_z(bean.z + 1, duration=SPEED_CHANGE, curve=curve.linear)

def decrease_speed(bean, factor):
	global SPEED_CHANGE, DEFAULT_SCROLL_SPEED
	n_steps = 10
	for i in range(n_steps):
		invoke(change_speed, flags.SCROLL_SPEED - i*factor/n_steps*DEFAULT_SCROLL_SPEED, delay=i/n_steps*SPEED_CHANGE)
	bean.animate_z(bean.z - 1, duration=SPEED_CHANGE, curve=curve.linear)

def block_right():
	flags.CAN_RIGHT = False

def release_right():
	flags.CAN_RIGHT = True

def block_left():
	flags.CAN_LEFT = False

def release_left():
	flags.CAN_LEFT = True

def block_jump():
	flags.CAN_JUMP = False

def release_jump():
	flags.CAN_JUMP = True

def flip_camera(camera):
	global camera_base_rot
	camera_base_rot[2] += 180

def return_camera(camera):
	global camera_base_rot
	camera_base_rot[2] += 180

nausea_time = 0

def set_nausea(camera, factor):
	global nausea_time
	camera.shader = nausea_shader
	camera.set_shader_input('strength', factor)
	camera.set_shader_input('time', nausea_time)
	camera.set_shader_input('pixel_size', 256)
	print(nausea_time)

def clear_nausea(camera, factor):
	camera.shader = fisheye_shader
	camera.set_shader_input('strength', 0.1)
	camera.set_shader_input('pixel_size', 256)