from ursina import *
import flags

class Shop(Entity):
	def __init__(self, player, inventory, coin_counter_ui, catalog):
		super().__init__(
		parent=camera.ui,
		model='quad',
		scale=(0.8, 0.5),      # A wide rectangle in the center of the screen
		position=(0, 0),
		color=color.rgba(20, 20, 20, 240), # Dark semi-transparent background
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
		Text(parent=self, text='ITEM SHOP', position=(0, 0.4), origin=(0, 0), scale=2)

		# 2. Close Button
		Button(parent=self, text='X', scale=(0.05, 0.08), position=(0.45, 0.4), color=color.red, on_click=self.hide_shop)

		# 3. Create the items automatically
		x_spacing = -0.3

		for item_name, cost in self.catalog.items():
			# Create the clickable item button
			btn = Button(
			parent=self,
			model='quad',
			texture=item_name,
			scale=(0.15, 0.25),
			position=(x_spacing, 0),
			color=color.white,
			tooltip=Tooltip(f"Buy {item_name.title()}")
			)
			# We use Ursina's 'Func' to pass the specific item and cost to our buy function
			btn.on_click = Func(self.buy_item, item_name, cost)

			# Create the price label under the item
			Text(parent=self, text=f'{cost} Coins', position=(x_spacing, -0.18), origin=(0, 0), scale=1.5, color=color.gold)

		x_spacing += 0.3 # Move the next item to the right

	def buy_item(self, item_name, cost):
		# Check if the player has enough money
		if self.player.coins >= cost:
			# Take the money
			self.player.coins -= cost
			self.coin_counter_ui.text = f'Coins: {self.player.coins}'

			# Give the item
			self.inventory.append(item_name)
			print(f"Purchased {item_name}!")
		else:
			print(f"Not enough coins for {item_name}! You need {cost - self.player.coins} more.")

	def show_shop(self):
		self.enabled = True

	def hide_shop(self):
		self.enabled = False
			
	def update(self):
		print(flags.STORE)
		if flags.STORE:
			self.show_shop()
		else:
			self.hide_shop()