from ursina import Vec3, curve

# -----------------
# Corridor config
# -----------------
WIDTH		= 3.0    # corridor width (x)
HEIGHT		= 1.0    # corridor height (y)
LENGTH		= 100.0  # length of each corridor segment (z)
CORRIDOR_HEIGHT = 3.0  # how high the corridor is (y)
SIDES_Z_0 = -LENGTH/2
ORIGIN_SIDES = Vec3(0, 0.5 + CORRIDOR_HEIGHT/2, 0)

# -----------------
# Player (bean) config
# -----------------
BEAN_HEIGHT = 0.5	# Size of the character
ORIGIN		= Vec3(0, 1.5/BEAN_HEIGHT - 0.5, 0)  # origin point for bean
JUMPING		= False
CURVE_JUMP_UP= curve.out_quad  # easing curve for bean "jump" when switching attachment
CURVE_JUMP_DOWN=curve.in_quad   # easing curve for bean "fall" when switching attachment

# -----------------
# Camera config
# -----------------
FOV = 60  # Field of view for the camera

# -----------------
# Main config
# -----------------
SEG_COUNT	= 10
SPEED		= 0.0    # how fast segments move toward the bean
SCROLL_SPEED= 0.05
SCROLL_FACTOR=1
TURN_TIME	= 0.5     # how long it takes to rotate segments when switching attachment

CURVE		= curve.in_quad  # easing curve for segment rotation
ROTATING	= False  # whether segments are currently rotating (to prevent input during rotation)
