from ursina import Entity, Vec3, random, invoke, color

def random_vec3(length=1.0):
    v = Vec3(
        random.uniform(-1, 1),
        random.uniform(-1, 1),
        random.uniform(-1, 1)
    )
    return v.normalized() * length

class Particles():
	def __init__(self, position, size, particle_number=100, particle_size=.01, color=color.red, debug_position=False, parent=None):
		self.position = position
		self.size = size
		self.particle_number = particle_number
		self.particle_size = particle_size
		self.color = color
		self.parent=parent
		self.playable = True
		self.debug_position = debug_position
		self.particles = [Entity(
			model='sphere',
			parent=self.parent,
			position=self.position,
			scale=self.particle_size,
			color=self.color,
			enabled=False
		)
		for _ in range(particle_number)]
		self.debuger_position = Entity(
			position=self.position,
			model='sphere',
			scale=self.size/2,
			color=color,
			enabled=debug_position,
			parent=self.parent
		)

	def play(self, duration, curve):
		if self.playable:
			self.playable = False
			for particle in self.particles:
				particle.position = self.position
				particle.enabled = True
				particle.animate_position(particle.position + random_vec3(self.size), duration=duration, curve=curve)
				invoke(setattr, particle, 'enabled', False, delay=duration)
				invoke(setattr, self, 'playable', True, delay=duration)

	def set_position(self, position):
		if self.playable:
			self.position = position
			self.debuger_position.position = position
			for particle in self.particles:
				particle.position = position