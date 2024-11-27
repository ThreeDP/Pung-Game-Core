class GameConfig:

    # Screen Configuration
    screen_width = 850
    screen_height = 550

    max_score = 10

    # Ball Configuration
    ball_speed = 5
    ball_size = 10

    # Player Configuration
    player_speed = 10

    player_height = 100
    player_width = 25

    player_positions = [
        {"x": 25, "y": 225},
        {"x": 800, "y": 225},
    ]

class GameStatus:
    WAITING = "WAITING"
    PLAYING = "PLAYING"
    FINISHED = "FINISHED"
    PAUSED = "PAUSED"