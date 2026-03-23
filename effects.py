from ursina import *
import flags
from config import DEFAULT_SCROLL_SPEED

active_timer_slots = []

class EffectTimer(Entity):
    def __init__(self, item_name, duration):
        super().__init__(parent=camera.ui)
        
        self.slot_index = -1
        for i, slot in enumerate(active_timer_slots):
            if slot is None:
                self.slot_index = i
                active_timer_slots[i] = self
                break
                
        if self.slot_index == -1:
            self.slot_index = len(active_timer_slots)
            active_timer_slots.append(self)

        self.position = (0.75, 0.45 - (self.slot_index * 0.08))
        self.time_left = duration
        
        self.icon = Entity(parent=self, model='quad', texture=item_name, scale=(0.06, 0.06), position=(0, 0), unlit=True)
        self.text_ui = Text(parent=self, text=f'{int(duration)}s', position=(0.04, 0), origin=(-0.5, 0), scale=1.5, color=color.white)
        
        # REMOVED the destroy(self, delay=duration) from here!

    def update(self):
        self.time_left -= time.dt
        if self.time_left > 0:
            self.text_ui.text = f'{int(self.time_left)}s'
        else:
            if active_timer_slots[self.slot_index] == self:
                active_timer_slots[self.slot_index] = None
            
            # ADDED manual destroy here so it safely cleans up!
            destroy(self)

class EffectUseUI(Entity):
    def __init__(self, item_name, effects_manager):
        super().__init__(parent=camera.ui)
        self.item_name = item_name
        self.effects_manager = effects_manager
        
        self.slot_index = -1 
        
        # We leave the parent Entity running, but start the visuals as False
        self.icon = Entity(parent=self, model='quad', texture=item_name, scale=(0.06, 0.06), position=(0, 0), unlit=True, enabled=False)
        self.text_ui = Text(parent=self, text='', position=(0.04, 0), origin=(-0.5, 0), scale=1.5, color=color.white, enabled=False)

    def update(self):
        # Safely check the dictionary for uses (defaults to 0 if not found)
        uses = self.effects_manager.effect_uses.get(self.item_name, 0)
        
        if uses > 0:
            # 1. If we have uses but no slot, find one!
            if self.slot_index == -1:
                for i, slot in enumerate(active_timer_slots):
                    if slot is None:
                        self.slot_index = i
                        active_timer_slots[i] = self
                        break
                
                # If no empty slots were found, add a new one to the end
                if self.slot_index == -1:
                    self.slot_index = len(active_timer_slots)
                    active_timer_slots.append(self)
                
                # Assign the fixed Y position based on the slot
                self.position = (0.75, 0.45 - (self.slot_index * 0.08))
                
                # Turn the visuals ON
                self.icon.enabled = True
                self.text_ui.enabled = True

            # Update the text to match the current uses
            self.text_ui.text = f'x{uses}'
            
        else:
            # 2. If we hit 0 uses, free up the slot for other UI!
            if self.slot_index != -1:
                if active_timer_slots[self.slot_index] == self:
                    active_timer_slots[self.slot_index] = None
                
                self.slot_index = -1
                
                # Turn the visuals OFF
                self.icon.enabled = False
                self.text_ui.enabled = False


# --- NEW: The Effects Manager ---
class EffectsManager:
    # 1. Catch the references passed from main.py
    def __init__(self, player, coin_counter_ui, score_mult_callback, score_callback, lose_effects_callback, add_effect_back_callback):
        self.player = player
        self.coin_counter_ui = coin_counter_ui
        self.score_mult_callback = score_mult_callback
        self.score_callback = score_callback
        self.extra_time = 0
        self.lose_effects_callback = lose_effects_callback  # This will be set by main.py after all effects are created
        self.add_effect_back_callback = add_effect_back_callback  # This will be set by main.py after all effects are created
        self.effect_time = {
            'chocolate': 4,
            'pizza': 3,
            'nachos': 5,
            'rice': 0,
            'hash_brown': 5,
            'apple': 5
        }
        self.effect_uses = {
            'pablo': 4
        }

        self.pablo_ui = EffectUseUI('pablo', self)

    # 2. Your effects logic, updated to use "self."
    def apply_item_effects(self, item_name):
        if item_name == 'chocolate':
            flags.SCROLL_SPEED += .5
            EffectTimer('chocolate', self.effect_time['chocolate'] + self.extra_time) 
            
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
        elif item_name == 'hash_brown':
            flags.MAGNET_ACTIVE = True
            EffectTimer('hash_brown', self.effect_time['hash_brown'] + self.extra_time)
            def reset_hash_brown():
                flags.MAGNET_ACTIVE = False
            invoke(reset_hash_brown, delay=self.effect_time['hash_brown'] + self.extra_time)
        elif item_name == 'fries':
            self.extra_time += 2
            def reset_fries():
                self.extra_time -= 2
            invoke(reset_fries, delay=self.effect_time['fries'] + self.extra_time)
        elif item_name == 'apple':
            EffectTimer('apple', self.effect_time['apple'] + self.extra_time)
            self.lose_effects_callback()  # Clear all current effects immediately
            flags.APPLE_MODE = True
            def reset_apple():
                flags.APPLE_MODE = False
                self.add_effect_back_callback()  # Re-apply any effects that should still be active after apple mode ends
            invoke(reset_apple, delay=self.effect_time['apple'] + self.extra_time)
        else:
            print(f"You ate {item_name}, but nothing happened.")