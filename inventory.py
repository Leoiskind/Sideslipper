from ursina import *
class Inventory(Entity):
	def __init__(self):
		super().__init__(
			parent = camera.ui,
			model = 'quad',
			scale = (.5, .8),
			origin = (-.5, .5),
			position = (-.3,.4),
			texture = 'white_cube',
			texture_scale = (5,8),
			color = color.dark_gray
			)
		self.item_parent = Entity(parent=self, scale=(1/5,1/8))

	def append(self, item):
		icon=Draggable(
			parent = self.item_parent,
			model = 'quad',
			texture= item,
			origin = (-.5,.5),
			color = color.white,
			position = self.find_free_spot(),
			z = -.1
			)
		
		def drag():
			icon.org_pos=(icon.x, icon.y)
			icon.z += .1

		def drop():
			icon.x = int(round(icon.x))
			icon.y = int(round(icon.y))
			icon.z = -.1

			if icon.x<0 or icon.x>=5 or icon.y>0 or icon.y<-7:
				print("out of bounds")
				icon.position=(icon.org_pos)
				icon.z= -.1
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
		
	def find_free_spot(self):
		taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]
		for y in range(8):
			for x in range(5):
				if not (x, -y) in taken_spots:
					return(x, -y)