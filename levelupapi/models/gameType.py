from django.db import models


class GameType(models.Model):

    genre = models.CharField(max_length=50)