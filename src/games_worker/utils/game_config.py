import random

class GameConfig:

    # Screen Configuration
    screen_width = 0
    screen_height = 0

    field_height = 80
    field_width = 90
    multiplayer_field_width = 80

    max_score = 1000

    # Ball Configuration
    ball_speed_x_coef = random.choice([-1, 1])
    ball_speed_y_coef = random.choice([-1, 1])
    ball_speed_x = ball_speed_x_coef * random.uniform(0.5, 1)
    ball_speed_y = ball_speed_y_coef * random.uniform(0.5, 1)
    ball_size = 2

    # Player Configuration
    player_speed = 4

    player_height = 16
    player_width = 2

    multiplayer_height = 2
    multiplayer_width = 16

    player_positions = [
        {"x": -44, "y": 0},
        {"x": 44, "y": 0},
    ]

    multiplayer_positions = [
        {"x": -29, "y": 0},
        {"x": 29, "y": 0},
        {"x": 0, "y": 29},
        {"x": 0, "y": -29},
    ]

class GameStatus:
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"
    PAUSED = "PAUSED"