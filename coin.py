from ursina import *
from config import WIDTH, HEIGHT, LENGTH, CORRIDOR_HEIGHT, SIDES_Z_0, ORIGIN_SIDES, COIN_TIMER, COIN_SPAWN_DISTANCE, COIN_POSITIONS, COIN_RARITY
import flags

class Coin(Entity):
	def __init__(self, position, player, coin_counter, parent):
		super().__init__(
			model='sphere',
			color=color.gold,
			scale=(0.3,0.3,0.05),
			position=position,
			rotation=(90,0,0),
			collider='box',
			parent=parent
		)

		self.player=player
		self.coin_counter = coin_counter
		self.speed=flags.SCROLL_SPEED * LENGTH
	
	def update(self):
		global LENGTH
		self.rotation_x += 100 * time.dt
		hit_info = self.intersects()
		if hit_info.hit and hit_info.entity == self.player.magnet:
			self.magnetized = True

		if getattr(self, 'magnetized', False):
			self.parent = self.player
			target_pos = self.player.position + Vec3(0, -2, 10)
			direction = (target_pos - self.position).normalized()
			self.position += direction * 20 * time.dt
			
		else:
			self.z += flags.SCROLL_SPEED * LENGTH * time.dt	
		if hit_info.hit and hit_info.entity == self.player:
			self.player.coins +=1
			self.coin_counter.text = f'coins: {self.player.coins}'
			destroy(self)
			return
		if self.z>5:
			destroy(self)
			return
		
def coin_spawner(player, coin_counter_ui, parent):
	global COIN_TIMER, COIN_SPAWN_DISTANCE, LENGTH, COIN_RARITY
	coin_time = COIN_SPAWN_DISTANCE / (flags.SCROLL_SPEED * LENGTH)
	COIN_TIMER += time.dt
	if COIN_TIMER > coin_time:  # spawn a coin
		COIN_TIMER -= coin_time
		if random.random() < COIN_RARITY:
			Coin(position=random.choice(COIN_POSITIONS), player=player, coin_counter=coin_counter_ui, parent=parent)