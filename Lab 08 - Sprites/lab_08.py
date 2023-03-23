""" Lab 8 """

import random
import arcade
import math

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_COIN = 0.2
SPRITE_SCALING_SAW = 0.4
COIN_COUNT = 40
SAW_COUNT = 20

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Coin(arcade.Sprite):
    def __init__(self, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.freeze = False

    def update(self):
        if not self.freeze:
            self.center_y -= 1
            if self.top < 0:
                # Reset the coin to a random spot above the screen
                self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
                self.center_x = random.randrange(SCREEN_WIDTH)


class Saw(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)
        self.freeze = False
        # Current angle in radians
        self.circle_angle = 0
        # How far away from the center to orbit, in pixels
        self.circle_radius = 0
        # How fast to orbit, in radians per frame
        self.circle_speed = 0.008
        # Set the center of the point we will orbit around
        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):

        if not self.freeze:

            """ Update the saw's position. """
            # Calculate a new x, y
            self.center_x = self.circle_radius * math.sin(self.circle_angle) \
                + self.circle_center_x
            self.center_y = self.circle_radius * math.cos(self.circle_angle) \
                + self.circle_center_y
            # Increase the angle in prep for the next round.
            self.circle_angle += self.circle_speed
            self.angle += 1
            # If we rotate past 360, reset it back a turn.
            if self.angle > 359:
                self.angle -= 360


class MyGame(arcade.Window):
    """ Custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")

        # Variables that will hold sprite lists
        self.player_list = None
        self.coin_list = None
        self.saw_list = None
        # Set up the player info
        self.player_sprite = None
        self.score = 0
        # Don't show the mouse cursor
        self.set_mouse_visible(False)
        # Good sound effect
        self.good_sound = arcade.load_sound(":resources:sounds/coin5.wav")
        # Bad sound effect
        self.bad_sound = arcade.load_sound(":resources:sounds/hurt3.wav")

        arcade.set_background_color(arcade.color.DUKE_BLUE)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.saw_list = arcade.SpriteList()
        # Score
        self.score = 0
        # Set up the player
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the coins
        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image directly from arcade
            coin = Coin(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)
            # Position the coin
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)
            # Add the coin to the lists
            self.coin_list.append(coin)

        for i in range(SAW_COUNT):

            saw = Saw(":resources:images/enemies/saw.png", SPRITE_SCALING_SAW)
            # Position the center of the circle the saw will orbit
            saw.circle_center_x = random.randrange(SCREEN_WIDTH)
            saw.circle_center_y = random.randrange(SCREEN_HEIGHT)
            # Random radius from 10 to 200
            saw.circle_radius = random.randrange(10, 200)
            # Random start angle from 0 to 2pi
            saw.circle_angle = random.random() * 2 * math.pi
            self.saw_list.append(saw)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        self.saw_list.draw()
        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 715, 580, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        if len(self.coin_list) > 0:
            # Move the center of the player sprite to match the mouse x, y
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.coin_list.update()
        # Generate a list of all sprites that collided with the player.
        coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                              self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in coins_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.good_sound)
        self.saw_list.update()
        saw_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.saw_list)

        for saw in saw_hit_list:
            saw.remove_from_sprite_lists()
            self.score -= 1
            arcade.play_sound(self.bad_sound)

        if len(self.coin_list) == 0:
            arcade.draw_text("GAME OVER", 85, 300, arcade.csscolor.WHITE, 75)
            for z in self.coin_list:
                z.freeze = True
            for z in self.saw_list:
                z.freeze = True

        arcade.finish_render()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
