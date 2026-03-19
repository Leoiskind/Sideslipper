from ursina import *

active_timers = []

class EffectTimer(Entity):
    def __init__(self, item_name, duration):
        super().__init__(parent=camera.ui)
        self.slot_index = len(active_timers)
        active_timers.append(self)
        self.position = (0.75, 0.45 - (self.slot_index * 0.08))
        self.time_left = duration
        self.icon = Entity(parent=self, model='quad', texture=item_name, scale=(0.06, 0.06), position=(0, 0), unlit=True)
        self.text_ui = Text(parent=self, text=f'{int(duration)}s', position=(0.04, 0), origin=(-0.5, 0), scale=1.5, color=color.white)
        destroy(self, delay=duration)

    def update(self):
        self.time_left -= time.dt
        if self.time_left > 0:
            self.text_ui.text = f'{int(self.time_left)}s'
        else:
            if self in active_timers:
                active_timers.remove(self)

# --- NEW: The Effects Manager ---
class EffectsManager:
    # 1. Catch the references passed from main.py
    def __init__(self, player, coin_counter_ui, speed_callback):
        self.player = player
        self.coin_counter_ui = coin_counter_ui
        self.change_speed = speed_callback  # A remote control to change SPEED in main.py

    # 2. Your effects logic, updated to use "self."
    def apply_item_effects(self, item_name):
        if item_name == 'fries':
            self.change_speed(30)  
            EffectTimer('fries', 4) 
            
            def reset_fries():
                self.change_speed(-30)
            invoke(reset_fries, delay=4)

        elif item_name == 'hash_brown':
            self.change_speed(-20)  
            EffectTimer('hash_brown', 3) 
            
            def reset_slow():
                self.change_speed(20)
            invoke(reset_slow, delay=3)

        elif item_name == 'nachos':
            self.player.coins += 10
            self.coin_counter_ui.text = f'Coins: {self.player.coins}'
            
        else:
            print(f"You ate {item_name}, but nothing happened.")