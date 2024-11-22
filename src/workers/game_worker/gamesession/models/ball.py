from .game_config import GameConfig

class Ball:
    def __init__(self):
        self.x = GameConfig.screen_width // 2
        self.y = GameConfig.screen_height // 2
        self.radius = GameConfig.ball_size

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "radius": self.radius,
        }