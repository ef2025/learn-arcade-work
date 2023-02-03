import arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


def lilypad(x, y):

    # lilypad
    arcade.draw_ellipse_filled(400 + x, 400 + y, 700, 700, arcade.color.DARK_GREEN)
    arcade.draw_triangle_filled(400 + x, 550 + y, 350 + x, 750 + y, 450 + x, 750 + y, arcade.csscolor.DARK_BLUE)


def frog(x, y):

    # head
    arcade.draw_triangle_filled(400 + x, 540 + y, 325 + x, 400 + y, 350 + x, 515 + y, arcade.csscolor.GREEN)
    arcade.draw_triangle_filled(400 + x, 540 + y, 475 + x, 400 + y, 450 + x, 515 + y, arcade.csscolor.GREEN)

    # torso
    arcade.draw_triangle_filled(400 + x, 540 + y, 325 + x, 400 + y, 475 + x, 400 + y, arcade.csscolor.LIME_GREEN)
    arcade.draw_triangle_filled(325 + x, 400 + y, 475 + x, 400 + y, 400 + x, 300 + y, arcade.csscolor.LIME_GREEN)

    # tail
    arcade.draw_triangle_filled(400 + x, 300 + y, 325 + x, 400 + y, 340 + x, 300 + y, arcade.csscolor.GREEN)
    arcade.draw_triangle_filled(460 + x, 300 + y, 475 + x, 400 + y, 400 + x, 300 + y, arcade.csscolor.GREEN)
    arcade.draw_triangle_filled(340 + x, 300 + y, 460 + x, 300 + y, 400 + x, 200 + y, arcade.csscolor.GREEN)

    # back legs
    arcade.draw_polygon_filled(((340 + x, 300 + y), (280 + x, 310 + y), (260 + x, 250 + y), (385 + x, 230 + y)), arcade.
                               csscolor.GREEN)
    arcade.draw_triangle_filled(260 + x, 250 + y, 310 + x, 242 + y, 280 + x, 170 + y, arcade.csscolor.GREEN)
    arcade.draw_triangle_filled(190 + x, 245 + y, 275 + x, 200 + y, 280 + x, 170 + y, arcade.csscolor.GREEN)
    arcade.draw_polygon_filled(((460 + x, 300 + y), (520 + x, 310 + y), (540 + x, 250 + y), (415 + x, 230 + y)), arcade.
                               csscolor.GREEN)
    arcade.draw_triangle_filled(540 + x, 250 + y, 490 + x, 242 + y, 520 + x, 170 + y, arcade.csscolor.GREEN)
    arcade.draw_triangle_filled(610 + x, 245 + y, 525 + x, 200 + y, 520 + x, 170 + y, arcade.csscolor.GREEN)

    # front legs
    arcade.draw_polygon_filled(((340 + x, 450 + y), (250 + x, 420 + y), (270 + x, 380 + y), (325 + x, 400 + y)), arcade.
                               csscolor.GREEN)
    arcade.draw_triangle_filled(250 + x, 420 + y, 230 + x, 480 + y, 280 + x, 427 + y, arcade.csscolor.GREEN)
    arcade.draw_polygon_filled(((460 + x, 450 + y), (550 + x, 420 + y), (530 + x, 380 + y), (475 + x, 400 + y)), arcade.
                               csscolor.GREEN)
    arcade.draw_triangle_filled(550 + x, 420 + y, 570 + x, 480 + y, 520 + x, 427 + y, arcade.csscolor.GREEN)

    # eyes
    arcade.draw_ellipse_filled(365 + x, 510 + y, 20, 20, arcade.csscolor.BLACK)
    arcade.draw_ellipse_filled(435 + x, 510 + y, 20, 20, arcade.csscolor.BLACK)


def dragonfly(x, y):

    arcade.draw_ellipse_filled(-40 + x, 45 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=20)
    arcade.draw_ellipse_filled(-40 + x, 15 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=-20)
    arcade.draw_ellipse_filled(40 + x, 15 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=20)
    arcade.draw_ellipse_filled(40 + x, 45 + y, 75, 20, arcade.csscolor.GRAY, tilt_angle=-20)
    arcade.draw_ellipse_filled(x, y, 20, 120, arcade.csscolor.BLACK)
    arcade.draw_circle_filled(x, 60 + y, 12, arcade.csscolor.BLACK)


def on_draw(delta_time):

    arcade.start_render()

    lilypad(0, 0)
    frog(0, 0)
    frog(350, -400)
    dragonfly(100, on_draw.dragonfly1_y)

    on_draw.dragonfly1_y += 2


on_draw.dragonfly1_y = 100


def main():

    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "My Drawing")
    arcade.set_background_color(arcade.csscolor.DARK_BLUE)

    arcade.schedule(on_draw, 1/60)
    arcade.run()


main()
