from ursina import *
import camera as cam
import flags
from config import DEFAULT_SCROLL_SPEED, CAM_BASE_POS, CAM_BASE_ROT

class Shop(Entity):
	def __init__(self, player, inventory, coin_counter_ui, catalog):
		super().__init__(
			parent=camera.ui,
			model='quad',
			scale=(0.8, 0.4),      # A wide rectangle in the center of the screen
			position=(0, -.20),
			color=color.dark_gray, # Dark semi-transparent background
			enabled=False          # Start with the shop hidden
		)

		# The shop needs to know about the player (for coins) and inventory (to store items)
		self.player = player
		self.inventory = inventory
		self.coin_counter_ui = coin_counter_ui

		# A dictionary of what you are selling and how much it costs
		self.catalog = catalog

		self.setup_ui()

	def setup_ui(self):
		# 1. Shop Title
		Text(parent=self, text='ITEM SHOP', position=(0, 0.4, -.2), origin=(0, 0), scale=2, color=color.black)
		
		# 2. Close Button
		Button(parent=self, text='X', scale=(0.05, 0.08), position=(0.45, 0.4, -.1), color=color.red, on_click=self.hide_shop)

		# 3. Create the items automatically
		x_spacing = -0.3
		
		for item_name, cost in self.catalog.items():
			# Create the clickable item button
			btn = Button(
				parent=self,
				model='quad',
				texture=item_name,
				scale=(0.15, 0.25),
				position=(x_spacing, 0, -.1),
				color=color.white,
				tooltip=Tooltip(f"Buy {item_name.title()}", z=-.2)
			)
			# We use Ursina's 'Func' to pass the specific item and cost to our buy function
			btn.on_click = Func(self.buy_item, item_name, cost, btn)
			
			# Create the price label under the item
			Text(parent=self, text=f'{cost} Coins', position=(x_spacing, -0.18, -.2), origin=(0, 0), scale=1.5, color=color.gold)
			
			x_spacing += 0.3 # Move the next item to the right

	def buy_item(self, item_name, cost, btn):
		# Check if the player has enough money
		if self.player.coins >= cost and not flags.INVENTORY_FULL:
			# Take the money
			self.player.coins -= cost
			self.coin_counter_ui.text = f'Coins: {self.player.coins}'
			
			# Give the item
			self.inventory.append(item_name)
			print(f"Purchased {item_name}!")
		else:
			btn.color = color.red
			invoke(setattr, btn, 'color', color.white, delay=0.2)
			invoke(print, "Changed color", delay=.2)
			print(f"Not enough coins for {item_name}! You need {cost - self.player.coins} more.")

	def show_shop(self):
		print("Showing shop")
		flags.SHOP = True
		flags.SCROLL_SPEED = 0
		self.enabled = True

	def hide_shop(self):
		global DEFAULT_SCROLL_SPEED, CAM_BASE_POS, CAM_BASE_ROT
		application.paused = False
		cam.camera_base_pos = CAM_BASE_POS
		cam.camera_base_rot = CAM_BASE_ROT
		flags.STORE = False
		flags.SCROLL_SPEED = DEFAULT_SCROLL_SPEED
		flags.INVENTORY = False
		self.enabled = False
		
