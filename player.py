from turtle import Turtle, getscreen
from image_utilities import resize_shape, register_shape
from projectile import Projectile
from scoreboard import ScoreBoard

LEFT = 180
RIGHT = 0
SCREEN_HEIGHT = 800
player_colour_hex = "#48fa34"


class Player(Turtle):
    # Class attribute to keep track of whether the shape is registered

    def __init__(self, position):
        super().__init__()
        self.player_lives = 3
        self.player_shape_registered = False
        self.player_projectiles = []

        self.register_shape_if_needed()
        self.create_player(position)

    def register_shape_if_needed(self):
        if not self.player_shape_registered:
            # Size argument takes (width in pixels, height in pixels)
            resized_player_img = resize_shape('./space_invaders_sprites/player_cannon.gif', (80, 50))
            register_shape(photo_image=resized_player_img, set_name="player_cannon_resized")

            resized_damaged_player_img = resize_shape('./space_invaders_sprites/player_cannon_damaged.gif',
                                                      (80, 50))
            register_shape(photo_image=resized_damaged_player_img, set_name="player_cannon_damaged_resized")
            self.player_shape_registered = True

    def create_player(self, position):
        self.shape("player_cannon_resized")
        self.setheading(RIGHT)
        self.penup()
        self.goto(position)

    def move_right(self):
        self.forward(25)

    def move_left(self):
        self.backward(25)

    def shoot(self):
        current_x, current_y = self.pos()
        player_projectile = Projectile(player_colour_hex, (current_x, current_y + 38))
        player_projectile.move()
        self.player_projectiles.append(player_projectile)

    def turn_red(self):
        self.shape("player_cannon_damaged_resized")

    def turn_green(self):
        self.shape("player_cannon_resized")

    def took_damage(self):
        self.turn_red()
        getscreen().ontimer(self.turn_green, 750)
