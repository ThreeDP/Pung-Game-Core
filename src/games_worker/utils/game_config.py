import random
import math

class playerColor(enumerate):
	BLUE = 0
	RED = 1
	GREEN = 3
	YELLOW = 4
	WHITE = 5
	BLACK = 6

class GameConfig:
	# Screen Configuration
	screen_width = 0
	screen_height = 0

	field_height = 40
	field_width = 70
	multiplayer_field_width = 80

	max_score = 1000

	# Ball Configuration
	speed_range_min = 0.4
	speed_range_max = 0.9
	ball_speed_x_coef = random.choice([-1, 1])
	ball_speed_y_coef = random.choice([-1, 1])
	ball_speed_x = ball_speed_x_coef * random.uniform(speed_range_min, speed_range_max)
	ball_speed_y = ball_speed_y_coef * random.uniform(speed_range_min, speed_range_max)

	# Tamanho proporcional da bola
	ball_size = min(field_width, field_height) * 0.03  # ~3% do menor lado

	# Player Configuration
	player_speed = 0.55

	player_height = field_height * 0.35  # ~40% da altura
	player_width = field_width * 0.025  # ~2.5% da largura

	multiplayer_height = field_height * 0.05  # ~5% da altura
	multiplayer_width = field_width * 0.2     # ~20% da largura

	player_positions = [
		{"x": -(field_width - player_width) / 2, "y": 0},
		{"x": (field_width - player_width) / 2, "y": 0},
	]

	multiplayer_positions = [
		{"x": -(multiplayer_field_width - player_width) / 2, "y": 0},
		{"x": (multiplayer_field_width - player_width) / 2, "y": 0},
		{"x": 0, "y": (multiplayer_field_width - multiplayer_height) / 2},
		{"x": 0, "y": -(multiplayer_field_width - multiplayer_height) / 2},
	]

	max_distance_ball_player = ball_size + math.sqrt((player_height / 2)**2 + (player_width / 2)**2)

class GameStatus:
	WAITING = "WAITING"
	PLAYING = "PLAYING"
	FINISHED = "FINISHED"
	PAUSED = "PAUSED"