from turtle import Turtle, getscreen
import pyglet
from ctypes import windll

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# To fix blurry tkinter font. Taken from https://stackoverflow.com/questions/41315873/attempting-to-resolve-
# blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp/43046744#43046744
windll.shcore.SetProcessDpiAwareness(1)

# Rendering custom fonts. Taken from https://stackoverflow.com/questions/11993290/truly-custom-font-in-tkinter
pyglet.font.add_file('./fonts/arcadeclassic/ARCADECLASSIC.TTF')


class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-SCREEN_WIDTH / 2 + 50, SCREEN_HEIGHT / 2 + 25)
        self.write(arg=f"Score: {self.score}", align="center", font=("ArcadeClassic", 30, "normal"))

    def display_next_wave(self):
        self.clear()
        self.goto(0, SCREEN_HEIGHT / 2 + 25)
        self.write(arg=f"Next Wave!", align="center", font=("ArcadeClassic", 30, "normal"))
        getscreen().ontimer(self.update_scoreboard, 2000)

    def final_score(self):
        self.clear()
        self.goto(0, SCREEN_HEIGHT / 2 + 25)
        self.write(arg=f"Final Score: {self.score}", align="center", font=("ArcadeClassic", 30, "normal"))
