from ursina import *
import flags
from config import DEFAULT_SCROLL_SPEED

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
    def __init__(self, player, coin_counter_ui, score_mult_callback, score_callback):
        self.player = player
        self.coin_counter_ui = coin_counter_ui
        self.score_mult_callback = score_mult_callback
        self.score_callback = score_callback
        self.extra_time = 0
        self.effect_time = {
            'chocolate': 4,
            'pizza': 3,
            'nachos': 5,
            'rice': 0
        }
        self.effect_uses = {
            'pablo': 1
        }

    # 2. Your effects logic, updated to use "self."
    def apply_item_effects(self, item_name):
        if item_name == 'chocolate':
            flags.SCROLL_SPEED += .5
            EffectTimer('chocolate', 4) 
            
            def reset_chocolate():
                flags.SCROLL_SPEED -= .5
            invoke(reset_chocolate, delay=self.effect_time['chocolate'] + self.extra_time)

        elif item_name == 'pizza':
            flags.SCROLL_SPEED -= 0.2 * DEFAULT_SCROLL_SPEED
            print(flags.SCROLL_SPEED)
            EffectTimer('pizza', 3) 
            
            def reset_pizza():
                flags.SCROLL_SPEED += .2 * DEFAULT_SCROLL_SPEED
            invoke(reset_pizza, delay=self.effect_time['pizza'] + self.extra_time)

        elif item_name == 'nachos':
            self.score_mult_callback(.5)
            EffectTimer('nachos', self.effect_time['nachos'] + self.extra_time)

            def reset_nachos():
                self.score_mult_callback(-0.5)
            invoke(reset_nachos, delay=self.effect_time['nachos'] + self.extra_time)
        elif item_name == 'rice':
            self.score_callback(100)
            EffectTimer('rice', self.effect_time['rice'] + self.extra_time)
        elif item_name == 'pablo':
            self.effect_uses['pablo'] += 1
        else:
            print(f"You ate {item_name}, but nothing happened.")