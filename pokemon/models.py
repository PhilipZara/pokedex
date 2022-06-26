from django.db import models


class Pokedex(models.Model):
    name = models.CharField(max_length=200)
    abilities = models.JSONField()
    stats = models.JSONField()
    sprite = models.CharField(max_length=300)

    def __str__(self):
        return self.name
