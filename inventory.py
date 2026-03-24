from ursina import *
import flags

class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            # Main bag: 3 slots wide, 2 slots high. 
            scale = (.3, .2), 
            origin = (-.5, .5),
            position = (.58, .2, -2),
            texture = 'white_cube',
            texture_scale = (3, 2),
            color = color.dark_gray,
            unlit = True
        )
        
        self.item_parent = Entity(parent=self, scale=(1/3, 1/2))
        self.use_item_callback = None

        self.mouth_bg = Entity(
            parent=self,
            model='quad',
            texture='white_cube',
            texture_scale=(3, 1), 
            scale=(1, 1/2),       
            origin=(-.5, .5),
            position=(0, -1.5),   
            color=color.red.tint(-.2),
            unlit=True
        )
        
        self.eat_anim = SpriteSheetAnimation(
            'mouth_animation',
            parent= self.mouth_bg,
            fps=6,
            tileset_size=(4, 1),
            scale=(1.2, 1.5),
            position=(.5, -.4, -3),
            animations={
                'idle': ((0,0), (1,0)),
                'eat': ((0, 0), (3, 0))
			}
            
		)

        self.eat_button = Button(
            parent=self,
            text='EAT!',
            scale=(1/3, 1/2),       
            origin=(-.5, .5),
            position=(1/3, -2.05),  
            color=color.green.tint(-.2),
            on_click=self.consume_mouth_items_anim
        )
        
        self.eat_anim.play_animation('idle')

    def append(self, item):
        free_spot = self.find_free_spot()
        if free_spot is None:
            print("Inventory is full!")
            return

        icon = Draggable(
            parent = self.item_parent,
            model = 'quad',
            texture = item,
            origin = (-.5, .5),
            color = color.white,
            position = free_spot,
            z = -.1,
            unlit = True
        )
        icon.item_name = item
        
        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z = -.3
            icon._always_on_top = True

        def drop():
            icon.x = int(round(icon.x))
            icon.y = int(round(icon.y))
            icon.z = -.1
            icon.always_on_top = False

            # Valid boundaries for dropping
            in_main_bag = (0 <= icon.x <= 2) and (0 >= icon.y >= -1)
            in_mouth = (icon.y == -3) and (0 <= icon.x <= 2)

            if not (in_main_bag or in_mouth):
                print("out of bounds")
                icon.position = icon.org_pos
                icon.z = -.1
                return

            for c in self.item_parent.children:
                if c == icon:
                    continue
                if c.x == icon.x and c.y == icon.y:
                    print('swap positions')
                    c.position = icon.org_pos
                    c.z = -0.1

        icon.drag = drag
        icon.drop = drop
        name = item.replace('_', ' ').title()
        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.hsv(0, 0, 0, .8)
    
    def hide_inventory(self):
        self.enabled = False
    
    def show_inventory(self):
        flags.INVENTORY = True
        self.enabled = True
        
    def find_free_spot(self):
        taken_spots = [(int(e.x), int(e.y)) for e in self.item_parent.children]
        for y in range(2):
            for x in range(3):
                if not (x, -y) in taken_spots:
                    return (x, -y)
        return None
    
    def consume_mouth_items_anim(self):
        self.eat_anim.play_animation('eat')
        invoke(self.consume_mouth_items, delay=2)

    def consume_mouth_items(self):
        mouth_items = [c for c in list(self.item_parent.children) if c.y == -3 and 0 <= c.x <= 2]
        mouth_items.sort(key=lambda c: c.item_name == 'fries', reverse=True) 
        for c in mouth_items:
            print(f"Eating {c.item_name}!")
            if self.use_item_callback is not None:
                self.use_item_callback(c.item_name)
            destroy(c)
            
        if hasattr(self, 'shop_reference') and self.shop_reference is not None:
            self.shop_reference.hide_shop()

    def update(self):
        main_items = [c for c in self.item_parent.children if c.y >= -1]
        if len(main_items) >= 6:
            flags.INVENTORY_FULL = True
        else:
            flags.INVENTORY_FULL = False