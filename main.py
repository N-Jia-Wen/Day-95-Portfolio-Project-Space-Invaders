from turtle import Screen, Turtle
from player import Player
from scoreboard import ScoreBoard
from enemy_manager import EnemyManager
from lives_display import LivesDisplay
import time

game_running = True
difficulty = "Easy"
PLAYER_START_POS = (0, -350)
# Screen width is slightly larger than as defined in other python files so that enemies have room to move sideways
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Setting up screen:
screen = Screen()
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.title("Space Invaders Arcade Game")
screen.tracer(0)


player = Player(PLAYER_START_POS)
scoreboard = ScoreBoard()
lives_display = LivesDisplay(player)
enemy_manager = EnemyManager(player, scoreboard)


# Player movement:
screen.listen()
screen.onkeypress(fun=player.move_right, key="Right")
screen.onkeypress(fun=player.move_left, key="Left")
screen.onkeypress(fun=player.shoot, key="space")


while game_running is True:
    screen.update()
    time.sleep(0.03)
    enemy_manager.check_collision_with_player(player, lives_display)
    enemy_manager.check_collision_with_enemy(player, scoreboard)
    enemy_manager.check_wave_cleared(scoreboard)
    game_running = lives_display.check_game_end(scoreboard)


screen.mainloop()
