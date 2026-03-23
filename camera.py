from ursina import Shader, Vec3, time, random, invoke
import flags
from config import DEFAULT_STRENGTH_SHADER

with open('assets/shaders/fisheye.vert', 'r') as f:
    vertex_src = f.read()

with open('assets/shaders/fisheye.frag', 'r') as f:
    fragment_src = f.read()

# Static camera behind the bean and looking toward origin (center of corridor)
fisheye_shader = Shader(
    name='fisheye',
    language=Shader.GLSL,
    vertex=vertex_src,
    fragment=fragment_src
)

with open('assets/shaders/nausea.vert', 'r') as f:
    vertex_src = f.read()

with open('assets/shaders/nausea.frag', 'r') as f:
    fragment_src = f.read()

nausea_shader = Shader(
      name='nausea',
      language=Shader.GLSL,
      vertex=vertex_src,
      fragment=fragment_src
)

# global camera_base_rot, camera_base_pos

shake_timer = 0.0
shake_duration = 0.0
shake_strength = 0.0
camera_base_pos = Vec3(.7, 0, -5)
camera_base_rot = Vec3(7, 190, 0)

def start_camera_shake(strength=0.15, duration=0.2):
    global shake_timer, shake_duration, shake_strength
    shake_timer = duration
    shake_duration = duration
    shake_strength = strength

def update_camera_shake(camera):
	global shake_timer, camera_base_rot, camera_base_pos, DEFAULT_STRENGTH_SHADER
	print(camera.rotation)
    
	camera.set_shader_input('strength', DEFAULT_STRENGTH_SHADER*flags.SCROLL_SPEED*10)

	if shake_timer > 0 and not flags.SHAKING:
		flags.SHAKING = True
		shakes = int(shake_timer / time.dt)
		cam_pos0 = camera.position
		cam_rot0 = camera.rotation
		for shake in range(shakes):
			current_strength  = (shakes - shake) * time.dt
			offset = Vec3(
				random.uniform(-current_strength, current_strength),
				random.uniform(-current_strength, current_strength),
				random.uniform(-current_strength, current_strength),
			)
			rot_offset = Vec3(
				random.uniform(-current_strength * 5, current_strength * 5),
				random.uniform(-current_strength * 5, current_strength * 5),
				random.uniform(-current_strength * 5, current_strength * 5),
			)
			invoke(camera.position_setter, camera.position+offset, delay=time.dt*shake)
			invoke(camera.rotation_setter, camera.rotation+rot_offset, delay=time.dt*shake)
		invoke(camera.position_setter, cam_pos0, delay=time.dt*(shake+1))
		invoke(camera.rotation_setter, cam_rot0, delay=time.dt*(shake+1))
		invoke(setattr, flags, 'SHAKING', False, delay=time.dt*(shake*1))
		shake_timer = 0

		# shake_timer -= time.dt

		# t = max(shake_timer, 0) / shake_duration
		# current_strength = shake_strength * t

		# offset = Vec3(
		# 	random.uniform(-current_strength, current_strength),
		# 	random.uniform(-current_strength, current_strength),
		# 	random.uniform(-current_strength, current_strength),
		# )
		# camera.position = camera_base_pos + offset

		# rot_offset = Vec3(
		# 	random.uniform(-current_strength * 5, current_strength * 5),
		# 	random.uniform(-current_strength * 5, current_strength * 5),
		# 	random.uniform(-current_strength * 5, current_strength * 5),
		# )
		# camera.rotation = camera_base_rot + rot_offset
	# else:
	# 	camera.position = camera_base_pos
	# 	camera.rotation = camera_base_rot