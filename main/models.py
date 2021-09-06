from django.db import models


class GameData(models.Model):
    id = models.UUIDField(primary_key=True)
    data = models.JSONField()


class UserMust(models.Model):
    username = models.CharField(max_length=255)
    must_game = models.ManyToManyField(GameData)
