from django.db import models
import uuid

class Game(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False, unique=True, blank=False)
    status = models.IntegerField(default=0)
    created_by = models.CharField(max_length=64, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=64, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = self.id or str(uuid.uuid4())
        super(Game, self).save(*args, **kwargs)

    def __str__(self):
        return f"Game {self.id} - Status: {self.status}"

class Player(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False, unique=True, blank=False)
    gameId = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_connected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = self.id or str(uuid.uuid4())
        super(Player, self).save(*args, **kwargs)

    def __str__(self):
        return f"Player {self.id} - Connected: {self.is_connected}"

class Score(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False, unique=True, blank=False)
    playerId = models.ForeignKey(Player, on_delete=models.CASCADE)
    gameId = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = self.id or str(uuid.uuid4())
        super(Score, self).save(*args, **kwargs)

    def __str__(self):
        return f"Score {self.id} - Player: {self.playerId.id} - Score: {self.score}"
