from turtle import Turtle, getscreen
from player import Player
from scoreboard import ScoreBoard
import pyglet
from ctypes import windll

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# To fix blurry tkinter font. Taken from https://stackoverflow.com/questions/41315873/attempting-to-resolve-
# blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp/43046744#43046744
windll.shcore.SetProcessDpiAwareness(1)

# Rendering custom fonts. Taken from https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
pyglet.font.add_file('./fonts/arcadeclassic/ARCADECLASSIC.TTF')


class LivesDisplay(Turtle):
    def __init__(self, player: Player):
        self.player = player

        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.update_player_lives()

    def update_player_lives(self):
        self.clear()
        self.goto(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 25)
        self.write(arg=f"Lives: {self.player.player_lives}", align="center", font=("ArcadeClassic", 30, "normal"))

    def check_game_end(self, scoreboard: ScoreBoard):
        if self.player.player_lives <= 0:
            self.player.turn_red()
            self.clear()
            getscreen().update()
            scoreboard.final_score()
            return False
        else:
            return True
