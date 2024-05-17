from turtle import Turtle
from projectile import Projectile
import warnings

DOWN = 270
enemy_colour = "white"


class Enemy(Turtle):
    def __init__(self, enemy_type: str, x, y):
        super().__init__()
        self.color(enemy_colour)
        self.enemy_type = enemy_type
        self.create_enemy(x, y)

    def create_enemy(self, x, y):
        if self.enemy_type == "generic":
            self.shape("generic_enemy_resized_1")
        elif self.enemy_type == "squid":
            self.shape("squid_enemy_resized_1")
        elif self.enemy_type == "octopus":
            self.shape("octopus_enemy_resized_1")
        elif self.enemy_type == "ufo":
            self.shape("ufo_enemy_resized_1")
        else:
            warnings.warn("Enemy type must be one of ['generic', 'squid', 'octopus', 'ufo']",
                          category=RuntimeWarning)

        self.setheading(DOWN)
        self.penup()
        self.goto(x, y)

    def enemy_attack(self):
        current_x, current_y = self.pos()
        enemy_projectile = Projectile(enemy_colour, (current_x, current_y - 25))
        enemy_projectile.move()
        return enemy_projectile
