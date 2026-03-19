from ursina import *

class Coin(Entity):
	def __init__(self, position, player, coin_counter):
		super().__init__(
			model='cylinder',
			color=color.gold,
			scale=(0.5,0.1,0.5),
			position=position,
			rotation=(90,0,0),
			collider='box'
		)

		self.player=player
		self.coin_counter = coin_counter
		self.speed=1
	
	def update(self):
		self.rotation_y += 100 * time.dt
		self.z += self.speed * time.dt
		if distance(self, self.player)<1.5:
			self.player.coins +=1
			self.coin_counter.text = f'coins: {self.player.coins}'
			print("dead 1")
			destroy(self)
			return
		if self.z>5:
			print("dead 2")
			destroy(self)
			return