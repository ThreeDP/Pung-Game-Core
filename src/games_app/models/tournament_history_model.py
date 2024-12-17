from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    score = models.IntegerField()
    profileImage = models.CharField(max_length=255)

class TournamentHistoryModel(models.Model):
    roomCode = models.CharField(max_length=30)
    winner = models.CharField(max_length=10)
    red = models.ForeignKey(Player, related_name='red_player', on_delete=models.CASCADE)
    blue = models.ForeignKey(Player, related_name='blue_player', on_delete=models.CASCADE)