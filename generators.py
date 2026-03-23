from ursina import Entity, Vec3, random, time
from config import LENGTH, CORRIDOR_HEIGHT, WIDTH, SIDES_Z_0, COIN_POSITIONS, COIN_SPACING, OBSTACLE_SPACING
import flags
from obstacles import MiddleObstacle, obstacle_list
from coin import Coin

class Generator(Entity):
    def __init__(self, obstacle_factory, coin_factory, player, coin_parent, coin_counter, spawn_ahead_segments=8):
        super().__init__()
        
		# player
        self.player = player
        self.coin_parent = coin_parent
        self.coin_counter = coin_counter
        
        self.obstacle_factory = obstacle_factory
        self.coin_factory = coin_factory
        
        # how many corridor segments ahead of the player we keep spawning into
        self.spawn_ahead_segments = spawn_ahead_segments
        
        # segment-aligned spawn tracking
        self.next_spawn_segment = 0
        
        # timers
        self.obstacle_timer = 0
        self.coin_timer = 0
        
        # tuning
        self.obstacle_spacing = OBSTACLE_SPACING
        self.coin_spacing = COIN_SPACING
        
        # avoid spawning on every wall all the time
        self.wall_choices = ['A', 'B', 'C', 'D']
        
        # offset so things appear centered on the corridor surface
        self.margin = 0.15

    def update(self):
        speed = flags.SCROLL_SPEED*LENGTH

        if speed <= 0:
            return

        # convert world spacing into time spacing
        obstacle_time = self.obstacle_spacing / speed
        coin_time = self.coin_spacing / speed

        self.obstacle_timer += time.dt
        self.coin_timer += time.dt

        if self.obstacle_timer >= obstacle_time:
            self.obstacle_timer -= obstacle_time
            self.spawn_obstacle()

        if self.coin_timer >= coin_time:
            self.coin_timer -= coin_time
            self.spawn_coin()

    # --------------------------------------------------
    # CORRIDOR-ALIGNED SPAWNING
    # --------------------------------------------------

    def segment_z(self, segment_index):
        """
        Returns the z position for a given corridor segment index.
        Segment 0 is near SIDES_Z_0, then repeats every LENGTH.
        """
        return SIDES_Z_0 - segment_index * LENGTH

    def random_wall_point(self):
        """
        Pick a wall and return a local position + rotation suitable for that wall.
        A = floor
        B = right wall
        C = left wall
        D = ceiling
        """
        wall = random.choice(self.wall_choices)

        if wall == 'A':   # floor
            pos = Vec3(0, 0.5-CORRIDOR_HEIGHT/2, 0)
            rot = Vec3(0, 0, 0)
        elif wall == 'B': # right wall
            pos = Vec3(0.5-CORRIDOR_HEIGHT/2, 0, 0)
            rot = Vec3(0, 0, 90)
        elif wall == 'C': # left wall
            pos = Vec3(-0.5+CORRIDOR_HEIGHT/2, 0, 0)
            rot = Vec3(0, 0, -90)
        else:             # ceiling
            pos = Vec3(0, -0.5+CORRIDOR_HEIGHT/2, 0)
            rot = Vec3(0, 0, 180)

        return wall, pos, rot

    def spawn_obstacle(self):
        segment = self.next_spawn_segment
        z = self.segment_z(segment)

        wall, local_pos, local_rot = self.random_wall_point()

        self.obstacle_factory(
            -100,
            random.randint(0, 3),
            self.coin_parent,
			local_pos
			)

        self.next_spawn_segment += 1

    def spawn_coin(self):
        segment = self.next_spawn_segment
        z = self.segment_z(segment)

        wall, local_pos, local_rot = self.random_wall_point()

        self.coin_factory(
            position=random.choice(COIN_POSITIONS),
            player=self.player,
            coin_parent=self.coin_parent,
            coin_counter=self.coin_counter
        )

def create_obstacle(z, wall, coin_parent, position):
    print("Creating obstacle")
    return random.choice(obstacle_list)(wall, position=Vec3(0, 0, z), parent=coin_parent)

def create_coin(position, player, coin_parent, coin_counter):
    return Coin(position=position, player=player, parent=coin_parent, coin_counter=coin_counter)
