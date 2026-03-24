from ursina import *
from ursina import texture
import camera as cam
import flags
import random
from config import DEFAULT_SCROLL_SPEED, CAM_BASE_POS, CAM_BASE_ROT

class Shop(Entity):
	def __init__(self, player, inventory, coin_counter_ui):
		super().__init__(
			parent=camera.ui,
			model='quad',
			scale=(0.8, 0.4),      # A wide rectangle in the center of the screen
			position=(.2, -.15, -2),
			color=color.clear, # Dark semi-transparent background
			enabled=False          # Start with the shop hidden
		)
		self.catalog={}
		self.inventory = inventory
		self.inventory.shop_reference=self

		# The shop needs to know about the player (for coins) and inventory (to store items)
		self.player = player
		self.coin_counter_ui = coin_counter_ui
		self.item_container=Entity(parent=self, enabled=True)
		# A dictionary of what you are selling and how much it costs

		self.shop_anim = SpriteSheetAnimation(
			'Store',
			tileset_size=(6, 1),
			fps=5,
			scale=(2.25, 1.5),
			animations={
				'idle': ((0, 0), (5, 0))
			},
			parent=camera.ui,
			collider=None,
			enabled=False
		)
		self.shop_anim.play_animation('idle')
		self.price = {
			'chocolate': 10,
			'pizza': 20,
			'shroom': 30,
			'pablo': 100,
			'nachos': 15,
			'rice': 12,
			'hash_brown': 20,
			'fries': 15,
			'donut': 17,
			'apple': 20
		}

		self.randomize_catalog()
		self.setup_ui()
		self.dialog_box = Text(
            parent=self, 
            text='', 
            position=(0, 1.1, -0.1), # Positioned above the items, slightly forward (Z)
            origin=(0, 0),
            scale=3,
            color=color.white,
            background=True,
            enabled=False
        )

	def randomize_catalog(self):
		avalailable_items = list(self.price.keys())
		picked_names = random.sample(avalailable_items, 3)

		self.catalog = {name: self.price[name] for name in picked_names}

	def setup_ui(self):
		# 1. This loop ONLY destroys things inside the container
		for child in self.item_container.children:
			destroy(child)

		x_spacing = -0.3
		for item_name, cost in self.catalog.items():
			btn = Button(
				parent=self.item_container, # <--- CRITICAL: Must be child of container!
				model='quad',
				texture=item_name,
				scale=(0.15, 0.25),
				position=(x_spacing, 0, -.1),
				color=color.white,
			)
			btn.on_click = Func(self.buy_item, item_name, cost, btn)
			btn.on_mouse_enter = Func(self.shopkeeper_speak, item_name)
			btn.on_mouse_exit = Func(self.shopkeeper_quiet)

			x_spacing += 0.3

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

	def shopkeeper_speak(self, item_name):
		lines = {
			'chocolate': f"{self.price[item_name]} Gold. Shit's chock full of sugar, enough of these and you'll start zooming!",
			'pizza': f"{self.price[item_name]} Gold. Pizza's heavy man, it'll weigh you down.",
			'apple': f"{self.price[item_name]} Gold. They say an apple a day, does what again?",
			'fries': f"{self.price[item_name]} Gold. Fries go with anything, may as well buy a few.",
			'hash_brown': f"{self.price[item_name]} Gold. Hash browns are solid, people always come back for more.",
			'rice': f"{self.price[item_name]} Gold. Good ol' reliable.",
			'nachos': f"{self.price[item_name]} Gold. Nachos are fire, ironically fire with the chocolate.",
			'shroom': f"{self.price[item_name]} Gold. How'd that get there? I wouldn't have that if I were you.",
			'pablo': f"{self.price[item_name]} Gold. Limited edition shit.",
			'donut': f"{self.price[item_name]} Gold. Not good for growth that."
		}

		spoken_line = lines.get(item_name, f"Ah, that {item_name}, Meh.")
		self.dialog_box.text = f" {spoken_line}"
		self.dialog_box.wordwrap=15
		self.dialog_box.create_background(
			padding=(0.05, 0.05), 
            radius=0.02, 
            color=color.rgba(0, 0, 0, 220)
		)
		self.dialog_box.enabled = True

	def shopkeeper_quiet(self):
		self.dialog_box.enabled=False

	def show_shop(self):
		self.enabled = True
		print("Showing shop")
		self.randomize_catalog()
		self.setup_ui()

		flags.SHOP = True
		self.shop_anim.enabled=True
		flags.SCROLL_SPEED = 0

	def hide_shop(self):
		global DEFAULT_SCROLL_SPEED, CAM_BASE_POS, CAM_BASE_ROT
		application.paused = False
		flags.STORE = False
		flags.SCROLL_SPEED = DEFAULT_SCROLL_SPEED
		flags.INVENTORY = False
		self.shop_anim.enabled = False
		self.enabled = False
 
		
