import random

class GameConfig:

    # Screen Configuration
    screen_width = 0
    screen_height = 0

    field_height = 60
    field_width = 90

    max_score = 10000

    # Ball Configuration
    ball_speed_x_coef = random.choice([-1, 1])
    ball_speed_y_coef = random.choice([-1, 1])
    ball_speed_x = ball_speed_x_coef * random.uniform(0.5, 1)
    ball_speed_y = ball_speed_y_coef * random.uniform(0.5, 1)
    ball_size = 2

    # Player Configuration
    player_speed = 1

    player_height = 16
    player_width = 2

    player_positions = [
        {"x": -44, "y": 0},
        {"x": 44, "y": 0},
    ]

class GameStatus:
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"
    PAUSED = "PAUSED"