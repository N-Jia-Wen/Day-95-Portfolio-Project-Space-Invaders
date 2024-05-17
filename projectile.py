from turtle import Turtle, getscreen

UP = 90
player_colour_hex = "#48fa34"
player_colour_rgb = (0.2823529411764706, 0.9803921568627451, 0.20392156862745098)
enemy_colour = "white"


class Projectile(Turtle):
    def __init__(self, colour, position):
        self.enemy_projectile_speed = 50

        super().__init__()
        self.shape("square")
        self.color(colour)
        self.setheading(UP)
        self.shapesize(stretch_wid=0.2, stretch_len=1)
        self.penup()
        self.goto(position)

    def move(self):
        if self.color()[0] == player_colour_hex or self.color()[0] == player_colour_rgb:
            self.forward(15)
        elif self.color()[0] == enemy_colour:
            self.backward(8)

        screen = getscreen()
        screen.ontimer(self.move, 50)

    def move_player(self):
        self.forward(15)
        getscreen().ontimer(self.move_player, 50)
