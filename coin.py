from ursina import *
from config import WIDTH, HEIGHT, LENGTH, CORRIDOR_HEIGHT, SIDES_Z_0, ORIGIN_SIDES, COIN_TIMER, COIN_SPACING, COIN_POSITIONS, COIN_RARITY
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
		self.sound = Audio('coin.mp3', autoplay=False, volume=flags.FX_VOLUME)
		self.player=player
		self.coin_counter = coin_counter
		self.magnetized = False
	
	def update(self):
		global LENGTH
		self.rotation_x += 100 * time.dt
		target_pos = self.player.world_position + Vec3(0, -1.25, 0)
		hit_info = self.intersects()

		if not self.magnetized:
			if flags.MAGNET_ACTIVE and hit_info.hit and hit_info.entity == self.player.magnet:
				self.magnetized = True

		if self.magnetized:
			direction = (target_pos - self.world_position).normalized()
			self.world_position += direction * 30 * time.dt
		else:
			self.z += flags.SCROLL_SPEED * LENGTH * time.dt
		
		if hit_info.hit and hit_info.entity == self.player:
			self.player.coins +=1
			self.coin_counter.text = f'coins: {self.player.coins}'
			self.sound.play()
			destroy(self)
			return
		
		if self.z>5:
			destroy(self)
			return
		
def coin_spawner(player, coin_counter_ui, parent):
	global COIN_TIMER, COIN_SPACING, LENGTH, COIN_RARITY
	coin_time = COIN_SPACING / (flags.SCROLL_SPEED * LENGTH)
	COIN_TIMER += time.dt
	if COIN_TIMER > coin_time:  # spawn a coin
		COIN_TIMER -= coin_time
		if random.random() < COIN_RARITY:
			Coin(position=random.choice(COIN_POSITIONS), player=player, coin_counter=coin_counter_ui, parent=parent)