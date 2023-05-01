import arcade
from pyglet.math import Vec2
"images, map and sprite assets from kenny.nl"
"example code for simple platformer from Python Arcade website"

SPRITE_SCALING = 1.5
TILE_SCALING = 1.5
GRID_PIXEL_SIZE = 128
GRAVITY = 0.25

LAYER_NAME_WALL = "Tile Layer 1"
LAYER_NAME_BACKGROUND = "Tile Layer 2"
LAYER_NAME_COINS = "Tile Layer 3"

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Erik Flint - Final Lab"

PLAYER_START_X = 325
PLAYER_START_Y = 575

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 50

# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

# How fast the character moves
PLAYER_MOVEMENT_SPEED = 5
JUMP_SPEED = 7

RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True), ]


class Mouse(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = SPRITE_SCALING

        # Track our state
        self.jumping = False
        self.pace = 0.150
        self.elapsed_time = 0

        # --- Load Textures ---

        '''Images and Tilemap assets from Kenney.nl's 1-Bit Platformer pack'''
        '''https://kenney.nl/assets/1-bit-platformer-pack'''

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair("./mousetr.png")
        self.jump_texture_pair = load_texture_pair("./mousejumptr.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(1, 3):
            texture = load_texture_pair(f"./mousewalk{i}tr.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Sets the hit box
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING

        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y != 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]

        # Idle animation
        elif self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
        else:
            self.elapsed_time += delta_time
            if self.elapsed_time > self.pace:  # walking pace
                self.elapsed_time = 0  # reset
                # Walking animation
                self.cur_texture += 1
                self.cur_texture %= 2
                self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Initializer """
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.decoration_layer = None
        self.coin_list = None
        self.spike_list = None
        self.goal_list = None

        self.score = 0

        # Set up the player
        self.player_sprite = None

        # Physics engine so we don't run into walls.
        self.physics_engine = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        self.allowed_jumps = None
        self.allow_multi_jump = None

        # Store our tile map
        self.tile_map = None
        self.tile_set = None

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        # Loading the sounds
        self.coin_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        self.hurt_sound = arcade.load_sound(":resources:sounds/hurt3.wav")

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Mouse()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        # --- Load our map

        # Read in the tiled map
        map_name = "./map_2.tmj"
        layer_options = {
            LAYER_NAME_WALL: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_BACKGROUND: {"use_spatial_hash": True}, LAYER_NAME_COINS: {"use_spatial_hash": True}}

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Set wall and coin SpriteLists
        # Any other layers here. Array index must be a layer.
        self.wall_list = self.tile_map.sprite_lists["Tile Layer 1"]
        self.decoration_layer = self.tile_map.sprite_lists["Tile Layer 2"]
        self.coin_list = self.tile_map.sprite_lists["Tile Layer 3"]
        self.spike_list = self.tile_map.sprite_lists["Tile Layer 4"]
        self.goal_list = self.tile_map.sprite_lists["Tile Layer 5"]

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Keep player from running through the wall_list layer
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            self.wall_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()
        # Draw all the sprites.
        self.decoration_layer.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.spike_list.draw()
        self.goal_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        if len(self.goal_list) <= 0:
            arcade.draw_text("GAME OVER", DEFAULT_SCREEN_WIDTH / 6, DEFAULT_SCREEN_HEIGHT / 2,
                         arcade.csscolor.WHITE, 64)

            # arcade.draw_text("GAME OVER", self.player_sprite.center_x, self.player_sprite.center_y,
            #              arcade.csscolor.WHITE, 200)

        # Draw the score
        text = f"Score: {self.score}"
        arcade.draw_text(text, 10, 10, arcade.color.YELLOW, 20)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if len(self.goal_list) > 0:
            if key == arcade.key.UP:
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = JUMP_SPEED
            elif key == arcade.key.LEFT:
                self.left_pressed = True
            elif key == arcade.key.RIGHT:
                self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        if len(self.goal_list) <= 0:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        else:

            """ Movement and game logic """
            self.player_sprite.update_animation()
            # Calculate speed based on the keys pressed
            self.player_sprite.change_x = 0
            # self.player_sprite.change_y = 0
            self.coin_list.update()

            coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
            for coin in coin_hit_list:
                coin.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(self.coin_sound)

            if arcade.check_for_collision_with_list(self.player_sprite, self.spike_list):
                self.player_sprite.center_x = PLAYER_START_X
                self.player_sprite.center_y = PLAYER_START_Y
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
                arcade.play_sound(self.hurt_sound)

            goal_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.goal_list)
            for goal in goal_hit_list:
                goal.remove_from_sprite_lists()
                arcade.play_sound(self.coin_sound)

            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

            # Call update on all sprites (The sprites don't do much in this
            # example though.)
            self.physics_engine.update()

            # Scroll the screen to the player
            self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.
        """

        position = Vec2(self.player_sprite.center_x - self.height / 2,
                        self.player_sprite.center_y - self.width / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    """ Main function """
    window = MyGame(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
