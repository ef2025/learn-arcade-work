""" Lab 7 - User Control """

import arcade

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 5

# lilypad drawing function

def lilypad(x, y):
    # lilypad
    arcade.draw_ellipse_filled(x, y, 300, 300, arcade.color.DARK_GREEN)
    arcade.draw_triangle_filled(x, 30 + y, -50 + x, 150 + y, 50 + x, 150 + y, arcade.csscolor.DARK_BLUE)

# tadpole drawing function

def tadpole(x, y):
    arcade.draw_ellipse_filled(x, -60 + y, 40, 90, arcade.color.GRAY)
    arcade.draw_ellipse_filled(x, -60 + y, 20, 70, arcade.color.BLACK)
    arcade.draw_ellipse_filled(x, y, 50, 70, arcade.color.BLACK)

# dragonfly drawing function

def dragonfly(x, y):
    arcade.draw_ellipse_filled(-40 + x, 45 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=20)
    arcade.draw_ellipse_filled(-40 + x, 15 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=-20)
    arcade.draw_ellipse_filled(40 + x, 15 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=20)
    arcade.draw_ellipse_filled(40 + x, 45 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=-20)
    arcade.draw_ellipse_filled(x, y, 20, 120, arcade.csscolor.BLACK)
    arcade.draw_ellipse_filled(x, 60 + y, 24, 24, arcade.csscolor.BLACK)

# Dragonfly class

class Dragonfly:
    def __init__(self, position_x, position_y, color):
        self.position_x = position_x
        self.position_y = position_y
        self.color = color

    def draw(self):
        arcade.draw_ellipse_filled(-40 + self.position_x, 45 + self.position_y, 75, 20, arcade.csscolor.GRAY,
                                   tilt_angle=20)
        arcade.draw_ellipse_filled(-40 + self.position_x, 15 + self.position_y, 75, 20, arcade.csscolor.GRAY,
                                   tilt_angle=-20)
        arcade.draw_ellipse_filled(40 + self.position_x, 15 + self.position_y, 75, 20, arcade.csscolor.GRAY,
                                   tilt_angle=20)
        arcade.draw_ellipse_filled(40 + self.position_x, 45 + self.position_y, 75, 20, arcade.csscolor.GRAY,
                                   tilt_angle=-20)
        arcade.draw_ellipse_filled(self.position_x, self.position_y, 20, 120, self.color)
        arcade.draw_ellipse_filled(self.position_x, 60 + self.position_y, 24, 24, self.color)

# Tadpole class

class Tadpole:
    def __init__(self, position_x, position_y, change_x, change_y, width, height, color):
        # Take the parameters of the init function above,
        # and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.width = width
        self.height = height
        self.color = color

        self.border_sound = arcade.load_sound(":resources:sounds/hurt3.wav")
        self.border_sound_player = None

    # Drawing function with class parameters

    def draw(self):

        arcade.draw_ellipse_filled(self.position_x, -60 + self.position_y, self.width + -10, self.height + 20,
                                   arcade.color.GRAY)
        arcade.draw_ellipse_filled(self.position_x, -60 + self.position_y, self.width + -30, self.height,
                                   self.color)
        arcade.draw_ellipse_filled(self.position_x, self.position_y, self.width, self.height, self.color)

    def play(self):
        if not self.border_sound_player or not self.border_sound_player.playing:
            self.border_sound_player = arcade.play_sound(self.border_sound)

    #
    def update(self):
        self.position_y += self.change_y
        self.position_x += self.change_x

        if self.position_x < 0:
            self.position_x = 0
            self.play()

        if self.position_x > SCREEN_WIDTH:
            self.position_x = SCREEN_WIDTH
            self.play()

        if self.position_y < 0:
            self.position_y = 0
            self.play()

        if self.position_y > SCREEN_HEIGHT:
            self.position_y = SCREEN_HEIGHT
            self.play()


class MyGame(arcade.Window):
    """ Our Custom Window Class"""

    def __init__(self):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Lab 7 - User Control")

        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.csscolor.DARK_BLUE)

        self.click_sound = arcade.load_sound(":resources:sounds/coin5.wav")

        self.tadpole = Tadpole(200, 200, 0, 0, 50, 70, arcade.csscolor.BLACK)
        self.dragonfly = Dragonfly(400, 400, arcade.csscolor.BLACK)

    def update(self, delta_time):
        self.tadpole.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.tadpole.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.tadpole.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.tadpole.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.tadpole.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.tadpole.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.tadpole.change_y = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """

        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.play_sound(self.click_sound)
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            arcade.play_sound(self.click_sound)

    def on_draw(self):

        arcade.start_render()
        lilypad(450, 700)
        lilypad(200, 400)
        lilypad(500, 100)
        self.tadpole.draw()
        self.dragonfly.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Called to update our objects.
        Happens approximately 60 times per second."""
        self.dragonfly.position_x = x
        self.dragonfly.position_y = y


def main():
    MyGame()
    arcade.run()


main()
