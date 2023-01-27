import arcade
arcade.open_window(800, 800, "My Drawing")
arcade.set_background_color(arcade.csscolor.DARK_BLUE)
arcade.start_render()

# lilypad
arcade.draw_ellipse_filled(400, 400, 700, 700, arcade.color.DARK_GREEN)
arcade.draw_triangle_filled(400, 550, 350, 750, 450, 750, arcade.csscolor.DARK_BLUE)

# head
arcade.draw_triangle_filled(400, 540, 325, 400, 350, 515, arcade.csscolor.GREEN)
arcade.draw_triangle_filled(400, 540, 475, 400, 450, 515, arcade.csscolor.GREEN)

# torso
arcade.draw_triangle_filled(400, 540, 325, 400, 475, 400, arcade.csscolor.LIME_GREEN)
arcade.draw_triangle_filled(325, 400, 475, 400, 400, 300, arcade.csscolor.LIME_GREEN)

# tail
arcade.draw_triangle_filled(400, 300, 325, 400, 340, 300, arcade.csscolor.GREEN)
arcade.draw_triangle_filled(460, 300, 475, 400, 400, 300, arcade.csscolor.GREEN)
arcade.draw_triangle_filled(340, 300, 460, 300, 400, 200, arcade.csscolor.GREEN)

# back legs
arcade.draw_polygon_filled(((340, 300), (280, 310), (260, 250), (385, 230)), arcade.csscolor.GREEN)
arcade.draw_triangle_filled(260, 250, 310, 242, 280, 170, arcade.csscolor.GREEN)
arcade.draw_triangle_filled(190, 245, 275, 200, 280, 170, arcade.csscolor.GREEN)
arcade.draw_polygon_filled(((460, 300), (520, 310), (540, 250), (415, 230)), arcade.csscolor.GREEN)
arcade.draw_triangle_filled(540, 250, 490, 242, 520, 170, arcade.csscolor.GREEN)
arcade.draw_triangle_filled(610, 245, 525, 200, 520, 170, arcade.csscolor.GREEN)

# front legs
arcade.draw_polygon_filled(((340, 450), (250, 420), (270, 380), (325, 400)), arcade.csscolor.GREEN)
arcade.draw_triangle_filled(250, 420, 230, 480, 280, 427, arcade.csscolor.GREEN)
arcade.draw_polygon_filled(((460, 450), (550, 420), (530, 380), (475, 400)), arcade.csscolor.GREEN)
arcade.draw_triangle_filled(550, 420, 570, 480, 520, 427, arcade.csscolor.GREEN)

# eyes
arcade.draw_ellipse_filled(365, 510, 20, 20, arcade.csscolor.BLACK)
arcade.draw_ellipse_filled(435, 510, 20, 20, arcade.csscolor.BLACK)


arcade.finish_render()
arcade.run()
