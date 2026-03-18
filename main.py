from ursina import *

app = Ursina()

# --- 2D style camera ---
camera.orthographic = True
camera.fov = 10
window.color = color.black

# --- Player ---
player = Entity(
    model='quad',
    color=color.azure,
    scale=(1,1),
    collider='box'
)

speed = 5

# --- Ground / reference ---
ground = Entity(
    model='quad',
    scale=(20,10),
    color=color.dark_gray,
    z=1
)

# --- Game loop ---
def update():
    player.x += (held_keys['d'] - held_keys['a']) * speed * time.dt
    player.y += (held_keys['w'] - held_keys['s']) * speed * time.dt

app.run()