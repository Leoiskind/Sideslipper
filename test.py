from ursina import *
from ursina.shaders import lit_with_shadows_shader

app = Ursina()
Entity.default_shader = lit_with_shadows_shader

def random_vec3(length=1.0):
    v = Vec3(
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )
    return v.normalized() * length

class Particles():
	def __init__(self, position, size, particle_number=100, particle_size=.01, color=color.red):
		self.position = position
		self.size = size
		self.particle_number = particle_number
		self.particle_size = particle_size
		self.color = color
		self.particles = []
		for n in range(particle_number):
			self.particles.append(
				Entity(
					model='sphere',
					position=self.position,
					scale=self.particle_size,
					color=self.color,
					enabled=False
					)
			)
		self.playable = True

	def play(self, duration):
		if self.playable:
			self.playable = False
			for particle in self.particles:
				particle.position = self.position
				particle.enabled = True
				particle.animate_position(particle.position + random_vec3(self.size), duration=duration, curve=curve.linear)
				invoke(setattr, particle, 'enabled', False, delay=duration)
				invoke(setattr, self, 'playable', True, delay=duration)

ground = Entity(
    model='plane',
    scale=30,
    y=-2,
    color=color.white,
    shader=lit_with_shadows_shader,
)

cube = Entity(
    model='cube',
	scale=.5,
    y=0,
    z=-5,
    color=color.red,
    shader=lit_with_shadows_shader,
    shadow=True,
)

particles = Particles(
	position=cube.position,
	size=.5,
	particle_size=.1,
	color=color.blue,
)

particles.parent = cube

sun = DirectionalLight(shadows=True)
sun.color = color.white
print(sun.color)
sun.look_at(Vec3(1, -1, 1))
sun.shadow_map_resolution = Vec2(4048, 4048)
sun.update_bounds(scene)

sun.shadow_bias = 0.04

AmbientLight(color=color.rgba(2,2,2,2))

def input(key):	
	speed = 100 * time.dt
	if held_keys['space']:
		particles.play(.4)
	if held_keys['q'] or held_keys['escape']:
		application.quit() 
	if held_keys['w']: cube.position += cube.forward*speed
	if held_keys['s']: cube.position += cube.back*speed
	if held_keys['a']: cube.position += cube.left*speed
	if held_keys['d']: cube.position += cube.right*speed
	if held_keys['i']: camera.position += camera.forward*speed
	if held_keys['k']: camera.position += camera.back*speed
	if held_keys['j']: camera.position += camera.left*speed
	if held_keys['l']: camera.position += camera.right*speed
	if held_keys['u']: camera.rotation_y -= speed
	if held_keys['o']: camera.rotation_y += speed
	if held_keys['n']: camera.y -= speed
	if held_keys['m']: camera.y += speed

app.run()