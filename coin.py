from ursina import *
from config import WIDTH, HEIGHT, LENGTH, CORRIDOR_HEIGHT, SIDES_Z_0, ORIGIN_SIDES, SCROLL_SPEED

class Coin(Entity):
	def __init__(self, position, player, coin_counter, parent):
		super().__init__(
			model='sphere',
			color=color.gold,
			scale=(0.25,0.25,0.05),
			position=position,
			rotation=(90,0,0),
			collider='box',
			parent=parent
		)

		self.player=player
		self.coin_counter = coin_counter
		self.speed=10
	
	def update(self):
		self.rotation_x += 100 * time.dt
		self.z += self.speed * time.dt
		hit_info = self.intersects()
		if hit_info.hit:
			self.player.coins +=1
			self.coin_counter.text = f'coins: {self.player.coins}'
			print("dead 1")
			destroy(self)
			return
		if self.z>5:
			print("dead 2")
			destroy(self)
			return