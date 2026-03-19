from ursina import *
class Inventory(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'quad',
			scale = (.45, .72),
			origin = (-.5, .5),
			position = (-.25,.45),
			texture = 'white_cube',
			texture_scale = (5,8),
			color = color.dark_gray,
			unlit=True
			)
		self.item_parent = Entity(parent=self, scale=(1/5,1/8))
		self.use_item_callback=None

		self.mouth_bg=Entity(
			parent=self,
			model='quad',
			texture='white_cube',
			texture_scale=(3, 1), # 3 columns wide, 1 row high
			scale=(3/5, 1/8),     # Match the scale of 3 inventory slots
			origin=(-.5, .5),
			position=(1/5, -9/8), # Placed at X=1, and exactly at Y=-9!
			color=color.red.tint(-.2), # Make it red so it looks like a mouth!
			unlit=True
		)

		self.eat_button = Button(
            parent=self,
            text='EAT!',
            # 2. Shrunk to fit 1 column, and moved to the right of the mouth!
            scale=(1/5, 1/8),       
            origin=(-.5, .5),
            position=(4/5, -9/8),   
            color=color.green.tint(-.2),
            on_click=self.consume_mouth_items 
		)

	def append(self, item):
		icon=Draggable(
			parent = self.item_parent,
			model = 'quad',
			texture= item,
			origin = (-.5,.5),
			color = color.white,
			position = self.find_free_spot(),
			z = -.1,
			unlit=True
			)
		icon.item_name=item
		
		def drag():
			icon.org_pos=(icon.x, icon.y)
			icon.z = -.3
			icon._always_on_top=True

		def drop():
			icon.x = int(round(icon.x))
			icon.y = int(round(icon.y))
			icon.z = -.1
			icon.always_on_top=False

			in_main_bag = (0 <= icon.x < 5) and (0 >= icon.y > -8)
			in_mouth = (icon.y == -9) and (icon.x in [1, 2, 3])

			if not (in_main_bag or in_mouth):
				print("out of bounds")
				icon.position = icon.org_pos
				icon.z = -.1
				return

			for c in self.item_parent.children:
				if c == icon:
					continue
				if c.x==icon.x and c.y==icon.y:
					print('swap positions')
					c.position = icon.org_pos
					c.z = -0.1

		icon.drag=drag
		icon.drop=drop
		name=item.replace('_', '').title()
		icon.tooltip=Tooltip(name)
		icon.tooltip.background.color=color.hsv(0,0,0,.8)
	
	def hide_inventory(self):
		self.enabled = False
	
	def show_inventory(self):
		self.enabled = True
		
	def find_free_spot(self):
		taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]
		for y in range(8):
			for x in range(5):
				if not (x, -y) in taken_spots:
					return(x, -y)
	
	def consume_mouth_items(self):
		for c in list(self.item_parent.children):
			if c.y == -9 and c.x in [1, 2, 3]:
				print(f"Eating {c.item_name}!")
				if self.use_item_callback is not None:
					self.use_item_callback(c.item_name)
				
				destroy(c)