from enemy import Enemy
from image_utilities import resize_shape, register_shape
from turtle import getscreen
from player import Player
from scoreboard import ScoreBoard
from lives_display import LivesDisplay
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
ENEMIES_PER_ROW = 10
ENEMY_TYPES = ["generic", "generic", "squid", "octopus", "ufo"]
enemy_sizes = [(59, 50), (46, 50), (64, 50), (70, 50)]
enemy_height = 50


class EnemyManager:

    def __init__(self, player: Player, scoreboard: ScoreBoard):
        self.player = player
        self.scoreboard = scoreboard

        self.move_sideways_period = 2500
        self.move_forward_period = 10000
        self.randomness = 25  # The lower the number, the more bullets are hit per second
        self.direction = random.choice(["left", "right"])
        self.enemy_list = []
        self.enemy_projectiles = []
        self.resize_register_enemy_shapes()
        self.generate_enemies()
        getscreen().ontimer(self.move_sideways, self.move_sideways_period)
        getscreen().ontimer(self.change_shape, 1000)  # Schedules the animation to start
        getscreen().ontimer(self.move_forward, self.move_forward_period)
        getscreen().ontimer(self.attack_frequency, 4000)

    def resize_register_enemy_shapes(self):
        enemy_types_unique = ENEMY_TYPES[1:]
        for num in range(len(enemy_types_unique)):
            enemy_name = enemy_types_unique[num]
            enemy_size = enemy_sizes[num]

            resized_enemy_image_1 = resize_shape(f"./space_invaders_sprites/{enemy_name}_enemy_frame_1.gif",
                                                 enemy_size)
            register_shape(resized_enemy_image_1, f"{enemy_name}_enemy_resized_1")

            resized_enemy_image_2 = resize_shape(f"./space_invaders_sprites/{enemy_name}_enemy_frame_2.gif",
                                                 enemy_size)
            register_shape(resized_enemy_image_2, f"{enemy_name}_enemy_resized_2")

    def generate_enemies(self):
        # The -5 is added as a buffer so that bricks are not displayed outside the window
        row_width = SCREEN_WIDTH / ENEMIES_PER_ROW -5

        for num in range(len(ENEMY_TYPES)):
            enemy_type = ENEMY_TYPES[num]
            y = num * enemy_height
            for nth_enemy in range(1, ENEMIES_PER_ROW + 1):
                # Using arithmetic sequence formula (and trial and error to render bricks properly):
                x = -430 + (nth_enemy - 1) * row_width
                enemy = Enemy(enemy_type, x, y)
                self.enemy_list.append(enemy)

    def change_shape(self):
        for enemy in self.enemy_list:
            enemy.shape(f"{enemy.enemy_type}_enemy_resized_2" if enemy.shape() == f"{enemy.enemy_type}_enemy_resized_1"
                        else f"{enemy.enemy_type}_enemy_resized_1")
        screen = getscreen()
        screen.ontimer(self.change_shape, 500)

    def move_forward(self):
        for enemy in self.enemy_list:
            current_x, current_y = enemy.pos()
            enemy.goto(current_x, current_y - 20)

            # Alternative lose condition, where the aliens reach the player and player loses
            if enemy.pos()[1] < self.player.pos()[1] + 40:
                self.player.player_lives = 0

        getscreen().ontimer(self.move_forward, self.move_forward_period)

    def move_sideways(self):
        enemy_x_cor = [enemy.pos()[0] for enemy in self.enemy_list]
        if self.direction == "right":
            for enemy in self.enemy_list:
                enemy.goto(enemy.pos()[0] + 20, enemy.pos()[1])
            if not all(x < 520 for x in enemy_x_cor):
                self.direction = "left"

        elif self.direction == "left":
            for enemy in self.enemy_list:
                enemy.goto(enemy.pos()[0] - 20, enemy.pos()[1])
            if not all(x > -520 for x in enemy_x_cor):
                self.direction = "right"

        getscreen().ontimer(self.move_sideways, self.move_sideways_period)

    def attack_frequency(self):
        for enemy in self.enemy_list:
            random_num = random.randint(1, self.randomness)
            if random_num == self.randomness:
                enemy_projectile = enemy.enemy_attack()
                self.enemy_projectiles.append(enemy_projectile)

        screen = getscreen()
        screen.ontimer(self.attack_frequency, 4000)

    # Both collision checks are done in EnemyManager to prevent circular importing:
    def check_collision_with_player(self, player: Player, lives_display: LivesDisplay):
        for enemy_projectile in self.enemy_projectiles:
            distance_to_player = player.distance(enemy_projectile)

            if distance_to_player < 40:
                player.player_lives -= 1
                player.took_damage()
                lives_display.update_player_lives()

                enemy_projectile.hideturtle()
                self.enemy_projectiles.remove(enemy_projectile)
                del enemy_projectile

            # Checks if projectile goes beyond boundary. If so, deletes the projectile
            elif enemy_projectile.pos()[1] < -(SCREEN_HEIGHT / 2):

                enemy_projectile.hideturtle()
                self.enemy_projectiles.remove(enemy_projectile)
                del enemy_projectile

    def check_collision_with_enemy(self, player: Player, scoreboard: ScoreBoard):
        for player_projectile in player.player_projectiles:
            for enemy in self.enemy_list:
                distance_to_enemy = enemy.distance(player_projectile)

                # Check if enemy was hit
                if distance_to_enemy < 30:
                    if enemy.enemy_type == "generic":
                        scoreboard.score += 2
                    elif enemy.enemy_type == "squid":
                        scoreboard.score += 4
                    elif enemy.enemy_type == "octopus":
                        scoreboard.score += 6
                    elif enemy.enemy_type == "ufo":
                        scoreboard.score += 8
                    scoreboard.update_scoreboard()

                    enemy.hideturtle()
                    self.enemy_list.remove(enemy)
                    player_projectile.hideturtle()
                    player.player_projectiles.remove(player_projectile)

                    del enemy
                    del player_projectile
                    break

                # Checks if projectile goes beyond boundary. If so, deletes the projectile
                elif player_projectile.pos()[1] > (SCREEN_HEIGHT / 2):

                    player_projectile.hideturtle()
                    player.player_projectiles.remove(player_projectile)
                    del player_projectile
                    break

    def check_wave_cleared(self, scoreboard: ScoreBoard):
        if not self.enemy_list:
            scoreboard.display_next_wave()

            # Increases the difficulty level:
            if self.randomness > 10:
                self.randomness -= 2
            if self.move_sideways_period > 500:
                self.move_sideways_period -= 500
            if self.move_forward_period > 5000:
                self.move_forward_period -= 1000

            self.generate_enemies()
