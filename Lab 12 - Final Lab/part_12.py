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
LAYER_NAME_PLAYER = "Tile Layer 3"

DEFAULT_SCREEN_WIDTH = 800
DEFAULT_SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Move with Scrolling Screen Example"

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

        # --- Load Textures ---

        # Images from Kenney.nl's 1-Bit Platformer pack
        main_path = "C:/Users/erikf/Downloads/kenney_1-bit-platformer-pack/Tiles/Default/"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}mouse.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}mousejump.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(1, 3):
            texture = load_texture_pair(f"{main_path}mousewalk{i}.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # set_hit_box = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture >= 2:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]


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

        #self.scene = None
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

        # Create the cameras. One for the GUI, one for the sprites.
        # We scroll the 'sprite world' but not the GUI.
        self.camera_sprites = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)

    def setup(self):
        """ Set up the game and initialize the variables. """

        #self.scene = arcade.Scene()

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Mouse()
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 575
        #self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
        self.player_list.append(self.player_sprite)

        # --- Load our map

        # Read in the tiled map
        map_name = "C:/Users/erikf/Downloads/map 1.tmj"
        # layer_options = {
        #     LAYER_NAME_WALL: {
        #         "use_spatial_hash": True,
        #     },
        # }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING)

        #self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set wall and coin SpriteLists
        # Any other layers here. Array index must be a layer.
        self.wall_list = self.tile_map.sprite_lists["Tile Layer 1"]
        self.decoration_layer = self.tile_map.sprite_lists["Tile Layer 2"]
        self.coin_list = self.tile_map.sprite_lists["Tile Layer 3"]

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

        self.clear()
        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()
        #self.scene.draw()
        # Draw all the sprites.
        self.decoration_layer.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()

        # Draw the GUI
        # arcade.draw_rectangle_filled(self.width // 2,
        #                              20,
        #                              self.width,
        #                              40,
        #                              arcade.color.ALMOND)
        text = f"Score: {self.score}"
        arcade.draw_text(text, 10, 10, arcade.color.YELLOW, 20)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
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
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        # self.player_sprite.change_y = 0
        self.coin_list.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        #self.scene.update_animation(delta_time, [LAYER_NAME_PLAYER])

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # Scroll the screen to the player
        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a
        smoother pan.
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
    # possible arcade schedule call here
    arcade.run()


if __name__ == "__main__":
    main()
